# rl-learning-in-dishonest-vcg
An experiment in how a reinforcement model learns to bid in a VCG Auction with bidders who don't quite understand the game

Using Q-Learning, we will see how a model learns to bid in a VCG Auction in 4 different scenarios:
- Perfect Winner Calculation, All Bidders Honest
- Imperfect Winner Calculation, All Bidders Honest
- Perfect Winner Calculation, 50% of Bidders overbid
- Imperfect Winner Calculation, 50% of Bidders overbid

My initial prediction is that, for both perfect winner walculation scenarios, the model will learn to bid it's valuation. However, with imperfect winner calculation, the model will learn to bid somewhat dishonestly when all other bidders are honest, and very dishonestly when some bidders are dishonest, in aims to exploit whatever weakness they leave in the auction.