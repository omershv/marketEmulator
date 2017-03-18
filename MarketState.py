import pickle

userPublicKeys = pickle.load(open("keys_public.pkl",'r'))
users = userPublicKeys.keys()

commodities = {0:{"name":"Banana"}, 1:{"name":"Kiwi"}, 2:{"name":"Pineapple"}, 3:{"name":"Mango"}}

userHoldings = pickle.load(open("user_holdings.pkl",'r'))
requestId = pickle.load(open("request_ids.pkl",'r'))

def saveData():
	global requestId, activeQueries, userHoldings
	pickle.dump(userHoldings, open("user_holdings.pkl",'wb'))
	pickle.dump(requestId, open("request_ids.pkl",'wb'))
	pickle.dump(activeQueries, open("active_queries.pkl",'wb'))

def resetStatus():
	global requestId, activeQueries, userHoldings
	for user in users:
		userHoldings[user] = {"funds": 100, "commodities": {0:10, 1:10, 2:10, 3:10}}
	for i in range(80,900):
		userHoldings[user] = {"funds": 999999999999999, "commodities": {0:0, 1:0, 2:0, 3:0}} # consumers are rich
	for i in range(90,100):
		userHoldings["user%d"%i] = {"funds": 0, "commodities": {0:999999999999999, 1:999999999999999, 2:999999999999999, 3:999999999999999}} # producers have it all
	userHoldings["user99"] = {"funds": 999999999999999, "commodities": {0:999999999999999, 1:999999999999999, 2:999999999999999, 3:999999999999999}} # test user
	requestId = 0
	activeQueries = []

def generateRequestId():
	global requestId
	requestId = requestId + 1
	return requestId