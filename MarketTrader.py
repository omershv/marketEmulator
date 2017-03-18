import MarketState

def performTrades():
	for commodity in MarketState.commodities:
		buys = filter(lambda query:query.commodity == commodity and query.type == "buy", MarketState.activeQueries)
		sells = filter(lambda query:query.commodity == commodity and query.type == "sell", MarketState.activeQueries)
		for buy in buys:
			for sell in sells:
				if buy.price >= sell.price and buy.amount > 0 and sell.amount > 0:
					amount = min(buy.amount, sell.amount)
					price = float(buy.price + sell.price) / 2
					buy.amount -= amount
					sell.amount -= amount
					print "Making a deal between %s and %s for %d units of %d commodity priced %d"%(buy.user, sell.user, amount, commodity, price)
					MarketState.userHoldings[buy.user]["commodities"][commodity] += amount
					MarketState.userHoldings[sell.user]["funds"] += amount * price
					MarketState.userHoldings[buy.user]["funds"] += (buy.price - price) * amount # refund the user for price diff
					if buy.amount == 0:
						idx = [i for i in range(len(MarketState.activeQueries)) if MarketState.activeQueries[i].id == buy.id][0]
						del MarketState.activeQueries[idx]
					if sell.amount == 0:
						idx = [i for i in range(len(MarketState.activeQueries)) if MarketState.activeQueries[i].id == sell.id][0]
						del MarketState.activeQueries[idx]