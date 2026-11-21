# Recovering the two half-tree edge-size histograms

Let a tree of order 2h have a balanced edge. Root its two h-vertex sides at the incident vertices. Each internal edge cuts off a subtree away from its root, called its fringe here. Write R_s and L_s for the counts of size-s fringes on the two sides. Write N_s for their sum. For s<h, N_s is the coefficient of (s,2h−s) in the ordinary unsigned cut polynomial. Also the sum of R_s over s<h is h−1.

**Sufficient criterion.** The following binary linear solves take only the one- and two-edge-cut coefficients as inputs. If each solve has a unique answer, both full histograms are determined up to a simultaneous side exchange. This determines the contribution of cuts through the balanced edge at every four-part partition whose parts are strictly below h.

### Equations for the two side histograms

Take a sorted triple (a,b,c) of total size 2h and c≤h. Form the distinct unordered pairs (x,y) drawn from its multiset, omitting pairs containing h. Use (x,x) only if x occurs at least twice. For tentative side counts r and l=N−r, define

- B(x,y)=l_x r_y+l_y r_x for x<y.
- B(x,x)=l_x r_x.

If c<h, the coefficient of the triple is the sum of B over these pairs. Indeed a cut through the balanced edge leaves an intact half if only one further edge is deleted. Two internal cuts in the same half also leave the other half connected to at least its opposite root, giving a part strictly greater than h. Thus the fringes cut off lie on opposite sides. Each pair of edges is counted once according to its two fringe sizes. The remaining part is the size of the joined central component. Repeated part sizes require the distinct-pair convention.

For c=h subtract from the observed count the sum of N_s over distinct sizes in {a,b}. This is the contribution of deleting the balanced edge and one more edge. Any other contributing pair of cuts lies on opposite sides by the same argument. Its contribution is again the sum of B over the eligible pairs.

Let F denote the polynomial sum in each row and C its observed right-hand side. Include the row sum_s r_s = h−1. Every true right-hand histogram solves this system. A size with N_s=1 may be selected to have r_s=0 by orienting the balanced edge. For 2s≥h, two size-s fringes cannot be in the same half, since they must be disjoint and omit its root. Thus if N_s=2 in this range, pin r_s=1. Sizes with N_s=0 are pinned to zero.

### Integer recovery

Start with pinned entries exact and all unpinned entries zero. At bit step t=1,2,4,…, assume r agrees with the true side counts modulo t. For unpinned coordinates with N_s≥t write r'_s=r_s+t b_s, with b_s a bit. The entries with N_s<t have already been determined, since 0≤R_s≤N_s. For each row solve, over the field with two elements,

    Σ_s ((F(r+t e_s)−F(r))/t) b_s = (C−F(r))/t   (mod 2).

All divisions here are exact. A mixed monomial in F has coefficient −2 from B(x,y), so a mixed correction at two bit positions is a multiple of 2t². A square in B(x,x) needs only the single-coordinate difference because b_s²=b_s. This proves the row equation for every true next bit, including t=1. If the matrix has full column rank, update r to r'; otherwise the sufficient test is inconclusive. The induction ends once t>max N_s. A valid tree guarantees consistency. Dropping the quadratic corrections at the initial bit in a repeated-size row would give an incorrect test.

For each i<h/2 the h-vertex side has R_i+R_(h−i) internal edges splitting it into parts i and h−i. At i=h/2 the count is R_i. The other side has the analogous L counts. Multiply these two two-part polynomials to obtain the claimed four-part contributions. With four components and all parts below h, a cut through the balanced edge necessarily includes exactly one further cut in each half.

### A connected example at unbounded order

Suppose h is a power of two at least four and N_s=1 at every size 2≤s<h. Then N_1=h. Complementary pairs s,h−s of distinct singleton sizes can be compared by the row with c=h. For a high singleton size a=h−t, t<h/2, the repeated triple (a,a,2t) compares the sides of a and 2t. Its coefficient is one for opposite sides and zero otherwise. These sizes differ because a power of two is indivisible by three.

Starting at any singleton size s other than h/2, fold it to t=min(s,h−s) by comparing the complementary sizes when needed, and use its high representative h−t to pass to size 2t. This multiplies the highest power of two dividing s by two. All sizes therefore connect to h/2. At s=h−1 the first move is directly to 2, so comparison with size 1 is unnecessary. This determines all singleton orientations up to exchange, then R_1 follows by the count of edges per side. The multiplicities occur, for instance, when joining the endpoint of a path to the center of a star of the same order. The criterion concerns the measured multiplicities for any tree, with no promise about the structure of its halves.

### Check and limitation

The companion script enumerates cuts of one and two edges by computing the components of each cut forest. It supplies only the resulting unsigned coefficients to the recovery algorithm, then compares any recovered spectrum against the labeled sides. Among all pairs of rooted h-vertex trees it recovered the two histograms for 3/3, 10/10, 38/45, 156/210, 839/1176 and 4472/6670 pairs for h=3 through 8 respectively. A deficient binary system can include solutions that fail a higher integer equation or tree realizability. The criterion certifies successes only. The histograms themselves do not specify all the internal cuts of either half.

### An ambiguity even among realizable trees

At h=6, encode each rooted half by parentheses around its unordered children; () is one vertex. More explicitly, use the half descriptions below.

* First tree: one root has two leaf children and a third child with two leaves. The other root begins a two-edge chain ending at the center of a three-leaf star (the endpoint has those three children).
* Second tree: one root has a leaf child and a child with three leaves. The other root has one child, which has a leaf child and another child with two leaves.

The size-4 and size-5 fringes are unique. They lie on the same side of the first tree and on opposite sides of the second. Nevertheless all one-cut coefficients and all three-component coefficients with maximum part at most six agree. Among all one- and two-cut coefficients the only differences are (1,4,7), with counts 8 and 7, and (2,3,7), with counts 0 and 1. Hence the restricted equations alone cannot always determine even the placement of two large fringes. The omitted coefficients supply information in this very example.

The obstruction transfers to order 12k for every positive k. Attach k−1 leaves to each old vertex. An old fringe of size t becomes a fringe of size kt; new pendant edges give singletons. Conditional on a cut of the old edges, each new pendant deletion increases the number of parts by one. By the substitution proved in [the linear extraction note](LINEAR-EXTRACTION.md), the old degree-one and degree-two signed profiles vanish identically and cannot produce differences in the new degree-three profile. Its only discrepancies are the two original partitions scaled by k, still with largest part 7k exceeding the half order 6k. The side placement of the unique 4k- and 5k-fringes is unchanged.

Run [verify_fringe_lift.py](verify_fringe_lift.py) with its sibling [edge enumeration helper](verify_complementary_fringe.py). In addition to the histogram comparisons above it checks the entire predicted four-part slice by direct deletion in every successful case through h=6 and the two explicit ambiguous trees. The general rank criterion and the ambiguity concern unlabeled coefficients. [Smith, Smith and Tian, Lemma 2.1 and Theorem 2.2](https://arxiv.org/pdf/1505.01889) give placement and reconstruction results using labeled cuts. Priority for the deductions here is undetermined.
