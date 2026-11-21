# Graffiti.pc Conjecture 318

The conjecture is due to Ermelinda DeLaViña's Graffiti.pc. The result and proof are credited to **@JesterInABarrel**. Cinna Davis's collection records and formalizes the contributed argument. This audit claims no discovery or publication priority. [Original 2007 catalogue entry, no. 318, p. 186 of the PDF](https://www.uhd.edu/academics/sciences/mathematics-statistics/wowii/files/wowiiaii.pdf) · [Contributor's report](https://x.com/JesterInABarrel/status/2123233964827812334) · [Pinned proof](https://github.com/1337isnot1337/solved-conjectures/blob/19b12e07dc23372f5cd939436b244565f1702a3c/results/graffiti-pc-318/PROOF.md)

## Scope and proof review

Let G be a finite simple connected graph on at least two vertices. Let q count its missing unordered edges. Include distance zero when counting the vertices at even distance from v. The catalogue conjectures that if some vertex v has at least q such vertices, every inclusion-minimal total dominating set has minimum cardinality. Total domination requires a neighbour in the set even for members of the set.

The contributed theorem proves that every total dominating set contains an adjacent total dominating pair. Hence each minimal set has size two. A connected graph of order at least two has its entire vertex set as a total dominating set, so such a pair exists. A singleton cannot totally dominate itself.

To check the reduction, let r count the nonneighbours of v other than v. Its even-distance count is at most r+1. Thus at most one missing edge has both endpoints outside v. Partition the other vertices into singleton classes, with the exceptional missing pair combined if it exists. Each class is independent and all cross-class pairs are adjacent. For a total dominating set D choose a member a adjacent to v. If a member b of D lies outside a's class and differs from v, then a and b dominate each other's classes as well as v and all remaining classes. Otherwise D lies in that class together with v. Every member of the entire class must be dominated from outside the class, forcing v into D and adjacency of v to the whole class. Then v and a totally dominate. These cases include the two-vertex graph.

In the sharpness example a universal vertex joins two disjoint edges. Four edges are missing. The maximum even-distance count is three. Its five minimal total dominating sets consist of four pairs containing the universal vertex and the four-element set omitting it. The conclusion therefore fails if the lower bound on the count is weakened by one.

## Local executions

Pinned upstream revision: `19b12e07dc23372f5cd939436b244565f1702a3c`. We followed the [pinned verification guide](https://github.com/1337isnot1337/solved-conjectures/blob/19b12e07dc23372f5cd939436b244565f1702a3c/docs/verification.md), using Python 3.12.14 with assertions enabled.

1. Run `python3 results/graffiti-pc-318/verify.py` in the upstream checkout. The audited source has Git blob ID `d944d69072497d56d934599d466bc33c2684abd2`. On execution it tested 419,235 labelled graphs of orders 2–7 with at most n+1 missing edges. Exactly 7,337 satisfied the hypotheses. All passed the pair-containment test and the sharpness check passed.
2. Run `python3 reviews/1337isnot1337/verify_graffiti318.py` in this repository. This [independent checker](verify_graffiti318.py) enumerates every labelled graph through order six by its present edges, computes all-pairs shortest paths by Floyd–Warshall, and extracts inclusion-minimal total dominating sets directly. In a finite graph the condition that all minimal total dominating sets have size two is equivalent to pair containment whenever a total dominating set exists. The last column counts connected graphs satisfying the relaxed inequality whose minimal total dominating sets have unequal sizes.

| Order | All graphs | Original hypotheses | Failures of relaxed conjecture |
| ---: | ---: | ---: | ---: |
| 2 | 2 | 1 | 0 |
| 3 | 8 | 4 | 0 |
| 4 | 64 | 26 | 0 |
| 5 | 1,024 | 236 | 15 |
| 6 | 32,768 | 1,371 | 405 |

Every qualifying graph in that enumeration had only minimal sets of size two. It also checked the exact family of minimal sets for the specified graph on five vertices.

## Lean and GitHub evidence

* **Audited statements.** The [pinned Lean note](https://github.com/1337isnot1337/solved-conjectures/blob/19b12e07dc23372f5cd939436b244565f1702a3c/results/graffiti-pc-318/LEAN.md) identifies `Graffiti318.conjecture318` and `Graffiti318.sharpness`. We inspected the source modules. The former proves pair containment, minimal cardinality two, well-total-domination, and total domination number two at all finite orders in scope. The latter gives the five-vertex counterexample to the one-unit relaxation.
* **This audit.** No local Lean build, axiom audit, or kernel replay ran. Both local programs above were Python checks.
* **Actual upstream replay.** We inspected the text log of the successful [historical Candidate base job](https://github.com/1337isnot1337/solved-conjectures/actions/runs/44448033989/job/135304859956) at `98b3433a16e3418ee833d388c8f69c47e8b5c2b3`. The log contains a separate `lake env leanchecker` invocation for each of `Conjectures.Graffiti318Basic`, `Conjectures.Graffiti318` and `Conjectures.Graffiti318Sharpness`, followed by a successful 31-module build, transitive axiom audit and kernel replay conclusion. The three theorem source files have identical Git blob IDs at that revision and the audit pin, respectively `b60d692e415116fa8bed1920119747ad5918e592`, `f4e06237cfdbbc3adcb57da141fc03dc98f34909`, `be4e335de9ad395c913849fa17266e5cd9af258f`. This comparison covers these source files only.
* **At the audit pin.** The [Lean workflow](https://github.com/1337isnot1337/solved-conjectures/actions/runs/44864887884) passed source selection and skipped the Lean job. The [computational job](https://github.com/1337isnot1337/solved-conjectures/actions/runs/44864887851/job/136726973176) completed successfully. Its Graffiti.pc 318 step passed on November 21, 2026 at 04:19:31 UTC. The historical replay and the local executions above supply separate evidence.
