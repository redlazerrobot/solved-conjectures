"""Test unmarked percolation identities against all cut subsets of actual trees."""
from fractions import Fraction
from itertools import combinations

def attach(a, b):
    offset = len(a) + 1
    return tuple(a) + (0,) + tuple(offset + i for i in b)


def profiles(tree, p, t):
    g = h = 0
    for mask in range(1 << len(tree)):
        sizes = [1] * (len(tree) + 1)
        detached = []
        for i in range(len(tree), 0, -1):
            if (mask >> (i - 1)) & 1:
                detached.append(sizes[i])
            else:
                sizes[tree[i-1]] += sizes[i]
        cuts = len(detached)
        mass = (1-p)**cuts * p**(len(tree)-cuts)
        g += mass * t**sizes[0]
        h += mass * (t**sizes[0] + sum(t**j for j in detached))
    return g, h


def reductions(b, a, c, p, t):
    gb, hb = profiles(b,p,t)
    ga, ha = profiles(a,p,t)
    gc, hc = profiles(c,p,t)
    _, ha_join = profiles(attach(b,a),p,t)
    _, hc_join = profiles(attach(b,c),p,t)
    assert ha_join == hb+ha+p*(gb*ga-gb-ga)
    assert 1+(ha_join-hc_join-ha+hc)/(p*(ga-gc)) == gb


def half(branches):
    a = ()
    for b in branches:
        a = attach(a,b)
    return a


def main():
    t = 3
    p = Fraction(2,3)
    # Size-three path rooted first at its center, then at an end.
    a, c = (0,0), (0,1)
    for b in [(), (0,), (0,0,0), (0,1,0), (0,1,1,2)]:
        reductions(b,a,c,p,t)
    print('five two-context inversions, including equal-size markers')
    branches = [(), (0,), (0,0), (0,1)]
    products, sums = set(), set()
    assignments = 0
    for size in range(5):
        for selected in combinations(range(4), size):
            left = half([b for i,b in enumerate(branches) if i in selected])
            right = half([b for i,b in enumerate(branches) if i not in selected])
            g1,h1 = profiles(left,p,t)
            g2,h2 = profiles(right,p,t)
            _,h = profiles(attach(left,right),p,t)
            products.add(g1*g2)
            reconstructed_sum = g1*g2 - (h-h1-h2)/p
            assert reconstructed_sum == g1+g2
            sums.add(reconstructed_sum)
            assignments += 1
    assert len(products) == 1
    print(assignments,'assignments gave',len(products),'product and',len(sums),'root-profile sums')


if __name__ == '__main__':
    main()
