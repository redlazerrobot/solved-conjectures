"""Independent verification of the 31-vertex Li witness (standard Python only)."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from math import prod

parser = ArgumentParser(description=__doc__)
parser.add_argument('--old-spider', action='store_true',
                    help='check the spider with arm lengths 1, 2, 12, 15 from Horňák–Woźniak, Table 2')
old_spider = parser.parse_args().old_spider
pendant_parent = 14 if old_spider else 8
PATHS = [(0, 1), (0, 2, 3), (0, *range(4, 15)), (pendant_parent, 15), (0, *range(16, 31))]
edges = [(a, b) for path in PATHS for a, b in zip(path, path[1:])]
adj = {v: set() for v in range(31)}
children = {v: [] for v in adj}
for a, b in edges:
    adj[a].add(b)
    adj[b].add(a)
    children[a].append(b)
assert len({b for a, b in edges}) == len(edges) == 30
assert all(a < b for a, b in edges)

# In three colors put weights (1, t, -1-t); only e2 and e3 survive.
# Conditional coloring sums factor over children, each forbidden the parent's color.
def color_value(t):
    weights = [1, t, -1-t]
    def rooted(v):
        sub = [rooted(w) for w in children[v]]
        return [x * prod(sum(block) - block[i] for block in sub)
                for i, x in enumerate(weights)]
    return sum(rooted(0))

terms = [(14, 1), (11, 3), (8, 5), (5, 7), (2, 9)]
rows = []
for t in range(1, 6):
    e2, e3 = -1-t-t*t, -t*(1+t)
    rows.append(list(map(Fraction, [e2**a * e3**b for a, b in terms] + [color_value(t)])))
for i in range(len(rows)):
    pivot = next(j for j in range(i, len(rows)) if rows[j][i])
    rows[i], rows[pivot] = rows[pivot], rows[i]
    rows[i] = [v / rows[i][i] for v in rows[i]]
    for j in range(len(rows)):
        if i != j:
            rows[j] = [v - rows[j][i]*w for v, w in zip(rows[j], rows[i])]
coefficients = [row[-1] for row in rows]
assert all(x.denominator==1 for x in coefficients)
print("e2,e3 coefficients:", [int(x) for x in coefficients])
expected = [7, -148, 472, -34432, -10496] if old_spider else [29, 83, -6304, -6800, -8384]
assert coefficients == expected

# Enumerate the connected block containing the root by its boundary subtrees.
# Each frontier is an unordered forest below that block. Its components can
# be partitioned independently. This partitions the possibilities uniquely.
@lru_cache(None)
def root_blocks(v):
    options = [(1, ())]
    for child in children[v]:
        child_options = [(0, (child,)), *root_blocks(child)]
        options = [(k+j, frontier+boundary)
                   for k,frontier in options for j,boundary in child_options]
    return tuple(options)

# Distinct primes encode component orders, so multiplication encodes multiset union.
primes = tuple(k for k in range(2, 129) if all(k%d for d in range(2, int(k**0.5)+1)))
assert len(primes) == 31

@lru_cache(None)
def forest(roots):
    if not roots:
        return {1:1}
    first = partitions(roots[0])
    tail = forest(roots[1:])
    counts = Counter()
    for m,c in first.items():
        for q,d in tail.items():
            counts[m*q] += c*d
    return counts

@lru_cache(None)
def partitions(v):
    counts = Counter()
    for size, frontier in root_blocks(v):
        label = primes[size-1]
        for m,c in forest(frontier).items():
            counts[label*m] += c
    return counts

def integer_partitions(n, lower=1):
    if n == 0:
        yield 1
    for i in range(lower, n+1):
        for rem in integer_partitions(n-i,i):
            yield primes[i-1]*rem

counts = partitions(0)
all_types = set(integer_partitions(len(adj)))
assert set(counts) == all_types
leaves = {v for v in adj if len(adj[v])==1}
print("types, total, triple+pairs:", len(counts), sum(counts.values()), counts[primes[2]*primes[1]**14])
print("degrees above two:", sorted((v,len(ns)) for v,ns in adj.items() if len(ns)>2))
print("leaf neighbors of 0:", sorted(adj[0] & leaves))
print("degree of 0 after leaf pruning:", len(adj[0]-leaves))
assert len(counts) == 6842 and sum(counts.values()) == 2**30
assert counts[primes[2]*primes[1]**14] == 8
assert adj[0] & leaves == {1} and len(adj[0]-leaves) == 3
