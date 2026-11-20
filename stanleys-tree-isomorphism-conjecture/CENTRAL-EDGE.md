# What the cuts through a central edge recover

**November 20, 2026.** The large-component extraction in [the first note](CENTROID.md) loses information at a balanced edge. Here is an explicit family exhibiting the loss, together with a coefficient of the full polynomial which always separates the pair. These trees give a counterexample to the proposed shortcut only. The calculation makes no claim of publication priority.

## Redistributing the branches of an edge

Fix two adjacent vertices u and v. Each carries some attached rooted branches. Make a second tree by redistributing the same multiset of branches between u and v, leaving u and v adjacent. In the unsigned cut polynomial, the contribution of cuts keeping uv is identical in both trees: use the same internal and attaching-edge cuts on each branch. The component containing u and v retains the same order, and all other components have identical orders. This is a bijection preserving the entire cut partition.

Let H₁ and H₂ be the two ordinary trees left after deleting uv in the first tree, and let J₁ and J₂ be the corresponding trees in the second. Cutting uv allows independent internal cuts on both sides. Consequently

    U(first) − U(second) = U(H₁) U(H₂) − U(J₁) U(J₂).

In particular, equality for the two trees is equivalent to equality of the unordered pair of half-polynomials. Indeed, every tree on h vertices has U=x_h+f(x_1,…,x_(h−1)), a monic linear polynomial in x_h, which is irreducible in the whole multivariate polynomial ring over the rationals. To see this directly, quotient by x_h+f; the quotient is again a polynomial ring and therefore an integral domain. Unique factorization and the leading coefficient 1 remove the scalar ambiguity. The single-vertex case gives x_1. This criterion concerns polynomials of the halves, so it does not assume Stanley’s conjecture.

If the redistribution preserves a balanced split into two halves of order h, a cut removing uv has every part at most h. It follows that every cut partition having a part strictly larger than h occurs equally often in the two trees. Thus the entire slice of the invariant used in the first note can agree.

## An infinite family and an exact witness

Choose any finite tree S of order s≥3 and with L leaves. Form rooted branch P by rooting S at a leaf and branch Q by rooting an identical copy of S at a nonleaf. Use two copies of P and two of Q. In T, attach both P branches at u and both Q branches at v. In T′, attach one P and one Q at each endpoint. Both trees have order 2h, where h=2s+1. The edge uv separates two h-vertex trees, hence the preceding large-part agreement holds.

A half consists of a central vertex of degree two and its two branches. Attaching a P consumes one leaf of S, whereas attaching a Q preserves all L leaves. The leaf counts of the halves are therefore 2L−2 and 2L for T, and 2L−1 and 2L−1 for T′.

Consider the partition (h−1,h−1,1,1). For a cut which deletes uv and produces this partition, each h-vertex half must contribute (h−1,1). Since h≥7, the only possible split is one large part and one singleton per half. Each choice cuts one leaf edge in its half, and every choice works. The cuts retaining uv cancel by the earlier bijection. Thus the difference, counting T first, is

    (2L−2)(2L) − (2L−1)² = −1.

T′ has exactly one more cut with these component orders. This proves the trees are nonisomorphic and distinguishes their full chromatic symmetric functions for every S. It also localizes what was lost by discarding the all-small-part partitions. For S the three-vertex path, the partition is (6,6,1,1).

## The next question

If both halves have the same number of leaves, the displayed coefficient can agree. For a reassignment with known pooled branches, the general product identity still supplies the exact test. For arbitrary input U, the pooled branches and the term arising from cuts retaining the central edge are themselves unknown. Can the contribution of cuts deleting that edge be isolated directly from U without being given the pooled branches?

Related work includes [Orellana and Scott](https://doi.org/10.1016/j.disc.2013.12.006), [Smith, Smith and Tian](https://arxiv.org/abs/1505.01889), and [Aliste-Prieto, de Mier and Zamora](https://arxiv.org/abs/2002.08186). The latter two study indistinguishability under other cut restrictions and related switching constructions.
