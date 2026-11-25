"""Check a three-part cut witness for switches of padded composition caterpillars."""
from collections import Counter
from itertools import combinations, product
from itertools import accumulate
from math import prod


def near(left, right):
    return left[:-1] + (left[-1] + right[0],) + right[1:]


def compose(outer, inner):
    result = ()
    for part in outer:
        block = inner
        for _ in range(part - 1):
            block = near(block, inner)
        result += block
    return result


def spine(factors):
    composition = (1,)
    for factor in factors:  # innermost first
        composition = compose(factor, composition)
    return near(near((1,), composition), (1,))


def asymmetry(factor):
    size = sum(factor)
    prefixes = set(accumulate(factor[:-1]))
    return [int(i in prefixes) - int(size - i in prefixes) for i in range(size)]


def witness(factors, switched):
    signs = [(-1 if change else 1) for change in switched]
    values = [asymmetry(factor) for factor in factors]
    active = [l for l, f in enumerate(values) if any(f)]
    if len({signs[l] for l in active}) <= 1:
        return None
    lower = active[0]
    higher = next(l for l in active if signs[l] != signs[lower])
    sizes = [sum(factor) for factor in factors]
    n = prod(sizes) + 2
    f, g = values[lower], values[higher]
    u = next(i for i in range(1, (len(g) + 1) // 2) if g[i])
    t = 1 + prod(sizes[:higher]) * u
    if lower == 0:
        i = next(i for i in range(1, len(f) - 1) if f[i] != f[i + 1])
        q = 1 + i
        numerator = g[u] * (f[i] - f[i + 1])
    else:
        v = next(i for i in range(1, len(f)) if f[i])
        q = 1 + prod(sizes[:lower]) * v
        numerator = g[u] * f[v]
    p = t - q
    assert min(p, q) >= 2 and 2 * t < n
    denominator = 1 + int(p == q)
    assert numerator and numerator % denominator == 0
    return tuple(sorted((p, q, n - t))), numerator // denominator


def component_counts(weights):
    """Enumerate all pairs of actual edges, using the three possible rooted pieces."""
    graph = [[] for _ in range(sum(weights))]
    next_leaf = len(weights)
    for v, weight in enumerate(weights):
        if v:
            graph[v].append(v - 1)
            graph[v - 1].append(v)
        for _ in range(weight - 1):
            graph[v].append(next_leaf)
            graph[next_leaf].append(v)
            next_leaf += 1

    # Deleting v's parent edge cuts off exactly its interval in DFS preorder.
    intervals = []
    preorder = 0

    def visit(v, parent):
        nonlocal preorder
        start = preorder
        preorder += 1
        for w in graph[v]:
            if w != parent:
                visit(w, v)
        if parent >= 0:
            intervals.append((start, preorder))

    visit(0, -1)
    counts = Counter()
    n = len(graph)
    for (a, b), (c, d) in combinations(sorted(intervals), 2):
        first, second = b - a, d - c
        if c < b:
            pieces = second, first - second, n - first
        else:
            pieces = first, second, n - first - second
        counts[tuple(sorted(pieces))] += 1
    return counts


def compositions(n):
    for cut in product((False, True), repeat=n - 1):
        boundaries = [0] + [s for s, present in enumerate(cut, 1) if present] + [n]
        yield tuple(b - a for a, b in zip(boundaries, boundaries[1:]))


def verify(factors):
    original = spine(factors)
    counts = component_counts(original)
    nontrivial = 0
    for changes in product((False, True), repeat=len(factors)):
        predicted = witness(factors, changes)
        changed = spine([factor[::-1] if change else factor
                         for factor, change in zip(factors, changes)])
        if predicted is None:
            assert changed == original or changed == original[::-1]
            continue
        cut, difference = predicted
        assert counts[cut] - component_counts(changed)[cut] == difference, (factors, changes)
        nontrivial += 1
    return nontrivial


if __name__ == "__main__":
    small = [c for n in range(2, 6) for c in compositions(n)]
    tested = sum(verify(factors) for factors in product(small, repeat=2))
    print(f"{tested} nontrivial oriented switches across 900 two-factor inputs passed.")
    # The first two exercise the symmetric innermost case. The last two also
    # exercise switches at more than one active level and global reflection.
    fixtures = [((2,), (1, 2), (1, 3)), ((1, 2, 1), (2, 1), (1, 2)),
                ((1, 2), (1, 3), (2, 1)), ((1, 2), (2,), (1, 2), (2, 1))]
    print(f"{sum(map(verify, fixtures))} additional multifactor switches passed.")
    factors = ((1, 2), (1, 1, 2))
    weights = spine(factors)
    changed = spine((factors[0][::-1], factors[1]))
    cut, difference = witness(factors, (True, False))
    print(f"{weights} vs {changed}: {cut} gives {component_counts(weights)[cut]} "
          f"versus {component_counts(changed)[cut]}, signed difference {difference}.")
