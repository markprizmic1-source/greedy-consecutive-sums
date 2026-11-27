#!/usr/bin/env python3
"""Check greedy consecutive-window sums using exact integers.

The default window is four, giving OEIS A394676. For any window r >= 2,
the sequence starts at a_1 = 1. Each later term is the least larger
positive integer that is not a sum of r consecutive earlier terms.
Such sums are strictly increasing and exceed all their summands, so they
can be kept in a sorted queue. No bound is used to generate
the sequence.

With C = r*(r-1)//2 - 1, the checked inequalities are
    floor(((r+1)*n-C-1)/r) <= a_n <= floor(((r+1)*n-1)/r),
    (r+1)*j <= b_j <= (r+1)*j+C.

This program checks a finite prefix; it is not a proof for all indices.
The SHA-256 input is the ASCII decimal sequence, one term per line,
with a final newline. Only the Python standard library is required.

Example:
    python code/verify.py --terms 200000 --output verification.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence


class VerificationError(ValueError):
    """A generated prefix failed an exact mathematical check."""


def generate_prefix(terms: int, window: int = 4) -> tuple[list[int], list[int]]:
    """Return a_1,...,a_N and every available window sum b_j.

    Storage is O(N). Generation takes O(N) arithmetic operations: each
    candidate is accepted or equals a distinct forbidden sum.
    """
    if terms < 1:
        raise ValueError("terms must be at least 1")
    if window < 2:
        raise ValueError("window must be at least 2")

    a: list[int] = []
    b: list[int] = []
    head = 0
    candidate = 1
    running_sum = 0

    while len(a) < terms:
        if head < len(b) and candidate == b[head]:
            head += 1
            candidate += 1
            continue

        a.append(candidate)
        running_sum += candidate
        if len(a) > window:
            running_sum -= a[-window - 1]
        if len(a) >= window:
            b.append(running_sum)
        candidate += 1

    return a, b


def verify_prefix(a: Sequence[int], b: Sequence[int], window: int = 4) -> dict:
    """Check definitions, bounds and the complement partition independently.

    The partition is checked through a_N. Any window sum omitted from a
    prefix must contain some later a-term, which is greater than a_N.
    Hence no omitted sum can affect this checked interval.
    """
    if window < 2:
        raise ValueError("window must be at least 2")
    if not a:
        raise ValueError("a must contain at least one term")
    if a[0] != 1:
        raise VerificationError("a_1 is not 1")
    if any(x >= y for x, y in zip(a, a[1:])):
        raise VerificationError("a is not strictly increasing")
    expected_sums = max(0, len(a) - window + 1)
    if len(b) != expected_sums:
        raise VerificationError("the number of available window sums is wrong")
    if any(x >= y for x, y in zip(b, b[1:])):
        raise VerificationError("b is not strictly increasing")

    coefficient = window + 1
    constant = window * (window - 1) // 2 - 1
    min_a_error = max_a_error = window * a[0] - coefficient
    min_upper_gap = max_upper_gap = 0
    for n, value in enumerate(a, start=1):
        lower = (coefficient * n - constant - 1) // window
        upper = (coefficient * n - 1) // window
        if not lower <= value <= upper:
            raise VerificationError(
                f"a bound failed at n={n}: {lower} <= {value} <= {upper}"
            )
        error = window * value - coefficient * n
        min_a_error = min(min_a_error, error)
        max_a_error = max(max_a_error, error)
        upper_gap = upper - value
        min_upper_gap = min(min_upper_gap, upper_gap)
        max_upper_gap = max(max_upper_gap, upper_gap)

    min_b_error = max_b_error = None
    for j, value in enumerate(b, start=1):
        # Recompute each short window directly, independently of the
        # generator's rolling-sum update.
        expected = sum(a[j - 1 : j - 1 + window])
        if value != expected:
            raise VerificationError(
                f"window sum failed at j={j}: stored {value}, expected {expected}"
            )
        error = value - coefficient * j
        if not 0 <= error <= constant:
            raise VerificationError(
                f"b bound failed at j={j}: 0 <= {error} <= {constant}"
            )
        min_b_error = error if min_b_error is None else min(min_b_error, error)
        max_b_error = error if max_b_error is None else max(max_b_error, error)

    ai = bi = 0
    for value in range(1, a[-1] + 1):
        in_a = ai < len(a) and a[ai] == value
        in_b = bi < len(b) and b[bi] == value
        if in_a == in_b:
            problem = "overlap" if in_a else "missing integer"
            raise VerificationError(f"complement partition has {problem}: {value}")
        if in_a:
            ai += 1
        else:
            bi += 1

    digest = hashlib.sha256()
    for value in a:
        digest.update(f"{value}\n".encode("ascii"))

    return {
        "sequence": "greedy consecutive-window sums",
        "oeis_id": {3: "A394576", 4: "A394676"}.get(window),
        "window": window,
        "bound_constant_C": constant,
        "terms": len(a),
        "status": "passed",
        "first20": list(a[:20]),
        "last_term": a[-1],
        "verified": {
            "a_two_sided_bounds": len(a),
            "b_window_sums": len(b),
            "b_two_sided_bounds": len(b),
            "partition_integers": a[-1],
            "partition_a_terms": ai,
            "partition_b_terms": bi,
        },
        "a_error": {
            "expression": "r*a_n-(r+1)*n", "min": min_a_error, "max": max_a_error
        },
        "gap_from_a_upper_bound": {"min": min_upper_gap, "max": max_upper_gap},
        "b_error": {
            "expression": "b_j-(r+1)*j", "min": min_b_error, "max": max_b_error
        },
        "prefix_sha256": digest.hexdigest(),
        "hash_encoding": "ASCII decimal a-terms, one per line, final newline",
        "scope": "finite prefix only",
    }


def positive_integer(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def window_size(value: str) -> int:
    number = positive_integer(value)
    if number < 2:
        raise argparse.ArgumentTypeError("must be at least 2")
    return number


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", type=positive_integer, default=200000)
    parser.add_argument("--window", type=window_size, default=4)
    parser.add_argument("--output", type=Path, help="also write the JSON report here")
    args = parser.parse_args(argv)

    try:
        a, b = generate_prefix(args.terms, args.window)
        report = verify_prefix(a, b, args.window)
        payload = json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n"
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
        sys.stdout.write(payload)
    except (OSError, VerificationError) as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
