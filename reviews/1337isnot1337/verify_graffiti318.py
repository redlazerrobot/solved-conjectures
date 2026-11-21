"""Direct finite audit of Graffiti.pc 318. Run with ordinary Python 3."""
from collections import Counter
from itertools import combinations


def even_distance_counts(neighbors):
    n = len(neighbors)
    infinity = n + 1
    distance = [[0 if i == j else 1 if j in neighbors[i] else infinity
                 for j in range(n)] for i in range(n)]
    for k in range(n):
        for row in distance:
            for j in range(n):
                row[j] = min(row[j], row[k] + distance[k][j])
    if infinity in distance[0]:
        return None
    return tuple(sum(d % 2 == 0 for d in row) for row in distance)


def minimal_total_dominators(neighbors):
    """Domination covers every vertex, including selected vertices."""
    minima = []
    for size in range(1, len(neighbors) + 1):
        for subset in combinations(range(len(neighbors)), size):
            chosen = frozenset(subset)
            if any(previous <= chosen for previous in minima):
                continue
            if all(chosen & adjacent for adjacent in neighbors):
                minima.append(chosen)
    return minima


def graph(order, edges):
    neighbors = [set() for _ in range(order)]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def check_order(n):
    pairs = list(combinations(range(n), 2))
    counts = Counter()
    for edge_count in range(len(pairs) + 1):
        missing = len(pairs) - edge_count
        for edges in combinations(pairs, edge_count):
            counts['all'] += 1
            neighbors = graph(n, edges)
            even = even_distance_counts(neighbors)
            if even is None or max(even) < missing - 1:
                continue
            sizes = {len(s) for s in minimal_total_dominators(neighbors)}
            if max(even) >= missing:
                counts['qualifying'] += 1
                assert sizes == {2}, (n, edges, sizes)
            elif len(sizes) > 1:
                counts['relaxed failures'] += 1
    return counts


if __name__ == '__main__':
    for n in range(2, 7):
        counts = check_order(n)
        print(n, counts['all'], counts['qualifying'], counts['relaxed failures'])
    sharp = graph(5, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4)])
    assert even_distance_counts(sharp) == (1, 3, 3, 3, 3)
    assert set(minimal_total_dominators(sharp)) == {
        frozenset((0, i)) for i in range(1, 5)
    } | {frozenset((1, 2, 3, 4))}
    print("Sharpness graph: four minimal pairs and one minimal set of size four.")
