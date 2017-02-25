from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import MarketRequest
import MarketState

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
		# Doesn't do anything with posted data
		self._set_headers()
		self.data_string = self.rfile.read(int(self.headers['Content-Length']))
		data = json.loads(self.data_string)
		req = MarketRequest.MarketRequest()
		resp = req.loadFromJson(data)
		if resp != True:
			self.wfile.write(str(resp))
		else:
			self.wfile.write(str(req.id))
		
def run(server_class=HTTPServer, handler_class=S, port=80):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd...'
	httpd.serve_forever()

if __name__ == "__main__":
	from sys import argv

	if len(argv) == 2:
		run(port=int(argv[1]))
	else:
		run()