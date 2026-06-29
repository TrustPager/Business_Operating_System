"""Tests for tools/finance_calc.py (Task 1.3, P5-money).

finance_calc.py is a thin wrapper over numpy-financial providing library-correct
financial math for money apps (load-bearing consumer: profit-per-job, forthcoming).

Two test categories -- mirroring the exact pattern in test_doc_lib_set.py:

  1. Missing-lib path (unconditional): block numpy_financial via a subprocess
     meta-path blocker, assert exit 2 + "pip install numpy-financial" in stderr.
     This always runs, even on a machine without the lib.

  2. Known-answer round-trips (skipUnless HAS_NUMPY_FINANCIAL): import the
     wrapper's Python API directly and assert computed values against reference
     answers (manually derived or cross-checked against financial tables).

Offline-safe: no network, no CRM key.
Run:
    BOS_OFFLINE=1 python -m unittest tests.test_finance_calc
"""

import json
import subprocess
import sys
import unittest
from importlib import util as importutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"


def _lib(name: str) -> bool:
    try:
        spec = importutil.find_spec(name)
        return spec is not None
    except (ImportError, ValueError):
        return False


HAS_NUMPY_FINANCIAL = _lib("numpy_financial")


def _run_blocked(script: str, args: list, block_import: str) -> subprocess.CompletedProcess:
    """Run a tools/ wrapper with block_import made un-importable via meta-path blocker.

    Mirrors the exact helper used in test_doc_lib_set.py so CI behaviour is
    identical across all doc-lib and finance-lib wrapper tests.
    """
    preamble = (
        "import sys\n"
        f"_BLOCK = {block_import!r}\n"
        "class _Blocker:\n"
        "    def find_spec(self, name, path=None, target=None):\n"
        "        if name == _BLOCK or name.startswith(_BLOCK + '.'):\n"
        "            raise ImportError('blocked for test: ' + name)\n"
        "        return None\n"
        "sys.meta_path.insert(0, _Blocker())\n"
        f"sys.argv = [{str(TOOLS / script)!r}, *{args!r}]\n"
        f"exec(compile(open({str(TOOLS / script)!r}, encoding='utf-8').read(), "
        f"{str(TOOLS / script)!r}, 'exec'))\n"
    )
    return subprocess.run([sys.executable, "-c", preamble],
                          capture_output=True, text=True)


# ---------------------------------------------------------------------------
# 1. Missing-lib path (unconditional)
# ---------------------------------------------------------------------------

class TestMissingLibPath(unittest.TestCase):
    """finance_calc.py exits 2 with a pip install hint when numpy-financial is absent."""

    def test_pmt_missing_lib_exits_2_with_hint(self):
        proc = _run_blocked("finance_calc.py", ["pmt", "--rate", "0.01", "--nper", "12", "--pv", "10000"],
                            "numpy_financial")
        self.assertEqual(proc.returncode, 2, f"expected exit 2; stderr:\n{proc.stderr}")
        self.assertIn("pip install numpy-financial", proc.stderr,
                      f"expected install hint; got:\n{proc.stderr}")

    def test_sln_missing_lib_exits_2_with_hint(self):
        proc = _run_blocked("finance_calc.py", ["sln", "--cost", "10000", "--salvage", "1000", "--life", "5"],
                            "numpy_financial")
        self.assertEqual(proc.returncode, 2, f"expected exit 2; stderr:\n{proc.stderr}")
        self.assertIn("pip install numpy-financial", proc.stderr)

    def test_no_bare_pip_recommendation(self):
        """The hint must recommend python -m pip, not a bare pip install."""
        proc = _run_blocked("finance_calc.py", ["pmt", "--rate", "0.01", "--nper", "12", "--pv", "10000"],
                            "numpy_financial")
        self.assertIn("python -m pip install", proc.stderr,
                      f"expected 'python -m pip install'; got:\n{proc.stderr}")
        for line in proc.stderr.splitlines():
            stripped = line.strip()
            self.assertFalse(
                stripped.startswith("pip install"),
                f"found a bare 'pip install' recommendation: {line!r}"
            )


