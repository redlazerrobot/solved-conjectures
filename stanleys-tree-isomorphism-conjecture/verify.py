"""Check the two proof notes directly from unlabelled edge-cut partitions."""

from collections import Counter
from itertools import combinations
from math import prod


def forest_partition(vertex_count, edges, removed, root=None):
    """Return sorted component sizes, omitting the root's component if requested."""
    parent = list(range(vertex_count))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index, (left, right) in enumerate(edges):
        if index not in removed:
            parent[find(left)] = find(right)
    sizes = Counter(find(v) for v in range(vertex_count))
    if root is not None:
        del sizes[find(root)]
    return tuple(sorted(sizes.values()))


def cuts(vertex_count, edges, root=None, cut_count=None):
    counts = Counter()
    levels = range(len(edges) + 1) if cut_count is None else [cut_count]
    for level in levels:
        for removed in combinations(range(len(edges)), level):
            partition = forest_partition(vertex_count, edges, set(removed), root)
            counts[partition] += 1
    return counts


def multiply(left, right, limit):
    result = Counter()
    for a, count_a in left.items():
        for b, count_b in right.items():
            if sum(a) + sum(b) <= limit:
                result[tuple(sorted(a + b))] += count_a * count_b
    return result


def quotient(numerator, unit, limit):
    """Invert a polynomial with constant coefficient 1 at finite weighted degree."""
    assert unit[()] == 1
    remainder = Counter({p: v for p, v in numerator.items() if sum(p) <= limit})
    result = Counter()
    for degree in range(limit + 1):
        layer = {p: v for p, v in remainder.items() if sum(p) == degree and v}
        result.update(layer)
        remainder.subtract(multiply(layer, unit, limit))
    assert not any(remainder.values())
    return result


def add_branch(edges, next_vertex, center, size, branch_edges, root):
    edges.append((center, next_vertex + root))
    edges.extend((next_vertex + a, next_vertex + b) for a, b in branch_edges)
    return next_vertex + size


def check_extraction(branch_edges, root):
    # The largest branch has four vertices. n=12 attains n=3M exactly.
    edges = []
    next_vertex = add_branch(edges, 1, 0, 4, branch_edges, root)
    for size in [3, 2, 1, 1]:
        path = [(i, i + 1) for i in range(size - 1)]
        next_vertex = add_branch(edges, next_vertex, 0, size, path, 0)
    n = next_vertex
    ordinary = cuts(n, edges)
    largest = max(p[0] for p in ordinary if len(p) == 2)
    assert n == 3 * largest and ordinary[(largest, n - largest)] == 1
    observed = Counter({p[:-1]: v for p, v in ordinary.items() if p[-1] > largest})
    quotient_factor = Counter({p[:-1]: v for p, v in observed.items()
                               if p.count(largest) == 1})
    independent = Counter({p: v for p, v in observed.items() if largest not in p})
    recovered = quotient(independent, quotient_factor, largest - 1)
    assert recovered == cuts(largest, branch_edges, root=root)
    return recovered


def switched_pair(size, arm, leaf, nonleaf):
    # Vertex 0 and vertex 1 are the endpoints of the central edge.
    for roots in [(leaf, leaf, nonleaf, nonleaf), (leaf, nonleaf, leaf, nonleaf)]:
        edges = [(0, 1)]
        next_vertex = 2
        for center, root in zip((0, 0, 1, 1), roots):
            next_vertex = add_branch(edges, next_vertex, center, size, arm, root)
        yield next_vertex, edges


def check_switch(size, arm, leaf, nonleaf, all_cuts):
    (n, first), (_, second) = switched_pair(size, arm, leaf, nonleaf)
    half = n // 2
    cut_count = None if all_cuts else 3
    a = cuts(n, first, cut_count=cut_count)
    b = cuts(n, second, cut_count=cut_count)
    if all_cuts:
        assert sum(a.values()) == sum(b.values()) == 2 ** (n - 1)
        assert {p: v for p, v in a.items() if p[-1] > half} == {
            p: v for p, v in b.items() if p[-1] > half
        }
    witness = (1, 1, half - 1, half - 1)
    assert b[witness] - a[witness] == 1
    print(f"n={n}, partition {witness}: {a[witness]} versus {b[witness]}")


def check_switch_with_equal_leaf_counts():
    """The roots next to an endpoint and at the center of the five-vertex path."""
    size = 5
    arm = [(i, i + 1) for i in range(size - 1)]
    polynomials = []
    values = []
    for roots in [(1, 1), (1, 2), (2, 2)]:
        edges = []
        n = add_branch(edges, 1, 0, size, arm, roots[0])
        n = add_branch(edges, n, 0, size, arm, roots[1])
        polynomial = cuts(n, edges)
        polynomials.append(polynomial)
        moments = [sum(t ** j for t in range(1, size + 2)) for j in range(n + 1)]
        values.append(sum(count * prod(moments[j] for j in partition)
                          for partition, count in polynomial.items()))

    segregated = multiply(polynomials[0], polynomials[2], 2 * n)
    mixed = multiply(polynomials[1], polynomials[1], 2 * n)
    assert segregated[(1, 1, 10, 10)] == mixed[(1, 1, 10, 10)]
    assert segregated[(2, 2, 7, 11)] - mixed[(2, 2, 7, 11)] == 1
    determinant = values[0] * values[2] - values[1] ** 2
    assert determinant == 8_876_663_201_636_208_811_155_456
    print(f"n=22: leaf witness tied, (2, 2, 7, 11) differs by 1; determinant {determinant}.")


if __name__ == "__main__":
    path4 = [(0, 1), (1, 2), (2, 3)]
    star4 = [(0, 1), (0, 2), (0, 3)]
    rooted_polynomials = [
        check_extraction(path4, 0), check_extraction(path4, 1),
        check_extraction(star4, 0), check_extraction(star4, 1),
    ]
    assert len({tuple(sorted(p.items())) for p in rooted_polynomials}) == 4
    print("Recovered all four rooted four-vertex tree types at n=3M.")
    check_switch(3, [(0, 1), (1, 2)], 0, 1, all_cuts=True)
    check_switch(4, star4, 1, 0, all_cuts=False)
    check_switch_with_equal_leaf_counts()
