"""Independent finite checks for the A394676 generator and verifier.

Run from the repository root:
    python -m unittest discover -s code -p 'test_*.py' -v
"""

import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from verify import VerificationError, generate_prefix, main, verify_prefix


# Exact terms displayed by https://oeis.org/A394676, checked 2026-11-27.
OEIS_FIRST_80 = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 23, 24,
    25, 27, 28, 29, 31, 32, 33, 34, 36, 37, 38, 39, 41, 42, 43, 44, 46, 47,
    48, 49, 50, 52, 53, 54, 55, 57, 58, 59, 60, 62, 63, 64, 65, 66, 68, 69,
    70, 71, 73, 74, 75, 76, 78, 79, 80, 81, 82, 84, 85, 86, 87, 89, 90, 91,
    92, 94, 95, 96, 97, 98,
]


def reference_prefix(terms: int, window: int = 4) -> list[int]:
    """Slow reference: rebuild the forbidden set at every step."""
    a = []
    while len(a) < terms:
        forbidden = {sum(a[j : j + window]) for j in range(len(a) - window + 1)}
        candidate = a[-1] + 1 if a else 1
        while candidate in forbidden:
            candidate += 1
        a.append(candidate)
    return a


class VerifyTests(unittest.TestCase):
    def test_exact_oeis_prefix(self):
        a, _ = generate_prefix(80)
        self.assertEqual(a, OEIS_FIRST_80)

    def test_against_independent_reference(self):
        expected = reference_prefix(300)
        for terms in (1, 2, 3, 4, 5, 9, 10, 40, 80, 300):
            with self.subTest(terms=terms):
                a, b = generate_prefix(terms)
                self.assertEqual(a, expected[:terms])
                self.assertEqual(b, [sum(a[j : j + 4]) for j in range(terms - 3)])
                self.assertEqual(verify_prefix(a, b)["status"], "passed")

    def test_bounds_and_complement_partition(self):
        a, b = generate_prefix(5000)
        report = verify_prefix(a, b)
        through = a[-1]
        a_set = set(a)
        b_set = {value for value in b if value <= through}
        self.assertFalse(a_set & b_set)
        self.assertEqual(a_set | b_set, set(range(1, through + 1)))
        self.assertTrue(all((5*n-6)//4 <= x <= (5*n-1)//4
                            for n, x in enumerate(a, 1)))
        self.assertTrue(all(5*j <= x <= 5*j+5 for j, x in enumerate(b, 1)))
        self.assertEqual(report["verified"]["partition_b_terms"], len(b_set))
        self.assertEqual(report["verified"]["b_window_sums"], 4997)

    def test_window_two_exact_formula(self):
        a, b = generate_prefix(1000, window=2)
        self.assertEqual(a, [(3*n-1)//2 for n in range(1, 1001)])
        self.assertEqual(b, [3*j for j in range(1, 1000)])
        self.assertEqual(verify_prefix(a, b, window=2)["status"], "passed")

    def test_other_windows_against_reference(self):
        for window in (3, 5, 6, 7, 8, 9, 10, 11, 12):
            with self.subTest(window=window):
                a, b = generate_prefix(200, window=window)
                self.assertEqual(a, reference_prefix(200, window=window))
                report = verify_prefix(a, b, window=window)
                self.assertEqual(report["status"], "passed")
        # A prefix shorter than its window has no available sums.
        a, b = generate_prefix(3, window=12)
        self.assertEqual(a, [1, 2, 3])
        self.assertEqual(b, [])
        self.assertEqual(verify_prefix(a, b, window=12)["b_error"]["min"], None)

    def test_rejects_corrupted_prefixes(self):
        a, b = generate_prefix(80)
        corrupted = b.copy()
        corrupted[0] += 1
        with self.assertRaisesRegex(VerificationError, "window sum"):
            verify_prefix(a, corrupted)

        # This increasing list passes the pointwise a and b bounds, but
        # it omits 9 and includes a forbidden 10. The partition must fail.
        a = [1, 2, 3, 4, 5, 6, 7, 8, 10]
        b = [sum(a[j : j + 4]) for j in range(len(a) - 3)]
        with self.assertRaisesRegex(VerificationError, "complement partition"):
            verify_prefix(a, b)

    def test_cli_json_and_hash_contract(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "result.json"
            with contextlib.redirect_stdout(output):
                result = main(["--terms", "80", "--window", "4", "--output", str(path)])
            self.assertEqual(result, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), output.getvalue())
        report = json.loads(output.getvalue())
        expected_bytes = ("\n".join(map(str, OEIS_FIRST_80)) + "\n").encode("ascii")
        self.assertEqual(report["prefix_sha256"], hashlib.sha256(expected_bytes).hexdigest())
        self.assertEqual(report["first20"], OEIS_FIRST_80[:20])

    def test_invalid_arguments(self):
        with self.assertRaises(ValueError):
            generate_prefix(0)
        with self.assertRaises(ValueError):
            generate_prefix(10, window=1)
        with self.assertRaises(ValueError):
            verify_prefix([], [])


if __name__ == "__main__":
    unittest.main()
