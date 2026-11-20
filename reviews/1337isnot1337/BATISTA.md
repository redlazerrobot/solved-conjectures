# Batista's Egyptian-fraction congruence

**Audit, November 20, 2026.** Claim checked at [upstream revision 3e0c5aaf3be0e6b9e092da1558f87ea09268799f](https://github.com/1337isnot1337/solved-conjectures/blob/3e0c5aaf3be0e6b9e092da1558f87ea09268799f/results/batista-egyptian-fractions/PROOF.md). David Batista posed the conjecture in [OEIS A398581](https://oeis.org/A398581). The proof note is credited to Cinna Davis and GPT-6.2 Astra. Hùng Việt Chu proved the best-two-term approximation theorem used in its first proof. The upstream result is an unrefereed repository note. This audit makes no claim about priority.

## Statement and paper argument

For a positive integer k admitting a solution to 5/k=1/x+1/y+1/z in positive integers x<y<z, with k not congruent to 1 modulo 5, the lexicographically first solution uniquely maximizes z. This is a one-way congruence restriction on exceptions; the note makes no assertion that every k congruent to 1 is exceptional.

I checked the applicability of [Chu, Theorem 1.3](https://arxiv.org/html/2306.12564v2). For k>5, reduce 5/k=p/q and put m=floor(q/p)+1, h=pm−q, B=qm. For residues 0,2,3,4 modulo 5, h is respectively 1,3,2,1. Chu's uniqueness theorem applies because h≤3 and 5/k cannot equal the exceptional rational 10/17. It remains essential that the best pair extends to an exact triple. For y=floor(B/h)+1, d=hy−B is between 1 and h. When h=2 the only case d>1 has even B. When h=3, B=m(5m−3) is 0 or 2 modulo 3; d is then either 3 dividing B or 1. Thus z=By/d is integral. The two strict greedy steps give y≥m(m−1)+1 and z≥y(y−1)>y since m≥2. Every admissible first pair is a strict underapproximation. The largest such sum gives the smallest positive remainder and the largest final denominator. The greedy lower bounds on x and then y give the lexicographic assertion. At k=1,2 the target exceeds 1+1/2+1/3; k=3,4,5 give (1,2,6), (1,5,20), (2,3,6), with first denominator forced. For that fixed first denominator, increasing the second strictly decreases the third.

## Independently executed

Run `python3 verify_batista.py` from this directory. For each k through 150 the [verifier](verify_batista.py) enumerates the integers k/5<x<3k/5. Write the residual 5/k−1/x=a/b in lowest terms. Positive solutions correspond to divisors d and e of b² paired by de=b² with d=ay−b, e=az−b. The strict order y<z gives 0<d<b. The code checks both congruences and x<y<z and compares all resulting triples. This uses a divisor-pair enumeration independently of the upstream scan over y.

The run enumerated **10,726** ordered triples and checked the assertion for **119** admissible k in the claimed residue classes. At k=11 the lexicographically first triple was (3,9,99), and the unique maximizer was (4,5,220). Across this range the denominators where the first triple fell short were 11,16,31,56,81,101,106,121,146. These finite checks do not extend the proven scope.

## Formal statement, replay and hosted checks

* **Source scope.** The pinned [Lean source](https://github.com/1337isnot1337/solved-conjectures/blob/3e0c5aaf3be0e6b9e092da1558f87ea09268799f/lean/Conjectures/EgyptianTheorem.lean) declares `Egyptian.batista_admissible_congruence` with positivity, admissibility and the residue exclusion. Its conclusion includes ordered validity, lexicographic minimality, maximality of the last denominator, and uniqueness in case of equality. The stronger `batista_congruence` proves existence and the same conclusion for k≥3 in those residue classes. The formal route uses a finite certificate below 100 and an elementary comparison above that threshold; Chu's theorem is not a premise.
* **This audit.** Inspected the declarations and the mathematical argument and ran the independent Python checker. No local Lean build or kernel replay ran. Upstream documents its prior replay separately in its [Lean status record](https://github.com/1337isnot1337/solved-conjectures/blob/3e0c5aaf3be0e6b9e092da1558f87ea09268799f/docs/lean-status.md).
* **GitHub CI at the pin.** The [computational workflow](https://github.com/1337isnot1337/solved-conjectures/actions/runs/44787694528) reported success for its Batista step. The [Lean workflow](https://github.com/1337isnot1337/solved-conjectures/actions/runs/44787694461) reported success for the selection job and **skipped** the job named `lean`. That run supplies no fresh kernel replay for this revision.

Other external audits already present when this claim was selected cover Li and Spivey. Their verification scripts are separate; neither has been counted as a new audit here.
