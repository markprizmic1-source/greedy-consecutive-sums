#!/usr/bin/env python3
"""Finite consistency checks for the proved A394676 long equality runs.

Generation uses the original greedy rule in verify_greedy.py.  None of the
new identities is used to generate the sequence.  Passing a finite check is
not a substitute for the proof in paper.tex.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from verify_greedy import generate_prefix


def check(terms: int = 400_000) -> dict:
    if terms < 10:
        raise ValueError("At least ten terms are required.")
    a, b = generate_prefix(terms, 4)
    e = [0] + [(5 * n - 1) // 4 - value for n, value in enumerate(a, 1)]
    d = [0] + [value - 5 * j for j, value in enumerate(b, 1)]
    if e[1:5] != [0, 0, 0, 0]:
        raise AssertionError("Initial errors differ.")
    for n in range(5, terms + 1):
        q, rem = divmod(n - 1, 4)
        s = rem + 1
        expected = int(d[q] >= s) + int(s == 1 and d[q - 1] == 5)
        if e[n] != expected:
            raise AssertionError(("error identity", n, e[n], expected))
    for j in range(1, len(d)):
        if not (0 <= d[j] <= 5 and d[j] >= d[j - 1] - 1):
            raise AssertionError(("preliminary bound", j))
        if d[j] != 5 - sum(e[j:j + 4]):
            raise AssertionError(("window identity", j))
        parent_zero = (j - 2) // 4
        zero_expected = parent_zero >= 1 and d[parent_zero] == 5
        if (d[j] == 0) != zero_expected:
            raise AssertionError(("zero-set identity", j))
        parent_five = (j + 2) // 4
        five_expected = j == 1 or d[parent_five] == 0
        if (d[j] == 5) != five_expected:
            raise AssertionError(("five-set identity", j))
        parent_base16 = (j - 6) // 16
        base16_expected = j == 1 or (parent_base16 >= 1 and d[parent_base16] == 5)
        if (d[j] == 5) != base16_expected:
            raise AssertionError(("base-sixteen identity", j))

    completed = []
    run_start = None
    for n in range(1, terms + 1):
        if e[n] == 0 and run_start is None:
            run_start = n
        elif e[n] != 0 and run_start is not None:
            if n - run_start >= 4:
                completed.append({"first_index": run_start, "last_index": n - 1,
                                  "length": n - run_start})
            run_start = None
    predicted = []
    m = 0
    while True:
        power = 16 ** m
        first = (7 * power - 2) // 5
        last = (12 * power + 8) // 5
        if last >= terms:
            break
        predicted.append({"first_index": first, "last_index": last,
                          "length": power + 3})
        m += 1
    if completed != predicted:
        raise AssertionError(("completed maximal long runs", completed, predicted))

    digest = hashlib.sha256("".join(f"{x}\n" for x in a).encode("ascii")).hexdigest()
    return {
        "sequence": "OEIS A394676", "terms_generated": terms,
        "last_selected_value": a[-1], "exact_error_instances_checked": terms - 4,
        "complete_windows_checked": len(b), "zero_set_identity": "pass",
        "five_set_identity": "pass", "base16_recurrence": "pass",
        "completed_maximal_equality_runs_of_length_at_least_four": completed,
        "prefix_sha256": digest,
        "scope": "Finite consistency checks; the written proof establishes the infinite claim."
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terms", type=int, default=400_000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(check(args.terms), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    print(result, end="")


if __name__ == "__main__":
    main()
