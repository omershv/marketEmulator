import os
try:
	os.chdir("C:\marketEmulator")
except:
	None

from SocketServer import ThreadingMixIn
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer

import SocketServer
import json
import MarketRequest
import MarketState
import MarketTrader
import threading
import time
import traceback
import sys
import copy
import numpy as np

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
	pass

class S(SimpleHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		holdings = sorted(MarketState.userHoldings.items(), key = lambda (k,v):int(k.split("user")[1]))
		history = map(lambda k:str((k, MarketState.marketHistory[k][-10:])), MarketState.commodities.keys())
		leading = map(lambda (a,b):a + " - " + str(b["funds"]), list(reversed(sorted(holdings[:80], key=lambda (k,v): v["funds"])))[:5])
		
		history2 = map(lambda k:((k, MarketState.marketHistory[k][-10:])), MarketState.commodities.keys())
		accumHoldings = dict(copy.deepcopy(holdings))
		for q in MarketState.activeQueries:
			if q.type == "buy":
				accumHoldings[q.user]["funds"]+=q.amount * q.price
			else:
				accumHoldings[q.user]["commodities"][q.commodity] += q.amount
		history2 = map(lambda i:(i,[(0,1,2)]),range(10))
		commodityWorth = dict(map(lambda (k,h):(k,np.mean(map(lambda o:o[1],h[-100:]))),history2))
		for user in accumHoldings.keys():
			for commodity, amount in accumHoldings[user]["commodities"].items():
				accumHoldings[user]["funds"] += amount * commodityWorth[commodity]
		accumHoldings = sorted(accumHoldings.items(), key=lambda (k,v):int(k.split("user")[1]))
		realLeading = map(lambda (a,b):a + " - " + str(b["funds"]), list(reversed(sorted(accumHoldings[:80], key=lambda (k,v): v["funds"])))[:5])
		
		self.wfile.write("<html><body>");
		self.wfile.write("<h1> Real Leaders </h1> <h3>%s</h3>"%str("<br>".join(realLeading)))
		self.wfile.write("<h1> Leaders </h1> <h3>%s</h3>"%str("<br>".join(leading)))
		self.wfile.write("<h1> History </h1> <h3>%s</h3>"%str("<br>".join(history)))
		self.wfile.write("<h1> Holdings </h1> %s"%str("<br>".join(map(lambda (k,v):k + " - " + str(v),holdings))))
		self.wfile.write("</body></html>");

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
		data = None
		resp = ""
		
		try:
			self._set_headers()
			self.data_string = self.rfile.read(int(self.headers['Content-Length']))
			data = json.loads(self.data_string)
		except Exception as e: 
			print traceback.print_exc()
			resp = str(e)
		
		MarketState.semaphore.acquire()
		if data is not None:
			try:			
				req = MarketRequest.MarketRequest()
				resp = req.loadFromJson(data)
			except Exception as e: 
				print traceback.print_exc()
				resp = str(e)
		
		MarketState.semaphore.release()
		#print "response = %s"%(resp)
		try:
			self.wfile.write(str(resp))
		except Exception as e: 
			print traceback.print_exc()
		
def run(server_class=HTTPServer, handler_class=S, port=80):
	global httpd
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd...'
	threading.Thread(target=httpd.serve_forever).start()
	
	while True:
		time.sleep(10)
		MarketState.semaphore.acquire()
		
		try:
			MarketTrader.performTrades()
			MarketState.saveData()
		except Exception as e: 
			print traceback.print_exc()
		
		if os.path.exists("shutdown"):
			os.unlink("shutdown")
			print 'Shutting down...'
			threading.Thread(target=httpd.shutdown).start()
			MarketState.semaphore.release()
			time.sleep(5)
			break
		MarketState.semaphore.release()

if __name__ == "__main__":
	from sys import argv

	if len(argv) > 0 and argv[-1] == "reset":
		MarketState.resetStatus()
		MarketState.saveData()
	elif len(argv) == 2:
		run(server_class=ThreadingSimpleServer, port=int(argv[1]))
	else:
		run(server_class=ThreadingSimpleServer)
	