"""Independent divisor-pair audit of Batista's A398581 congruence."""
from math import gcd


def triples(k):
    # 1/x < 5/k < 3/x. Reduce the residual a/b = 1/y + 1/z.
    for x in range(k // 5 + 1, (3*k - 1) // 5 + 1):
        a, b = 5*x-k, k*x
        g = gcd(a, b)
        a, b = a//g, b//g
        # (ay-b)(az-b) = b^2. Strict y<z puts the smaller divisor below b.
        for d in range(1, b):
            e, rem = divmod(b*b, d)
            if rem or (d+b) % a or (e+b) % a:
                continue
            y, z = (d+b)//a, (e+b)//a
            if x < y < z:
                assert 5*x*y*z == k*(x*y + x*z + y*z)
                yield x, y, z


def main():
    eligible = solutions = 0
    outside = []
    for k in range(1, 151):
        rows = list(triples(k))
        solutions += len(rows)
        if not rows:
            assert k in (1, 2)
            continue
        first = min(rows)
        max_z = max(row[2] for row in rows)
        best = [row for row in rows if row[2] == max_z]
        if k % 5 != 1:
            eligible += 1
            assert best == [first]
        elif first[2] != max_z:
            outside.append(k)
            if k == 11:
                print("k=11:", first, best)
    print("ordered triples:", solutions, "eligible denominators:", eligible)
    print("lex-first falls short outside the hypothesis:", outside)


if __name__ == "__main__":
    main()
