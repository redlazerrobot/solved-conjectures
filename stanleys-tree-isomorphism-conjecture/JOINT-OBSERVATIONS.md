# Balanced-edge reconstruction from connected sets and edge cuts

The open question here is whether two observations determine the cuts through the unique edge that divides a tree into equal halves. The first observation counts connected vertex sets by their order and number of boundary edges. The second counts every partition of component sizes obtained by deleting edges when its largest component contains more than half of the vertices.

## Results

**Agreement to any fixed cut depth.** For every fixed number of deletions and every fixed fraction above three fifths, there are balanced trees that agree on all cuts up to that depth, on every cut with a component reaching that fraction, and on their entire connected-set census. Their counts for cuts through the balanced edge differ. The proof locates the first differing large-component coefficient by weight and explains why the examples still separate at the half-tree threshold. [Proof and four worked orders](CUT-DEPTH.md)

**Finite reconstruction.** Through order 28 the connected-set census together with the large-component coefficients from at most three edge deletions distinguishes every balanced tree up to isomorphism. Among 634,947,353 trees, there are 486 unordered pairs of distinct trees of the same order sharing the entire connected-set census. In 456 of those pairs there is a distinguishing two-edge cut leaving a component larger than half the tree. In the other 30 pairs, three deletions suffice and two do not when only these large-component cuts are retained.

**Conditional reconstruction.** Suppose the tree has order $2h$ and its largest branch at either endpoint of the balanced edge has order $M$. When $3M\le 2h+1$, the one- and two-boundary connected-set counts together with the two-edge cuts having a component larger than $h$ determine all two-edge-cut counts. The argument also recovers some coefficients for three-edge cuts passing through the balanced edge. [Derivation and scope](JOINT-TRIPLES.md)

**Caterpillar switches.** For every nonisomorphic pair arising from the composition-factor reversals in Theorem 14 of Aliste-Prieto, Martin, Wagner and Zamora, two edge deletions give a distinguishing partition whose largest part exceeds half the order. The proof gives the partition from the composition factors. [Proof and examples](CATERPILLAR-SWITCH-CUTS.md)

### The finite search

Every balanced tree is uniquely an unordered pair of equal-order rooted halves joined at their roots. A rooted tree, in turn, consists of its root and an unordered multiset of smaller rooted trees. These two descriptions give an exhaustive generation without requiring a graph-isomorphism heuristic.

The first pass evaluates the connected-set polynomial at fixed values modulo $2^{61}-1$. Unequal evaluations certify unequal polynomials. Every pair with equal evaluations enters a second pass which compares its complete census with exact integer arithmetic and directly enumerates the small edge cuts. All 486 first-pass matches had equal exact censuses. Thus modular collisions could increase the work but could never discard an actual equal pair. The census also detects the balanced edge from the two connected half-order sets with one boundary edge.

| Vertices | Balanced trees | Equal-census pairs | Two edge deletions* | Three edge deletions* |
|---:|---:|---:|---:|---:|
| 2 through 12 | 270 | 0 | 0 | 0 |
| 14 | 1,176 | 2 | 2 | 0 |
| 16 | 6,670 | 3 | 3 | 0 |
| 18 | 41,041 | 4 | 4 | 0 |
| 20 | 258,840 | 18 | 17 | 1 |
| 22 | 1,697,403 | 36 | 35 | 1 |
| 24 | 11,359,761 | 49 | 46 | 3 |
| 26 | 77,956,341 | 183 | 172 | 11 |
| 28 | 543,625,851 | 191 | 177 | 14 |
| **Total** | **634,947,353** | **486** | **456** | **30** |

*The last two columns count pairs by the minimum number of edges deleted in a single distinguishing cut leaving a component larger than half the tree.*

The smallest example requiring three deletions has 20 vertices. For the two trees encoded in the Python checker, all ordinary one- and two-edge counts coincide and the connected-set census counts 19,155 sets in 132 bins. At partition $(1,3,3,13)$ the ordinary three-edge counts are 2 and 3. At $(1,1,8,10)$ the counts restricted to cuts through the balanced edge are 34 and 33.

### Reproduction

From this directory use a C++17 compiler with unsigned 128-bit arithmetic and Python 3.8 or newer. The second argument to the first executable controls how many batches it uses for sorting, trading memory for runtime. Twenty batches at order 28 require about 435 MB of pair records plus overhead.

```sh
c++ -std=c++17 -O3 verify_joint_range.cpp -o verify_joint_range
./verify_joint_range 14 20 1 log > candidates.txt
python3 verify_short_witnesses.py candidates.txt
python3 verify_cut_depth.py
python3 verify_joint_triples.py
python3 verify_switch_witness.py
```

[Enumeration source](verify_joint_range.cpp) · [Exact short-cut checker and the 20-vertex example](verify_short_witnesses.py)

The finite search concerns the restricted observations on balanced trees. The general tree-isomorphism question asks whether the full ordinary chromatic symmetric function distinguishes all trees. The mathematical context and the implication from the chromatic symmetric function to the connected-set census are given by [Aliste-Prieto, Martin, Wagner and Zamora](https://arxiv.org/html/2402.10333v2).

