import json
import urllib2
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import pickle
import argparse
import sys

def makeBuyRequest(commodity, amount, price):
	req = {
        "auth": {"user": user, "token": token},
		"type": "buy",
		"commodity": commodity,
		"amount": amount,
		"price": price
	}
	return makeReq(req)

def makeSellRequest(commodity, amount, price):
	req = {
        "auth": {"user": user, "token": token},
		"type": "sell",
		"commodity": commodity,
		"amount": amount,
		"price": price
	}
	return makeReq(req)

def makeQueryUserRequest():
	req = {
        "auth": {"user": user, "token": token},
		"type": "queryUser",
	}
	return makeReq(req)

def makeExtendedQueryUserRequest():
	ret = ""
	resp = json.loads(makeQueryUserRequest())
	if resp.has_key("requests"):
		for req in resp["requests"]:
			ret += "\n" + makeQueryBuySellRequest(req)
	return ret

def makeQueryMarketRequest(commodity):
	req = {
        "auth": {"user": user, "token": token},
		"type": "queryMarket",
		"commodity":commodity,
	}
	return makeReq(req)

def makeQueryBuySellRequest(id): 
	req = {
        "auth": {"user": user, "token": token},
		"type": "queryBuySell",
		"id": id,
	}
	return makeReq(req)

def makeCancelBuySellRequest(id): 
	req = {
        "auth": {"user": user, "token": token},
		"type": "cancelBuySell",
		"id":id,
	}
	return makeReq(req)

def cancelAllBuySells():
	ret = ""
	resp = json.loads(makeQueryUserRequest())
	if resp.has_key("requests"):
		for req in resp["requests"]:
			ret += "\n" + makeCancelBuySellRequest(req)
	return ret

def cancelOldBuySells():
	ret = ""
	resp = json.loads(makeQueryUserRequest())
	if resp.has_key("requests"):
		for req in sorted(resp["requests"])[:-10]:
			ret += "\n" + makeCancelBuySellRequest(req)
	return ret

def makeReq(data):
	print
	print json.dumps(data)
	print
	req = urllib2.Request(addr)
	req.add_header("Content-Type", "application/json")
	response = urllib2.urlopen(req, json.dumps(data))
	return response.read()

def init(username, url):
	global token, user, addr
	user = username
	addr = url

	keys = private_key = open("keys_private.txt","r").read()
	key = keys[keys.index(user):]
	key = key[key.index("-----BEGIN RSA PRIVATE KEY-----"):]
	key = key[:key.index("-----END RSA PRIVATE KEY-----") + len("-----END RSA PRIVATE KEY-----")]

	privateKey = RSA.importKey(key)

	cipher = PKCS1_v1_5.new(privateKey)
	digest = SHA256.new()
	digest.update(user)
	token = cipher.sign(digest).encode("base64")