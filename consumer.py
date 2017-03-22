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

def parse_args():
	parser = argparse.ArgumentParser(description='Producer')
	
	parser.add_argument('commodity', type=int)
	parser.add_argument('user', type=str)

	args = parser.parse_args()
	if type(args) != argparse.Namespace:
		quit()
	
	return args

def consumed_something(amount):
	global consumingRate
	marketPrices = json.loads(clientFramework.makeQueryMarketRequest(commodity))
	bid = marketPrices["bid"]
	ask = marketPrices["ask"]
	print marketPrices
	print consumingRate
	if bid == 0: # no buyers
		if ask == 9999999: # no sellers
			price = 10 # default price
		else:
			price = max(2, ask - 1) # buy for cheap
	else:
		if ask == 9999999: # no sellers
			price = bid + 1 # buy expensive
		else:
			price = int((ask + bid) / 2) + 1 # compromise
	
	consumingRateTarget = 1 + (10 - price) * 0.1
	consumingRate = consumingRate * 0.8 + consumingRateTarget * 0.2
	print clientFramework.makeBuyRequest(commodity, amount, price)
	
args = parse_args()
commodity = args.commodity

#clientFramework.init("user99", "http://ise172.ise.bgu.ac.il")
clientFramework.init(args.user, "http://127.0.0.1")
clientFramework.cancelAllBuySells()

consumingRate = 1.0
while True:
	time.sleep(random.randrange(1, 10))
	consumed_something(int(random.randrange(10) * consumingRate) + 1)