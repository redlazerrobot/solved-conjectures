"""Verify the balanced-edge certificate by deleting edges directly."""
from collections import Counter
from verify_stable_relation import HALVES, TERMS


def partition(edges, mask):
    groups = [{i} for i in range(10)]
    for i, (u, v) in enumerate(edges):
        if mask & (1 << i):
            continue
        left = next(g for g in groups if u in g)
        right = next(g for g in groups if v in g)
        groups.remove(right)
        left.update(right)
    return tuple(sorted(map(len, groups)))


def main():
    total_difference = Counter()
    witness = (1, 2, 2, 5)
    witness_counts = []
    for sign, pair in TERMS:
        edges = [(0, 5)]
        for offset, key in zip((0, 5), pair):
            edges.extend((offset + child, offset + par)
                         for child, par in enumerate(HALVES[key], 1))
        ordinary, separated = Counter(), Counter()
        for mask in range(1 << len(edges)):
            sizes = partition(edges, mask)
            ordinary[sizes] += 1
            if mask & 1:
                separated[sizes] += 1
        for j in range(1, 3):
            expected = sum(ordinary[(t, 10-t)] for t in {j, 5-j})
            assert separated[(j, 5-j, 5)] == expected
        assert separated[(5, 5)] == 1
        assert sum(separated.values()) == 256
        witness_counts.append(separated[witness])
        for sizes, count in ordinary.items():
            total_difference[sizes] += sign * count
    assert not any(total_difference.values())
    signed = sum(n * sign for n, (sign, _) in zip(witness_counts, TERMS))
    assert signed == -1
    print("Full signed difference is zero; separated counts:", witness_counts)
    print("Signed coefficient at", witness, "=", signed)


if __name__ == "__main__":
    main()
