"""Recount the primary Pham necklace using bounded prefixes of ordinary pile sizes."""
from collections import Counter
from fractions import Fraction

WORD = (0, 0, 0, 1, 0, 0, 1, 0, 1, 1)
Q = (1, 0, 0, -1, -4, -6)
R = (10, 4, 10, 8, -14, -34, 14, 2)


def forward(piles):
    return tuple(sorted([len(piles)] + [v - 1 for v in piles if v > 1], reverse=True))


def level_counts(depth=25):
    copies = depth + 2
    length = copies * len(WORD)
    width = 3 * depth + 4
    roots = []
    for t in range(len(WORD)):
        parts = (length - i - 1 + WORD[(t+i) % len(WORD)] for i in range(length))
        roots.append(tuple(v for v in parts if v))
    assert len(set(roots)) == 10 and set(map(forward, roots)) == set(roots)
    root_keys = {(len(p), p[:width-1]) for p in roots}
    assert len(root_keys) == 10
    current = Counter((len(p), p[:width]) for p in roots)
    totals = [len(roots)]
    for d in range(depth):
        next_level = Counter()
        for (m, head), ways in current.items():
            assert len(head) == width - d and head[-1] < m-1 and len(head) < m
            last = None
            for i, v in enumerate(head):
                if v < m-1:
                    break
                if v != last:
                    updated = (v, tuple(a + 1 for a in head[:i] + head[i+1:]))
                    if d == 0:
                        # Removing the largest pile on a necklace-cycle vertex
                        # returns its predecessor, as checked on the full finite cycle.
                        part = next(p for p in roots if (len(p), p[:width]) == (m, head))
                        remain = part[:i] + part[i+1:]
                        full = tuple(a + 1 for a in remain) + (1,)*(v-m+1)
                        assert forward(full) == part
                        assert (full in roots) == (updated in root_keys)
                        if full in roots:
                            last = v
                            continue
                    next_level[updated] += ways
                last = v
        current = next_level
        totals.append(sum(current.values()))
    return totals


def reduced_gcd(a, b):
    a, b = list(map(Fraction, a)), list(map(Fraction, b))
    while b:
        while len(a) >= len(b):
            shift = len(a) - len(b)
            factor = a[-1] / b[-1]
            for i, v in enumerate(b):
                a[shift+i] -= factor*v
            while a and not a[-1]:
                a.pop()
        a, b = b, a
    return [c / a[-1] for c in a]


if __name__ == "__main__":
    h = level_counts()
    coefficients = [sum(q*h[n-j] for j, q in enumerate(Q) if j <= n) for n in range(len(h))]
    assert coefficients == list(R) + [0]*(len(h)-len(R))
    assert reduced_gcd(R,Q) == [1]
    print("h[0..25] =", h)
    print("Rational certificate and gcd hold.")
