import os
os.chdir("C:\marketEmulator")

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import MarketRequest
import MarketState
import MarketTrader
import threading
import time

semaphore =  threading.Semaphore()

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()
		self.wfile.write("<html><body><h1>get</h1></body></html>")

	def do_HEAD(self):
		self._set_headers()
		
	def do_POST(self):
		semaphore.acquire()
		self._set_headers()
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		data = json.loads(self.data_string)
		req = MarketRequest.MarketRequest()
		resp = req.loadFromJson(data)
		self.wfile.write(str(resp))
		semaphore.release()
		
def run(server_class=HTTPServer, handler_class=S, port=80):
	global httpd
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd...'
	threading.Thread(target=httpd.serve_forever).start()
	
	while True:
		time.sleep(10)
		semaphore.acquire()
		
		MarketTrader.performTrades()
		MarketState.saveData()
		
		if os.path.exists("shutdown"):
			os.unlink("shutdown")
			print 'Shutting down...'
			threading.Thread(target=httpd.shutdown).start()
			semaphore.release()
			time.sleep(5)
			break
		semaphore.release()

if __name__ == "__main__":
	from sys import argv

	if len(argv) > 0 and argv[-1] == "reset":
		MarketState.resetStatus()
		MarketState.saveData()
	elif len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()
	