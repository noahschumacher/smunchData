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

### Returning prediction for company in array with cID, rID, prediciton
def myCustomCalculation(cID, rID, cOR, y, m, d):
	dat = dt.datetime(year = y, month = m, day = d)
	print("\nCOMPANY:", cID, "RESTAURANT:", rID, "Delivery Date:", dat, '\n========================================================')
	PREDICTION = prediction.main(cID, rID, cOR, dat)
	return {'cID':cID, 'rID': rID, 'prediction': PREDICTION}


### Returning unique restraunt dictionary with val = 0
def get_unique_restraunts(params):
	rest_ids = {}
	for param in params:
		if param['rID'] not in rest_ids:
			rest_ids[param['rID']] = 0
	return rest_ids
	
	
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

#Create custom HTTPRequestHandler class
class KodeFunHTTPRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		start = dt.datetime.now()
		self.send_response(200)
		self.send_header('Content-type','text-html')
		self.end_headers()
		
		if self.path == "/favicon.ico":
			return

		####################################################################################
		#http://127.0.0.1?cID=1&rID=1&cOR=1&year=1&mon=1&day=1&cID=2&rID=2&cOR=2&year=2&mon=2&day=2&cID=3&rID=3&cOR=3&year=3&mon=3&day=3
		params = []
		company_params = {}
		count = 1
		for param in str(self.path).replace('/', '').replace('?','').split('&'):
			company_params[param.split('=')[0]] = int(param.split('=')[1])
			if count % 6 == 0:
				params.append(company_params.copy())
			count += 1

		rID_total_orders = get_unique_restraunts(params)
		print("\n==============  INITIALIZING PREDICTIONS  ================")

		total_per_company = []

		
		for i in params:
			total_per_company.append(myCustomCalculation(
				i['cID'], 
				i['rID'], 
				i['cOR'],
				i['year'],
				i['mon'],
				i['day']))
		end = dt.datetime.now()

		print("==============   PREDICTIONS COMPLETED   =================\n")
		print("\nRUN TIME:", end-start, "\n-------------------------------------------")


		for i in total_per_company:
			print("result:", i)
			rID_total_orders[i['rID']] += i['prediction']
		print("\nRestaurant Aggregated:", rID_total_orders, "\n")

		self.wfile.write(
			bytes((rID_total_orders), "utf-8"))

		####################################################################################



		##################################################################
		'''params = {}
		#example of query: 
		#http://127.0.0.1?cID=22&rID=23&cOR=12&year=2017&mon=8&day=16
		for param in str(self.path).replace('/', '').replace('?','').split('&'):
			params[param.split('=')[0]] = int(param.split('=')[1])
		print("\nPassed in Params:")
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
		return'''
		########################################################################

  
def run():
	print('http server is starting...')
	server_address = ('', 8080)
	httpd = HTTPServer(server_address, KodeFunHTTPRequestHandler)
	print('http server is running...')
	httpd.serve_forever()
  
if __name__ == '__main__':
	run()

'''
cID=117&rID=3&cOR=14&year=2017&mon=8&day=23&
cID=248&rID=1&cOR=32&year=2017&mon=8&day=23&
cID=288&rID=3&cOR=12&year=2017&mon=8&day=23&
cID=90&rID=1&cOR=13&year=2017&mon=8&day=23&
cID=263&rID=3&cOR=13&year=2017&mon=8&day=23&
cID=132&rID=1&cOR=13&year=2017&mon=8&day=23&
cID=9&rID=1&cOR=13&year=2017&mon=8&day=23&
cID=194&rID=3&cOR=13&year=2017&mon=8&day=23&
cID=85&rID=1&cOR=13&year=2017&mon=8&day=23&

cID=117&rID=3&cOR=14&year=2017&mon=8&day=23&cID=248&rID=1&cOR=8&year=2017&mon=8&day=23&cID=288&rID=3&cOR=3&year=2017&mon=8&day=23&cID=90&rID=1&cOR=8&year=2017&mon=8&day=23&cID=263&rID=3&cOR=6&year=2017&mon=8&day=23&cID=132&rID=1&cOR=4&year=2017&mon=8&day=23&cID=9&rID=1&cOR=14&year=2017&mon=8&day=23&cID=194&rID=3&cOR=12&year=2017&mon=8&day=23&cID=85&rID=1&cOR=16&year=2017&mon=8&day=23

'''