# ---------------------------------------------------------------------------
# 2. Known-answer round-trips (require numpy-financial)
# ---------------------------------------------------------------------------

@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestPmt(unittest.TestCase):
    """pmt: loan/equipment repayment.

    Reference: monthly payment on a $10,000 loan, 12% annual rate (1%/month),
    12 months. Standard annuity formula: PMT = PV * r / (1 - (1+r)^-n)
    = 10000 * 0.01 / (1 - 1.01^-12) = 888.4879...

    numpy_financial.pmt returns a negative value (cash out). We expose the
    magnitude via abs() in our API so callers get a positive repayment figure.
    """

    def _fc(self):
        import sys
        sys.path.insert(0, str(TOOLS))
        import finance_calc
        return finance_calc

    def test_pmt_monthly_loan(self):
        fc = self._fc()
        result = fc.pmt(rate=0.01, nper=12, pv=10000.0)
        self.assertAlmostEqual(result, 888.49, places=1,
                               msg=f"pmt result {result} not close to 888.49")

    def test_pmt_is_positive(self):
        """API contract: pmt returns a positive repayment amount."""
        fc = self._fc()
        result = fc.pmt(rate=0.005, nper=60, pv=20000.0)
        self.assertGreater(result, 0, "pmt must return a positive amount")

    def test_pmt_zero_rate(self):
        """At 0% rate, payment = PV / nper."""
        fc = self._fc()
        result = fc.pmt(rate=0.0, nper=10, pv=1000.0)
        self.assertAlmostEqual(result, 100.0, places=6)


@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestIpmtPpmt(unittest.TestCase):
    """ipmt/ppmt: interest and principal portions of a given payment period.

    Reference: same $10,000 loan at 1%/month, 12 months.
    Period 1 interest = 10000 * 0.01 = 100.00
    Period 1 principal = pmt - interest = 888.49 - 100.00 = 788.49
    Sum of ipmt + ppmt must equal pmt for every period.
    """

    def _fc(self):
        import sys
        sys.path.insert(0, str(TOOLS))
        import finance_calc
        return finance_calc

    def test_ipmt_period1(self):
        fc = self._fc()
        result = fc.ipmt(rate=0.01, per=1, nper=12, pv=10000.0)
        self.assertAlmostEqual(result, 100.0, places=2,
                               msg=f"ipmt period 1 = {result}, expected 100.00")

    def test_ppmt_period1(self):
        fc = self._fc()
        result = fc.ppmt(rate=0.01, per=1, nper=12, pv=10000.0)
        self.assertAlmostEqual(result, 788.49, places=1,
                               msg=f"ppmt period 1 = {result}, expected ~788.49")

    def test_ipmt_ppmt_sum_equals_pmt(self):
        """For every period, ipmt + ppmt must equal pmt (within floating point)."""
        fc = self._fc()
        rate, nper, pv = 0.01, 12, 10000.0
        payment = fc.pmt(rate=rate, nper=nper, pv=pv)
        for per in range(1, nper + 1):
            interest = fc.ipmt(rate=rate, per=per, nper=nper, pv=pv)
            principal = fc.ppmt(rate=rate, per=per, nper=nper, pv=pv)
            self.assertAlmostEqual(interest + principal, payment, places=6,
                                   msg=f"period {per}: ipmt+ppmt != pmt")

    def test_ipmt_decreases_over_time(self):
        """Interest portion must decrease monotonically as the balance is paid down."""
        fc = self._fc()
        rate, nper, pv = 0.01, 12, 10000.0
        interests = [fc.ipmt(rate=rate, per=p, nper=nper, pv=pv) for p in range(1, nper + 1)]
        for i in range(len(interests) - 1):
            self.assertGreater(interests[i], interests[i + 1],
                               f"interest should decrease: period {i+1} ({interests[i]}) "
                               f"not > period {i+2} ({interests[i+1]})")


