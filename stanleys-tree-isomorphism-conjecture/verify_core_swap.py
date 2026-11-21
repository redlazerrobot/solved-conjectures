"""Whole-forest check of swaps at arbitrary vertices in a fixed base tree."""
from collections import Counter
from fractions import Fraction
from verify_packet_switch import cut_polynomial, difference, grow, packet


def verify(core, u, v, b, c):
    def graft(first, second):
        graph = list(core)
        grow(graph, u, first)
        grow(graph, v, second)
        return cut_polynomial(graph)

    def rooted_at(vertex):
        # Relabel by the transposition (0, vertex) to reuse the root-0 counter.
        def label(w):
            return vertex if w == 0 else 0 if w == vertex else w
        return cut_polynomial([(label(i), label(j)) for i,j in core], rooted=True)

    lhs = difference(graft(b,c), graft(c,b))
    bc = difference(packet(b), packet(c))
    uv = difference(rooted_at(u), rooted_at(v))
    rhs = Counter()
    for (i,a), w in bc.items():
        for (j,d), y in uv.items():
            rhs[i+j,a+d-1] += w*y
    assert lhs == rhs
    p, z = Fraction(2,5), Fraction(3,2)
    return sum(v != 0 for v in lhs.values()), sum(
        w*p**i*z**j for (i,j), w in lhs.items())


if __name__ == '__main__':
    leaf = ()
    edge = (leaf,)
    b, c = (leaf,edge), (edge,)
    tree = [(0,1),(1,2),(2,3),(3,4),(1,5)]
    print("same-degree leaves in different orbits:", verify(tree,0,4,b,c))
    print("leaves in one orbit:", verify(tree,0,5,b,c))
    print("move all branches to a distant vertex:", verify(tree,0,4,b,()))
