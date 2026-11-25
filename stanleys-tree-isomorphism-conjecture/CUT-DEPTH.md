# How much of a tree can its largest cut components conceal?

## Result

Fix a nonnegative integer $k$ and a number $\theta>3/5$. There are two trees of the same order $n$, each with an edge dividing it into equal halves, that agree on all three of the following observations simultaneously.

1. The number of connected vertex sets of each order and boundary size.
2. The number of ways to obtain each component-size partition by deleting at most $k$ edges.
3. The number of ways to obtain each component-size partition having a part at least $\theta n$, with any number of edges deleted.

The two trees have **different counts for cuts through their balanced edges**. Their full chromatic symmetric functions also differ. This leaves the reconstruction question at the half-tree threshold open. Publication priority for the three-observation result has not been established.

For the smallest member below, $n=28$. Every cut coefficient with a part at least 18 agrees. The coefficient at $(1,3,7,17)$ is 5 in one tree and 4 in the other. Thus we can locate precisely how far the agreement extends.

## The two trees

Write $H_T(x,y)$ for the sum of $x^{|W|}y^{|\partial W|}$ over nonempty connected vertex sets $W$, and $R_T$ for the analogous sum restricted to sets containing a specified root. Here $\partial W$ is the set of edges with exactly one endpoint in $W$. The ordinary cut polynomial $U_T$ counts all edge deletions with a factor $z_i$ for each resulting component of order $i$. On trees this carries the same information as the ordinary chromatic symmetric function, and it determines $H_T$. [Aliste-Prieto, Martin, Wagner and Zamora](https://arxiv.org/html/2402.10333v2)

Use the rooted pair from Proposition 11 of Aliste-Prieto, de Mier and Zamora. Start with the three-vertex path rooted at its middle in one copy and at an end in the other. At each step join the roots of the two previous trees by an edge. The next pair consists of this single unrooted tree rooted at the two ends of the joining edge. At level $j$ write the two rooted trees as $B,C$, of common order $s=3\cdot 2^j$. [Original rooted construction, Proposition 11](https://arxiv.org/pdf/2002.08186)

Write $b=R_B$ and $c=R_C$. They differ at every level. At level zero the two counts differ already on root-containing singleton sets. On taking the next pair their difference becomes $b(y+c)-c(y+b)=y(b-c)$.

Identify the roots of $B,C$ to form a rooted tree $D$ of order $2s-1$. Put $L=y+R_D=y+bc/x$. A site is a rooted tree whose root will be a vertex of a five-vertex path. Use the following sites.

| Site | Construction | Rooted connected-set polynomial | Order |
|---|---|---|---:|
| $B,C$ | The two rooted trees above | $b,c$ | $s$ each |
| $P$ | Attach $D$ by one edge to the root of $C$ | $p=Lc$ | $3s-1$ |
| $Q$ | Attach $D$ by one edge to the root of $B$ | $q=Lb$ | $3s-1$ |
| $A$ | Attach $D$ by one edge to a new root | $a=xL$ | $2s$ |

Join the site roots in the order $P,A,B,C,Q$ for $T$, and in the order $P,B,C,A,Q$ for $T'$. Their common order is $n=10s-2$. In $T$ the edge after the second site is balanced. In $T'$ the edge after the third site is balanced. Each half has order $h=5s-1$. Every other edge detaches a proper subset of a half, so the balanced edge is unique.

## Equal connected-set counts, different balanced-edge cuts

A connected set meeting the path roots meets a nonempty interval of them. Its contribution for that interval is the product of the corresponding site polynomials times $y$ for each path edge leaving the interval. The sets avoiding all path roots cancel between the two orders because the site multiset agrees.

Expanding the intervals and subtracting in the order $T-T'$ gives

$$
\frac{H_T-H_{T'}}{y}
=p(a-b)+q(c-a)+ya(b-c)+pb(a-c)+qc(b-a).
$$

Substitute $p=Lc$ and $q=Lb$. The expression is $(c-b)[a(L-y)-Lbc]=0$, by the choice of $D$ and $A$.

Now perform the same interval sum separately on the two halves of each tree. For a two-site path with rooted polynomials $u,v$ the intervals contribute $y(u+v)+uv$. For three sites $u,v,w$ they contribute $y(u+w)+y^2v+y(uv+vw)+uvw$. The difference of the two sums of half-tree censuses is therefore

$$
(c-b)\,[y^2-y+L(a-bc)] = y(c-b)(y-1+a).
$$

This is nonzero. The second factor $y-1+a$ has constant term $y-1$ in $x$.

The polynomial counting cuts through the balanced edge is the product of the ordinary cut polynomials of its two halves. Each order-$h$ half polynomial is monic linear in $z_h$, with leading coefficient one and all other terms in $\mathbb Q[z_1,\ldots,z_{h-1}]$. It is irreducible. If the two products were equal, unique factorization would give the same unordered pair of ordinary half polynomials. These would give equal sums of the two half-tree censuses, contradicting the displayed difference.

## Agreement after any fixed number of edge deletions

A rooted cut state records the size of the component containing the root, all the other sizes, and the number of deleted edges. The level-$j$ trees $B,C$ have equal multiplicities of every rooted cut state through $j$ deletions. Here is an induction. The claim at zero uses their equal order. At the next step, cuts retaining the new joining edge have the same root component viewed from either end. If that edge is deleted, the difference of the two rooted cut enumerators is the previous rooted difference multiplied by the common unrooted cut enumerator and by one additional deletion. This shifts the first possible discrepancy up by at least one. The underlying unrooted tree agrees at each step.

These truncated rooted states may be substituted at any site, including one with several outside edges incident to its root. Once all outside cuts are fixed, only the root component can merge with outside components. Reverse the path for $T$ and interchange the exposed $B,C$ site cores, keeping the copies of $D$ fixed. This gives precisely the path for $T'$. The substitution preserves all ordinary counts through $j$ cuts, so any $j\ge k$ suffices.

## The first differing large component

For a rooted tree $X$, let $G_X$ sum the monomials from cuts with the root component omitted, and let $F_X=G_X+U_X$. Retaining an attaching edge contributes $G_X$ and deleting it contributes $U_X$. Each $G_X$ and $F_X$ has constant term one. Give $z_i$ weight $i$.

Any component larger than $h$ contains both endpoints of the balanced edge. Erasing that component from its partition leaves a monomial of weight $w<h$. The coefficients of all these monomials are therefore given by the product of $F_X$ over the branches at those two endpoints, truncated to weights below $h$. The erased component has size $n-w$ and can be restored uniquely.

Use $C Q$ for the rooted arm formed by joining the sites $C,Q$ at their roots by an edge, rooted on the $C$ side. Define $B P$ likewise. The products at the two balanced edges are respectively

$$
F_D\,G_B\,F_P\,(G_C F_Q + U_{C Q}),\qquad
F_D\,G_C\,F_Q\,(G_B F_P + U_{B P}).
$$

After cancellation their difference is

$$
F_D\left(G_B F_P U_{C Q}-G_C F_Q U_{B P}\right).
$$

Both arm polynomials are homogeneous of weight $4s-1$. Thus all smaller weights cancel and the term of weight $4s-1$ is $U_{C Q}-U_{B P}$. This term is nonzero. The off-path sets in the two arms come from the same attached branches, while the two-site interval formula gives

$$
H_{C Q}-H_{B P}= y(c+q-b-p)+cq-bp=y(1-L)(c-b)\ne 0.
$$

It follows that the **largest component size at which any coefficient differs is exactly $6s-1$**. This exceeds $h$ and satisfies

$$
\frac{6s-1}{10s-2}=\frac35+\frac{1}{5(10s-2)}.
$$

For any fixed $\theta>3/5$, choose $j\ge k$ so that this ratio is strictly below $\theta$. This proves the result. The argument does not settle the endpoint $\theta=3/5$.

## Two explicit coefficients at every level

Put $s_i=3\cdot2^i$ and $s=s_j$. At the largest differing part, the two following differences of ordinary cut coefficients, in the order $T-T'$, are always exactly $+1$ and $-1$.

$$
\begin{aligned}
(1,s_0,\ldots,s_j,2s+1,6s-1)&\quad +1,\\
(2,s_0,\ldots,s_j,2s,6s-1)&\quad -1.
\end{aligned}
$$

To see this, use $t$ for the root component marker in a rooted cut enumerator, so a root component of order $a$ contributes $t^a$. Completing an enumerator means replacing $t^a$ by $z_a$ in each term. The arms $CQ,BP$ are the tree obtained by joining $B$ to $C$, with $D$ attached at the $B$ root or the $C$ root, respectively. When the attaching edge of $D$ is deleted the two ordinary contributions agree. When it is retained, complete the product of the rooted enumerator of $D$ and the difference of the rooted enumerators at the two sites of the joined tree.

That rooted difference is $(z_1t^2-z_2t)\prod_{i=0}^j U_{B_i}$. Indeed, the parenthesized term is the rooted difference on the initial path. At each joining step its retained-edge terms cancel and its deleted-edge terms multiply the previous rooted difference by the common ordinary cut polynomial. In counting the number of resulting components, the smallest-degree term of each ordinary factor is $z_{s_i}$. The cut-free term of the rooted enumerator of $D$ is $t^{2s-1}$. Every extra deletion in those factors produces an extra component. Consequently the lowest ordinary degree of the arm difference gives exactly
$$
(z_1 z_{2s+1}-z_2 z_{2s})\prod_{i=0}^j z_{s_i}.
$$
Restoring the erased component multiplies by $z_{6s-1}$, proving the two coefficient claims. Both witnesses delete $j+3$ edges. This calculation identifies the minimum number of deletions for a discrepancy **at that largest part**.


## Reproduce the checks

Run **python3 -B verify_cut_depth.py** from this directory. It uses the local **verify_short_witnesses.py** for direct edge deletion and exact connected-set counts. The script compares every ordinary partition through the stated deletion depth. It checks the entire connected-set polynomial on the first two examples, integer evaluations on all four, and a modular cut evaluation that detects a discrepancy at the predicted component size. The proof above establishes equality of every coefficient above that size.

The checker also computes both displayed witness coefficients as exact integers on each tree, using a separate subtree recursion that retains only the specified component sizes.

| Rooted level | Tree order | Edge subsets checked per tree through that level | Largest differing part |
|---:|---:|---:|---:|
| 0 | 28 | 1 | 17 |
| 1 | 58 | 58 | 35 |
| 2 | 118 | 6,904 | 71 |
| 3 | 238 | 2,218,874 | 143 |

[Finite search through 28 vertices](JOINT-OBSERVATIONS.md) · [Verification code](verify_cut_depth.py)