@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestSln(unittest.TestCase):
    """sln: straight-line (prime-cost) depreciation.

    Reference: asset cost $10,000, salvage $1,000, life 5 years.
    Annual depreciation = (10000 - 1000) / 5 = 1800.00 per year.
    """

    def _fc(self):
        import sys
        sys.path.insert(0, str(TOOLS))
        import finance_calc
        return finance_calc

    def test_sln_basic(self):
        fc = self._fc()
        result = fc.sln(cost=10000.0, salvage=1000.0, life=5)
        self.assertAlmostEqual(result, 1800.0, places=6)

    def test_sln_zero_salvage(self):
        """Zero salvage: depreciation = cost / life."""
        fc = self._fc()
        result = fc.sln(cost=5000.0, salvage=0.0, life=4)
        self.assertAlmostEqual(result, 1250.0, places=6)

    def test_sln_value_is_correct(self):
        """Straight-line per-period amount: (cost - salvage) / life."""
        fc = self._fc()
        d = fc.sln(cost=12000.0, salvage=2000.0, life=10)
        self.assertAlmostEqual(d, 1000.0, places=6)


@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestDb(unittest.TestCase):
    """db: declining-balance (diminishing-value) depreciation.

    Reference: numpy-financial docs example -- asset cost $1,000,000, salvage $100,000,
    life 6 years. Period 1 depreciation using DB:
    rate = 1 - (salvage/cost)^(1/life) = 1 - (0.1)^(1/6) = 0.3187...
    period_1 = cost * rate * (month/12) using month=12 -> 1000000 * 0.3187 = 318,695.
    We test to 3 significant figures to stay robust against floating-point variation.
    """

    def _fc(self):
        import sys
        sys.path.insert(0, str(TOOLS))
        import finance_calc
        return finance_calc

    def test_db_period1_approximate(self):
        fc = self._fc()
        result = fc.db(cost=1_000_000.0, salvage=100_000.0, life=6, period=1)
        # numpy-financial db default month=12 -> period 1 ~ 319,000
        self.assertAlmostEqual(result, 319_000.0, delta=2000.0,
                               msg=f"db period 1 = {result}, expected ~319000")

    def test_db_positive(self):
        """Depreciation is always a positive amount."""
        fc = self._fc()
        for p in range(1, 7):
            result = fc.db(cost=10000.0, salvage=1000.0, life=6, period=p)
            self.assertGreater(result, 0, f"db period {p} must be positive")

    def test_db_partial_first_year(self):
        """month != 12 prorates period 1 by month/12 (partial-first-year branch).

        rate = round(1 - (100000/1000000)^(1/6), 3) = 0.319.
        period 1, month=6: cost * rate * 6/12 = 1000000 * 0.319 * 0.5 = 159500.
        """
        fc = self._fc()
        result = fc.db(cost=1_000_000.0, salvage=100_000.0, life=6, period=1, month=6)
        self.assertAlmostEqual(result, 159_500.0, delta=1000.0,
                               msg=f"db period 1 month=6 = {result}, expected ~159500")

    def test_db_total_within_reasonable_range(self):
        """Sum of DB period depreciations stays within a reasonable range of cost - salvage.

        The Excel DB method rounds the derived rate to 3 decimal places, which can cause
        the total to slightly exceed (cost - salvage) by a small amount. We allow up to
        5 percent overshoot to accommodate rounding, while confirming the figure is
        in the right ballpark (not wildly off).
        """
        fc = self._fc()
        cost, salvage, life = 10000.0, 1000.0, 6
        depreciable = cost - salvage
        total = sum(fc.db(cost=cost, salvage=salvage, life=life, period=p) for p in range(1, life + 1))
        # Total should be reasonably close to the depreciable amount (within 5 percent).
        self.assertLessEqual(total, depreciable * 1.05,
                             f"total db depreciation {total} is more than 5 pct over cost-salvage {depreciable}")
        self.assertGreater(total, depreciable * 0.50,
                           f"total db depreciation {total} is less than half of cost-salvage {depreciable}")


