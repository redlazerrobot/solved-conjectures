"""Check recovery from large two-edge cuts and the connected-set census."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from math import isqrt


@lru_cache(None)
def rooted_shapes(order):
    """A rooted tree is the sorted tuple of the rooted trees at its children."""
    choices = [(n, tree) for n in range(1, order) for tree in rooted_shapes(n)]
    result = []

    def choose(remaining, start, children):
        if remaining == 0:
            result.append(tuple(children))
        for i in range(start, len(choices)):
            n, tree = choices[i]
            if n > remaining:
                break
            choose(remaining - n, i, children + [tree])

    choose(order - 1, 0, [])
    return result


def join(left, right):
    edges = [(0, 1)]
    next_vertex = 2

    def append(tree, parent):
        nonlocal next_vertex
        for child in tree:
            v = next_vertex
            next_vertex += 1
            edges.append((parent, v))
            append(child, v)

    append(left, 0)
    append(right, 1)
    return edges


@lru_cache(None)
def subset_orders(n):
    orders = bytearray(1 << n)
    for mask in range(1, 1 << n):
        orders[mask] = 1 + orders[mask & (mask - 1)]
    return orders


def direct_census(edges):
    """Enumerate all vertex subsets, checking connectivity by induced edge count."""
    n = len(edges) + 1
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    orders = subset_orders(n)
    degree = [orders[mask] for mask in adjacency]
    internal_edges = bytearray(1 << n)
    total_degree = bytearray(1 << n)
    census, spanning = Counter(), Counter()
    for mask in range(1, 1 << n):
        first = mask & -mask
        v = first.bit_length() - 1
        rest = mask ^ first
        internal = internal_edges[rest] + orders[rest & adjacency[v]]
        degrees = total_degree[rest] + degree[v]
        internal_edges[mask], total_degree[mask] = internal, degrees
        k = orders[mask]
        if internal == k - 1:
            key = (k, degrees - 2 * internal)
            census[key] += 1
            if mask & 3 == 3:
                spanning[key] += 1
    return census, spanning


def direct_cut_counts(edges, cut_sets):
    n = len(edges) + 1
    counts = Counter()
    for cuts in cut_sets:
        owner = list(range(n))
        for i, (a, b) in enumerate(edges):
            if i in cuts:
                continue
            while owner[a] != a:
                a = owner[a]
            while owner[b] != b:
                b = owner[b]
            owner[b] = a
        sizes = Counter()
        for v in range(n):
            while owner[v] != v:
                v = owner[v]
            sizes[v] += 1
        counts[tuple(sorted(sizes.values()))] += 1
    return counts


def recover(h, census, large):
    n = 2 * h
    N = [0] + [census[i, 1] for i in range(1, h)]
    M = max(i for i in range(1, h) if N[i])
    assert 3 * M <= n + 1
    # Count occurrences, including repeated parts of the same triple.
    residual = Counter({k: census[k, 2] + (n - k - 1) * census[k, 1]
                        for k in range(1, n)})
    known = large.copy()
    for i in range(1, h):
        known[tuple(sorted((i, h - i, h)))] += N[i]
    for triple, count in known.items():
        for k in triple:
            residual[k] -= count
    assert min(residual.values()) >= 0
    total, remainder = divmod(sum(residual.values()), 3)
    assert not remainder

    convolution = {}
    for s in range(h, 2 * M + 1):
        if n - s > M:
            convolution[s] = residual[n - s]
        elif s == 2 * M:
            convolution[s] = int(N[M] == 2)
    unknown = set(range(h, 2 * M + 1)) - convolution.keys()
    assert len(unknown) <= 1
    if unknown:
        convolution[unknown.pop()] = total - sum(convolution.values())
    assert sum(convolution.values()) == total

    square = {}
    for s, value in convolution.items():
        pooled = sum(N[i] * N[s - i] for i in range(1, h) if 0 < s - i < h)
        square[s] = pooled - 4 * value
    imbalance = [0] * h
    nonzero = [s for s, value in square.items() if value]
    if nonzero:
        highest = max(nonzero)
        assert not highest % 2
        d = highest // 2
        imbalance[d] = isqrt(square[highest])
        assert imbalance[d] ** 2 == square[highest]
        for j in range(d - 1, h - d - 1, -1):
            s = d + j
            inside = sum(imbalance[i] * imbalance[s - i] for i in range(j + 1, d))
            imbalance[j], extra = divmod(square[s] - inside, 2 * imbalance[d])
            assert not extra
    for i in range(1, M + 1):
        for j in range(max(i, h - i), M + 1):
            numerator = N[i] * N[j] - imbalance[i] * imbalance[j]
            cross, extra = divmod(numerator, 4 if i == j else 2)
            assert not extra and cross >= 0
            known[tuple(sorted((i, j, n - i - j)))] += cross
    four_parts = Counter()
    if nonzero:
        sides = [Counter(), Counter()]
        for i in range(h - d, h):
            pair = tuple(sorted((i, h - i)))
            if pair[0] < h - d:
                continue
            for side, sign in zip(sides, (1, -1)):
                side[pair] += (N[i] + sign * imbalance[i]) // 2
        for lpair, a in sides[0].items():
            for rpair, b in sides[1].items():
                four_parts[tuple(sorted(lpair + rpair))] += a * b
    return +known, (h - d if nonzero else None), +four_parts


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-half", type=int, default=7, choices=range(2, 9))
    args = parser.parse_args()
    for h in range(2, args.max_half + 1):
        n = 2 * h
        cases = reconstructed = boundary = nonzero = four_nonzero = 0
        for left, right in combinations_with_replacement(rooted_shapes(h), 2):
            edges = join(left, right)
            census, spanning = direct_census(edges)
            all_triples = direct_cut_counts(edges, combinations(range(n - 1), 2))
            actual_marginals = Counter()
            for triple, count in all_triples.items():
                for k in triple:
                    actual_marginals[k] += count
            for k in range(1, n):
                assert actual_marginals[k] == census[k, 2] + (n - k - 1) * census[k, 1]
            for b in range(n):
                assert census[h, b] - spanning[h, b] == (2 if b == 1 else 0)
                removed = (census[h - 1, 1] if b == 1 else census[1, 1] if b == 2 else 0)
                assert census[h - 1, b] - spanning[h - 1, b] == removed
            cases += 1
            M = max(i for i in range(1, h) if census[i, 1])
            if 3 * M <= n + 1:
                large = Counter({p: c for p, c in all_triples.items() if max(p) > h})
                recovered, first, four_parts = recover(h, census, large)
                assert recovered == all_triples, (h, left, right)
                reconstructed += 1
                if first is not None:
                    nonzero += 1
                    cuts = ((0, a, b) for a, b in combinations(range(1, n - 1), 2))
                    separated = direct_cut_counts(edges, cuts)
                    allowed = Counter({p: v for p, v in separated.items()
                                       if min(p) >= first and max(p) < h})
                    assert four_parts == allowed, (h, left, right)
                    four_nonzero += len(four_parts)
                boundary += 3 * M >= n
        print(f"h={h}: checked {cases} trees; {reconstructed} reconstructed, "
              f"{boundary} boundary cases, {nonzero} nonzero square tails, "
              f"{four_nonzero} positive four-part bins.")


if __name__ == "__main__":
    main()
