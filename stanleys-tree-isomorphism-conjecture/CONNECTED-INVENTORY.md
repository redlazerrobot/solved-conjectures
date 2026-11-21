# Recovering the balanced-edge inventory from connected sets

Use H_T(x,y) to count nonempty connected vertex sets by order and number of boundary edges, and R_D(x,y) to count the sets containing the root of a rooted tree D. These are the conventions of [the two-site exchange note](TWO-SITE-EXCHANGE.md). H is obtainable from the ordinary chromatic symmetric function. Its unrooted information is equivalent to the classical bivariate subtree polynomial by [Aliste-Prieto, Martin, Wagner and Zamora, Theorem 8](https://arxiv.org/html/2402.10333v2).

Let T have order 2h and a balanced edge uv. Deleting u and v leaves rooted branches D attached to either endpoint. Write M for their maximum order, c_D for their pooled multiplicities, and r_m for the number of possible rooted tree types of order m. For h>1, H detects both the balanced edge and M. Indeed each connected set with exactly one boundary edge is an entire side of an edge deletion. Thus [x^h y]H is two in the balanced case and zero otherwise. The maximum smaller side strictly below h that occurs is M.

**Reconstruction theorem.** A known pool of rooted branches and H suffice to recover both rooted halves and their separated cut polynomial, at any order. Even when the pool is unknown, H reconstructs the entire tree among all trees if

    h−1 ≥ D(M),    D(M) = Σ_{m=1}^M m r_m.

The order-two tree is immediate. Arbitrary multiplicities of every branch type are allowed.

## Recovering the two sides once the pool is known

Put Q_D=y+R_D. Let L and R be the rooted connected-set polynomials of the two halves at u and v, computed with the central edge removed. Let W count connected sets meeting neither endpoint. Then

    W = Σ_D c_D (H_D + (y−1)R_D),
    LR = x² ∏_D Q_D^{c_D},
    H_T = W + y(L+R) + LR.

For the first identity, a set meeting neither endpoint lies in one branch. Its boundary gains the attaching edge exactly when it contains the branch root. For the second, a set containing an endpoint chooses independently on each incident branch, either omitting the branch or choosing a set containing its root. For the last, a set meeting just one endpoint gains a boundary edge at uv. A set meeting both restricts to a rooted set in each half, and their orders and boundaries add.

The first two quantities are computable from the pool without its allocation. Dividing H_T−W−LR by y gives L+R. The two roots of the resulting monic quadratic over Q(x,y) are precisely L and R, including the repeated-root case. By rooted completeness, each recovers its rooted half. Their ordinary cut polynomials multiply to give the full contribution of cuts through uv. In particular, the earlier condition h−1≥B(M) in [BRANCH-MULTIPLICITIES.md](BRANCH-MULTIPLICITIES.md) already suffices for reconstruction from the full chromatic symmetric function: its separate, stronger half-precision condition can be dropped.

## Recovering an unknown pool

Every connected set of order greater than h meets both endpoints. Hence the top h coefficients in x of H_T come from LR alone. Over the field K=Q(y), introduce t=1/x and the reversed factors

    f_D(t) = t^m Q_D(1/t,y),     m=|D|.

Each f_D has degree m and constant coefficient one. The polynomials Q_D are monic, irreducible and pairwise different by the rooted theorem of [Burghart](https://arxiv.org/html/2302.08394v3). Passing to K and reversing preserves irreducibility (Q_D has nonzero constant coefficient), and the f_D are pairwise nonassociate because of their normalization. The top slice therefore supplies

    P(t) = ∏_D f_D(t)^{c_D}  modulo t^h,

by reversing H_T at degree 2h. Enumerate all rooted types through the observable M and let F be the product of their f_D, each once, including absent types. The polynomial

    F P'/P = Σ_D c_D f'_D (F/f_D)

has degree at most D(M)−1. The truncation determines it through degree h−2, enough under the stated bound. Reduction modulo f_E kills all terms except c_E f'_E(F/f_E). That multiplier is invertible in K[t]/(f_E), since distinct factors are coprime and K has characteristic zero. This reads every c_E. Combining the recovered inventory with the quadratic proves the theorem. A competitor with the same H must have the same order, balanced edge and M, so the search never assumes an unobservable bound on a competitor.

A sharper observable bound uses the linear term in y. In a branch, the reversed factor enumerates sets of pairwise incomparable rooted subtrees: take the maximal omitted subtrees of a root-containing set, or the whole branch for the term y corresponding to omission of its root. Their total order is the exponent of t and their number is the exponent of y. Thus N_i=[t^i y]P counts all order-i subtrees cut off by a single outward edge, including whole branches. These numbers are observed through M<h. If two candidate inventories agree on the slice, the number of distinct possibly mismatched order-i factors is at most min(r_i,2N_i). Put D_obs=Σ_i i min(r_i,2N_i). Form the difference of their logarithmic derivatives and clear just its distinct mismatched factors. The numerator has degree at most D_obs−2: the usual degree D_obs−1 term cancels because both products have the same total degree 2h−2, so both logarithmic derivatives have leading term (2h−2)/t at infinity. A nonzero numerator cannot vanish through t^(h−2) when h−1≥D_obs−1. Therefore that condition also suffices, even without explicitly finding the mismatched factors. The two bounds are sufficient; neither is asserted necessary.

There is also an instance-specific test at any precision: enumerate nonnegative candidate multiplicities of total weight 2h−2, compare the truncated products, then test each candidate against the quadratic and the actual rooted tree dictionary. No claim of efficient enumeration is required. The [companion Python check](verify_connected_inventory.py) uses finite inventory matching and an exact bivariate square root. Starting only from the unmarked census of the order-20 example, it tested 106 inventories, recovered (2,2,3,1), and identified the unordered endpoint allocations (1,1,1,1) and (1,1,2,0). Types in order are singleton, edge, end-rooted three-vertex path, center-rooted three-vertex path. The input had 11,768 connected sets in 105 bins. The separated polynomial reconstructed from those data agreed in all 367 bins with independently deleting the central edge and each possible subset of the other edges (262,144 cuts in total).

## An exact obstruction outside the criterion

Consider two caterpillars with consecutive spine-site weights

    (2,2,1,2,1,3,3)    and    (3,1,2,1,2,3,2).

A site of weight w carries w−1 leaves. Both fourth prefix sums are seven, so the edge after the fourth spine vertex is balanced. The signatures arise from the composition-factor reversal of Aliste-Prieto, Martin, Wagner and Zamora, Theorem 14, using outer composition (1,1,2), inner factor (1,2) or its reversal, and near-concatenation with a singleton at both ends. The [direct certificate](verify_balanced_hdp_switch.py) also establishes equality of H without invoking that construction: on each tree it examines all 16,383 nonempty vertex subsets and finds the same 419 connected sets by count, distributed identically over 62 bins. Enumeration of all 8,192 edge cuts per tree gives separated counts **1 and 0** at partition (3,3,4,4). The full ordinary cut polynomials already differ at (1,3,10), with counts 7 and 8.

This obstruction occurs at all orders 14k, k≥1. Append k−1 fresh leaves to each original vertex. A connected set meeting the old tree chooses any subset of the pendant leaves at its included vertices. Each such leaf is included or is a boundary edge. The remaining connected sets are single fresh leaves. Hence

    H_new(x,y) = H_old(x(x+y)^(k−1),y) + 14(k−1)xy.

The equality of H persists. For k≥2 a cut counted at (3k,3k,4k,4k) retains every new pendant edge, since otherwise it creates a singleton. The separated discrepancy at the scaled balanced edge is still one. Thus even the complete connected-set census cannot recover the separated polynomial for arbitrary unknown pools. The additional joint component-size information in the ordinary cut polynomial is essential to any unrestricted recovery.

This is a conditional reconstruction theorem and an obstruction for a weaker invariant. The caterpillar switching construction and rooted completeness are prior work; publication priority for the extraction criterion is undetermined.
