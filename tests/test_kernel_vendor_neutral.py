"""Vendor-neutrality invariant for the kernel.

The kernel is the vendor-agnostic core: it must never name or hardcode any
specific API vendor. This test scans every Python file under kernel/ for
vendor literals (secret-key prefixes, the vendor host, the vendor config
filename, the vendor name) and asserts ZERO matches.

It is an invariant guard: it protects the kernel/driver boundary as code is
moved in. If it fails, a vendor literal leaked into the kernel — move it out
to a driver (or register it from outside the kernel) instead.

Offline-safe: no network, no key. Run:
    python -m unittest tests.test_kernel_vendor_neutral
"""

import pathlib
import re
import unittest

KERNEL = pathlib.Path(__file__).resolve().parent.parent / "kernel"

# Case-insensitive: any of these substrings in a kernel .py file is a leak.
_VENDOR_LITERAL = re.compile(r"tp_(live|test)_|api\.trustpager\.com|bos\.json|trustpager", re.I)


class TestKernelVendorNeutral(unittest.TestCase):
    def test_kernel_has_no_vendor_literals(self):
        offenders = []
        for p in KERNEL.rglob("*.py"):
            text = p.read_text(encoding="utf-8")
            if _VENDOR_LITERAL.search(text):
                offenders.append(str(p.relative_to(KERNEL.parent)))
        self.assertEqual(
            offenders, [],
            f"vendor literals leaked into kernel/: {offenders}",
        )


if __name__ == "__main__":
    unittest.main()
