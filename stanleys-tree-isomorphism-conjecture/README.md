# Stanley’s tree isomorphism conjecture

Do two finite unrooted trees with the same chromatic symmetric function have to be isomorphic?

For a tree T, its chromatic symmetric function sums a monomial over every proper coloring by positive integers. The exponent of each variable records the number of vertices receiving that color. Renaming vertices leaves the function unchanged. Stanley asked whether the function contains enough information to recover the tree.

## Research record

- [Literature search and status, November 20, 2026](LITERATURE.md)
- [A sufficient condition to recover a rooted branch from unrooted cuts](CENTROID.md)
- [A central-edge obstruction and a coefficient separating an infinite family](CENTRAL-EDGE.md)
- [A proof distinguishing the segregated and mixed arrangements for every pair of distinct, equal-order rooted branches](SWITCHING.md)
- [Exact linear recovery through three components and a four-component obstruction at all orders 10k](LINEAR-EXTRACTION.md)
- [Nonlinear recovery from complementary fringe counts on the two sides of a balanced edge](COMPLEMENTARY-FRINGES.md)
- [Branch multiplicities and reconstruction from an unknown pool](BRANCH-MULTIPLICITIES.md)
- [A support-sensitive reconstruction bound](SPARSE-BRANCHES.md)
- [Recovering half-tree fringe histograms](FRINGE-LIFT.md)
- [Distinguishing exchanges at any two sites of a tree](TWO-SITE-EXCHANGE.md)
- [Connected-set reconstruction, its exact output, and an infinite obstruction](CONNECTED-INVENTORY.md)
- [Different inventories with identical full large-component slices](DIFFERENT-POOLS.md)
- [Known edge contexts and the extra observation they provide](EDGE-CONTEXTS.md)
- [Formal linear ambiguities for several contexts](LINEAR-CONTEXT-MAPS.md)

The first proof attempt asks how much of each branch at a centroid can be reconstructed from the sizes of components left by edge cuts. The research target is the unrestricted conjecture.

## Reproducing the checks

Run `python3 verify.py` with standard Python 3. The script computes component sizes directly by deleting edges. It tests the extraction identity at its stated boundary on each rooted tree of order four. For the central-edge obstruction it compares all 8,192 cuts on each of the two 14-vertex trees and checks every three-edge cut on a second pair.

| Check | Observed result |
| --- | --- |
| Rooted branch extraction with n=12 and M=4 | All four rooted types recovered |
| Cut partition (6,6,1,1) in the 14-vertex pair | 8 versus 9 |
| Cut partition (8,8,1,1) in the 18-vertex pair | 24 versus 25 |
| Two nonleaf rootings of a five-vertex path | The leaf witness ties. The (11,7,2,2) cut counts differ by one and the moment determinant is positive. |

The general proofs are in the linked notes. These finite examples check sign, multiplicity, and endpoint conventions.

For the balanced-edge results, run `python3 verify_stable_relation.py`, `python3 verify_balanced_linear.py`, and `python3 verify_complementary_fringe.py` in this directory. The first check uses proper color classes. The other two enumerate edge deletions.

The independent [proper-coloring check](verify_exchange_colorings.py) counts 156 versus 168 assignments of three named colors used three times each after a limb exchange. It also compares all monomial coefficients in an exchange at automorphic sites.
