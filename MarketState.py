import pickle

userPublicKeys = pickle.load(open("keys_public.pkl",'rb'))
users = userPublicKeys.keys()

commodities = {0:{"name":"Banana"}, 1:{"name":"Kiwi"}, 2:{"name":"Pineapple"}, 3:{"name":"Mango"}}

userHoldings = pickle.load(open("user_holdings.pkl",'rb'))
requestId = pickle.load(open("request_ids.pkl",'rb'))

def saveData():
	pickle.dump(userHoldings, open("user_holdings.pkl",'wb'))
	pickle.dump(requestId, open("request_ids.pkl",'wb'))

def resetStatus():
	global requestId
	for user in users:
		userHoldings[user] = {"funds": 100, "commodities": {0:0, 1:0, 2:0, 3:0}}
	requestId = 0

def generateRequestId():
	global requestId
	requestId = requestId + 1
	return requestId