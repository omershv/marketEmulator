import MarketState
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5 as pkcs
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import traceback
import json
import RequestOperations
import pickle
import time
import os

userTimings = dict(map(lambda i:(("user%d"%i), list(range(0,2000,100))),range(100)))
userNonces = dict(map(lambda i:(("user%d"%i), []),range(100)))

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
			
			if self.amount <= 0:
				return "Bad amount"
			
			if self.price <= 0:
				return "Bad price"
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
	
	def loadQueryNoArgs(self, json):
		try:
			return RequestOperations.processReq(self)
		except Exception as e: 
			print traceback.print_exc()
			return str(e)
	
	def loadQueryMarket(self, json):
		try:
			if not json.has_key("commodity"):
				return "No commodity"
			
			if not MarketState.commodities.has_key(json["commodity"]):
				return "Bad commodity"
			
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
	"queryUser":loadQueryNoArgs, "queryMarket":loadQueryMarket, "queryAllMarket":loadQueryNoArgs,
	"cancelBuySell":loadCancelBuySell, "queryUserRequests":loadQueryNoArgs}
	
	def loadFromJson(self, json):
		try:
			if not json.has_key("auth"):
				return "No auth key"
			
			if not json["auth"].has_key("user") or not json["auth"].has_key("token"):
				return "No user or auth token"
			
			nonce = None
			if json["auth"].has_key("nonce"):
				nonce = json["auth"]["nonce"]
			
			user = json["auth"]["user"].encode("utf8")
			token = json["auth"]["token"]
			
			keys = MarketState.userPublicKeys
			
			if not keys.has_key(user):
				return "Bad user"
			
			public_key_object = RSA.importKey(keys[user])
			cipher = PKCS1_v1_5.new(public_key_object)
			digest = SHA256.new()
			if nonce is not None:
				digest.update("%s_%s"%(user,nonce))
				if nonce in userNonces[user]:
					return "Non unique nonce"
				userNonces[user].append(nonce)
				userNonces[user] = userNonces[user][-100:]
			else:
				digest.update(user)
			
			verified = cipher.verify(digest, token.decode('base64'))
			
			if not verified:
				return "Verification failure"
			
			self.user = user
			
			userTimings[self.user].append(time.time())
			userTimings[self.user] = userTimings[self.user][-20:]
			if userTimings[self.user][-1] - userTimings[self.user][0] < 10:
				print "Penalty for user %s"%(self.user)
				MarketState.semaphore.release()
				time.sleep(120)
				MarketState.semaphore.acquire()
			
			if not json.has_key("type"):
				return "No type key"
			
			self.type = json["type"].encode("utf8")
			
			print "User %s Request %s"%(user, self.type)
			
			if not self.requestTypes.has_key(self.type):
				return "Bad request type"
			
			resp = self.requestTypes[self.type](self, json)
			if nonce is not None:
				cipher = pkcs.new(public_key_object)
				resp = "".join(map(lambda i:cipher.encrypt(resp[i:i + 64]), range(0,len(resp),64)))
				return resp.encode('base64')
			else:
				return resp
			
		except Exception as e: 
			print traceback.print_exc()
			return str(e)

MarketState.activeQueries = pickle.load(open("active_queries.pkl",'r'))