# How far linear extraction can go at a balanced edge

Let T have 2h vertices and an edge e with h vertices on each side. Write U for its unsigned cut polynomial and S for the sum restricted to cuts deleting e. Equivalently S is the product of the ordinary cut polynomials of the two halves. The coefficient of x_h² in U detects e. Such an edge is unique: every other edge cuts off a proper subset of one half on its side away from e. All the statements below use the ordinary invariant, without a list of branches.

## All coefficients through three components

Write N_t for the coefficient of x_t x_(2h−t) in U, for 1 ≤ t < h. Direct each half away from the endpoint of e. A noncentral edge isolates t vertices away from e if and only if its smaller side in the whole tree has order t. Thus N_t counts these edges across the two halves.

The two-component part of S is x_h². To get three components, cut e and exactly one other edge. Consequently the only possible partitions are (h,i,h−i), and their coefficients in S are the sum of N_t over the **distinct** elements of {i,h−i}. This also handles i=h/2. The one-component part is zero.

## A four-component count outside the linear span

For every positive integer k, on balanced trees of order 10k there is no rational linear functional of the **entire** U that returns the coefficient of (5k,2k,2k,k) in S. Even an order-specific affine functional fails. This limits extraction by universal coefficient weights. It leaves nonlinear reconstruction open.

Here is an exact certificate. A letter denotes a rooted tree on vertices 0 through 4. The four entries are the parents of vertices 1 through 4, respectively. In XY join the two roots by e.

| Half | Parents |
| --- | --- |
| A | 0,0,0,0 |
| B | 0,0,2,3 |
| C | 0,1,0,3 |
| D | 0,0,0,3 |
| E | 0,1,1,1 |
| F | 0,0,2,2 |
| G | 0,1,1,3 |

Take −AB + AC − DE + FB − FG + EE as a formal integer combination. The signed sum of the six ordinary U polynomials vanishes identically. The coefficient of (5,2,2,1) in their six S polynomials, in that order, is 3, 3, 2, 5, 4, 0. Its signed sum is −1. The coefficients of the formal combination sum to zero, so adding a constant to a linear functional cannot repair it.

The finite identity can be verified by the following exhaustive proof algorithm: for each of the six parent lists, start with ten singleton blocks. For each subset of the nine edges, merge the endpoint blocks for exactly the retained edges. Add the sign of the tree to the bin indexed by the sorted block sizes. All bins finish at zero. For S retain only subsets deleting the join. [Executable certificate](verify_balanced_linear.py). An independent [proper-coloring check](verify_stable_relation.py) assigns each vertex either to a compatible existing independent color class or to a new class in order of first occurrence. Each stable set partition appears once. For a size pattern its multiplicity in the monomial symmetric basis is this count times the product of the factorials of equal-part multiplicities. All 38 occurring size patterns cancel for the joined trees. Both checks were run with standard Python 3. The search which located the relation used rational linear dependencies among balanced joins; only the six displayed trees are needed to verify it.

## Transfer to arbitrary scale

At every old vertex attach k−1 fresh leaves. The old balanced edge remains balanced. Given the cut on the old edges, each old component of order s carries (k−1)s fresh pendant edges. Deleting exactly j of them produces j singleton parts and one part ks−j. Thus ordinary U and restricted S both transform by the same multiplicative substitution

    x_s ↦ Σ_{j=0}^{(k−1)s} binom((k−1)s,j) x_1^j x_(ks−j).

For k≥2, a monomial using only indices divisible by k must come from j=0 in every factor. Hence the coefficient at the scaled partition in the transformed S is exactly the original coefficient. Linearity of substitution preserves the zero relation for U. This proves the assertion for all k; k=1 is the certificate itself.

The uniform leaf construction is also used by [Orellana and Tomba, November 13, 2026](https://arxiv.org/abs/2611.18940), who reduce Stanley's full question to k-weighted proper trees. Our use propagates a failure of linear balanced-edge extraction. [Loebl and Sereni](https://kam.mff.cuni.cz/~loebl/clanky/LoSe18rev2.pdf) use smaller shape information in Procedure 1 to count shaped partitions. [Stanley's power-sum expansion](https://sites.math.washington.edu/~billey/classes/Hopf.algebra/bulletins/stanley.1995.pdf) identifies U and the ordinary chromatic symmetric function by a fixed change of coefficient signs for trees. The obstruction and low-component formulas were independently derived here. Publication priority is undetermined. A signed identity among six trees gives no pair of trees with equal invariant.
