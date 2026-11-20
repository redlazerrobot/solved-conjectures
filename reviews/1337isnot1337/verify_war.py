"""Verify the published War witnesses by tracking each card's owner and arrival time.

Witness data: 1337isnot1337/solved-conjectures, revision 3e0c5aa,
results/spivey-multiplayer-war/PROOF.md. Run with normal Python 3.
"""

WITNESSES = {
    "rank": (
        ((15, 7, 16, 8, 1, 22, 17, 9), (10, 2, 23, 18, 11, 19, 12, 3),
         (4, 20, 13, 5, 21, 14, 6)),
        90, 6,
    ),
    "seat": (
        ((1, 2, 14, 3, 4, 15, 5, 6), (16, 17, 7, 8, 21, 9, 18),
         (10, 22, 11, 19, 20, 12, 13)),
        180, 6,
    ),
    "clockwise": (
        ((35, 1, 2, 36, 24, 3, 25, 4, 5, 43, 37, 6, 38, 7, 8),
         (26, 9, 10, 44, 11, 39, 40, 27, 12, 41, 13, 28, 29, 14, 15),
         (16, 30, 31, 17, 18, 32, 19, 20, 33, 21, 22, 42, 23, 34)),
        19_320, 12,
    ),
}


def first_return(rule, hands, bound):
    deck = [hand[i] for i in range(max(map(len, hands))) for hand in hands if i < len(hand)]
    n = len(deck)
    assert sorted(deck) == list(range(1, n + 1))
    assert tuple(tuple(deck[i::3]) for i in range(3)) == hands

    owner = {card: i % 3 for i, card in enumerate(deck)}
    arrival = {card: i for i, card in enumerate(deck)}
    minimum = min(map(len, hands))
    wins = [0, 0, 0]
    state = hands
    for turn in range(1, bound + 1):
        played = [hand[0] for hand in state]
        winner = played.index(max(played))
        wins[winner] += 1
        if rule == "rank":
            collected = sorted(played, reverse=True)
        elif rule == "seat":
            collected = [played[winner]] + [c for i, c in enumerate(played) if i != winner]
        elif rule == "clockwise":
            collected = played[winner:] + played[:winner]
        else:
            raise ValueError(rule)
        for i, card in enumerate(collected):
            owner[card] = winner
            arrival[card] = n + 3 * (turn - 1) + i
        ordered = sorted(deck, key=arrival.__getitem__)
        state = tuple(tuple(c for c in ordered if owner[c] == player) for player in range(3))
        minimum = min(minimum, *map(len, state))
        assert minimum > 0
        if state == hands:
            return turn, minimum, tuple(wins)
    raise AssertionError("Starting hands did not return within the certificate bound")


if __name__ == "__main__":
    for rule, (hands, period, minimum) in WITNESSES.items():
        result = first_return(rule, hands, period)
        assert result == (period, minimum, (period // 3,) * 3)
        print(rule, result)
