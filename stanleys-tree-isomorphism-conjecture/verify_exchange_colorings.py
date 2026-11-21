"""Directly compare chromatic symmetric functions for a two-site exchange."""
from collections import Counter
from itertools import product
from math import factorial, prod


def monomial_coefficients(n, edges):
    neighbors = [set() for _ in range(n)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    blocks = []
    counts = Counter()

    def place(v):
        if v == n:
            sizes = tuple(sorted(map(len, blocks), reverse=True))
            counts[sizes] += 1
            return
        for block in blocks:
            if neighbors[v].isdisjoint(block):
                block.add(v)
                place(v + 1)
                block.remove(v)
        # Order the color classes by their smallest vertex.
        blocks.append({v})
        place(v + 1)
        blocks.pop()

    place(0)
    # Equal-sized blocks can permute their assigned colors for a fixed monomial.
    return {sizes: c * prod(factorial(m) for m in Counter(sizes).values())
            for sizes, c in counts.items()}


def graft(leaf_site, path_site):
    # The core is path 0-1-2-3-4 with an additional leaf 5 at 1.
    core = [(0,1), (1,2), (2,3), (3,4), (1,5)]
    return core + [(leaf_site,6), (path_site,7), (7,8)]


def main():
    for a, b in [(0,4),(0,5)]:
        forward = monomial_coefficients(9, graft(a,b))
        reverse = monomial_coefficients(9, graft(b,a))
        keys = set(forward) | set(reverse)
        changed = sorted((s for s in keys if forward.get(s,0) != reverse.get(s,0)),
                         key=lambda s: (len(s), s))
        print(f"sites {a},{b}: {len(changed)} differing coefficients")
        if b == 4:
            assert len(changed) == 14
            size = (3,3,3)
            observed = forward[size], reverse[size]
            assert observed == (156,168)
            # Independently count the specific monomial x_1^3 x_2^3 x_3^3.
            for graph, expected in zip((graft(a,b), graft(b,a)), observed):
                actual = sum(colors.count(0) == colors.count(1) == 3
                             and all(colors[u] != colors[v] for u,v in graph)
                             for colors in product(range(3), repeat=9))
                assert actual == expected
            print("m_(3,3,3):", *observed)
        else:
            assert not changed


if __name__ == '__main__':
    main()
