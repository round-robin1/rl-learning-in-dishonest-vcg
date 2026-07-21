from itertools import combinations


class Bidder():
    def __init__(self, id, synergies, values):
        self.id = id
        self.bids = self.calculate_bids(synergies, values)

    def calculate_bids(self, synergies, values):
        bids = {}
        normalized_synergies = {frozenset(key): value for key, value in synergies.items()}

        items = list(values)
        for size in range(1, len(items) + 1):
            for combo in combinations(items, size):
                key = frozenset(combo)
                bundle_value = sum(values[item] for item in combo)
                synergy = normalized_synergies.get(key, 1)
                bids[key] = bundle_value * synergy

        return bids