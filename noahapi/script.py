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

def myCustomCalculation(dow, cID, rID, cOR):
	start = dt.datetime.now()
	PREDICTION = prediction.main(dow, cID, rID, cOR, '2017-08-16')
	end = dt.datetime.now()
	print(PREDICTION)
	print(end-start)
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
		#http://127.0.0.1?dow=3&cID=22&rID=23&cOR=12&dD=2017-08-05
		for param in str(self.path).replace('/', '').replace('?','').split('&'):
			params[param.split('=')[0]] = int(param.split('=')[1])
		print(params)
		#You have now the variables in the format params['dow'] = 3, params['cID'] = 22, params['rID'] = 23
		
		
		#just run the function here: 
		self.wfile.write(
			myCustomCalculation(
				params['dow'], 
				params['cID'], 
				params['rID'], 
				params['cOR']) )
		return

  
def run():
	print('http server is starting...')
	server_address = ('', 8080)
	httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
	print('http server is running...')
	httpd.serve_forever()
  
if __name__ == '__main__':
	run()





