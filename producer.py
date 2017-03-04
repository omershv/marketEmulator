import json
import urllib2
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import pickle

def makeReq(data):
	print
	print json.dumps(data)
	print
	req = urllib2.Request("http://127.0.0.1")
	req.add_header("Content-Type", "application/json")
	response = urllib2.urlopen(req, json.dumps(data))
	return response.read()

user = "user99"

keys = private_key = open("keys_private.txt","r").read()
key = keys[keys.index(user):]
key = key[key.index("-----BEGIN RSA PRIVATE KEY-----"):]
key = key[:key.index("-----END RSA PRIVATE KEY-----") + len("-----END RSA PRIVATE KEY-----")]

privateKey = RSA.importKey(key)

cipher = PKCS1_v1_5.new(privateKey)
digest = SHA256.new()
digest.update(user)
token = cipher.sign(digest).encode("base64")

#token = privateKey.sign(user,"")[0]

buyRequest1 = {
        "auth": {"user": user, "token": token},
		"type": "buy",
		"commodity": 1,
		"amount":10,
		"price": 5
}

buyRequest2 = {
        "auth": {"user": user, "token": token},
		"type": "buy",
		"commodity": 1,
		"amount":10,
		"price": 1
}

sellRequest1 = {
        "auth": {"user": user, "token": token},
		"type": "sell",
		"commodity": 2,
		"amount":10,
		"price": 5
}

queryUserRequest = {
        "auth": {"user": user, "token": token},
		"type": "queryUser",
}

queryBuySellRequest = {
        "auth": {"user": user, "token": token},
		"type": "queryBuySell",
		"id":1,
}

queryMarketRequest = {
        "auth": {"user": user, "token": token},
		"type": "queryMarket",
		"commodity":1,
}

cancelBuySell1 = {
        "auth": {"user": user, "token": token},
		"type": "cancelBuySell",
		"id":1,
}

cancelBuySell2 = {
        "auth": {"user": user, "token": token},
		"type": "cancelBuySell",
		"id":2,
}


print makeReq(queryUserRequest)
print makeReq(buyRequest1)
print makeReq(buyRequest2)
print makeReq(sellRequest1)
print makeReq(queryUserRequest)
print makeReq(queryBuySellRequest)
print makeReq(queryMarketRequest)
print makeReq(cancelBuySell1)
print makeReq(queryMarketRequest)
print makeReq(cancelBuySell2)
print makeReq(queryUserRequest)