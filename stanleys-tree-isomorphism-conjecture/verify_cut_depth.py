"""Check the five-site family by whole-tree cuts and polynomial evaluations."""
from functools import lru_cache
from math import comb

from verify_short_witnesses import census, cuts, descendants


def limbs(level):
    left, right = ((), ()), (((),),)
    for _ in range(level):
        left, right = left + (right,), right + (left,)
    return left, right


def five_sites(level):
    b, c = limbs(level)
    d = b + c  # identify their roots
    p, q, a = c + (d,), b + (d,), (d,)
    return (p, a, b, c, q), (p, b, c, a, q)


def path(sites):
    tree = sites[-1]
    for site in reversed(sites[:-1]):
        tree = site + (tree,)
    return tree


def at_site(sites, i):
    return sites[i] + (path(sites[:i][::-1]), path(sites[i+1:]))


@lru_cache(None)
def connected_sets_at(tree, x, y):
    """Evaluate the rooted and ordinary connected-set polynomials at integers."""
    root, away = x, 0
    for child in tree:
        marked, whole = connected_sets_at(child, x, y)
        root *= y + marked
        away += whole + (y - 1) * marked
    return root, root + away


def large_slice(sites, center, h):
    """One exact modular evaluation per total order outside the central component."""
    prime = 1000000007
    weights = [1]
    for _ in range(2*h):
        weights.append((weights[-1]**2 + 18313) % prime)

    @lru_cache(None)
    def branch(node):
        coefficients = [1]
        for child in node:
            factor = branch(child)
            product = [0] * (len(coefficients) + len(factor) - 1)
            for i, a in enumerate(coefficients):
                for j, b in enumerate(factor):
                    product[i+j] += a*b
            coefficients = [v % prime for v in product]
        order = len(coefficients)
        ordinary = sum(v * weights[order-i] for i, v in enumerate(coefficients))
        return tuple(coefficients + [ordinary % prime])

    return branch(at_site(sites, center))[:h]


def cut_coefficient(tree, parts):
    """Count cuts with a specified partition into distinct sizes."""
    assert len(set(parts)) == len(parts)
    bits = {size: 1 << i for i, size in enumerate(parts)}
    full = (1 << len(parts)) - 1
    weights = [sum(value for value, bit in bits.items() if mask & bit)
               for mask in range(full + 1)]

    @lru_cache(None)
    def visit(node):
        size, counts = 1, {0: 1}
        for child in node:
            child_size, child_counts = visit(child)
            ways = {}
            for used, count in counts.items():
                for other, child_count in child_counts.items():
                    if used & other:
                        continue
                    occupied = used | other
                    product = count * child_count
                    ways[occupied] = ways.get(occupied, 0) + product
                    bit = bits.get(child_size - weights[other], 0)
                    if bit and not bit & occupied:
                        cut = occupied | bit
                        ways[cut] = ways.get(cut, 0) + product
            size += child_size
            counts = ways
        return size, counts

    size, counts = visit(tree)
    return sum(count for used, count in counts.items()
               if bits.get(size - weights[used]) == full ^ used)


def verify(level):
    first, second = five_sites(level)
    trees = [path(p) for p in (first, second)]
    sides = [(path(first[:2]), path(first[2:])), (path(second[:3]), path(second[3:]))]
    masks = list(map(descendants, trees))
    s = 3 * 2**level
    n, h = 10*s-2, 5*s-1
    assert all(len(m) == n for m in masks)
    assert all(len(descendants(t)) == h for pair in sides for t in pair)
    for k in range(level+1):
        left, right = [cuts(m, k)[0] for m in masks]
        assert left == right and sum(left.values()) == comb(n-1,k)
    if level <= 1:
        assert census(trees[0])[1] == census(trees[1])[1]
    for x, y in [(1,1), (2,3), (3,2)]:
        assert connected_sets_at(trees[0],x,y)[1] == connected_sets_at(trees[1],x,y)[1]
    sums = [sum(connected_sets_at(t,2,3)[1] for t in side) for side in sides]
    assert sums[0] != sums[1]
    a, b = large_slice(first,1,h), large_slice(second,3,h)
    first_difference = next(i for i in range(h) if a[i] != b[i])
    assert first_difference == 4*s-1
    limb_sizes = [3 * 2**i for i in range(level+1)]
    for small, large, sign in [(1, 2*s+1, 1), (2, 2*s, -1)]:
        parts = [small, *limb_sizes, large, 6*s-1]
        counts = [cut_coefficient(tree, parts) for tree in trees]
        assert counts[0] - counts[1] == sign, (parts, counts)
        print(f"coefficient {tuple(parts)}: {counts[0]} versus {counts[1]}")
    difference_example = None
    if level == 0:
        for k in range(1,5):
            left, right = [cuts(m, k)[0] for m in masks]
            for part in sorted(left.keys() | right.keys()):
                if part[-1] == n-first_difference and left[part] != right[part]:
                    difference_example = (part, left[part], right[part])
                    break
            if difference_example:
                break
        assert difference_example
    checked = sum(comb(n-1,k) for k in range(level+1))
    print(f"level={level} n={n} cuts through level per tree={checked} "
          f"first differing deficit={first_difference} largest differing part={n-first_difference}")
    if difference_example:
        print("Direct coefficient at the first differing deficit:", difference_example)


if __name__ == "__main__":
    for level in range(4):
        verify(level)
