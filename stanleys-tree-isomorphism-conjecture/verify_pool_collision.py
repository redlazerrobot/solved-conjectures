"""Enumerate all cut subsets for the unequal-inventory balanced pair."""
from collections import Counter


def tree(branches):
    parents = []
    for b in branches:
        base = len(parents)+1
        parents.append(0)
        parents.extend(base+i for i in b)
    return tuple(parents)


def table(left, right):
    parents = list(left)
    pivot = len(parents)
    base = pivot+1
    parents.append(0)
    parents.extend(base+i for i in right)
    total = Counter()
    separated = Counter()
    for bits in range(1<<len(parents)):
        sizes = [1]*(len(parents)+1)
        groups = []
        for i in range(len(parents),0,-1):
            if bits & (1<<(i-1)):
                groups.append(sizes[i])
            else:
                sizes[parents[i-1]] += sizes[i]
        signature = tuple(sorted(groups+[sizes[0]],reverse=True))
        total[signature] += 1
        if bits & (1<<pivot):
            separated[signature] += 1
    return total,separated


if __name__ == '__main__':
    # Arms 1,1,2. Removing a short leaf gives root with a leaf and a 2-path.
    # Removing the long arm tip gives a root whose one child has two leaves.
    r, s = tree([(),(0,)]), tree([tree([(),()])])
    halves = lambda a,b: (tree([tree([a]),()]), tree([b,(),()]))
    (a,ac),(b,bc) = [table(*halves(i,j)) for i,j in [(r,s),(s,r)]]
    h = len(halves(r,s)[0])+1
    hi = lambda c: Counter({k:v for k,v in c.items() if max(k)>h})
    assert hi(a) == hi(b)
    print('order',2*h,'subsets each',sum(a.values()), 'high signatures',len(hi(a)),'high cuts each',sum(hi(a).values()))
    keys=sorted(ac.keys() | bc.keys(),key=lambda k:(len(k),k))
    print('different separated signatures',sum(ac[k]!=bc[k] for k in keys))
    print('different full signatures',sum(a[k]!=b[k] for k in a.keys()|b.keys()))
    print('first separated witnesses (signature, separated counts, total counts)')
    print([(k, ac[k],bc[k],a[k],b[k]) for k in keys if ac[k]!=bc[k]][:8])
    assert sum(a.values()) == sum(b.values()) == 8192
    assert len(hi(a)) == 27 and sum(hi(a).values()) == 753
    assert sum(ac[k] != bc[k] for k in keys) == 66
    witness = (5, 4, 3, 2)
    assert (ac[witness], bc[witness], a[witness], b[witness]) == (4, 3, 5, 4)
