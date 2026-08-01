from functools import lru_cache
from itertools import combinations

def gather_bids(bidders, items):
    bids = []
    for bidder in bidders:
        for size in range(1, len(items) + 1):
            for combo in combinations(items, size):
                bid_value = round(bidder.get_bid(combo), 2)
                if bid_value > 0:
                    density = round(bid_value / len(combo), 2)
                    bids.append((bid_value, density, bidder.id, combo))
    bids.sort(reverse=True, key=lambda x: (x[1], x[0]))
    return bids

def greedy_auction(bidders, items):
    sold_items = []
    finished_buyers = []
    allocation = []
    bids = gather_bids(bidders, items)
    for bid_value, density, bidder_id, bundle in bids:
        if all(item not in sold_items for item in bundle) and bidder_id not in finished_buyers:
            sold_items.extend(bundle)
            finished_buyers.append(bidder_id)
            allocation.append((bidder_id, bundle, bid_value, density))

    return allocation

def calculate_payments(bidders, items):
    payments = {}
    allocation = []
    sold_items = []
    finished_buyers = []
    bids = gather_bids(bidders, items)

    for bid_value, density, bidder_id, bundle in bids:
        if all(item not in sold_items for item in bundle) and bidder_id not in finished_buyers:
            sold_items.extend(bundle)
            finished_buyers.append(bidder_id)
            allocation.append((bidder_id, bundle, bid_value))

    total_welfare = round(sum(bid_value for _, _, bid_value in allocation), 2)

    for bidder_id, bundle, bid_value in allocation:
        remaining_bidders = [b for b in bidders if b.id != bidder_id]
        remaining_sold = []
        remaining_finished = []
        remaining_bids = gather_bids(remaining_bidders, items)
        replacement_welfare = 0

        for other_value, other_density, other_id, other_bundle in remaining_bids:
            if all(item not in remaining_sold for item in other_bundle) and other_id not in remaining_finished:
                remaining_sold.extend(other_bundle)
                remaining_finished.append(other_id)
                replacement_welfare += other_value

        other_welfare = round(total_welfare - bid_value, 2)
        payments[bidder_id] = round(max(0, replacement_welfare - other_welfare), 2)

    return payments

def proper_auction(bidders, items):
    item_positions = {item: index for index, item in enumerate(items)}
    all_mask = (1 << len(items)) - 1

    bidder_bids = []
    for bidder in bidders:
        bids = []
        for size in range(1, len(items) + 1):
            for combo in combinations(items, size):
                bid_value = round(bidder.get_bid(combo), 2)
                if bid_value > 0:
                    density = round(bid_value / len(combo), 2)
                    bids.append((bid_value, density, bidder.id, combo))
        bids.sort(reverse=True, key=lambda x: (x[1], x[0]))
        bidder_bids.append(bids)

    @lru_cache(maxsize=None)
    def best_allocation(bidder_index, remaining_mask):
        if bidder_index == len(bidders):
            return 0.0, ()

        best_welfare = 0.0
        best_choice = ()

        skip_welfare, skip_choice = best_allocation(bidder_index + 1, remaining_mask)
        if skip_welfare > best_welfare:
            best_welfare = skip_welfare
            best_choice = skip_choice

        for bid_value, density, bidder_id, bundle in bidder_bids[bidder_index]:
            bundle_mask = 0
            for item in bundle:
                bundle_mask |= 1 << item_positions[item]

            if bundle_mask & remaining_mask != bundle_mask:
                continue

            future_welfare, future_choice = best_allocation(bidder_index + 1, remaining_mask ^ bundle_mask)
            total_welfare = round(bid_value + future_welfare, 2)
            if total_welfare > best_welfare:
                best_welfare = total_welfare
                best_choice = ((bidder_id, bundle, bid_value, density),) + future_choice

        return round(best_welfare, 2), best_choice

    _, allocation = best_allocation(0, all_mask)
    return list(allocation)
