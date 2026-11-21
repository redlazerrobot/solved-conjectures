# What a known tree attached by an edge can reveal

Let B be an unknown n-vertex rooted tree. Let S be a specified s-vertex rooted tree, s≥1. Join their roots by a new edge and observe the **ordinary** unsigned cut polynomial of the unmarked result. One such observation determines B as a rooted tree for all inputs exactly when n≤s+2. Two observations obtained using two nonisomorphic rooted contexts determine B for every n, including contexts of the same order. These are inverse results with extra information. Knowing U for a single arbitrary tree does not supply a second decorated observation.

## One context and its first ambiguity

For each r≥1 let b_r record cuts of B in which the root component has order r, with the monomial recording all *other* components. The variables u_i have weight i, so b_r is homogeneous of weight n−r. Write a_j for the analogous polynomials of S. Given the root component of B, the joining edge is cut or retained, giving

    U_(S—B) = Σ_r b_r J_r(S),      J_r(S) = u_r U_S + Σ_j a_j u_(r+j).

J_r is homogeneous of weight s+r and is u_(s+r) plus a polynomial in strictly lower-index variables, because a_s=1. In Q[u_1,…,u_(s+n)], replacing each u_(s+r) by J_r in increasing r is a triangular graded change of variables. In the new coordinates two distinct summands in the displayed map can involve the same monomial only if that monomial contains both corresponding J variables. Its weight is then at least (s+1)+(s+2), while the output weight is s+n. For n≤s+2 there is no overlap. The individual b_r are uniquely determined and constitute the complete rooted U-polynomial. [Aliste-Prieto, de Mier and Zamora](https://arxiv.org/abs/2002.08186).

At n=s+3 the only possible overlap is J_1 J_2 itself. The formal kernel in that weight is one-dimensional, spanned by (J_2,−J_1,0,…). Actual tree inputs realize an ambiguity at every n≥s+3: choose a tree on n−s≥3 vertices, fix a leaf and a vertex of degree at least two, and attach one copy of S by an edge at each site. Remove either copy and root what remains at the site it formerly occupied. The two remaining n-vertex rooted trees have different root degrees, yet reattaching S gives the identical unrooted tree. This obstacle persists if the observer is given the entire unmarked joined graph.

The [cut-subset check](verify_context_threshold.py) tests 194 context/input pairs in the injective range, using explicit truncated division or comparing the last residual with its unique possible multiplier. The [first-kernel check](verify_context_syzygy.py) verifies the precise signed relation for all 17 rooted contexts through order five by using the three-vertex path for the base construction.

## Two distinct contexts at arbitrary order

In the connected-set convention of [the exchange theorem](TWO-SITE-EXCHANGE.md), write R_B for its root-containing polynomial and H_B for its unrooted polynomial. Directly separating sets contained in a single side from sets crossing the new edge gives

    H_(B—S) = H_B + H_S + (y−1)(R_B+R_S) + R_B R_S.

Sets lying in one side and containing its root acquire an extra boundary edge. A crossing set is exactly a pair of rooted sets, one on each side. Subtract the two identities for contexts S and T. After removing H_S−H_T, the answer is (R_S−R_T)(R_B+y−1). The known divisor is nonzero by rooted completeness, so this determines R_B and hence B. If H_B itself is supplied, a single known nonempty context also suffices, since R_S+y−1 is nonzero. The calculation is a consequence of the classical joining and rooted-reconstruction principles. See [Chaudhary and Gordon, Propositions 15–17](https://webbox.lafayette.edu/~gordong/pubs/TPFT.pdf) and [Burghart's rooted polynomial](https://arxiv.org/abs/2302.08394). The [percolation check](verify_percolation_bridge.py) also verifies the corresponding numerical inversion on five inputs using the two different rootings of a three-vertex path.

The missing observation has a precise averaging issue. For an unrooted tree B, summing U of its single-leaf extensions over all attachment vertices gives

    n u_1 U_B + Σ_j j u_(j+1) ∂U_B/∂u_j.

The first term cuts the new edge. For the second, a component of order j offers j places to attach a leaf while replacing its variable by u_(j+1). Ordinary U_B supplies the sum directly, while the two-observation inverse requires an individual rooted-site observation.

## Conditional inversion from the separated contribution

Suppose an unmarked T has a balanced edge with prime half order h, and suppose its full separated contribution S_e is also supplied or has already been extracted. This assumption can replace knowing the branch pool. Factor S_e=U_B U_C: the half-polynomials are normalized irreducibles, monic linear in u_h. Hence H_B+H_C is known. By the bridge identity the product (R_B+y−1)(R_C+y−1) is known.

For a rooted h-tree D, R_D+y−1 vanishes at x=1−y by the recursion Q_D=y+x∏Q_child, with Q_D=y+R_D. Divide by x+y−1. The quotient is monic in x, and at y=0 it is (x^h−1)/(x−1), irreducible over Q for prime h. A nontrivial factorization would retain both x-degrees upon this specialization since the polynomial is monic; a y-only factor must be a unit. Thus the quotient is irreducible in Q[x,y]. Factoring the known product after removing (x+y−1)^2 determines both monic quotients and hence the two rooted halves. For an end-rooted path of composite order h the quotient equals (x^h−1)/(x−1) already before specialization, so this irreducibility argument cannot be used indiscriminately.

For the unrestricted problem the separated contribution itself is usually unknown. No decorated input, successful symbolic factorization on a promised input, or result here supplies it for every tree.
