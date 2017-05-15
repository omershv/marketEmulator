import MarketState
import time
import pyodbc
import os
import traceback
import datetime

sqlUsername = None
if os.path.exists("credentials.txt"):
	sqlUsername = open("credentials.txt").read().splitlines()[0]
	sqlPass = open("credentials.txt").read().splitlines()[1]
else:
	print "No SQL credentails"

def performTrades():
	cnxn = None
	if sqlUsername is not None:
		try:
			cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=history;UID=%s;PWD=%s'%(sqlUsername, sqlPass))
			cnxn.timeout = 1
			cursor = cnxn.cursor()
		except:
			print traceback.print_exc()
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
					MarketState.marketHistory[commodity].append((time.time(), price, amount))
					MarketState.marketHistory[commodity] = MarketState.marketHistory[commodity][-2000:]
					if cnxn is not None:
						try:
							ts = datetime.datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
							seller = int(sell.user.split("user")[1])
							buyer = int(buy.user.split("user")[1])
							q = 'INSERT INTO "history"."dbo"."items" ("timestamp", "commodity", "amount", "price", "seller", "buyer") VALUES (\'%s\', \'%d\', \'%d\', \'%f\', \'%d\', \'%d\'); commit;'%(ts, commodity, amount, price, seller, buyer)
							cursor.execute(q)
						except:
							print traceback.print_exc()