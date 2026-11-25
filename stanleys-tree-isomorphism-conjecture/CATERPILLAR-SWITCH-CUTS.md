# Two edge deletions distinguish every nonisomorphic composition switch

[Aliste-Prieto, Martin, Wagner and Zamora, Theorem 14](https://arxiv.org/html/2402.10333v2#S6) construct nonisomorphic caterpillars with identical connected-set censuses by reversing composition factors. For every nonisomorphic pair related by such a switch, the large-component slice already distinguishes the trees. More precisely, there is a partition into three parts, each at least two, whose largest part strictly exceeds half the tree order and whose unsigned cut coefficients differ. The proof constructs the partition from the factors. The balanced edge may be present or absent.

## Counting a three-component cut

Write each spine-site weight as one plus the number of pendant leaves at that site. The construction pads the composition at both ends by near-concatenating a singleton, so each spine end has weight at least two. Let S be the set of proper prefix sums of the weights, and n their total. Put A_k = 1 if k belongs to S and zero otherwise, and B_k = A_(n−k). These record a spine edge detaching order k from the left or the right. Write ε_k = A_k−B_k.

Choose p,q≥2 with t=p+q<n/2. No pendant edge can contribute to the coefficient C at (p,q,n−t), since cutting that edge would leave a singleton. The largest component occupies either the middle, left or right interval after the two spine cuts. Therefore

    (1 + [p=q]) C = A_p B_q + A_q B_p + A_t(A_p+A_q) + B_t(B_p+B_q).

The factor two when p=q compensates for counting both orders of the identical parts. Write s_k=A_k+B_k. Twice the right side is

    s_p s_q + s_t(s_p+s_q) − ε_p ε_q + ε_t(ε_p+ε_q).

## Where factor reversals change orientations

Index composition factors from the inside out, with orders b_1,…,b_m≥2. Unit composition factors can be discarded. Put B(0)=1, B(l)=b_1⋯b_l and N=B(m), so n=N+2. For factor l, let I_l be the proper prefix-sum set of its parts and define

    f_l(i) = 1_{i∈I_l} − 1_{b_l−i∈I_l},    1 ≤ i < b_l.

For 0<d<N let l be the first level for which B(l) does not divide d. The padded spine has a cut at position 1+d exactly when i=(d/B(l−1)) modulo b_l belongs to I_l. To see this, composing an outer factor with an inner composition of order b repeats its internal cut positions in every block of length b. A boundary jb between two copies persists precisely when j is an outer prefix position. This recursion gives the rule, and left padding shifts every prefix position by one. On replacing 1+d by n−(1+d), the integer d becomes N−d, giving digit b_l−i at the same level. Thus ε_(1+d)=f_l(i).

A reversal at level l exchanges A_k and B_k there and fixes the other levels. In particular every s_k is unchanged. Call a level active if f_l is nonzero, equivalently if its factor differs from its reversal. If no active level is switched, the padded words coincide. If all active levels are switched, the padded words reverse, giving isomorphic caterpillars. Otherwise choose the first active level s and a higher active level j whose change of orientation differs from that at s. Choose u<b_j/2 with f_j(u)≠0, possible by antisymmetry, and set t=1+B(j−1)u. Then 2t<n.

**If s=1**, choose 1≤i≤b_1−2 with f_1(i)≠f_1(i+1). A nonzero antisymmetric sequence cannot be constant. Use q=1+i and p=t−q. Since B(j−1)≥b_1, both p and q are at least two. Both belong to level 1, with ε_q=f_1(i) and ε_p=−f_1(i+1). The product ε_p ε_q is unchanged, while the term ε_t(ε_p+ε_q) changes sign. Consequently

    C_before − C_after = f_j(u) (f_1(i)−f_1(i+1)) / (1+[p=q]) ≠ 0.

**If s>1**, the innermost level is symmetric. Choose any v with f_s(v)≠0. Put q=1+B(s−1)v and p=t−q. Then p≥B(s−1)≥2, since B(j−1)≥B(s). Also p is a multiple of b_1, so p−1 has nonzero residue b_1−1 and the symmetric innermost level gives ε_p=0. The product ε_t ε_q changes sign, giving

    C_before − C_after = f_j(u) f_s(v) / (1+[p=q]) ≠ 0.

This covers every nonisomorphic pair obtained from factor reversals. ∎

## Example, checks and scope

For the 14-vertex example with spine weights (2,2,1,2,1,3,3) and (3,1,2,1,2,3,2), the coefficient at **(2,2,10) is one and zero**, respectively. In the first tree the cuts detach a two-vertex prefix and the next two vertices. The test also illustrates the repeated-part factor.

[verify_switch_witness.py](verify_switch_witness.py) constructs each composition from near-concatenations, builds the ordinary tree and counts every pair of edge deletions using subtree sizes and ancestry. It verifies the predicted signed coefficient differences for 648 nontrivial oriented switches across all 900 ordered pairs of composition factors of orders 2 through 5, plus 26 oriented switches on multifactor fixtures.

This rules out the whole Theorem 14 switching construction as a source of a collision for the combined census and large-component slice. The paper also gives a broader construction for polarized trees in Theorem 17 and examples outside that construction. The argument here uses the caterpillar spine. General balanced-edge reconstruction and any novelty claim remain open.
