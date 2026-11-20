"""Check the equality in the definition of X_G using stable set partitions."""
from collections import Counter

# Entry j (starting at 1) is the parent of vertex j. Root is 0.
HALVES = {
    "A": (0, 0, 0, 0),
    "B": (0, 0, 2, 3),
    "C": (0, 1, 0, 3),
    "D": (0, 0, 0, 3),
    "E": (0, 1, 1, 1),
    "F": (0, 0, 2, 2),
    "G": (0, 1, 1, 3),
}
TERMS = [(-1, "AB"), (1, "AC"), (-1, "DE"),
         (1, "FB"), (-1, "FG"), (1, "EE")]


def stable_profile(pair, join):
    """Count partitions into unlabeled independent sets by sorted sizes."""
    previous = [0] * 10
    for offset, name in zip((0, 5), pair):
        for child, parent in enumerate(HALVES[name], 1):
            previous[offset + child] |= 1 << (offset + parent)
    if join:
        previous[5] |= 1  # join the roots 0 and 5

    profile = Counter()
    classes = []

    def extend(vertex):
        if vertex == 10:
            profile[tuple(sorted(c.bit_count() for c in classes))] += 1
            return
        bit = 1 << vertex
        for i, block in enumerate(classes):
            if not block & previous[vertex]:
                classes[i] |= bit
                extend(vertex + 1)
                classes[i] = block
        # New blocks appear in increasing order of their minimum vertex.
        classes.append(bit)
        extend(vertex + 1)
        classes.pop()

    extend(0)
    return profile


def main():
    for join in (True, False):
        difference = Counter()
        support = set()
        totals = []
        for sign, pair in TERMS:
            profile = stable_profile(pair, join)
            totals.append(sum(profile.values()))
            support.update(profile)
            for partition, count in profile.items():
                difference[partition] += sign * count
        witness = [(p, v) for p, v in sorted(difference.items()) if v]
        print("joined:", join, "totals:", totals, "support:", len(support),
              "nonzero differences:", len(witness))
        if join:
            assert not witness
        else:
            print("first discrepancy:", witness[0])
            assert witness


if __name__ == "__main__":
    main()
