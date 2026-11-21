# Reconstructing both halves from an unknown multiset of branches

Let a tree T on 2h vertices have a balanced edge e. The ordinary chromatic symmetric function determines whether this edge exists: in the unsigned cut polynomial U its one-edge deletion gives the part pair (h,h). It is unique, since any other edge detaches a proper subset of one half. Delete both endpoints of e and call the remaining connected components branches, each rooted at its former point of attachment. Write M for their maximum order. For h>1, M is the largest smaller part in a two-part cut other than (h,h): every noncentral edge detaches a subset of one such branch, and the entire largest branch is attained.

Let r_m be the number of rooted unlabeled trees on m vertices, and put B(M)=max_{1≤m≤M} m r_m. Multiplicities of branches of the same order, including nonisomorphic rootings, are unrestricted.

1. If h−1≥B(M), U determines the entire pooled multiset of rooted branches and the polynomial S counting exactly the cuts through e.
2. If h−M−1≥B(M), U determines T up to isomorphism among all trees.
3. For a single centroid in a tree of order n, if its largest branch has order M and n−M−1≥B(M), the same method reconstructs the tree.

Thus for each branch-size bound there is an explicit order beyond which reconstruction works in either setting. The [support-sensitive bound](SPARSE-BRANCHES.md) below uses the number of types actually present and allows unbounded branch orders. The two-vertex tree needs no reconstruction procedure.

## Reading a product from ordinary cuts

Give x_j weight j. For a rooted branch D of order m, let A_D be the sum over all its edge cuts of the monomial in components *away from its root*. Let U_D count all components in the same cuts. At the attaching edge, keeping it contributes A_D and deleting it contributes U_D. Thus the branch factor is F_D=A_D+U_D. Its constant term is 1. It has weighted degree m and has the form x_m+g_D in which g_D uses only lower-index variables. Distinct rooted types of order m yield different g_D. Indeed their terms of weight less than m are the A_D, which recover the rooted U-polynomial by restoring the root-component order m minus the weight. Use the [rooted reconstruction theorem of Aliste-Prieto, de Mier and Zamora](https://arxiv.org/abs/2002.08186).

Let P be the product of F_D over all branches with multiplicities. In cuts retaining e, omit the component containing both endpoints. The remaining monomials sum to P by independence. If their weight is d<h, the omitted component has size 2h−d>h. Conversely, every term of U having a part larger than h comes from such a cut, and the part is unique. Erasing it recovers P through weight h−1. In particular, this observation does not require knowledge of either endpoint or its neighbors.

## Multiplicity lemma

Consider any product of the factors from a finite list of rooted types of orders at most M. For each m let q_m be the number of allowed types of order m. From the product truncated through weight K, one recovers all multiplicities when K≥max_m m q_m. Allowed types can be absent. Taking the list of all rooted types gives B(M).

Proceed in descending order. Divide by each already recovered factor to its known power; its constant term 1 permits division in the truncated formal series ring. For the residual product at order m, the logarithmic derivative with respect to x_m is

    (∂P/∂x_m)/P = Σ_D c_D/(x_m+g_D),

with the sum over allowed order-m types, since smaller types use no x_m. The left side is known through weight K−m. Multiply by the known polynomial Q=∏_D(x_m+g_D). The exact result is a polynomial of weighted degree at most m(q_m−1). Consequently the available terms determine the whole polynomial. Substitution x_m=−g_E now gives c_E times the product of g_D−g_E over D≠E. This product is nonzero in a polynomial ring over the rationals. The substitution is applied *after* recovering the polynomial, so it never evaluates an unknown series tail. An absent order can be skipped; its total multiplicity is the coefficient of the lone variable x_m in the residual product.

## Recovering S and rooting the halves

Once the pooled inventory is recovered, compute full P. Restore x_(2h−d) to every monomial of weight d, counting multiplicity. This gives all cuts retaining e, since d≤2h−2. Subtracting this polynomial from U gives S. On deleting e the halves H and J can be cut independently, hence S=U_H U_J. Each half polynomial is monic linear in x_h, with its remaining terms in lower variables, and therefore irreducible. Unique factorization gives the unordered pair of ordinary half polynomials, also when they coincide.

Inside a half of order h, omit its attachment vertex's component. Whenever that component has order >M it is recognized from the half polynomial alone: every component away from it lies inside one branch. Erasing the unique large part gives the half's branch-factor product through weight h−M−1. The allowed types can now be restricted to the recovered pool. The lemma identifies the branch multiplicities at that endpoint and hence the rooted half. Joining the two recovered roots finishes the construction. Every rival with the same U has the same balanced edge test and M, and the same recovered inventory and half polynomials. No assumptions on a rival's unobserved branches enter this step. For the single-centroid assertion use the identical erasure argument at order n, as in [the centroid note](CENTROID.md).

## Reproducible example and boundaries

Run [verify_dictionary_example.py](verify_dictionary_example.py) with standard Python 3. The fixture has order 20 and branch orders at most three. Both three-vertex path rootings occur, and the largest order is repeated. The program constructs its input by direct enumeration of all 524,288 cuts. At weight nine, matching the truncation against all feasible branch counts recovers (2,2,3,1) in the order singleton, two-vertex tree, end-rooted three-vertex path, middle-rooted three-vertex path. Subtraction gives 262,144 separated cuts. Testing every equal-weight allocation of the recovered pool against their polynomial gives exactly the unordered split (1,1,1,1) and (1,1,2,0). It also checks each half truncation at weight six. The finite test uses exact enumeration of candidates in place of rational-function arithmetic or general polynomial factorization.

The limiting step is the precision lost in taking the derivative and clearing its distinct possible denominators. If the numerical bound fails, the argument gives no collision. The [linear obstruction](LINEAR-EXTRACTION.md) remains compatible with this nonlinear reconstruction. Historical comparisons include [Loebl and Sereni's shape procedure](https://arxiv.org/abs/1405.4132), [reconstruction at small diameter](https://arxiv.org/abs/2507.15986), and [Zeng's multiplicity-isolated weighted cores](https://arxiv.org/abs/2608.18179). Here the observable truncation supplies multiplicities of rooted branches even when several types have the same order. These arguments were independently derived for this project; publication priority is undetermined.
