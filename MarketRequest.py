import pickle
import MarketState
from Crypto.PublicKey import RSA
import traceback
import json

class MarketRequest:
	def toDict(self):
		d = {
		"user":self.user,
		"type": self.type,
		"commodity": self.commodity,
		"amount": self.amount,
		"price": self.price,
		}
		return d
		
	def processBuySell(self):
		if self.type=="buy":
			if MarketState.userHoldings[self.user]["funds"] < self.price * self.amount:
				return "Insufficient funds"
			MarketState.userHoldings[self.user]["funds"] -= self.price * self.amount
		else:
			if MarketState.userHoldings[self.user]["commodities"][self.commodity] < self.amount:
				return "Insufficient commodity"
			MarketState.userHoldings[self.user]["commodities"][self.commodity] -= self.amount
		MarketState.activeQueries.append(self)
		return str(self.id)
	
	def processQueryBuySell(self):
		matches = [x for x in MarketState.activeQueries if x.id == self.id]
		if len(matches) == 0:
			return "Id not found"
		if matches[0].user != self.user:
			return "User does not match"
		
		return json.dumps(matches[0].toDict())
	
	def processQueryUser(self):
		MarketState.userHoldings[self.user]["requests"] = [x.id for x in MarketState.activeQueries if x.user == self.user]
		return json.dumps(MarketState.userHoldings[self.user])
	
	def processQueryMarket(self):
		requests = [x for x in MarketState.activeQueries if x.commodity == self.commodity]
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
	
	def processCancelBuySell(self):
		matches = [x for x in MarketState.activeQueries if x.id == self.id]
		if len(matches) == 0:
			return "Id not found"
		if matches[0].user != self.user:
			return "User does not match"
		
		req = matches[0]
		if req.type=="buy":
			MarketState.userHoldings[self.user]["funds"] += req.price * req.amount
		else:
			MarketState.userHoldings[self.user]["commodities"][req.commodity] += req.amount
		
		del MarketState.activeQueries[MarketState.activeQueries.index(req)]
		return str("Ok")
	
	def loadBuySell(self, json):
		try:
			if not json.has_key("price") or not json.has_key("commodity") or not json.has_key("amount"):
				return "No price or commodity type/amount"
				
			self.price = abs(int(json["price"]))
			self.commodity = int(json["commodity"])
			self.amount = abs(int(json["amount"]))
			
			if not MarketState.commodities.has_key(self.commodity):
				return "Bad commodity"
			
			self.id = MarketState.generateRequestId()
			return self.processBuySell()
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryBuySell(self, json):
		try:
			if not json.has_key("id"):
				return "No query id"
			self.id = int(json["id"])
			
			return self.processQueryBuySell()
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryUser(self, json):
		try:
			return self.processQueryUser()
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryMarket(self, json):
		try:
			if not json.has_key("commodity"):
				return "No commodity"
			
			self.commodity = int(json["commodity"])
			return self.processQueryMarket()
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadCancelBuySell(self, json):
		try:
			if not json.has_key("id"):
				return "No query id"
			self.id = int(json["id"])
			
			return self.processCancelBuySell()
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	requestTypes = {"buy": loadBuySell, "sell": loadBuySell, "queryBuySell":loadQueryBuySell, 
	"queryUser":loadQueryUser, "queryMarket":loadQueryMarket,
	"cancelBuySell":loadCancelBuySell}
	
	def loadFromJson(self, json):
		try:
			if not json.has_key("auth"):
				return "No auth key"
			
			if not json["auth"].has_key("user") or not json["auth"].has_key("token"):
				return "No user or auth token"
				
			user = json["auth"]["user"].encode("utf8")
			token = json["auth"]["token"]
			
			keys = MarketState.userPublicKeys
			
			if not keys.has_key(user):
				return "Bad user"
			
			public_key_object = RSA.importKey(keys[user])
			
			verified = public_key_object.verify(user, (token,))
			
			if not verified:
				return "Verification failure"
			
			self.user = user
			
			if not json.has_key("type"):
				return "No type key"
			
			self.type = json["type"].encode("utf8")
			
			if not self.requestTypes.has_key(self.type):
				return "Bad request type"
			
			return self.requestTypes[self.type](self, json)
			
		except Exception as e: 
			print traceback.print_exc()
			return str(e)

