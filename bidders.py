from itertools import combinations
from random import choice, random


class Bidder():
    def __init__(self, id, synergies, values, honest=True):
        self.id = id
        self.honest = honest
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
                if self.honest != True:
                    bids[key] = bundle_value * synergy * 1.1
                else:
                    bids[key] = bundle_value * synergy
        return bids
    
    def get_bid(self, bundle):
        key = frozenset(bundle)
        return self.bids.get(key, 0)

    def get_valuation(self, bundle):
        key = frozenset(bundle)
        return self.bids.get(key, 0)


class QLearningBidder(Bidder):
    def __init__(self, id, synergies, values, actions=None, alpha=0.05, gamma=0.95, epsilon=0.2):
        super().__init__(id, synergies, values)
        self.actions = actions or [
            0.60, 0.65, 0.70, 0.75, 0.80,
            0.85, 0.90, 0.95, 1.00, 1.05,
            1.10, 1.15, 1.20, 1.25, 1.30,
            1.35, 1.40, 1.45, 1.50, 1.55,
            1.60,
        ]
        self.q_values = {action: 0.0 for action in self.actions}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.current_action = 1.0
        self.last_action_pct = 0.0
        self.last_profit_pct = 0.0
        self.total_value_won = 0.0
        self.total_paid = 0.0
        self.history = []

    def choose_action(self):
        if random() < self.epsilon:
            action = choice(self.actions)
        else:
            action = self.best_action()

        self.current_action = action
        self.last_action_pct = round((action - 1.0) * 100, 2)
        return action

    def best_action(self):
        max_q = max(self.q_values.values())
        best_actions = [a for a, q in self.q_values.items() if q == max_q]
        return choice(best_actions)

    def decay_epsilon(self, min_epsilon=0.01, decay_rate=0.9999):
        self.epsilon = max(min_epsilon, self.epsilon * decay_rate)

    def get_bid(self, bundle):
        base_bid = super().get_bid(bundle)
        return round(base_bid * self.current_action, 2)

    def record_outcome(self, bundle, payment):
        valuation = round(self.get_valuation(bundle) if bundle else 0.0, 2)
        profit = round(valuation - payment, 2)
        if valuation > 0:
            profit_pct = round((profit / valuation) * 100, 2)
        else:
            profit_pct = 0.0

        self.last_profit_pct = profit_pct
        self.total_value_won += valuation
        self.total_paid += payment
        self.history.append({
            'bid_pct': self.last_action_pct,
            'policy_action_pct': round((self.best_action() - 1.0) * 100, 2),
            'epsilon': round(self.epsilon, 4),
            'valuation': valuation,
            'payment': round(payment, 2),
            'profit': profit,
            'profit_pct': profit_pct,
            'action': self.current_action,
        })

        reward = profit_pct
        best_future = max(self.q_values.values())
        current_q = self.q_values[self.current_action]
        self.q_values[self.current_action] = round(
            current_q + self.alpha * (reward + self.gamma * best_future - current_q),
            4,
        )
