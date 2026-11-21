"""Recover both layers of an order-20 fixture directly from edge-cut profiles."""
from collections import Counter
from itertools import product

# Parent lists for branches rooted at vertex 0.
types = [(), (0,), (0,1), (0,0)]


def grow(p, root, branches):
    for t, count in zip(types, branches):
        for _ in range(count):
            offset = len(p) + 1
            p.append(root)
            p.extend(offset + parent for parent in t)


def profiles(parents, root_omitted=False):
    n = len(parents) + 1
    result = Counter()
    for cut in range(1 << (n - 1)):
        sizes = [1] * n
        parts = []
        for i in range(n - 1, 0, -1):
            if cut & (1 << (i - 1)):
                parts.append(sizes[i])
            else:
                sizes[parents[i-1]] += sizes[i]
        if not root_omitted:
            parts.append(sizes[0])
        result[tuple(sorted(parts))] += 1
    return result


def multiply(a, b, k):
    c = Counter()
    for x, u in a.items():
        for y, v in b.items():
            if sum(x) + sum(y) <= k:
                c[tuple(sorted(x+y))] += u*v
    return c


factors = []
for t in types:
    factors.append(profiles([0]+[i+1 for i in t], root_omitted=True))


def pooled(counts, k):
    result = {():1}
    for f, c in zip(factors, counts):
        for _ in range(c):
            result = multiply(result, f, k)
    return result


def recover(u, n, k, total_branch_weight):
    observed = Counter()
    for parts, c in u.items():
        if n-parts[-1] <= k:
            observed[parts[:-1]] += c
    answers = []
    weights = [len(t)+1 for t in types]
    for counts in product(*(range(total_branch_weight//w+1) for w in weights)):
        if sum(a*b for a,b in zip(counts,weights)) != total_branch_weight:
            continue
        if pooled(counts,k) == observed:
            answers.append(counts)
    return answers


def main():
    left = (1,1,2,0)
    right = (1,1,1,1)
    combined = [0]
    grow(combined,0,left)
    grow(combined,1,right)
    u = profiles(combined)
    pooled_answers = recover(u,20,9,18)
    assert pooled_answers == [(2,2,3,1)]
    keep = Counter()
    for parts, c in pooled(pooled_answers[0],18).items():
        keep[tuple(sorted(parts+(20-sum(parts),)))] += c
    separated = u.copy()
    separated.subtract(keep)
    assert min(separated.values()) >= 0
    separated = +separated
    # Starting from the recovered pool, try every equal-weight allocation.
    # This avoids needing a symbolic multivariate factorization package.
    inventory = pooled_answers[0]
    recovered = []
    for allocation in product(*(range(c+1) for c in inventory)):
        if sum(c*(len(t)+1) for c,t in zip(allocation,types)) != 9:
            continue
        other = tuple(c-a for c,a in zip(inventory,allocation))
        if allocation > other:
            continue
        profiles_of_pair = []
        for counts in (allocation,other):
            parents = []
            grow(parents,0,counts)
            profiles_of_pair.append(profiles(parents))
        if multiply(*profiles_of_pair,20) == separated:
            recovered.append((allocation,other))
    assert recovered == [tuple(sorted((left,right)))]
    halves = []
    for counts in [left,right]:
        parents = []
        grow(parents,0,counts)
        halves.append(profiles(parents))
    deleted = multiply(*halves,20)
    assert u == keep + deleted
    assert recover(halves[0],10,6,9) == [left]
    assert recover(halves[1],10,6,9) == [right]
    print('full cuts',sum(u.values()),'kept',sum(keep.values()),'separated',sum(deleted.values()))
    print('unique pooled counts',pooled_answers[0],'recovered unordered split',recovered)


if __name__ == '__main__':
    main()
