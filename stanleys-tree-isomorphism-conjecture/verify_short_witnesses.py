"""Check the 20-vertex obstruction, then find short witnesses in optional census-candidate logs.

    python3 verify_short_witnesses.py
    python3 verify_short_witnesses.py candidates.txt

Each candidate line is emitted by verify_joint_range.cpp with its fourth argument set.
Uses standard Python 3.8 or later. All polynomial coefficients use exact integers.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import sys

popcount = getattr(int, "bit_count", lambda n: bin(n).count("1"))
FIXTURE = (
    ("(()()()(())(()()()))", "((())(()()(()(()))))"),
    ("(()()()(())(()(())))", "(()()((())(()()())))"),
)


def parse(code):
    stack = []
    for char in code:
        if char == "(":
            stack.append([])
        elif char == ")":
            children = tuple(stack.pop())
            if stack:
                stack[-1].append(children)
        else:
            raise ValueError(code)
    if stack:
        raise ValueError(code)
    return children


@lru_cache(maxsize=None)
def census(tree):
    """(root-containing, all) connected sets, indexed by (order, boundary)."""
    rooted = Counter({(1, 0): 1})
    away = Counter()
    for branch in tree:
        marked, whole = census(branch)
        away.update(whole)
        away.subtract(marked)
        away.update({(i, j+1): v for (i, j), v in marked.items()})
        options = marked + Counter({(0, 1): 1})
        joined = Counter()
        for (i, j), v in rooted.items():
            for (k, l), z in options.items():
                joined[i+k, j+l] += v*z
        rooted = joined
    return rooted, away + rooted


def whole(halves):
    left, right = map(parse, halves)
    return left + (right,)


def descendants(tree):
    """Number vertices in preorder. A parent's bit mask contains its descendants and itself."""
    parent = [None]

    def visit(children, root):
        for branch in children:
            child = len(parent)
            parent.append(root)
            visit(branch, child)

    visit(tree, 0)
    masks = [1 << i for i in range(len(parent))]
    for i in reversed(range(1, len(parent))):
        masks[parent[i]] |= masks[i]
    return masks


def cuts(masks, k):
    """Directly delete k edges. Count total partitions and those cutting the balanced edge."""
    n = len(masks)
    balanced, = [i for i in range(1, n) if popcount(masks[i]) == n//2]
    total, separated = Counter(), Counter()
    for subset in combinations(range(1, n), k):
        remaining = masks[0]
        parts = []
        # Descendant edges come first, so every detached vertex is counted exactly once.
        for index in reversed(subset):
            detached = masks[index] & remaining
            parts.append(popcount(detached))
            remaining ^= detached
        shape = tuple(sorted(parts + [popcount(remaining)]))
        total[shape] += 1
        if balanced in subset:
            separated[shape] += 1
    return total, separated


def verify_fixture():
    left, right = map(whole, FIXTURE)
    h_left, h_right = census(left)[1], census(right)[1]
    assert h_left == h_right and (sum(h_left.values()), len(h_left)) == (19155, 132)
    left, right = map(descendants, (left, right))
    for k in (1, 2):
        assert cuts(left, k) == cuts(right, k)
    total_a, through_a = cuts(left, 3)
    total_b, through_b = cuts(right, 3)
    assert (total_a[1, 3, 3, 13], total_b[1, 3, 3, 13]) == (2, 3)
    assert (through_a[1, 1, 8, 10], through_b[1, 1, 8, 10]) == (34, 33)
    print("Fixture: H has 19,155 sets in 132 bins, and all one- and two-edge cuts agree.")
    print("Three-edge counts: 2 vs 3 at (1,3,3,13); separated 34 vs 33 at (1,1,8,10).")


def check_logs(filenames):
    rows = defaultdict(Counter)
    totals = Counter()
    for filename in filenames:
        with open(filename) as source:
            for line in source:
                if line.startswith("h="):
                    fields = dict(item.split("=") for item in line.split())
                    totals[int(fields["h"])] += int(fields["census_candidates"])
                if not line.startswith("candidate "):
                    continue
                _, number, a, b, _, c, d = line.split()
                h = int(number)
                left, right = whole((a,b)), whole((c,d))
                if census(left)[1] != census(right)[1]:
                    rows[h]["accidental"] += 1
                    continue
                left, right = map(descendants, (left, right))
                # Equal H implies agreement on all one-edge partitions.
                for k in range(2, 5):
                    ca, cb = cuts(left, k)[0], cuts(right, k)[0]
                    if any(t[-1] > h and ca[t] != cb[t] for t in ca.keys() | cb.keys()):
                        rows[h][k] += 1
                        break
                else:
                    raise RuntimeError(("four cuts insufficient", h, a, b, c, d))
    print("h  candidates  accidental  first-witness-by-cuts(2,3,4)")
    for h in sorted(rows.keys() | totals.keys()):
        row = rows[h]
        if sum(row.values()) != totals[h]:
            raise ValueError("Candidate log missing records at h=%s" % h)
        print(h, totals[h], row["accidental"], *(row[k] for k in (2, 3, 4)))


if __name__ == "__main__":
    verify_fixture()
    if len(sys.argv) > 1:
        check_logs(sys.argv[1:])
