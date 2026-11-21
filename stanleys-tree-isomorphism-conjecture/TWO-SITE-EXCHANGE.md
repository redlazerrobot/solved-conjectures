# A two-site exchange on any tree

Let X be any finite tree with distinct vertices u and v, and let B and C be any two rooted trees. Identify the root of B with u and the root of C with v. Form a second tree by exchanging the two attachments. A rooted attachment can consist of any multiset of branches around its root; a one-vertex attachment adds nothing.

**Theorem.** The two resulting trees have different ordinary chromatic symmetric functions unless B and C are rooted-isomorphic, or an automorphism of X takes u to v. In either exceptional case the resulting trees are isomorphic. The half-generalized degree polynomial already distinguishes every nonisomorphic exchange of this kind. There is no size, distance, balance, degree or branch-multiplicity hypothesis.

In particular, every nontrivial redistribution of a fixed multiset of rooted branches across an edge is distinguished. To apply the theorem, leave the stationary branches at their endpoints in X. Collect all branches moved in one direction into B and all those moved in the other direction into C. This includes the four-arbitrary-branches question left in [SWITCHING.md](SWITCHING.md).

## Counting the difference

Use the connected-set polynomial H_X(x,y) that counts nonempty connected vertex sets W by x to the power |W| and y to the number of edges with one end in W. This is x times the half-generalized degree polynomial with its variables ordered appropriately, since a connected set in a tree spans |W|−1 edges. Write R_(X,u) for the restriction to sets containing u. R_B and R_C use the specified roots. Let T and T' be the trees before and after exchange, respectively. Then

    x (H_T − H_T') = (R_B − R_C)(R_(X,u) − R_(X,v)).

A connected set disjoint from X lies entirely in one of the two attachments away from its root. Its contribution cancels. Any other connected set meets X in a nonempty connected set W. For each attachment site in W, multiply W's monomial by the corresponding rooted polynomial divided by x: the two vertex sets share exactly their root and their edge boundaries add. If a site is absent, no vertex of that attachment can be included. Terms from W containing both sites or neither agree. The difference on the two remaining classes gives the displayed factorization, since the sets containing both sites cancel in the difference of the rooted polynomials.

These data are observable from ordinary cuts. Retain each edge independently with probability p and let Z_T(p,z) be the expected sum of z to the order of each component. For a specific connected W the probability of appearing as a component is p^(|W|−1)(1−p)^boundary(W). Therefore pZ_T(p,z)=H_T(pz,1−p), an invertible rational substitution. Equivalently, a cut partition with l parts has probability weight p^(|T|−l)(1−p)^(l−1), multiplied by its ordinary unsigned cut coefficient. This includes singleton and full-tree terms.

## Why a zero factor gives exactly the two exceptions

For a rooted tree P let Q_P=y+R_P. At the root, each child branch E is either excluded (one boundary edge, factor y) or included in a rooted connected set. This gives the recursion

    Q_P = y + x ∏_E Q_E.

Q_P is monic of degree |P| in x, reduces to x^|P| modulo y, and has constant term y as a polynomial in x. Eisenstein's criterion at y makes it irreducible in Q[y,x]. Unique factorization of (Q_P−y)/x recovers all child types recursively. This is the established rooted polynomial and completeness argument of [Fabian Burghart, Definition 2, Theorem 9 and Proposition 12](https://arxiv.org/html/2302.08394v3). Earlier rooted completeness results include [Chaudhary and Gordon, 1991](https://webbox.lafayette.edu/~gordong/pubs/TPFT.pdf).

Thus equality of the unrooted statistics implies B and C are rooted-isomorphic, or (X,u) and (X,v) are rooted-isomorphic. For the latter case one needs an automorphism actually **interchanging** u and v. Root X at its invariant center, subdividing its central edge if necessary. An automorphism taking u to v preserves depth and fixes their common ancestor where the two root paths diverge. It identifies the two child subtrees there, carrying the first marked vertex to the second. Exchange those subtrees by that identification and its inverse, and fix everything else. This involution interchanges u and v and gives the required isomorphism after grafting.

A corollary concerns possible counterexamples to Stanley's conjecture. Two nonisomorphic trees with a common unrooted leaf-deleted tree have different chromatic symmetric functions: they arise by moving a single leaf between two sites of the common tree. The leaf case is also obtainable from Chaudhary and Gordon’s Proposition 15. Their Proposition 16 gives a related joining-edge product formula; both are direct historical precedents. The theorem covers moving a whole rooted limb or exchanging two arbitrary collections of limbs in one step.

## Checks, prior results, and scope

[The general-site verifier](verify_core_swap.py) and [the adjacent-site verifier](verify_packet_switch.py) enumerate whole-tree edge subsets and expand the full bivariate percolation polynomials. The checks compare every coefficient. A separate [connected-set enumeration](verify_exchange_connected.py) checked the identity in 421 pairs of sites on rooted representatives of base trees through order six; 318 differences were nonzero. For two same-degree leaves at distance four in a six-vertex base tree, swapping the test attachments gave 21 nonzero difference terms and value 3564/78125 at p=2/5, z=3/2. Swapping at leaves in one automorphism orbit gave zero. The adjacent tests include unequal and empty branch collections, two different rootings of a path, and a zero-difference control.

[Aliste-Prieto, Martin, Wagner and Zamora](https://arxiv.org/html/2402.10333v2) prove that the half-generalized degree polynomial and the edge/leaf subtree polynomial determine one another. Their Theorem 14 constructs collisions by reversing composition factors. [Eisenstat and Gordon](https://doi.org/10.1016/j.disc.2006.01.022) give earlier unrooted subtree-polynomial collisions. Consequently this weaker invariant does have collisions in general. The theorem above precludes obtaining one by a single nonisomorphic two-site exchange on a common base tree. The rooted completeness and earlier leaf recurrence belong to the cited authors. The general exchange identity was independently derived here; its publication priority is undetermined.

For the balanced-edge problem this isolates the remaining ambiguity: once the branch inventory is recovered, a finite search over its allocations using just H has a unique unrooted answer. Reconstructing that inventory from a single arbitrary input is still open.
