"""Verify the packet-switch identity as a bivariate polynomial by deleting edges."""
from collections import Counter
from fractions import Fraction
from math import comb


def grow(graph, root, branches):
    for branch in branches:
        nxt = len(graph)+1
        graph.append((root, nxt))
        grow(graph, nxt, branch)


def joined(a, b, c, d):
    graph = [(0, 1)]
    grow(graph, 0, a+b)
    grow(graph, 1, c+d)
    return graph


def cut_polynomial(graph, rooted=False):
    """Directly expand the distribution in p,z, without factoring at the join."""
    m = len(graph)
    bernstein = Counter()
    for mask in range(1 << m):
        parent = list(range(m+1))
        def find(v):
            while parent[v] != v:
                v = parent[v]
            return v
        for j, (u, v) in enumerate(graph):
            if mask >> j & 1:
                parent[find(u)] = find(v)
        counts = Counter(find(v) for v in range(m+1))
        orders = [counts[find(0)]] if rooted else counts.values()
        for size in orders:
            bernstein[mask.bit_count(), size] += 1
    # Change p^k(1-p)^(m-k) to ordinary powers of p.
    result = Counter()
    for (k, size), count in bernstein.items():
        for j in range(m-k+1):
            result[k+j, size] += count*(-1)**j*comb(m-k,j)
    return result


def packet(branches):
    graph = []
    grow(graph, 0, branches)
    return cut_polynomial(graph, rooted=True)


def difference(a,b):
    diff = a.copy()
    diff.subtract(b)
    return diff


def verify(a, b, c, d):
    graph = joined(a,b,c,d)
    lhs = difference(cut_polynomial(graph), cut_polynomial(joined(a,c,b,d)))
    ad = difference(packet(a), packet(d))
    bc = difference(packet(b), packet(c))
    rhs = Counter()
    for (i,u), alpha in ad.items():
        for (j,v), beta in bc.items():
            rhs[i+j,u+v-1] += alpha*beta
            rhs[i+j+1,u+v-1] -= alpha*beta
    assert lhs == rhs
    p, z = Fraction(2,5), Fraction(3,2)
    value = sum(w * p**j * z**s for (j,s),w in lhs.items())
    return len(graph)+1, sum(v != 0 for v in lhs.values()), value


if __name__ == '__main__':
    leaf = ()
    edge = (leaf,)
    fork = (leaf,leaf)
    path = (edge,)
    examples = [
        ("empty and unequal", (), (leaf,), (edge,), (leaf,leaf)),
        ("two multibranch packets", (leaf,edge), (edge,), (fork,), (leaf,leaf)),
        ("different three-vertex rootings", (fork,), (path,), (fork,), (path,)),
        ("identical packets", (edge,leaf), (), (fork,), (leaf,edge)),
    ]
    for label, a,b,c,d in examples:
        n, terms, value = verify(a,b,c,d)
        print(label, "vertices", n, "nonzero p,z terms", terms, "value", value)
