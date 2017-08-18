# Noah M. Schumacher, Aug 18, 2017
# Gets the avg daily orders
# 

#####################################################################################
#############	  					NOTES		  						#############
#####################################################################################
''' Currently this file is a single run file so I did write it with the intention
of making a it a minimal memory, cpu load file. In the future if this is delpoyed on
the website it should be modified with smarter logic as to mitigate the extensive
quarries and looping done to complete. '''

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime as dt


#####################################################################################
#############	  			CONNECT TO SMUNCH DB   						#############
#####################################################################################
def get_connections():
	try:
		connection = psycopg2.connect(
			"dbname='smunch_development_pricing' user='nschumacher' host='localhost' password='12' port='5432'")
		connection.autocommit = True
		cursor = connection.cursor()
	except:
		print("Did not connect to database")
	return cursor


#####################################################################################
#############	  				SQL QUERIES  							#############
#####################################################################################
#### General format for sql query and dataForm
def sql_Query(cursor, dataForm, query):
	if dataForm == "Series":
		get_command = query
		cursor.execute(get_command)
		data = Series(cursor.fetchall())
		return data
	else:
		get_command = query
		cursor.execute(get_command)
		data = DataFrame(cursor.fetchall())
		return data



#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################