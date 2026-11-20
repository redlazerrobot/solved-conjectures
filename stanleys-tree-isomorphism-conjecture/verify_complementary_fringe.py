"""Direct deletion of at most three edges on balanced joins of rooted trees."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, combinations_with_replacement


@lru_cache(None)
def halves(order):
    if order == 1:
        return ((),)
    options = [(s, t) for s in range(1, order) for t in halves(s)]
    def build(start, left):
        if not left:
            yield ()
        for j in range(start, len(options)):
            size, tree = options[j]
            if size > left:
                break
            for rest in build(j, left - size):
                yield (tree,) + rest
    return tuple(build(0, order - 1))


def edges(tree, root):
    result = []
    def visit(node, v):
        for child in node:
            w = root + len(result) + 1
            result.append((v, w))
            visit(child, w)
    visit(tree, root)
    return result


def partition(n, graph, removed):
    parent = list(range(n))
    def find(v):
        while v != parent[v]:
            v = parent[v]
        return v
    for k, (u, v) in enumerate(graph):
        if k not in removed:
            parent[find(u)] = find(v)
    return tuple(sorted(Counter(find(v) for v in range(n)).values()))


def main():
    for h in range(3, 7):
        checked = Counter()
        examples = {}
        equal_part_checks = 0
        for left, right in combinations_with_replacement(halves(h), 2):
            graph = [(0, h)] + edges(left, 0) + edges(right, h)
            counts = Counter()
            deleted = Counter()
            side = [Counter(), Counter()]
            for length in (1, 2, 3):
                for subset in combinations(range(len(graph)), length):
                    p = partition(2*h, graph, subset)
                    counts[p] += 1
                    if 0 in subset:
                        deleted[p] += 1
                    elif length == 1:
                        side[int(subset[0] >= h)][p[0]] += 1

            for i in range(1, (h+1)//2):
                j = h-i
                ni = counts[i, 2*h-i]
                nj = counts[j, 2*h-j]
                c = counts[i, j, h]
                m = c-ni-nj
                assert m == side[0][i]*side[1][j] + side[1][i]*side[0][j]
                observed = deleted[i, i, j, j]
                if nj == 1:
                    assert observed == m*(ni-m+1)
                if nj == 2 and 3*i >= h:
                    assert observed == 1 + ni + ni*(ni-1)//2
                checked[nj] += 1
                examples.setdefault((i, ni, nj, c), set()).add(observed)
            if h % 2 == 0:
                i = h//2
                ni = counts[i, 2*h-i]
                m = counts[i, i, h] - ni
                assert m == side[0][i]*side[1][i]
                assert m == counts[i, i, i, i] == deleted[i, i, i, i]
                equal_part_checks += 1
        print(f"h={h}: checks by N_j={dict(sorted(checked.items()))}; "
              f"equal-part checks={equal_part_checks}")
        if h == 5:
            for key, expected in [((1, 7, 1, 12), {16}), ((1, 5, 1, 9), {9}),
                                  ((1, 6, 0, 6), {8, 9}), ((1, 4, 2, 10), {8, 9})]:
                assert examples[key] == expected
                print(f"  (i,N_i,N_j,C)={key}: separated counts {sorted(expected)}")


if __name__ == "__main__":
    main()
