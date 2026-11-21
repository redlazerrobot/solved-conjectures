"""Recover a sparse branch inventory from an unmarked tree's ordinary cut slice."""
from collections import Counter
from itertools import combinations
from verify_complementary_fringe import halves, edges, partition

M = 6
H = 49
K = H - 1
# x_i = WEIGHTS[i] t^i for i<M; x_M = y. Keep y-degree at most four.
WEIGHTS = [0, 2, 3, 5, 7, 11]


def ordinary_slice(graph, root):
    """Root merely orders the DP. A component is classified only upon closing."""
    neighbours = [[] for _ in range(2*H)]
    for u, v in graph:
        neighbours[u].append(v)
        neighbours[v].append(u)

    def close(size, large, degree, marks):
        if size > H and not large:
            return (True, degree, marks), 1
        if size == M and marks < 4:
            return (large, degree, marks+1), 1
        if size < M:
            return (large, degree+size, marks), WEIGHTS[size]
        return None

    def visit(v, parent):
        # State: order of open component, closed large component, t and y degrees.
        states = {(1, False, 0, 0): 1}
        for child in neighbours[v]:
            if child == parent:
                continue
            child_states = visit(child, v)
            new = Counter()
            for (a, big, d, j), count in states.items():
                for (b, big2, f, ell), count2 in child_states.items():
                    if big and big2:
                        continue
                    t, y = d+f, j+ell
                    if y > 4 or t+M*y > K:
                        continue
                    has_large = big or big2
                    weight = count * count2
                    new[a+b, has_large, t, y] += weight
                    closed = close(b, has_large, t, y)
                    if closed:
                        (flag, u, w), scale = closed
                        if u+M*w <= K:
                            new[a, flag, u, w] += weight*scale
            states = new
        return states

    result = Counter()
    for (a, big, t, y), count in visit(root, -1).items():
        closed = close(a, big, t, y)
        if closed:
            (flag, u, w), scale = closed
            if flag and u+M*w <= K:
                result[u, w] += count*scale
    assert result[0, 0] == 1
    return result


def multiply(a, b, limit):
    result = [0]*(limit+1)
    for i, u in enumerate(a[:limit+1]):
        if u:
            for j, v in enumerate(b[:limit+1-i]):
                result[i+j] += u*v
    return result


def inverse(a, limit):
    assert a[0] == 1
    z = [1]
    for n in range(1, limit+1):
        z.append(-sum(a[i]*z[n-i] for i in range(1, min(n+1, len(a)))))
    return z


def moments(data, limit):
    # Power-series identity P * (d log P / dy) = dP/dy.
    rows = [[data[t, j] for t in range(limit+1)] for j in range(5)]
    inverse_zero = inverse(rows[0], limit)
    derivatives = []
    for j in range(4):
        out = [(j+1)*x for x in rows[j+1]]
        for i in range(1, j+1):
            term = multiply(rows[i], derivatives[j-i], limit)
            out = [a-b for a, b in zip(out, term)]
        derivatives.append(multiply(out, inverse_zero, limit))
    return [[rows[1][0]]+[0]*limit] + [
        [(-1)**j * v for v in row] for j, row in enumerate(derivatives)]


def branch_inverse(branch, limit):
    # Build g_B by cutting the standalone branch and its attaching edge.
    parents = [0] + [p+1 for p, v in edges(branch, 0)]
    g = [0]*(M+1)
    for mask in range(1 << M):
        sizes = [1]*(M+1)
        parts = []
        for i in range(M, 0, -1):
            if mask & (1 << (i-1)):
                parts.append(sizes[i])
            else:
                sizes[parents[i-1]] += sizes[i]
        if M not in parts:
            weight = 1
            for s in parts:
                weight *= WEIGHTS[s]
            g[sum(parts)] += weight
    return inverse(g, limit)


def annihilates(z, w, p, limit):
    # Evaluate the moment functional on (Y-z)^2 (Y-w)^2.
    coefficients = [[1]+[0]*limit]
    for root in [z, z, w, w]:
        updated = [[0]*(limit+1) for _ in range(len(coefficients)+1)]
        for j, coeff in enumerate(coefficients):
            constant = multiply(coeff, root, limit)
            for t in range(limit+1):
                updated[j][t] -= constant[t]
                updated[j+1][t] += coeff[t]
        coefficients = updated
    terms = [multiply(q, moment, limit) for q, moment in zip(coefficients, p)]
    return not any(map(sum, zip(*terms)))


def main():
    types = halves(M)
    # Two nonisomorphic rootings/shapes at arbitrary positions in the generator.
    left, right = 3, 16
    graph = [(0, 1)]
    next_vertex = 2
    for endpoint, branch_id in [(0, left), (1, right)]:
        for _ in range(8):
            graph.append((endpoint, next_vertex))
            graph.extend(edges(types[branch_id], next_vertex))
            next_vertex += M
    assert next_vertex == 2*H
    one_cut = [partition(next_vertex, graph, (i,))[0] for i in range(len(graph))]
    assert one_cut.count(H) == 1 and max(s for s in one_cut if s != H) == M
    # Both traversals start away from the central endpoints.
    data = ordinary_slice(graph, 5)
    assert data == ordinary_slice(graph, 2*H-1)
    limit = K - 4*M
    p = moments(data, limit)
    z = [branch_inverse(branch, limit) for branch in types]
    # The chosen numeric specialization must still distinguish candidate types.
    assert len({tuple(v[:M]) for v in z}) == len(z)
    answers = [(i,j) for i,j in combinations(range(len(z)), 2)
               if annihilates(z[i], z[j], p, limit)]
    assert answers == [(left, right)]
    i, j = answers[0]
    t = next(t for t in range(limit+1) if z[i][t] != z[j][t])
    total = p[0][0]
    count, rem = divmod(p[1][t]-total*z[j][t], z[i][t]-z[j][t])
    assert rem == 0 and (count, total-count) == (8, 8)
    print("vertices", next_vertex, "rooted types", len(types), "candidate pairs",
          len(types)*(len(types)-1)//2, "surviving pair", answers[0])
    print("branch counts", (count, total-count), "moment precision", limit)


if __name__ == "__main__":
    main()
