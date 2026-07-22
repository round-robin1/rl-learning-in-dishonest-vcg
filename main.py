from bidders import Bidder
from itertools import combinations
from random import choice, randint, sample, seed, uniform

seed(42)

items = ['a', 'b', 'c', 'd', 'e', 'f']

def generate_bidders(num_bidders, items):
    bidders = []
    for i in range(num_bidders):
        values = {item: randint(1, 20) for item in items}
        synergies = generate_synergies(items)
        bidder = Bidder(i, synergies, values)
        bidders.append(bidder)
    return bidders

def generate_synergies(items):
    size2_candidates = [frozenset(combo) for combo in combinations(items, 2)]
    size3_candidates = [frozenset(combo) for combo in combinations(items, 3)]

    synergies = {}
    include_size3 = choice([True, False])
    if include_size3:
        chosen_size3 = choice(size3_candidates)
        synergies[chosen_size3] = round(uniform(1.2, 1.6), 2)
        remaining = 2
    else:
        remaining = 3

    available_size2 = [s for s in size2_candidates if s not in synergies]
    chosen_size2 = sample(available_size2, remaining)
    for synergy in chosen_size2:
        synergies[synergy] = round(uniform(1.2, 1.6), 2)

    return synergies

bidders = generate_bidders(8, items)
print("All Bidders and their bids for {a, c}")
for bidder in bidders:
    print(f"Bidder ID: {bidder.id}")
    print(f"Bid for {{a, c}}: {bidder.get_bid(['a', 'c'])}")

