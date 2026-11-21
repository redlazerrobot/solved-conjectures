# A reconstruction bound in terms of the branch types actually present

Use the notation of [the branch multiplicity theorem](BRANCH-MULTIPLICITIES.md). For each occupied order m let s_m be the number of distinct rooted order-m branch types in the actual pool at the balanced edge; copies of a type are counted once. Define

    H = max over occupied orders m of (4m−2) s_m.

**Theorem.** If h−1≥H, the ordinary chromatic symmetric function reconstructs the whole tree among all trees. A rival need not satisfy any bound on the number of distinct types present. The proof supplies a certificate: one can enumerate feasible pools, check their truncated products, and use the bound for a matching candidate. This formulation avoids assuming prior knowledge of the true inventory.

## A moment test for absent branch types

Let K=h−1. Descend in m after removing larger factors. An order with no branches is identified from the coefficient of x_m, since K≥M. For an occupied order write s=s_m and z_D=1/g_D in the weight-completed ring of lower variables over the rationals. Each g_D is a unit with constant term 1. For j≥1, the coefficient of x_m^j in the formal logarithm of the residual product equals

    (−1)^(j−1) / j times p_j,     p_j = Σ_D c_D z_D^j.

This follows from log(g_D+x_m)=log(g_D)+log(1+x_m/g_D), interpreted at constant term 1. Smaller factors do not contribute. We know p_j through weight K−jm. Also p_0=Σ c_D is the constant term of p_1.

Suppose a rival product agrees to weight K. Take the polynomial q(Y)=∏(Y−z_B) over the s distinct types B of the actual support. Its coefficients are formal series in the lower variables with nonnegative weights. Expanding q² as a polynomial in Y requires moments only through j=2s. Hence

    Σ_D c'_D q(z_D)²

for the rival vanishes through weight K−2sm: it agrees to that precision with the actual sum, which is identically zero. Constructing q from a candidate support is sufficient to test it.

If D is outside that support, each z_D−z_B has some nonzero term of weight at most m−1. Indeed the difference of the underlying g's has this property by the rooted reconstruction theorem, and multiplying by units preserves the least nonzero weight. The least weight of a product is the sum of the least weights because the polynomial ring of initial forms is an integral domain. Thus q(z_D)² has first nonzero weight at most 2s(m−1). In a sum with positive multiplicities, terms attaining the least weight cannot cancel: their homogeneous initial forms are real squares with positive coefficients, and at least one of the polynomials being squared is nonzero at some real point. If K≥s(4m−2), the precision already reaches that weight. No outside type can occur. Applying the multiplicity lemma on the s allowed types recovers their individual counts, including any putative zeros. This proves equality of the full inventories. For m=1 there is only one possible type and the argument about outside types is vacuous.

## Why the same bound suffices for the two roots

The full pool yields S and the two ordinary half polynomials by the preceding theorem. Its largest occupied order satisfies M≤K/2 since 4M−2≥2M. Also m s_m≤K/2 at every occupied order. The half truncation reaches K−M≥K/2. The ordinary multiplicity lemma with the now known dictionary therefore recovers both rooted halves. No second sparsity hypothesis on either half is needed.

For instance, choose any two rooted trees B,C of the same order m. Attach a copies of B at one endpoint and a copies of C at the other, with a≥8. Here h−1=am and s_m≤2, so the theorem reconstructs the resulting unrooted tree against every rival. Both m and the internal shapes are unrestricted. More generally the copies may be distributed in any way that preserves the balanced halves. The proof does not assume that either endpoint is homogeneous.

The square in the moment test is essential to this argument: with arbitrary signed candidate multiplicities equal-weight leading terms can cancel. A failure of the precision condition does not imply equality of full invariants. Reconstruction beyond these sufficient conditions remains unresolved. The proof is an independent derivation; the completeness result used for rooted factors is due to [Aliste-Prieto, de Mier and Zamora](https://arxiv.org/abs/2002.08186). We make no claim of publication priority.
