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

def makeReq(data):
	print
	print json.dumps(data)
	print
	req = urllib2.Request("http://127.0.0.1")
	req.add_header("Content-Type", "application/json")
	response = urllib2.urlopen(req, json.dumps(data))
	return response.read()

def init():
	global user
	global token
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

def parse_args():
	parser = argparse.ArgumentParser(description='Runs queries on the market server.')
	
	subparsers = parser.add_subparsers(help='sub-command help')

	parser_buy = subparsers.add_parser('buy', help='buy request')
	parser_buy.add_argument('commodity', type=int)
	parser_buy.add_argument('amount', type=int)
	parser_buy.add_argument('price', type=int)

	parser_sell = subparsers.add_parser('sell', help='sell request')
	parser_sell.add_argument('commodity', type=int)
	parser_sell.add_argument('amount', type=int)
	parser_sell.add_argument('price', type=int)

	parser_query_user = subparsers.add_parser('query_user', help='query user request')

	parser_query_buy_sell = subparsers.add_parser('query_buy_sell', help='query buy/sell request')
	parser_query_buy_sell.add_argument('id', type=int)

	parser_query_market = subparsers.add_parser('query_market', help='query market request')
	parser_query_market.add_argument('commodity', type=int)

	parser_cancel_buy_sell = subparsers.add_parser('cancel_buy_sell', help='cancel buy/sell request')
	parser_cancel_buy_sell.add_argument('id', type=int)

	parser_query_user = subparsers.add_parser('cancel_all_buy_sell', help='cancels all of the user requests')

	args = parser.parse_args()
	if type(args) != argparse.Namespace:
		quit()
	
	return args


args = parse_args()
init()

print {'buy': makeBuyRequest, 'sell': makeSellRequest, 'query_user': makeQueryUserRequest, 
'query_buy_sell': makeQueryBuySellRequest, 'query_market': makeQueryMarketRequest, 
'cancel_buy_sell': makeCancelBuySellRequest, 'cancel_all_buy_sell': cancelAllBuySells}[sys.argv[1]](**vars(args))