import pickle
import MarketState
from Crypto.PublicKey import RSA
import traceback

class MarketRequest:
	def loadBuySell(self, json):
		try:
			if not json.has_key("price") or not json.has_key("commodity"):
				return "No price or commodity type"
				
			self.price = abs(int(json["price"]))
			self.commodity = int(json["commodity"])
			
			if not MarketState.commodities.has_key(self.commodity):
				return "Bad commodity"
			
			self.id = MarketState.generateRequestId()
			return True
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	requestTypes = {"buy": loadBuySell, "sell": loadBuySell}
	
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

