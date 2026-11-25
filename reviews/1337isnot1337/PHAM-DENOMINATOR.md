# Audit of the Bulgarian solitaire denominator counterexample

The independent reviewing agent prepared this report and ran the accompanying checker.

**Finding.** For the primitive necklace 0001001011, the limiting level series has reduced denominator of degree 5, while the necklace has length 10. I independently reproduced every coefficient required for the primary counterexample and checked the argument extending the finite count to all degrees. The counterexample comes from the collection curated by Cinna Davis and GPT-6.2 Astra. Nhung Pham posed the question and supplied the rationality and stabilization theorems used here. [Pinned upstream proof](https://github.com/1337isnot1337/solved-conjectures/blob/9ad9f0a0cef469e9205b4a964b756a3dab6cb2b5/results/pham-denominator-degree/PROOF.md) · [Pham, Theorem 1.2 and Sections 4 and 6](https://arxiv.org/pdf/2208.14496)

## Independent count

Bulgarian solitaire subtracts one from every pile, discards empty piles and adds a new pile equal to the previous number of piles. The coefficient at depth $n$ counts the partitions that first reach the necklace's recurrent cycle after exactly $n$ forward steps. I started from the ten staircase-plus-necklace partitions for 27 repetitions. Applying the forward game confirmed that these partitions are distinct and stable as a set. The necklace is primitive since it has no period 1, 2 or 5. Pham's stabilization in Section 4 makes this finite model sufficient through depth 25.

For a partition of length $m$, each distinct pile size $v\ge m-1$ gives one predecessor. Remove one pile of that size, increment every remaining pile and append $v-m+1$ singletons. Distinct choices give distinct predecessor lengths. Because a position has a unique forward image, removing cycle predecessors on the first step leaves disjoint reverse trees.

The checker stores the length and a decreasing prefix of actual pile sizes, keeping multiplicities for distinct paths that share this information. It starts with the first 79 piles and shortens the retained prefix by one per reverse move. At each reached state it asserts that the final retained pile is too small to be selected and that the head ends before the full partition ends. Thus the omitted suffix cannot supply a playable pile, and the next prefix is determined exactly. The checker tests cycle exclusions using the full root partitions and ordinary forward moves. This recount uses neither the upstream prefix encoding nor its coefficient table. Run **python3 verify_pham.py** in this directory. [Independent checker](verify_pham.py)

For depths 0 through 25, the count was

```text
10, 4, 10, 18, 30, 52, 96, 164, 280, 484, 860, 1512, 2588,
4476, 7856, 13796, 23900, 41288, 72076, 126220, 219664,
380628, 662252, 1157000, 2016604, 3502748.
```

## All-degree conclusion and scope

Let $Q=1-x^3-4x^4-6x^5$ and $R=10+4x+10x^2+8x^3-14x^4-34x^5+14x^6+2x^7$. I used integer convolution to verify $QH\equiv R\pmod{x^{26}}$ and the rational Euclidean algorithm to verify $\gcd(Q,R)=1$. Pham's theorem gives $H=A/B$ with $\deg A\le20$, $\deg B\le10$ and $B(0)\ne0$. Consequently $QA-RB$ has degree at most 25 and is divisible by $x^{26}$, so it vanishes. This establishes the primary identity exactly.

Pham's Section 6 describes the conjectured denominator degree as exactly the primitive necklace length. The counterexample addresses its reduced-denominator interpretation. The question of representing a dual pair over a common denominator is separate. This audit used Pham's published theorems and independently executed Python. The dual identity and the upstream Lean kernel build are outside the audit. [Later duality formulation, Harris and Nguyen](https://arxiv.org/abs/2308.05321) · [Upstream formal proof description](https://github.com/1337isnot1337/solved-conjectures/blob/9ad9f0a0cef469e9205b4a964b756a3dab6cb2b5/results/pham-denominator-degree/FORMAL_PROOF.md)
