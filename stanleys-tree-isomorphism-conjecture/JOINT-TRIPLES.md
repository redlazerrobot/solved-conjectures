# Recovering two-edge cuts from the connected-set census and the large-component slice

Let an unrooted tree on $2h$ vertices have a balanced edge $e$, with $h\ge2$. Root the halves of $T-e$ at their incident vertices. Every other edge cuts off a rooted subtree away from $e$, called its fringe. Let $N_i$ count the order-$i$ fringes, and let $M$ be the largest occupied order. Write $H(k,b)$ for the number of connected vertex sets of order $k$ with exactly $b$ boundary edges. Write $U_\lambda$ for the number of edge subsets whose deletion produces the component orders $\lambda$.

**Theorem.** Suppose $3M\le 2h+1$. From $H(k,1),H(k,2)$ and just those three-part coefficients $U_\lambda$ with a part greater than $h$, one can reconstruct every three-part coefficient. The same data determine the number of cross-side pairs of fringes of each size pair $i,j$ with $i+j\ge h$. In a range identified from the input, they also recover individual four-part counts for cuts through the balanced edge.

All preliminary quantities are observable. A connected set with one boundary edge is one side of an edge deletion. At order $h$, two such sets indicate a balanced edge, which is necessarily unique. For $1\le i<h$ the value $H(i,1)$ is exactly $N_i$. Thus the bound can be tested on an unmarked tree.

## From connected sets to a product of the two fringe histograms

Over all two-edge cuts, count each occurrence of a part of size $k$, including repeated parts. The total is

$$
H$k,2$+$2h-k-1$H$k,1$.
$$

Indeed, both boundary edges of a set counted by $H(k,2)$ must be deleted. For a set counted by $H(k,1)$, the complement is a tree on $2h-k$ vertices and any one of its edges can supply the second deletion. These are all ways a particular connected set can be a component.

Subtract from these totals all part occurrences in the known triples with maximum greater than $h$. Also subtract, for each $i<h$, the $N_i$ occurrences of the whole triple $(i,h-i,h)$ produced by cutting $e$ and one fringe edge. Call the remaining multiplicities $J_k$. The residual triples arise precisely from cutting a fringe on each side with $i+j\ge h$. In fact, two cuts on the same side of an intact $e$ leave a component of order at least $h+1$. On different sides the component orders are $i,j,2h-i-j$. Thus the total number of residual cuts is $B=\sum_k J_k/3$.

Let $L(z)=\sum_i L_i z^i$ and $R(z)=\sum_i R_i z^i$ count the fringes on the two sides, with $L+R=N$ known. For $h\le s\le2M$, let $b_s=[z^s]LR$. Whenever $k=2h-s>M$, $J_k=b_s$, since this part cannot be a fringe. Furthermore $\sum_s b_s=B$ over this range. If $2M<h$ it is empty, and there are no residual triples.

When $3M<2h$, every $b_s$ in the range is read directly. At $3M=2h$, just $b_{2M}$ may be missing and its value follows by subtraction from $B$. At $3M=2h+1$, the only missing values are $b_{2M-1}$ and $b_{2M}$. Now $b_{2M}=L_M R_M$ equals 1 if $N_M=2$ and 0 otherwise. Two distinct fringes of equal order must be disjoint, and two size-$M$ fringes cannot fit in one half while omitting its root, since $2M\ge h$. Subtract the known values from $B$ to obtain $b_{2M-1}$.

## From the product to individual coefficients

Set $D=L-R$. The coefficients of $D^2=N^2-4LR$ at degrees at least $h$ are now known. If they all vanish, $D_iD_j=0$ whenever $i+j\ge h$. Otherwise their highest nonzero degree is $2d$, where $d=\deg D$. Choose the positive square root for $D_d$, exchanging the names of the two halves if needed. Descend from $j=d-1$ to $h-d$. At degree $d+j$ in $D^2$, the only terms not yet known are the two copies of $D_dD_j$. This recovers all $D_j$ down through $h-d$. For any $i+j\ge h$, either an index exceeds $d$, making $D_iD_j=0$, or both are in the recovered interval.

For $i<j$, the number of such cross-side pairs is $(N_iN_j-D_iD_j)/2$. For $i=j$ it is $(N_i^2-D_i^2)/4$. Restore the triple $(i,j,2h-i-j)$ for every pair. Adding back the two previously subtracted categories proves the three-part statement, including all coincidences of part sizes.

**Four-component consequence.** If the observed square tail is nonzero, $L_i=(N_i+D_i)/2$ and $R_i=(N_i-D_i)/2$ are known up to a common exchange for every $i\ge h-d$. Consider any four-part partition with every part in $[h-d,h-1]$. A cut through $e$ of this type must split each half into two. For a complementary pair $(a,h-a)$, the number of single cuts in the left half producing it is $L_a+L_{h-a}$ when $2a\ne h$, and $L_a$ when $2a=h$. Use the corresponding counts for the right half and multiply the half two-part polynomials restricted to this interval. The coefficient is the required separated count, with its multiplicities retained. This directly recovers some of the four-part information whose unrestricted separation is open.

## Two additional layers of the pooled connected-set product

The following identity needs no bound on $M$. Let $V_k(y)$ count the order-$k$ connected sets containing **both** endpoints of $e$, by their full-tree boundary size. Write $H_k(y)=\sum_b H(k,b)y^b$. Every connected set of order greater than $h$ contains both endpoints. At the next two orders one still has exact extraction:

$$
V_h=H_h-2y,\qquad
V_{h-1}=H_{h-1}-N_{h-1}y-N_1y^2 .
$$

A connected set avoiding at least one endpoint lies entirely in one half. At order $h$ it is the whole half. At order $h-1$ it omits one leaf from that half. Omitting a leaf other than its root gives a set with boundary two, once for each ordinary whole-tree leaf. Omitting a leaf that is the root gives boundary one, once for each size-$(h-1)$ fringe. This includes $h=2$. In the notation of [the connected-inventory note](https://github.com/redlazerrobot/solved-conjectures/blob/30246ee3e0454e1addcc74789f60fe4135d213ab/stanleys-tree-isomorphism-conjecture/CONNECTED-INVENTORY.md), $V$ is the product of the rooted connected-set polynomials of the halves. Hence the reversed pooled product is observable through degree $h+1$, two beyond the earlier cutoff $h-1$. The same denominator proof recovers the pool if $h+1\ge D(M)$, and the support-sensitive version applies if $h+1\ge D_{\mathrm{obs}}-1$.

## Verification and scope

[The checker](verify_joint_triples.py) generates all unordered pairs of rooted halves of equal order. It computes $H$ by enumerating vertex subsets and independently computes cut coefficients using edge deletions and connected components. The reconstruction receives only the two prescribed observations. Each selected four-part slice is checked against cuts deleting the balanced edge and two additional edges. The program also compares the two additional connected-set layers directly on every tree, including trees outside the numerical bound. Run `python3 verify_joint_triples.py` for $2\le h\le7$.

The theorem supplies a sufficient condition for recovering the ordinary two-edge cut data and the stated separated slice. It leaves open reconstruction of arbitrary cuts through the balanced edge from the two joint observations. Related two-cut placement tests using a larger input are in [the fringe-lifting note](https://github.com/redlazerrobot/solved-conjectures/blob/30246ee3e0454e1addcc74789f60fe4135d213ab/stanleys-tree-isomorphism-conjecture/FRINGE-LIFT.md). Publication priority for this derivation is unverified.
