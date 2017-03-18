import MarketState
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import traceback
import json
import RequestOperations
import pickle

class MarketRequest:
	def toDict(self):
		d = {
		"user": self.user,
		"type": self.type,
		"commodity": self.commodity,
		"amount": self.amount,
		"price": self.price,
		}
		return d
	
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
			return RequestOperations.processReq(self)
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryBuySell(self, json):
		try:
			if not json.has_key("id"):
				return "No query id"
			self.id = int(json["id"])
			
			return RequestOperations.processReq(self)
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryUser(self, json):
		try:
			return RequestOperations.processReq(self)
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryMarket(self, json):
		try:
			if not json.has_key("commodity"):
				return "No commodity"
			
			self.commodity = int(json["commodity"])
			return RequestOperations.processReq(self)
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadCancelBuySell(self, json):
		try:
			if not json.has_key("id"):
				return "No query id"
			self.id = int(json["id"])
			
			return RequestOperations.processReq(self)
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
			cipher = PKCS1_v1_5.new(public_key_object)
			digest = SHA256.new()
			digest.update(user)
			verified = cipher.verify(digest, token.decode('base64'))
			
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

MarketState.activeQueries = pickle.load(open("active_queries.pkl",'r'))