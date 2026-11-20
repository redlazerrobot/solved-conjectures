# Recovering complementary fringe counts on the two sides

**November 20, 2026.** Write T for a tree on 2h vertices with balanced edge e. U counts all edge cuts by component sizes, and S counts the cuts deleting e. Both halves have h vertices. No branch multiset or side labels are supplied. The [linear obstruction](LINEAR-EXTRACTION.md) motivates looking for products of counts.

## Cross-side counts visible in U

For a noncentral edge, call the component cut off away from e its fringe. For 1 ≤ i < j and i+j=h, let L_s and R_s count the order-s fringes in the respective halves. Their sum N_s is the ordinary two-component coefficient at (s,2h−s). Let C be the ordinary three-component coefficient at (i,j,h). Then

    M = C − N_i − N_j = L_i R_j + R_i L_j.

To prove this, first count cuts producing (i,j,h) and deleting e. An edge whose fringe has size i or j can be the unique additional cut, giving N_i+N_j possibilities. Among the cuts retaining e, nested fringes leave the central component larger than h, since the outer fringe has size less than h. For disjoint fringes the central component must have size h, because both detached components have size less than h. The fringes of sizes i and j must lie in different halves: disjoint fringes in one half omit its root and cover at most h−1 vertices. Conversely every such cross-side pair works. There is no ordering factor since i and j are distinct. In particular the product of side imbalances (L_i−R_i)(L_j−R_j) is observable as N_i N_j−2M.

## An identifiable four-component coefficient

Let D be the coefficient of (i,i,j,j) in S. Neither half can be uncut; each must contribute exactly two parts, one of each size. Therefore D=(L_i+L_j)(R_i+R_j).

* **If N_j=1**, name the side with the unique j-fringe left. Then R_i=M and L_i=N_i−M, so **D=M(N_i−M+1)**. This is a nonlinear formula using three ordinary coefficients. For i=1 and h>2 it recovers the unordered pair of leaf counts of the halves as M and N_i−M+1: the unique (h−1)-fringe marks the unique half whose root is itself a leaf.
* **If N_j=2 and 3i≥h**, each side has one j-fringe. Indeed distinct j-fringes have equal sizes and hence are disjoint, and two cannot fit in one half. Every i-fringe must lie inside the j-fringe on its own side; a disjoint one would cover the half with it while omitting the root. Two distinct i-fringes inside that j-fringe omit its root, so together cover at most j−1 vertices. Since 2i≥j, each side contains at most one. Thus **D=1+N_i+binom(N_i,2)**.
* If i=j=h/2, take the coefficient C at (i,i,h). An edge of fringe order i is counted once, and each cross-side pair is counted once. This gives C−N_i=L_i R_i, also the separated coefficient at (i,i,i,i).

The [direct verifier](verify_complementary_fringe.py) generated rooted halves as unordered multisets of smaller rooted trees, joined all unordered pairs for h=3 through 6, and enumerated every subset of one, two or three deleted edges. It checked the cross-side identity on 523 (tree,i) choices with i<j, including 240 choices with N_j=1, and checked 220 equal-index cases. With h=5, i=1, the input triples (N_i,N_j,C)=(7,1,12) and (5,1,9) gave D=16 and 9 respectively. The same verifier exhibits D=8 and D=9 for the single triple (6,0,6), and likewise for (4,2,10). Those examples rule out recovery from the three inputs alone without a further hypothesis. Other coefficients of U are available.

## A boundary for using only the partition shape

Fix any partition of 2h. Across **all** balanced trees, a cut of that shape always deletes e exactly when all its parts have the same size k dividing h. For sufficiency, if a size-k component crossed e, each side would consist of whole size-k pieces and a strictly positive proper portion of the crossing piece. This contradicts divisibility of h by k.

For necessity, realize any ordering of the parts as consecutive blocks on the path of order 2h. The central edge is deleted exactly when a proper prefix sums to h. If no subset sums to h, all these cuts retain e. Otherwise arrange a subset summing to h first. If the parts are not all equal, the two groups admit unequal elements on opposite sides (otherwise every element would be equal). Put these at the ends adjacent to the boundary and interchange them. Only the boundary prefix sum changes and it now differs from h. This constructs a cut retaining e. In the all-equal case with k not dividing h, no subset sums to h. This classification concerns deciding from a single partition shape; the formula for D instead uses relationships between coefficients.

These deductions use the cut interpretation in [Stanley's paper](https://sites.math.washington.edu/~billey/classes/Hopf.algebra/bulletins/stanley.1995.pdf). Related shape reconstruction with additional shape counts appears in [Loebl and Sereni](https://kam.mff.cuni.cz/~loebl/clanky/LoSe18rev2.pdf). The identities were independently derived in this project; priority has not been established. An unresolved step is separating correlations for noncomplementary sizes, for which two disjoint fringes may occupy the same half. The examples above do not answer whether the complete U determines S.
