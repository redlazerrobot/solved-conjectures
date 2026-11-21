"""Exact rank from two ordinary cut polynomials for marker paths of orders 1,2."""
from collections import Counter
from sympy import Matrix
from verify_context_threshold import cuts, complete, mult

def partitions(n, least=1):
    if not n:
        yield ()
    for v in range(least, n + 1):
        for tail in partitions(n - v, v):
            yield (v,) + tail

def rank_matrix(n, sizes):
    columns = []
    for r in range(1, n + 1):
        terms=[]
        for s in sizes:
            marker = tuple(range(s-1))
            a, u = cuts(marker, True), cuts(marker, False)
            terms.append(complete(s + r, a) + mult({(r,): 1}, u))
        for p in partitions(n-r):
            column = Counter()
            for s, polynomial in zip(sizes, terms):
                for q, value in polynomial.items():
                    column[s, tuple(sorted(p+q))] = value
            columns.append(column)
    keys=sorted(set().union(*columns))
    return Matrix([[c[key] for c in columns] for key in keys])
if __name__ == "__main__":
    for n in [7, 8, 9, 10]:
        a=rank_matrix(n, (1, 2))
        b=a.to_DM().rank()
        print(n, a.rows, a.cols, b, "kernel", a.cols-b)
        if n<=9:
            assert a.cols-b==(n==9)
