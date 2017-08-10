# Noah M. Schumacher, Aug 10, 2017
# File creating a retention table from the smunch DB

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
		data = fixSeries(Series(cursor.fetchall()))
		return data
	else:
		get_command = query
		cursor.execute(get_command)
		data = DataFrame(cursor.fetchall())
		return data

def get_user_ids(cursor):
	user_ids = sql_Query(cursor, "Series", "SELECT DISTINCT user_id FROM choices WHERE menue_dish_id NOTNULL AND menue_Dish_id != 0")
	return user_ids

def get_user_order_history(cursor, user_id):
	user_order_history = sql_Query(cursor, "Series", "SELECT updated_at FROM choices WHERE user_id = %s AND menue_dish_id NOTNULL AND menue_dish_id != 0" %(user_id))
	return user_order_history

#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################
def retention(cursor):

	cols = ['2016-5','2016-6','2016-7','2016-8','2016-9','2016-10','2016-11','2016-12',
	'2017-1','2017-2','2017-3','2017-4','2017-5','2017-6','2017-7','2017-8']

	retentionDF = DataFrame(0, index = cols, columns = cols)
	print("Here is the initial retention DataFrame\n")
	print(retentionDF)

	user_ids = get_user_ids(cursor)

	### Cycling through all active users
	for id in user_ids:
		user_order_history = get_user_order_history(cursor, id)

		### Getting first order to set cohort
		first_order = min(user_order_history)
		year = first_order.year
		month = first_order.month
		year_month = str(year)+'-'+str(month)

		retentionDF.ix[year_month, str(2016)+'-'+str(5)] += ordered_in(user_order_history, 2016, 5)
		retentionDF.ix[year_month, str(2016)+'-'+str(6)] += ordered_in(user_order_history, 2016, 6)
		retentionDF.ix[year_month, str(2016)+'-'+str(7)] += ordered_in(user_order_history, 2016, 7)
		retentionDF.ix[year_month, str(2016)+'-'+str(8)] += ordered_in(user_order_history, 2016, 8)
		retentionDF.ix[year_month, str(2016)+'-'+str(9)] += ordered_in(user_order_history, 2016, 9)
		retentionDF.ix[year_month, str(2016)+'-'+str(10)] += ordered_in(user_order_history, 2016, 10)
		retentionDF.ix[year_month, str(2016)+'-'+str(11)] += ordered_in(user_order_history, 2016, 11)
		retentionDF.ix[year_month, str(2016)+'-'+str(12)] += ordered_in(user_order_history, 2016, 12)
		retentionDF.ix[year_month, str(2017)+'-'+str(1)] += ordered_in(user_order_history, 2017, 1)
		retentionDF.ix[year_month, str(2017)+'-'+str(2)] += ordered_in(user_order_history, 2017, 2)
		retentionDF.ix[year_month, str(2017)+'-'+str(3)] += ordered_in(user_order_history, 2017, 3)
		retentionDF.ix[year_month, str(2017)+'-'+str(4)] += ordered_in(user_order_history, 2017, 4)
		retentionDF.ix[year_month, str(2017)+'-'+str(5)] += ordered_in(user_order_history, 2017, 5)
		retentionDF.ix[year_month, str(2017)+'-'+str(6)] += ordered_in(user_order_history, 2017, 6)
		retentionDF.ix[year_month, str(2017)+'-'+str(7)] += ordered_in(user_order_history, 2017, 7)
		retentionDF.ix[year_month, str(2017)+'-'+str(8)] += ordered_in(user_order_history, 2017, 8)

	print(retentionDF)
	retentionDF.to_csv("retentionDF.csv",sep = ',')
	return retentionDF

def ordered_in(user_order_history, year, month):
	for updated_at in user_order_history:
		yr = updated_at.year
		mon = updated_at.month
		if yr == year and mon == month:
			return 1
	return 0


def fixSeries(ss):
	newSS = []
	for i in ss:
		newSS.append(i[0])
	return newSS


def main():
	cursor = get_connections()

	retentionDF = retention(cursor)

main()

