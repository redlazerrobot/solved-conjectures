"""Recover side counts by binary lifting and compare with independent edge cuts.

Runs with Python 3 alongside verify_complementary_fringe.py.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement
from verify_complementary_fringe import halves, edges, partition


def rows(h, counts, n):
    """Store distinct unordered endpoint size pairs possible in each equation."""
    equations = []
    for a in range(1, h):
        for b in range(a, h):
            c = 2*h-a-b
            if not b <= c <= h:
                continue
            parts = (a, b, c)
            pairs = {p for p in combinations(parts, 2) if p[1] < h}
            value = counts[parts]
            if c == h:
                value -= sum(n[s] for s in {a, b})
            equations.append((sorted(pairs), value))
    return equations


def evaluate(pairs, n, r):
    value = 0
    for a, b in pairs:
        value += (n[a]-r[a])*r[b]
        if a != b:
            value += (n[b]-r[b])*r[a]
    return value


def solve_binary(rows, width):
    """Return the unique solution mask, or None if the system lacks full rank."""
    pivots = {}
    for row, rhs in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = row, rhs
                break
            prior_row, prior_rhs = pivots[pivot]
            row ^= prior_row
            rhs ^= prior_rhs
        else:
            assert rhs == 0
    if len(pivots) < width:
        return None
    answer = 0
    for pivot in sorted(pivots):
        row, rhs = pivots[pivot]
        if (row & answer).bit_count() % 2 != rhs:
            answer |= 1 << pivot
    return answer


def recover(h, counts):
    n = [0] + [counts[s, 2*h-s] for s in range(1, h)]
    pinned = {s: 1 for s in range(1, h) if 2*s >= h and n[s] == 2}
    # Even equality 2*s=h also forces at most one s-fringe per half.
    anchor = next((s for s in reversed(range(1, h)) if n[s] == 1), None)
    if anchor is not None:
        pinned[anchor] = 0
    r = [pinned.get(s, 0) for s in range(h)]
    equations = rows(h, counts, n)
    step = 1
    while step <= max(n):
        active = [s for s in range(1, h) if step <= n[s] and s not in pinned]
        system = []
        for pairs, obs in equations:
            value = evaluate(pairs, n, r)
            assert (obs-value) % step == 0
            mask = 0
            for j, s in enumerate(active):
                r[s] += step
                delta = (evaluate(pairs, n, r)-value)//step
                r[s] -= step
                mask |= (delta % 2) << j
            system.append((mask, ((obs-value)//step) % 2))
        assert (h-1-sum(r)) % step == 0
        system.append(((1 << len(active))-1, ((h-1-sum(r))//step) % 2))
        update = solve_binary(system, len(active))
        if update is None:
            return None
        for j, s in enumerate(active):
            r[s] += step*((update >> j) & 1)
        step *= 2
    return tuple(r[1:])


def split_counts(histogram, h):
    """Monomials for exactly one edge cut inside the given half."""
    counts = Counter()
    for size, multiplicity in enumerate(histogram, 1):
        counts[tuple(sorted((size, h-size)))] += multiplicity
    return counts


def check_four_parts(h, graph, counts, profile):
    other = tuple(counts[s, 2*h-s] - profile[s-1] for s in range(1, h))
    prediction = Counter()
    for p, a in split_counts(profile, h).items():
        for q, b in split_counts(other, h).items():
            prediction[tuple(sorted(p+q))] += a*b
    actual = Counter()
    for a, b in combinations(range(1, len(graph)), 2):
        sizes = partition(2*h, graph, (0, a, b))
        if max(sizes) < h:
            actual[sizes] += 1
    assert actual == prediction


def check_ambiguity():
    leaf = ()
    joins = [((leaf, leaf, (leaf, leaf)), (((leaf, leaf, leaf),),)),
             ((leaf, (leaf, leaf, leaf)), ((leaf, (leaf, leaf)),))]
    profiles = []
    placements = []
    for left, right in joins:
        graph = [(0, 6)] + edges(left, 0) + edges(right, 6)
        counts = Counter(partition(12, graph, cut) for size in (1, 2)
                         for cut in combinations(range(11), size))
        side = {partition(12, graph, (j,))[0] for j in range(1, 6)}
        placements.append((4 in side) == (5 in side))
        assert recover(6, counts) is None
        profiles.append(counts)
    a, b = profiles
    changes = {p: (a[p], b[p]) for p in set(a) | set(b) if a[p] != b[p]}
    assert changes == {(1, 4, 7): (8, 7), (2, 3, 7): (0, 1)}
    assert placements == [True, False]
    print("large-fringe placement ambiguity confirmed:", changes)


def main():
    for h in range(3, 9):
        hits = 0
        total = 0
        example = None
        for left, right in combinations_with_replacement(halves(h), 2):
            graph = [(0, h)] + edges(left, 0) + edges(right, h)
            counts = Counter()
            ground = [Counter(), Counter()]
            for length in (1, 2):
                for cut in combinations(range(len(graph)), length):
                    p = partition(2*h, graph, cut)
                    counts[p] += 1
                    if length == 1 and cut[0] != 0:
                        ground[int(cut[0] >= h)][p[0]] += 1
            profile = recover(h, counts)
            if profile is not None:
                assert any(profile == tuple(s[k] for k in range(1, h)) for s in ground)
                hits += 1
                if profile[0] >= 3 and any(profile[1:]):
                    example = (left, right, profile)
            total += 1
        print(f"h={h}: recovered {hits}/{total} joins", flush=True)
        if h == 6:
            print("example:", example)


if __name__ == "__main__":
    main()
    check_ambiguity()
