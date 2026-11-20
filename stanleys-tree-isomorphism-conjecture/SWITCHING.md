# Distinguishing segregated and mixed branches

**November 20, 2026.** This note answers a question left by the leaf-count witness. The argument treats every pair of distinct rooted branches of equal order, including pairs for which leaf counts agree. It uses the published completeness theorem for rooted U-polynomials. Publication priority for the switching statement has not been established.

## Statement

Let P and Q be nonisomorphic as rooted trees, each of order s. At the ends of a single edge construct T by attaching P,P to one end and Q,Q to the other. Construct T′ by attaching P,Q to each end. Then their ordinary chromatic symmetric functions differ.

Both trees have the same counts for every cut partition containing a component larger than half the tree. The distinction must therefore occur in the remaining partitions. The earlier leaf-count argument identifies such a partition when the branches arise by rooting a common tree at a leaf and at a nonleaf. Here the witness can depend on the branches.

## Proof

Write H(P,Q) for the tree consisting of a central vertex with attached branches P and Q, and put h=2s+1. The central-edge bijection in [the preceding note](CENTRAL-EDGE.md) gives the polynomial difference

    U(T) − U(T′) = U(H(P,P)) U(H(Q,Q)) − U(H(P,Q))².

It suffices to find one evaluation making this determinant positive. For a polynomial in the component variables, give x_j weight j. Let D_h replace each monomial of weight d by its product with x_(h−d), extending linearly. In this use d≤2s, so h−d≥1. With the branch factors from [the centroid note](CENTROID.md),

    U(H(P,Q)) = D_h(F_P F_Q).

Indeed the monomial before applying D_h counts components away from the central vertex. The missing component has exactly h−d vertices.

Choose s+1 distinct positive numbers t_i and positive weights a_i. Make the substitution x_j=Σ_i a_i t_i^j for every needed index. For a branch B write f_B(y)=F_B(x_1 y, x_2 y², …, x_s y^s) after fixing these x_j. Both f_P and f_Q are polynomials of degree at most s with constant term 1. For any monomial of weight d, the missing variable contributes Σ_i a_i t_i^(h−d). Applying this term by term gives

    U(H(P,Q)) = Σ_i a_i t_i^h f_P(1/t_i) f_Q(1/t_i).

This is a positive-weight inner product of two evaluation vectors. The displayed determinant is their Gram determinant. It is strictly positive whenever those vectors are linearly independent.

It remains to show that some positive weights ensure independence. If F_P=F_Q, the terms of weight below s would give A_P=A_Q. Restoring the root variable gives equal rooted U-polynomials, contradicting the [rooted reconstruction theorem](https://arxiv.org/abs/2002.08186). Fix the last weight and vary the first s weights in the positive orthant. The map to (x_1,…,x_s) has an invertible linear part (t_i^j) for 1≤i,j≤s, a Vandermonde matrix times a nonsingular diagonal matrix. Its image contains an open set. A nonzero real polynomial cannot vanish on that open set. Hence the weights can be chosen with F_P(x)≠F_Q(x), so f_P(1)≠f_Q(1).

If the two evaluation vectors were proportional, f_P and a constant multiple of f_Q would agree at the s+1 distinct points 1/t_i. They would be identical polynomials of degree at most s. Their constant terms force the multiple to be 1, contradicting f_P(1)≠f_Q(1). Each vector is nonzero by the same interpolation argument. Strict Cauchy–Schwarz proves the claim. ∎

## Example missed by the leaf coefficient

Use the five-vertex path. Root P next to an endpoint and Q at the middle. Both roots are nonleaves. On the resulting 22-vertex trees the earlier leaf witness (10,10,1,1) has difference zero. The coefficient for (11,7,2,2) is one larger in T. With t_i=1,…,6 and all six weights equal to 1, the determinant in the proof evaluates to 8,876,663,201,636,208,811,155,456. Both checks follow by enumerating only the cuts on the 11-vertex halves and applying the exact central-edge identity.

## Scope and remaining gap

The theorem excludes the P,P | Q,Q versus P,Q | P,Q pattern as a source of a counterexample. For four arbitrary branches A,B,C,D, the switch produces a mixed difference of inner products; strict Cauchy–Schwarz does not supply its sign. Another unresolved step is recovering the central-edge contribution from one unmarked input polynomial when the attached branches are unknown.

For related gluing formalisms, see [Tom and Vailaya](https://arxiv.org/abs/2503.19344) and [the rooted coloring invariant](https://arxiv.org/abs/2206.05392). This proof is a partial result about the ordinary invariant. It does not establish the unrestricted conjecture.
