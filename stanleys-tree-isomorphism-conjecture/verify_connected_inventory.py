"""Recover the order-20 fixture from its unmarked connected-set census.

Python 3, standard library. A monomial is indexed by (vertex count, boundary).
The only cut-forest computation on the input tree is the final comparison.
"""
from collections import Counter
from itertools import product
from math import isqrt

from verify_complementary_fringe import halves, edges


def census(n, graph, root=None):
    adjacency = [0]*n
    for u,v in graph:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    data = Counter()
    for mask in range(1,1 << n):
        if root is not None and not (mask >> root) & 1:
            continue
        # Visit only vertices of the selected set; count edges crossing out.
        frontier = seen = mask & -mask
        boundary = 0
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            nbrs = adjacency[bit.bit_length()-1]
            boundary += (nbrs & ~mask).bit_count()
            new = nbrs & mask & ~seen
            frontier |= new
            seen |= new
        if seen == mask:
            data[mask.bit_count(),boundary] += 1
    return data


def mul(a,b):
    c = Counter()
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            c[i+k,j+l] += v*w
    return {s:v for s,v in c.items() if v}


def combine(*terms):
    c = Counter()
    for poly,scale in terms:
        for s,v in poly.items():
            c[s] += scale*v
    return {s:v for s,v in c.items() if v}


def shift(f,dx,dy):
    assert all(x+dx >= 0 and y+dy >= 0 for x,y in f)
    return {(x+dx,y+dy):v for (x,y),v in f.items()}


def exact_square_root(square):
    if not square:
        return {}
    i,j = max(square)
    v = isqrt(square[i,j])
    assert i%2 == j%2 == 0 and v*v == square[i,j]
    lead = (i//2,j//2)
    q = {lead:v}
    while True:
        residual = combine((square,1),(mul(q,q),-1))
        if not residual:
            return q
        r,s = max(residual)
        pos = (r-lead[0],s-lead[1])
        coeff,rem = divmod(residual[r,s],2*v)
        assert min(pos)>=0 and pos < min(q) and rem == 0
        q[pos] = coeff


def build_side(counts, dictionary):
    shape = tuple(t for copies,t in zip(counts,dictionary) for _ in range(copies))
    return edges(shape,0)


def join_sides(left,right,dictionary):
    a,b = build_side(left,dictionary),build_side(right,dictionary)
    h = len(a)+1
    return [(0,h)] + a + [(h+u,h+v) for u,v in b]


def reverse_at_degree(poly,degree,limit):
    return {(degree-i,j):v for (i,j),v in poly.items() if 0<=degree-i<=limit}


def branch_product(factors,counts):
    f = {(0,0):1}
    for g,k in zip(factors,counts):
        for _ in range(k):
            f = mul(f,g)
    return f


def reconstruct(data):
    n = max(i for i,j in data)
    h = n//2
    assert n == 2*h and data[h,1] == 2
    largest = max(i for (i,j),v in data.items() if i<h and j==1 and v)
    dictionary = [t for m in range(1,largest+1) for t in halves(m)]
    weights = [len(edges(t,0))+1 for t in dictionary]
    factors = []
    away = []
    for t,m in zip(dictionary,weights):
        graph = edges(t,0)
        r = census(m,graph,0)
        factors.append(combine((r,1),({(0,1):1},1)))
        away.append(combine((census(m,graph),1),(r,-1),(shift(r,0,1),1)))
    observed = reverse_at_degree(data,n,h-1)
    inventories = []
    tested = 0
    for counts in product(*(range(1+(n-2)//m) for m in weights)):
        if sum(k*m for k,m in zip(counts,weights)) != n-2:
            continue
        tested += 1
        p = branch_product(factors,counts)
        if reverse_at_degree(p,n-2,h-1) == observed:
            inventories.append((counts,p))
    assert len(inventories)==1
    counts,p = inventories[0]
    residual = combine((data,1),(shift(p,2,0),-1),
                       *((a,-k) for a,k in zip(away,counts)))
    total = shift(residual,-1,-1)
    delta = exact_square_root(combine((mul(total,total),1),(p,-4)))
    roots = []
    for sign in (+1,-1):
        twice = combine((total,1),(delta,sign))
        assert all(v%2 == 0 for v in twice.values())
        roots.append({s:v//2 for s,v in twice.items()})
    assert mul(*roots)==p
    decoded = []
    for root_poly in roots:
        hits = [c for c in product(*(range(k+1) for k in counts))
                if sum(k*m for k,m in zip(c,weights)) == h-1
                and branch_product(factors,c)==root_poly]
        assert len(hits)==1
        decoded.append(hits[0])
    assert tuple(a+b for a,b in zip(*decoded)) == counts
    return dictionary, counts, tuple(sorted(decoded)), tested


def cut_profile(graph, forced=None):
    m = len(graph)
    free = [i for i in range(m) if i!=forced]
    totals = Counter()
    for keep in range(1 << len(free)):
        parent = list(range(m+1))
        def find(v):
            while v != parent[v]:
                v = parent[v]
            return v
        for j,i in enumerate(free):
            if (keep >> j)&1:
                u,v = graph[i]
                parent[find(u)] = find(v)
        sizes = Counter(find(v) for v in range(m+1))
        totals[tuple(sorted(sizes.values()))] += 1
    return totals


def main():
    # Use the type order of verify_dictionary_example.py: singleton, edge,
    # three-vertex path rooted at an end, three-vertex path rooted at its center.
    leaf = ()
    dictionary = [leaf,(leaf,),((leaf,),),(leaf,leaf)]
    left,right = (1,1,2,0),(1,1,1,1)
    graph = join_sides(left,right,dictionary)
    data = census(20,graph)
    types,counts,split,tested = reconstruct(data)
    # Check in the fixture's own type order, independent of generator ordering.
    reorder = lambda c: tuple(c[types.index(t)] for t in dictionary)
    assert reorder(counts)==(2,2,3,1)
    assert sorted(map(reorder,split)) == sorted([left,right])
    l,r = (cut_profile(build_side(c,types)) for c in split)
    reconstructed = Counter()
    for x,v in l.items():
        for y,w in r.items():
            reconstructed[tuple(sorted(x+y))] += v*w
    direct = cut_profile(graph,forced=0)
    assert direct==reconstructed
    print("connected vertex sets",sum(data.values()),"nonzero census entries",len(data))
    print("candidate inventories",tested,"matching inventory",reorder(counts))
    print("quadratic split", sorted(map(reorder,split)))
    print("separated partitions",len(direct),"separated edge sets",sum(direct.values()))


if __name__=='__main__':
    main()
