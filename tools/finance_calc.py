#!/usr/bin/env python3
"""finance_calc.py: library-correct financial math for BOS money apps.

Wraps numpy-financial (BSD-3-Clause) for loan/repayment functions (pmt, ipmt,
ppmt) and implements depreciation schedules (sln, db, ddb) using the standard
financial formulas (numpy-financial 1.0 does not include depreciation functions;
the formulas are reproduced from the public financial standard).

Load-bearing consumer: profit-per-job.

Python API (import and call directly):
    from finance_calc import pmt, ipmt, ppmt, sln, db, ddb

CLI (subcommands, each writes a JSON result to stdout):
    python tools/finance_calc.py pmt  --rate 0.01 --nper 12 --pv 10000
    python tools/finance_calc.py ipmt --rate 0.01 --per 1  --nper 12 --pv 10000
    python tools/finance_calc.py ppmt --rate 0.01 --per 1  --nper 12 --pv 10000
    python tools/finance_calc.py sln  --cost 10000 --salvage 1000 --life 5
    python tools/finance_calc.py db   --cost 10000 --salvage 1000 --life 5 --period 1
    python tools/finance_calc.py ddb  --cost 10000 --salvage 0    --life 5 --period 1

Missing-dependency contract (mirrors markitdown_convert.py / write_xlsx.py D11 pattern):
  - If numpy_financial is absent: print BOS_MISSING_DEP: numpy-financial to stderr
    (machine-readable signal the SKILL layer keys off), then a human install line
    recommending python -m pip install numpy-financial (BSD-3-Clause, not bare pip),
    then exit 2. No network at runtime once installed.
  - Bad input: exit 1.
  - Success: exit 0.

Excluded (out of P5 scope, no P5 app consumes them): npv, irr.
These are deferred to a future investment-view app.
"""
import sys
import json
import argparse


# pip spec for the backing library.
MISSING_DEP_SPEC = "numpy-financial"

# Machine-readable + human install hint (D11). The SKILL layer keys off
# BOS_MISSING_DEP: prefix to trigger a detect -> offer -> install -> verify loop.
# Always recommend python -m pip (never bare pip, a multi-Python trap on Windows).
INSTALL_HINT = (
    f"BOS_MISSING_DEP: {MISSING_DEP_SPEC}\n"
    "numpy-financial isn't installed (the financial math library for BOS money apps, BSD-3-Clause).\n"
    f"Install it with: python -m pip install {MISSING_DEP_SPEC}\n"
)


def _require_numpy_financial():
    """Import numpy_financial or emit the install hint and exit 2."""
    try:
        import numpy_financial as npf  # noqa: F401
        return npf
    except ImportError:
        sys.stderr.write(INSTALL_HINT)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Python API
# Loan/repayment functions delegate to numpy_financial.
# All functions return positive scalars (magnitudes, not signed-convention
# values). numpy_financial returns negative cash-out values for payments;
# we take abs() consistently.
# Depreciation functions use the standard financial formulas directly
# (numpy-financial 1.0 removed sln/db/ddb; formulas are public standard).
# ---------------------------------------------------------------------------

def pmt(rate: float, nper: int, pv: float, fv: float = 0.0) -> float:
    """Periodic payment for a loan or equipment finance.

    rate: periodic interest rate (e.g. 0.01 for 1 percent per period)
    nper: total number of payment periods
    pv:   present value (loan principal)
    fv:   future value after all payments (default 0)

    Returns the payment amount as a positive number. numpy_financial uses a
    negative cash-out sign convention; we normalise to a positive magnitude via
    abs() so callers get a plain payment figure.
    """
    npf = _require_numpy_financial()
    return abs(float(npf.pmt(rate, nper, pv, fv)))


def ipmt(rate: float, per: int, nper: int, pv: float, fv: float = 0.0) -> float:
    """Interest portion of payment ``per`` in a loan/finance schedule.

    Returns a positive amount (the interest component of that period's payment).
    numpy_financial uses a negative cash-out sign convention; we normalise to a
    positive magnitude via abs() so callers get a plain interest figure.
    """
    npf = _require_numpy_financial()
    return abs(float(npf.ipmt(rate, per, nper, pv, fv)))


