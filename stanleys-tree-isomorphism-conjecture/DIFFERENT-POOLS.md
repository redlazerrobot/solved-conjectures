# The whole large-component slice can conceal different branch inventories

Let U_T be the unsigned edge-cut polynomial of a balanced tree of order 2h. Retain all coefficients at partitions with a part strictly greater than h. This entire slice can agree between trees whose **pooled rooted branches differ**, even though their separated polynomials also differ. Earlier examples redistributed a common inventory; they could not establish failure of inventory recovery. The construction below allows unbounded branch order and tree diameter.

## Two ways to prune one tree

Choose any finite tree D with two leaves in different automorphism orbits. Delete the first leaf and root at its old neighbor to form R; use the second for S. Write m=|D|−1. The rooted trees R and S are distinct, since a rooted isomorphism would extend across the deleted leaf to an automorphism of D exchanging the two sites. Given a rooted tree B, form E(B) by attaching a fresh leaf at its root and declaring the fresh leaf the new root. E(R) and E(S) have the same underlying unrooted tree D, with inequivalent roots.

Take adjacent vertices u,v. At u attach the branches E(R) and a singleton. At v attach S and two singletons. Construct the second tree by exchanging R and S in this description. Both halves have order h=m+3. The unique branch of order m+1 in the first pool is E(R); in the second it is E(S). For example, one can use a three-arm tree D with lengths 1,1,k for any k≥2, and delete a short-arm leaf or the long-arm tip.

## Equality of every observable large-component coefficient

In the notation of [BRANCH-MULTIPLICITIES.md](BRANCH-MULTIPLICITIES.md), F_B=A_B+U_B is the branch factor: A_B omits the root component and U_B includes all components. The cuts inside E(R), after omitting its new root component, give F_R exactly, according as the edge from the new root is retained or cut. Thus

    F_E(R) = F_R+U_D,       F_E(S) = F_S+U_D.

The inventory products for cuts retaining uv, with the common endpoint component omitted, have difference

    (1+x_1)^3 [(F_R+U_D)F_S − (F_S+U_D)F_R]
      = (1+x_1)^3 U_D (F_S−F_R).

Assign weight j to x_j. The constants of F_S and F_R are both 1. Their weight-one coefficients also agree: cutting off a singleton away from the root amounts to choosing one of the leaves of D other than the deleted one. If deletion creates a new leaf, it is the root and is excluded. The term U_B contributes only in weight m. Hence the displayed difference vanishes through weight m+2, since U_D is homogeneous of weight m+1. That precision is exactly h−1. Erasing the unique part larger than h in U is precisely the inventory-product truncation through that weight. This proves equality of the entire large-component slice.

## Why the separated contributions differ

Once uv is deleted, the two unrooted halves are R and S each joined by one edge to a three-vertex path. For the half at u that path is rooted at an end; for the half at v the path is rooted at its center. Let the two rooted contexts be J and K. In the second tree the attachments of R and S to these contexts are reversed.

Write H for the connected-set size/boundary polynomial and write r_B for its restriction to the root of a rooted B. By the [joining-edge identity](EDGE-CONTEXTS.md), the signed sum of the four unrooted half polynomials H is

    H_(J—R)+H_(K—S)−H_(J—S)−H_(K—R) = (r_J−r_K)(r_R−r_S).

Both factors are nonzero by rooted completeness. If the two separated ordinary cut products agreed, their unordered pairs of ordinary half polynomials would agree by unique factorization (each is monic linear in the half-order variable). Their sums of H polynomials would then agree as well. This contradiction proves that the separated contributions differ. The full chromatic symmetric functions differ too: the two whole trees exchange distinct limbs at a leaf and at a degree-three vertex of a common six-vertex base, so [the two-site theorem](TWO-SITE-EXCHANGE.md) applies.

## Check and remaining information

For arm lengths 1,1,2, [verify_pool_collision.py](verify_pool_collision.py) enumerates all 8,192 edge subsets on each 14-vertex tree. Exactly 753 cuts per tree have a part larger than seven, with identical counts in all 27 such bins. The separated count at (5,4,3,2) is 4 versus 3; the full counts there are 5 versus 4. In all, 66 separated bins differ. Together with the [caterpillar obstruction](CONNECTED-INVENTORY.md), this rules out using either the whole high-component slice alone or the complete connected-set census alone to recover the separated polynomial for every balanced tree. The two obstructions use different pairs. Whether the **combination** of those statistics suffices is a distinct open step in this approach.

The construction and its scope are recorded as an independent derivation. It supplies no counterexample to Stanley’s conjecture. The underlying cut and rooted-completeness sources are linked in the two preceding notes.
