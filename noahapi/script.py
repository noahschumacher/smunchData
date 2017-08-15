#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import prediction
import datetime as dt
#from imp import reload 
#reload(sys)  
#sys.setdefaultencoding('utf8')

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""

def myCustomCalculation(cID, rID, cOR, y, m, d):
	start = dt.datetime.now()
	dat = dt.datetime(year = y, month = m, day = d)
	print(dat)
	PREDICTION = prediction.main(cID, rID, cOR, dat)
	end = dt.datetime.now()
	print("PREDICTION:", PREDICTION)
	print("RUN TIME:", end-start)
	return PREDICTION


	
#IGNORE FROM HERE -- HTTP SERVER 
	
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
print('aa')
#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text-html')
		self.end_headers()
		
		params = {}
		
		if self.path == "/favicon.ico":
			return
		
		#example of query: 
		#http://127.0.0.1?cID=22&rID=23&cOR=12&year=2017&mon=8&day=16
		for param in str(self.path).replace('/', '').replace('?','').split('&'):
			params[param.split('=')[0]] = int(param.split('=')[1])
		print(params)
		#You have now the variables in the format params['dow'] = 3, params['cID'] = 22, params['rID'] = 23
		
		
		#just run the function here: 
		self.wfile.write(
			bytes(str(myCustomCalculation(
				params['cID'], 
				params['rID'], 
				params['cOR'],
				params['year'],
				params['mon'],
				params['day'])), "utf8"))
		return

  
def run():
	print('http server is starting...')
	server_address = ('', 8080)
	httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
	print('http server is running...')
	httpd.serve_forever()
  
if __name__ == '__main__':
	run()





