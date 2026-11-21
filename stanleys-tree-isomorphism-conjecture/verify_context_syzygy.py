"""Check the first fixed-context collision via actual cut subsets."""
from collections import Counter, defaultdict
from verify_complementary_fringe import edges, halves


def cut_table(n, graph, free_edges, root=None):
    """Classify components by traversal; edges outside free_edges stay intact."""
    table = defaultdict(Counter)
    for mask in range(1 << len(free_edges)):
        removed = {e for k, e in enumerate(free_edges) if mask >> k & 1}
        adjacency = [[] for _ in range(n)]
        for k, (u, v) in enumerate(graph):
            if k not in removed:
                adjacency[u].append(v)
                adjacency[v].append(u)
        seen = set()
        sizes = []
        root_size = None
        for v in range(n):
            if v in seen:
                continue
            group = {v}
            queue = [v]
            while queue:
                u = queue.pop()
                for w in adjacency[u]:
                    if w not in group:
                        group.add(w)
                        queue.append(w)
            seen.update(group)
            if root in group:
                root_size = len(group)
            else:
                sizes.append(len(group))
        table[root_size][tuple(sorted(sizes))] += 1
    return table


def j_row(s, context, r):
    # Represent the weight-r vertex by a path of r vertices permanently joined.
    graph = edges(context, 0) + [(0, s)]
    graph += [(s+i-1, s+i) for i in range(1, r)]
    return cut_table(s+r, graph, range(s))[None]


def branch(s, context, endpoint):
    return [(0, 1), (1, 2), (endpoint, 3)] + edges(context, 3)


def verify(s, context):
    n = s+3
    # Delete the context attached at the leaf 0 or at the middle 1 of P3.
    b, c = branch(s, context, 1), branch(s, context, 0)
    bt = cut_table(n, b, range(n-1), root=0)
    ct = cut_table(n, c, range(n-1), root=1)
    for r in range(1,n+1):
        signed = bt[r].copy()
        signed.subtract(ct[r])
        expected = Counter()
        if r == 1:
            expected.update(j_row(s, context, 2))
        if r == 2:
            expected.subtract(j_row(s, context, 1))
        assert signed == expected
    # Rejoin the removed context through each specified root; evaluate ordinary U.
    def rejoin(graph, root):
        joined = graph + [(root, n)] + edges(context, n)
        return cut_table(n+s, joined, range(n+s-1))[None]
    assert rejoin(b, 0) == rejoin(c, 1)


if __name__ == '__main__':
    for s in range(1,6):
        for context in halves(s):
            verify(s, context)
        print("context order", s, "rooted types checked", len(halves(s)))
