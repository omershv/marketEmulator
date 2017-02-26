import MarketState
import json

def __processBuySell(req):
	if req.type=="buy":
		if MarketState.userHoldings[req.user]["funds"] < req.price * req.amount:
			return "Insufficient funds"
		MarketState.userHoldings[req.user]["funds"] -= req.price * req.amount
	else:
		if MarketState.userHoldings[req.user]["commodities"][req.commodity] < req.amount:
			return "Insufficient commodity"
		MarketState.userHoldings[req.user]["commodities"][req.commodity] -= req.amount
	MarketState.activeQueries.append(req)
	return str(req.id)

def __processQueryBuySell(req):
	matches = [x for x in MarketState.activeQueries if x.id == req.id]
	if len(matches) == 0:
		return "Id not found"
	if matches[0].user != req.user:
		return "User does not match"
	
	return json.dumps(matches[0].toDict())

def __processQueryUser(req):
	MarketState.userHoldings[req.user]["requests"] = [x.id for x in MarketState.activeQueries if x.user == req.user]
	return json.dumps(MarketState.userHoldings[req.user])

def __processQueryMarket(req):
	requests = [x for x in MarketState.activeQueries if x.commodity == req.commodity]
	buyRequests = [x for x in requests if x.type == "buy"]
	sellRequests = [x for x in requests if x.type == "sell"]
	
	buyRequests = list(reversed(sorted(buyRequests, key = lambda r:r.price)))
	sellRequests = sorted(sellRequests, key = lambda r:r.price)
	
	bid = 0
	ask = 9999999
	if len(buyRequests) > 0:
		bid = buyRequests[0].price
	if len(sellRequests) > 0:
		ask = sellRequests[0].price
	return json.dumps({"bid":bid, "ask":ask})

def __processCancelBuySell(req):
	matches = [x for x in MarketState.activeQueries if x.id == req.id]
	if len(matches) == 0:
		return "Id not found"
	if matches[0].user != req.user:
		return "User does not match"
	
	req = matches[0]
	if req.type=="buy":
		MarketState.userHoldings[req.user]["funds"] += req.price * req.amount
	else:
		MarketState.userHoldings[req.user]["commodities"][req.commodity] += req.amount
	
	del MarketState.activeQueries[MarketState.activeQueries.index(req)]
	return str("Ok")

def processReq(req):
	requestTypes = {"buy": __processBuySell, "sell": __processBuySell, "queryBuySell":__processQueryBuySell, 
	"queryUser":__processQueryUser, "queryMarket":__processQueryMarket,
	"cancelBuySell":__processCancelBuySell}
	
	return requestTypes[req.type](req)