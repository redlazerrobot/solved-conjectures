"""Check the fixed-context inversion and its first noninjective order by deletion."""
from collections import Counter
from itertools import combinations
from functools import lru_cache


def join(marker, branch):
    offset = len(marker) + 1
    return marker + (0,) + tuple(offset + p for p in branch)


def cuts(parents, root_omitted):
    n = len(parents) + 1
    result = Counter()
    for mask in range(1 << len(parents)):
        sizes = [1] * n
        detached = []
        for child, parent in reversed(list(enumerate(parents, 1))):
            if mask & (1 << (child - 1)):
                detached.append(sizes[child])
            else:
                sizes[parent] += sizes[child]
        if not root_omitted:
            detached.append(sizes[0])
        result[tuple(sorted(detached))] += 1
    return result


def mult(left, right):
    result = Counter()
    for p, a in left.items():
        for q, b in right.items():
            result[tuple(sorted(p + q))] += a * b
    return result


def complete(n, erased):
    result = Counter()
    for p, a in erased.items():
        result[tuple(sorted(p + (n - sum(p),)))] += a
    return result


def verify(marker, branch):
    s, n = len(marker) + 1, len(branch) + 1
    assert n <= s + 2
    u = cuts(join(marker, branch), False)
    a = cuts(marker, True)
    um = cuts(marker, False)
    if n > s:
        # Among separated cuts with a component of size >=n only the whole B can occur.
        u.subtract(mult({(n,): 1}, um))
    k = min(n - 1, s) if n > s else n - 1
    observed = Counter()
    for p, c in u.items():
        if s + n - p[-1] <= k:
            observed[p[:-1]] += c
    # Divide the truncated product by a, which has constant coefficient 1.
    b = Counter()
    for d in range(k + 1):
        old = mult(a, b)
        for p in observed.keys() | old.keys():
            if sum(p) == d:
                b[p] += observed[p] - old[p]
    b = +b
    actual_b = cuts(branch, True)
    assert b == +Counter({p: c for p, c in actual_b.items() if sum(p) <= k})
    if k == n - 1:
        return
    # n=s+2. All remaining terms contain the common factor J_1.
    residual = cuts(join(marker, branch), False)
    for r in range(2, n + 1):
        br = {p: c for p, c in b.items() if sum(p) == n - r}
        jr = complete(s + r, a) + mult({(r,): 1}, um)
        residual.subtract(mult(br, jr))
    j1 = complete(s + 1, a) + mult({(1,): 1}, um)
    top = {p: c for p, c in actual_b.items() if sum(p) == n - 1}
    assert residual == mult(top, j1)


if __name__ == "__main__":
    from verify_complementary_fringe import halves, edges
    tested = 0
    for s in range(1, 5):
        for t in halves(s):
            marker = tuple(a for a, _ in edges(t, 0))
            for n in range(1, s + 3):
                for b in halves(n):
                    branch = tuple(a for a, _ in edges(b, 0))
                    verify(marker, branch)
                    tested += 1
    print(tested, "marker/branch pairs passed")
    # s=1, n=4. Two different root degrees, but both joins form the same fork.
    assert cuts(join((), (0, 0, 1)), False) == cuts(join((), (0, 1, 1)), False)
    assert cuts((0, 0, 1), True) != cuts((0, 1, 1), True)
    print("s=1,n=4 collision verified")
