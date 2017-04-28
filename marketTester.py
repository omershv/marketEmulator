import json
import urllib2
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import pickle
import argparse
import sys
import clientFramework

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
	
	parser_query_user_requests = subparsers.add_parser('query_user_requests', help='query user requests request')
	parser_query_user_requests.add_argument('user', type=str)
	
	parser_query_user_extended = subparsers.add_parser('query_user_extended', help='extended query user request')
	parser_query_user_extended.add_argument('user', type=str)

	parser_query_buy_sell = subparsers.add_parser('query_buy_sell', help='query buy/sell request')
	parser_query_buy_sell.add_argument('id', type=int)

	parser_query_market = subparsers.add_parser('query_market', help='query market request')
	parser_query_market.add_argument('commodity', type=int)

	parser_query_all_market = subparsers.add_parser('query_all_market', help='query all market request')
	
	parser_cancel_buy_sell = subparsers.add_parser('cancel_buy_sell', help='cancel buy/sell request')
	parser_cancel_buy_sell.add_argument('id', type=int)

	parser_query_user = subparsers.add_parser('cancel_all_buy_sell', help='cancels all of the user requests')

	args = parser.parse_args()
	if type(args) != argparse.Namespace:
		quit()
	
	return args


user = "user99"
args = parse_args()
if sys.argv[1] == "query_user_extended" or sys.argv[1] == "query_user_requests":
	user = args.user
	del args.user
clientFramework.init(user, "http://ise172.ise.bgu.ac.il")
#clientFramework.init(user, "http://127.0.0.1")

print {'buy': clientFramework.makeBuyRequest, 'sell': clientFramework.makeSellRequest, 'query_user': clientFramework.makeQueryUserRequest, 
'query_user_requests': clientFramework.makeQueryUserRequestsRequest, 'query_user_extended': clientFramework.makeExtendedQueryUserRequest, 
'query_buy_sell': clientFramework.makeQueryBuySellRequest, 'query_market': clientFramework.makeQueryMarketRequest, 
'query_all_market': clientFramework.makeQueryAllMarketRequest, 'cancel_buy_sell': clientFramework.makeCancelBuySellRequest, 
'cancel_all_buy_sell': clientFramework.cancelAllBuySells}[sys.argv[1]](**vars(args))