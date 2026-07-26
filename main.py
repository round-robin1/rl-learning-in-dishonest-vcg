from bidders import Bidder, QLearningBidder
from auction_house import greedy_auction, calculate_payments
from itertools import combinations
from random import choice, randint, sample, seed, uniform
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

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

def run_auction(bidders, q_bidder, items, auction_number):
    q_bidder.choose_action()
    active_bidders = bidders + [q_bidder]
    allocation = greedy_auction(active_bidders, items)
    payments = calculate_payments(active_bidders, items)

    q_bundle = None
    q_payment = 0.0
    for bidder_id, bundle, bid_value, density in allocation:
        if bidder_id == q_bidder.id:
            q_bundle = bundle
            q_payment = payments.get(bidder_id, 0.0)
            break

    q_bidder.record_outcome(q_bundle, q_payment)


q_learning_bidder = QLearningBidder(8, generate_synergies(items), {item: randint(1, 20) for item in items})
for i in range(500):
    normal_bidders = generate_bidders(8, items)
    run_auction(normal_bidders, q_learning_bidder, items, i + 1)
    q_learning_bidder.decay_epsilon()
    q_learning_bidder.history[-1]['auction'] = i + 1
auctions = [entry['auction'] for entry in q_learning_bidder.history]
bid_pcts = [entry['bid_pct'] for entry in q_learning_bidder.history]
policy_pcts = [entry['policy_action_pct'] for entry in q_learning_bidder.history]
profit_pcts = [entry['profit_pct'] for entry in q_learning_bidder.history]

plt.style.use('ggplot')
window = min(200, max(1, len(auctions) // 10))


def moving_average(data, window):
    averaged = []
    for i in range(len(data)):
        start = max(0, i - window + 1)
        averaged.append(sum(data[start:i + 1]) / (i - start + 1))
    return averaged

bid_ma = moving_average(policy_pcts, window)
profit_ma = moving_average(profit_pcts, window)

sample_step = max(1, len(auctions) // 200)
sample_idx = list(range(0, len(auctions), sample_step))

fig, ax = plt.subplots(figsize=(12, 6))
ax2 = ax.twinx()
ax.plot(auctions, bid_ma, color='tab:blue', linewidth=2, label=f'Greedy policy bid % (MA{window})')
ax2.plot(auctions, profit_ma, color='tab:orange', linewidth=2, label=f'Profit % (MA{window})')
ax.scatter([auctions[i] for i in sample_idx], [bid_pcts[i] for i in sample_idx], color='tab:blue', alpha=0.15, s=10, label='Exploring bid %')
ax2.scatter([auctions[i] for i in sample_idx], [profit_pcts[i] for i in sample_idx], color='tab:orange', alpha=0.15, s=10)
ax.set_xlabel('Auction')
ax.set_ylabel('Bid % Adjustment', color='tab:blue')
ax2.set_ylabel('Profit %', color='tab:orange')
ax.set_title('Q-Learner Bid Adjustment and Profit % Over Time')
ax.tick_params(axis='y', labelcolor='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax.grid(True, alpha=0.4)
ax.xaxis.set_major_locator(mticker.MaxNLocator(10))
ax.yaxis.set_major_locator(mticker.MaxNLocator(10))
ax2.yaxis.set_major_locator(mticker.MaxNLocator(10))
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc='upper left')
fig.tight_layout()
fig.savefig('q_learning_bid_profit.png', dpi=200)
print('Saved plot to q_learning_bid_profit.png')
plt.close(fig)