def ppmt(rate: float, per: int, nper: int, pv: float, fv: float = 0.0) -> float:
    """Principal portion of payment ``per`` in a loan/finance schedule.

    Returns a positive amount (the principal repaid in that period).
    numpy_financial uses a negative cash-out sign convention; we normalise to a
    positive magnitude via abs() so callers get a plain principal figure.
    """
    npf = _require_numpy_financial()
    return abs(float(npf.ppmt(rate, per, nper, pv, fv)))


def sln(cost: float, salvage: float, life: int) -> float:
    """Straight-line (prime-cost) depreciation per period.

    Formula: (cost - salvage) / life   -- constant each period.

    numpy_financial 1.0 does not expose sln; implemented from the public
    straight-line depreciation standard (identical to the numpy legacy formula).
    The library guard still runs so a missing numpy-financial exits 2.
    """
    _require_numpy_financial()  # guard: exits 2 if lib absent
    if life <= 0:
        sys.stderr.write("life must be > 0\n")
        sys.exit(1)
    return (cost - salvage) / life


def db(cost: float, salvage: float, life: int, period: int,
       month: int = 12) -> float:
    """Declining-balance (diminishing-value) depreciation for a given period.

    Uses the fixed-declining-balance method matching the Excel DB formula:
      rate = 1 - (salvage / cost) ^ (1 / life)   (rounded to 3 decimal places)
    Period 1: cost * rate * month / 12
    Period N (2..life): (cost - sum_prior_depreciation) * rate
    Final period: ((cost - sum_prior) * rate * (12 - month)) / 12

    month: number of months in the first year (default 12, full year).
    Returns a positive depreciation amount.

    numpy_financial 1.0 does not expose db; implemented from the Excel DB
    specification (public standard). The library guard still runs.
    """
    _require_numpy_financial()  # guard: exits 2 if lib absent
    if cost <= 0 or life <= 0 or period < 1 or period > life:
        sys.stderr.write("Invalid inputs for db depreciation.\n")
        sys.exit(1)
    if salvage <= 0:
        salvage = 0.0

    # Rate rounded to 3 decimal places, matching Excel DB behaviour.
    rate = round(1.0 - (salvage / cost) ** (1.0 / life), 3)
    dep = 0.0
    book = cost
    for p in range(1, period + 1):
        if p == 1:
            d = book * rate * month / 12.0
        elif p == life and month != 12:
            d = book * rate * (12 - month) / 12.0
        else:
            d = book * rate
        if p == period:
            dep = d
        book -= d
    return dep


def ddb(cost: float, salvage: float, life: int, period: int,
        factor: float = 2.0) -> float:
    """Double-declining-balance (or custom-factor declining-balance) depreciation.

    Formula (matching Excel DDB):
      Each period: min(book_value - salvage, book_value * (factor / life))
    Returns a positive depreciation amount for the given period.

    factor: multiplier on the straight-line rate (default 2.0 = double-declining).

    numpy_financial 1.0 does not expose ddb; implemented from the Excel DDB
    specification (public standard). The library guard still runs.
    """
    _require_numpy_financial()  # guard: exits 2 if lib absent
    if life <= 0 or period < 1 or period > life or factor <= 0:
        sys.stderr.write("Invalid inputs for ddb depreciation.\n")
        sys.exit(1)

    book = cost
    for p in range(1, period + 1):
        d = min(book - salvage, book * factor / life)
        d = max(d, 0.0)
        if p == period:
            return d
        book -= d
    return 0.0


# ---------------------------------------------------------------------------
# CLI
# Each subcommand writes {"result": <float>} to stdout as JSON.
# ---------------------------------------------------------------------------

def _emit(value: float) -> None:
    # round to 10 dp: strips float noise while preserving precision for chaining.
    sys.stdout.write(json.dumps({"result": round(value, 10)}) + "\n")


def _cmd_pmt(args: argparse.Namespace) -> None:
    _emit(pmt(rate=args.rate, nper=args.nper, pv=args.pv, fv=args.fv))


def _cmd_ipmt(args: argparse.Namespace) -> None:
    _emit(ipmt(rate=args.rate, per=args.per, nper=args.nper, pv=args.pv, fv=args.fv))


