"""Independent test of the Sonntag–Teichert claim, starting with out-arcs."""
from collections import Counter
from itertools import combinations, product


def hyperedges(vertices, arcs):
    """Try sets in increasing size, rejecting supersets of an earlier edge."""
    edges = []
    for size in range(1, len(vertices) + 1):
        for subset in combinations(vertices, size):
            chosen = frozenset(subset)
            if any(edge <= chosen for edge in edges):
                continue
            outside = vertices - chosen
            if all(any((u, v) in arcs for u in chosen) for v in outside):
                edges.append(chosen)
    return edges


def components(edges):
    """Traverse intersections of hyperedges. Ignore isolated vertices."""
    pending = set(edges)
    groups = []
    while pending:
        frontier = {pending.pop()}
        group = set(frontier)
        while frontier:
            neighbours = {e for e in pending if any(e & f for f in frontier)}
            pending -= neighbours
            group |= neighbours
            frontier = neighbours
        groups.append(group)
    return groups


def check(order, tournament):
    vertices = frozenset(range(order))
    pairs = list(combinations(sorted(vertices), 2))
    directions = (-1, 1) if tournament else (-1, 0, 1)
    counts = Counter()
    for orientation in product(directions, repeat=len(pairs)):
        arcs = {(i, j) if sign == 1 else (j, i)
                for (i, j), sign in zip(pairs, orientation) if sign}
        groups = components(hyperedges(vertices, arcs))
        counts[len(groups)] += 1
        if len(groups) > 1:
            assert not tournament and len(groups) == 2
            for g in groups:
                assert all(len(e) == 2 for e in g) and set.intersection(*map(set, g))
    return counts


if __name__ == "__main__":
    for tournament, orders in [(True, range(1, 7)), (False, range(1, 6))]:
        print("tournaments" if tournament else "oriented graphs")
        for order in orders:
            counts = check(order, tournament)
            print(order, sum(counts.values()), counts[2])
