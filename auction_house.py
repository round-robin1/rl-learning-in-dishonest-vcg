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

    payments = calculate_payments(bidders, items)
    for bidder_id, bundle, bid_value, density in allocation:
        payment = payments.get(bidder_id, 0)
        print(f"Bidder {bidder_id} wins bundle {bundle} with bid {bid_value} (density={density:.2f}) and pays {payment}")


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
    return -1
    