def _cmd_ppmt(args: argparse.Namespace) -> None:
    _emit(ppmt(rate=args.rate, per=args.per, nper=args.nper, pv=args.pv, fv=args.fv))


def _cmd_sln(args: argparse.Namespace) -> None:
    _emit(sln(cost=args.cost, salvage=args.salvage, life=args.life))


def _cmd_db(args: argparse.Namespace) -> None:
    _emit(db(cost=args.cost, salvage=args.salvage, life=args.life,
             period=args.period, month=args.month))


def _cmd_ddb(args: argparse.Namespace) -> None:
    _emit(ddb(cost=args.cost, salvage=args.salvage, life=args.life,
              period=args.period, factor=args.factor))


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Financial math wrapper over numpy-financial (BSD-3-Clause).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="command", required=True)

    # pmt
    p = sub.add_parser("pmt", help="Periodic loan/equipment repayment amount.")
    p.add_argument("--rate", type=float, required=True,
                   help="Periodic interest rate as a decimal (0.01 = 1 percent per period).")
    p.add_argument("--nper", type=int, required=True, help="Total number of periods.")
    p.add_argument("--pv", type=float, required=True, help="Present value (loan principal).")
    p.add_argument("--fv", type=float, default=0.0, help="Future value after all payments (default 0).")
    p.set_defaults(func=_cmd_pmt)

    # ipmt
    p = sub.add_parser("ipmt", help="Interest portion of a specific payment period.")
    p.add_argument("--rate", type=float, required=True,
                   help="Periodic interest rate as a decimal.")
    p.add_argument("--per", type=int, required=True, help="Payment period (1-indexed).")
    p.add_argument("--nper", type=int, required=True, help="Total number of periods.")
    p.add_argument("--pv", type=float, required=True, help="Present value (loan principal).")
    p.add_argument("--fv", type=float, default=0.0, help="Future value (default 0).")
    p.set_defaults(func=_cmd_ipmt)

    # ppmt
    p = sub.add_parser("ppmt", help="Principal portion of a specific payment period.")
    p.add_argument("--rate", type=float, required=True,
                   help="Periodic interest rate as a decimal.")
    p.add_argument("--per", type=int, required=True, help="Payment period (1-indexed).")
    p.add_argument("--nper", type=int, required=True, help="Total number of periods.")
    p.add_argument("--pv", type=float, required=True, help="Present value (loan principal).")
    p.add_argument("--fv", type=float, default=0.0, help="Future value (default 0).")
    p.set_defaults(func=_cmd_ppmt)

    # sln
    p = sub.add_parser("sln", help="Straight-line (prime-cost) depreciation per period.")
    p.add_argument("--cost", type=float, required=True, help="Asset cost.")
    p.add_argument("--salvage", type=float, required=True, help="Salvage value at end of life.")
    p.add_argument("--life", type=int, required=True, help="Useful life in periods.")
    p.set_defaults(func=_cmd_sln)

    # db
    p = sub.add_parser("db", help="Declining-balance (diminishing-value) depreciation.")
    p.add_argument("--cost", type=float, required=True, help="Asset cost.")
    p.add_argument("--salvage", type=float, required=True, help="Salvage value.")
    p.add_argument("--life", type=int, required=True, help="Useful life in periods.")
    p.add_argument("--period", type=int, required=True, help="Depreciation period (1-indexed).")
    p.add_argument("--month", type=int, default=12, help="Months in first year (default 12).")
    p.set_defaults(func=_cmd_db)

    # ddb
    p = sub.add_parser("ddb", help="Double-declining-balance (or custom-factor) depreciation.")
    p.add_argument("--cost", type=float, required=True, help="Asset cost.")
    p.add_argument("--salvage", type=float, required=True, help="Salvage value.")
    p.add_argument("--life", type=int, required=True, help="Useful life in periods.")
    p.add_argument("--period", type=int, required=True, help="Depreciation period (1-indexed).")
    p.add_argument("--factor", type=float, default=2.0,
                   help="Depreciation rate factor (default 2.0 for double-declining).")
    p.set_defaults(func=_cmd_ddb)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
