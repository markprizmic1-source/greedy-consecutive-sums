#!/usr/bin/env python3
"""Independent BFS checks of the proposed exact A242364 distance function.

Finite verification corroborates the written proof; it is not the proof.
"""
from functools import lru_cache
import argparse
import json


@lru_cache(None)
def height(x):
    if x == 0:
        return 1
    if x == 1:
        return 0
    if x % 2 == 0:
        return height(x // 2) + 1
    parent = (1 - x) // 2
    magnitude = -parent
    exceptional = parent < 0 and (magnitude & (magnitude - 1)) == 0
    return height(parent) + 2 - int(exceptional)


def verify(max_distance, edge_radius):
    frontier = {1}
    visited = {1}
    rows = []
    fib_previous, fib_current = 0, 1
    for distance in range(max_distance + 1):
        if distance:
            frontier = {y for x in frontier for y in (2*x, 1-x, 2-x)} - visited
            visited.update(frontier)
        assert all(height(x) == distance for x in frontier)
        positive = sum(x > 0 for x in frontier)
        even = sum(x % 2 == 0 for x in frontier)
        if distance >= 1:
            assert len(frontier) == 2 * fib_current
            assert positive == fib_current
            if distance >= 3:
                assert even == 2 * fib_previous
            fib_previous, fib_current = fib_current, fib_previous + fib_current
        rows.append({"distance": distance, "layer": distance + 1,
                     "total": len(frontier), "positive": positive,
                     "even": even, "odd": len(frontier) - even})
    for x in range(-edge_radius, edge_radius + 1):
        assert abs(height(1-x) - height(x)) <= 1
        assert abs(height(2-x) - height(x)) <= 1
        assert height(2*x) <= height(x) + 1
    return {"status": "passed", "scope": "finite verification only",
            "max_distance": max_distance,
            "visited_integers": len(visited),
            "edge_test_interval": [-edge_radius, edge_radius],
            "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-distance", type=int, default=25)
    parser.add_argument("--edge-radius", type=int, default=100000)
    args = parser.parse_args()
    print(json.dumps(verify(args.max_distance, args.edge_radius), indent=2))