@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestDdb(unittest.TestCase):
    """ddb: double-declining-balance depreciation.

    Reference: asset cost $2,000, salvage $0, life 10 years, factor 2.
    Period 1 depreciation = cost * (factor/life) = 2000 * 0.2 = 400.
    Period 2: remaining book value = 2000 - 400 = 1600; 1600 * 0.2 = 320.
    """

    def _fc(self):
        import sys
        sys.path.insert(0, str(TOOLS))
        import finance_calc
        return finance_calc

    def test_ddb_period1(self):
        fc = self._fc()
        result = fc.ddb(cost=2000.0, salvage=0.0, life=10, period=1)
        self.assertAlmostEqual(result, 400.0, places=4)

    def test_ddb_period2(self):
        fc = self._fc()
        result = fc.ddb(cost=2000.0, salvage=0.0, life=10, period=2)
        self.assertAlmostEqual(result, 320.0, places=4)

    def test_ddb_decreases_over_time(self):
        """DDB depreciation decreases each period (front-loaded method)."""
        fc = self._fc()
        vals = [fc.ddb(cost=2000.0, salvage=0.0, life=10, period=p) for p in range(1, 6)]
        for i in range(len(vals) - 1):
            self.assertGreaterEqual(vals[i], vals[i + 1],
                                    f"ddb period {i+1} ({vals[i]}) < period {i+2} ({vals[i+1]})")

    def test_ddb_custom_factor(self):
        """factor=1.5 gives 150% declining balance instead of 200%."""
        fc = self._fc()
        result = fc.ddb(cost=2000.0, salvage=0.0, life=10, period=1, factor=1.5)
        self.assertAlmostEqual(result, 300.0, places=4)

    def test_ddb_nonpositive_factor_errors(self):
        """A factor <= 0 is invalid input and exits 1 (no nonsense output)."""
        fc = self._fc()
        with self.assertRaises(SystemExit):
            fc.ddb(cost=2000.0, salvage=0.0, life=10, period=1, factor=0.0)


@unittest.skipUnless(HAS_NUMPY_FINANCIAL, "numpy-financial not installed")
class TestCliSubcommands(unittest.TestCase):
    """CLI subcommands produce numeric JSON output to stdout."""

    def _run(self, args: list) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOLS / "finance_calc.py"), *args],
            capture_output=True, text=True
        )

    def test_cli_pmt_json(self):
        proc = self._run(["pmt", "--rate", "0.01", "--nper", "12", "--pv", "10000"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertIn("result", data)
        self.assertAlmostEqual(data["result"], 888.49, places=1)

    def test_cli_sln_json(self):
        proc = self._run(["sln", "--cost", "10000", "--salvage", "1000", "--life", "5"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertAlmostEqual(data["result"], 1800.0, places=4)

    def test_cli_db_json(self):
        proc = self._run(["db", "--cost", "1000000", "--salvage", "100000",
                          "--life", "6", "--period", "1"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertAlmostEqual(data["result"], 319_000.0, delta=2000.0)

    def test_cli_ddb_json(self):
        proc = self._run(["ddb", "--cost", "2000", "--salvage", "0",
                          "--life", "10", "--period", "1"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertAlmostEqual(data["result"], 400.0, places=4)

    def test_cli_ipmt_json(self):
        proc = self._run(["ipmt", "--rate", "0.01", "--per", "1", "--nper", "12", "--pv", "10000"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertAlmostEqual(data["result"], 100.0, places=2)

    def test_cli_ppmt_json(self):
        proc = self._run(["ppmt", "--rate", "0.01", "--per", "1", "--nper", "12", "--pv", "10000"])
        self.assertEqual(proc.returncode, 0, f"stderr:\n{proc.stderr}")
        data = json.loads(proc.stdout)
        self.assertAlmostEqual(data["result"], 788.49, places=1)


if __name__ == "__main__":
    unittest.main()
