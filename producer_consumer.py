import json
import urllib2
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import pickle
import argparse
import sys
import clientFramework
import time
import random
import traceback
import os

def parse_args():
	parser = argparse.ArgumentParser(description='Producer/Consumer')
	
	parser.add_argument('producer_or_consumer', type=str, choices=['producer','consumer'])
	parser.add_argument('commodity', type=int)
	parser.add_argument('price_target', type=int)
	parser.add_argument('user', type=str)

	args = parser.parse_args()
	if type(args) != argparse.Namespace:
		quit()
	
	return args

def tradeSomething(amount):
	global rate
	marketPrices = json.loads(clientFramework.makeQueryMarketRequest(commodity))
	bid = marketPrices["bid"]
	ask = marketPrices["ask"]
	print marketPrices
	print amount, rate
	if bid == 0: # no buyers
		if ask == 9999999: # no sellers
			price = args.price_target # default price
		else:
			price = max(2, ask - 1) # buy/sell for cheap
	else:
		if ask == 9999999: # no sellers
			price = bid + 1 # buy/sell expensive
		else:
			if args.producer_or_consumer == "consumer":
				price = int((ask + bid) / 2) + 1 # compromise
			else:
				price = max(1, int((ask + bid) / 2) - 1) # compromise
	
	if args.producer_or_consumer == "consumer":
		rateTarget = max(0, 1 + (float(args.price_target - price) / args.price_target))
	else:
		rateTarget = min(10, 1 + (float(price - args.price_target) / args.price_target))
	rate = rate * 0.8 + rateTarget * 0.2
	if args.producer_or_consumer == "consumer":
		print clientFramework.makeBuyRequest(commodity, amount, price)
	else:
		print clientFramework.makeSellRequest(commodity, amount, price)

args = parse_args()
commodity = args.commodity

#clientFramework.init("user99", "http://ise172.ise.bgu.ac.il")
clientFramework.init(args.user, "http://127.0.0.1")

while True:
	try:
		clientFramework.cancelAllBuySells()
		break
	except Exception as e: 
		print traceback.print_exc()

rate = 1.0
while True:
	time.sleep(random.randrange(1, 10))
	if os.path.exists("shutdownc"):
		print 'Shutting down...'
		break
	try:
		tradeSomething(int(random.randrange(10) * rate) + 1)
	except Exception as e: 
		print traceback.print_exc()