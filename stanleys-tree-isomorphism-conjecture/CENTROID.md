# Recovering a branch at a centroid

**Working note, November 20, 2026.** This is a sufficient condition for reading a rooted branch from the ordinary, unrooted invariant. The unrestricted conjecture is open. The argument was derived for this project. Priority has not been established.

## What can be read from a cut

Let T be a tree of order n ≥ 2. Its unsigned cut polynomial U is the sum, over all subsets of edges deleted, of the product of x_j over the resulting components, where j is each component’s order. Stanley’s power-sum expansion gives U from the chromatic symmetric function: a coefficient indexed by a partition λ gains the sign (-1)^(n−length(λ)). Give x_j weight j.

Choose a centroid c, a vertex whose removal leaves branches of order at most n/2. Let M be the largest branch order. It can be read without choosing a labeled edge: take the largest smaller part among two-part monomials in U. Indeed the smaller side cut off by an edge directed away from c is contained in a single branch. Equality is attained by cutting the attaching edge of a largest branch. The equal-halves case M=n/2 admits two centroids; the polynomial statements below hold for either choice.

For every cut forest erase the variable of the component containing c, leaving the monomial in the other component orders. Sum these monomials as P. Define K=n−M−1. The part of P of weight at most K is determined by U. A cut in this range leaves n−d>M vertices in the component of c, where d is the erased-root complement weight. Every component avoiding c lies in a single branch and has order at most M. Therefore any part larger than M uniquely identifies the erased component, even when it contains at most half of the tree. Delete that part from each qualifying monomial of U, keeping multiplicities.

## Factoring at the centroid

Root each branch B at its vertex adjacent to c and let m=|B|. For each internal cut of B, record the product over components other than the one containing its root. Their sum is A_B; its weights range from 0 through m−1, with constant coefficient 1. The rooted U-polynomial is recovered from A_B by multiplying each monomial of weight d by z^(m−d). The rooted U-polynomial determines the rooted tree by Aliste-Prieto, de Mier and Zamora.

Set F_B=A_B+U_B, where U_B is the ordinary unsigned cut polynomial of B. The attaching edge is either kept (giving A_B) or deleted (giving U_B), independently for every branch. This proves P=∏F_B. Only the uncut term x_m of U_B uses the variable x_m, and its coefficient is 1. Thus F_B=x_m+G_B, with G_B free of x_m. Once A_B is known, U_B can also be calculated by multiplying each weight-d term of A_B by x_(m−d) and summing.

## A unique largest branch

**Claim.** If there is a unique branch of maximum order M and n≥3M, the unrooted chromatic symmetric function determines that entire branch as a rooted tree.

**Proof.** These hypotheses are detectable from U. The inequality gives M<n/2. Each edge whose smaller side has order M attaches an entire maximal branch, so their number is the two-part coefficient for (n−M,M).

Write P=(x_M+G_B)Q where Q is the product of the smaller-branch factors and contains no x_M. The coefficient of x_M to the first power in P, viewed as a polynomial in x_M, is Q. The observable truncation determines Q through weight K−M. The term independent of x_M is G_B Q and is known through weight K. Divide by Q as a formal series (Q has constant term 1) and keep weights through M−1. This is valid because K−M≥M−1. The result is A_B, since every term of U_B has weight M. Restore the root variable by weight and apply rooted reconstruction. ∎

**Iteration.** Compute F_B and divide the observed P by this factor in the ring truncated above weight K. The same original K is retained. In the residual product the largest index m occurring as a single variable is the next-largest remaining branch order, provided m≤K. Its coefficient equals its multiplicity. The argument can be repeated for each unique next-largest branch with 2m−1≤K. Equal singleton branches have the known factor 1+x_1.

**Consequence.** Every tree with maximum branch order M at a centroid, n≥3M, and pairwise distinct orders among its branches of order greater than one is determined by its ordinary chromatic symmetric function among all trees. A rival with the same invariant yields the same successive extraction steps; no promise about the rival’s branch orders is required. The all-singleton case is directly recognizable.

For a concrete family, start with any rooted tree of order m≥2, attach its root to a new vertex, and attach at least 2m−1 singleton leaves to that new vertex. The condition holds for every choice of the rooted tree and arbitrarily large m. The centroid has one unrestricted nontrivial branch. This illustrates what the criterion measures without limiting the target to this family.

## Where the argument stops

When the largest order occurs twice, the coefficient of x_M becomes a sum of two products. Substituting it for Q in the unique-branch quotient would mix the two rooted trees. When the centroid separates two nearly equal halves, K can be too small even for the unique-factor argument. Terms whose every part is at most M remain available in the full U and are discarded by this extraction. They are a source of possible additional equations.

Sources: [Stanley’s power-sum expansion](https://sites.math.washington.edu/~billey/classes/Hopf.algebra/bulletins/stanley.1995.pdf), [Aliste-Prieto, de Mier and Zamora on rooted U-polynomials](https://arxiv.org/abs/2002.08186), and [the literature record](LITERATURE.md).
