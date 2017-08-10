# Noah M. Schumacher
# Order times table for specific company (subset of sqlPredictions)

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime as dt
import presentingTime

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

def get_delivery_dates_on_DofW(cursor, company_id, DofW):
	delivery_dates = sql_Query(cursor, "Series", "SELECT DISTINCT delivered_at FROM closings WHERE company_id = %d" %company_id)
	delivery_dates.sort_values()
	return delivery_dates

def get_order_times_and_count(cursor, company_id, delivered_at):
	order_times_count_df = sql_Query(cursor, "DataFrame", "SELECT closings.dish_count, closings.delivered_at, choices.updated_at FROM closings INNER JOIN choices ON closings.choice_id = choices.id WHERE choices.menue_dish_id IS NOT null AND closings.company_id = %d AND closings.delivered_at = '%s'" %(company_id, delivered_at))
	return order_times_count_df

#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################
#### Used to grab first value in sql tuple list
def fixSeries(ss):
	newSS = []
	for i in ss:
		newSS.append(i[0])
	return newSS

#### Given company cycles through Monday-Friday and finds avg, std, and plots time 
#### from closing for x% or orders to be placed.
def createTable(company_id, DofW):
	cursor =  get_connections()

	print("Day Of Week:", DofW)

	company_times_95 = []	#### List of time deltas for company
	company_times_90 = []
	company_times_75 = []

	delivery_dates = fixSeries(get_delivery_dates_on_DofW(cursor, company_id, DofW))

	#### filters out dates that arent specified DofW
	delivery_dates = list(filter(lambda a: a.weekday() == DofW, delivery_dates))

	####
	for delivery_date in delivery_dates:
		daily_company_orders = get_order_times_and_count(cursor, company_id, delivery_date)
	
		### Checking if no orders placed
		if daily_company_orders.empty == True:
			print("Empty DF: didnt order for this day")
		else:
			daily_company_orders = DataFrame(daily_company_orders.values, columns = ['dish_count', 'delivered_at', 'updated_at'])
			daily_company_orders = daily_company_orders.sort_values('updated_at')
			company_times_95.append(order_time_percentage(daily_company_orders, .95))	### Finds where 95% timestamp is
			company_times_90.append(order_time_percentage(daily_company_orders, .90))	### Finds where 90% timestamp is
			company_times_75.append(order_time_percentage(daily_company_orders, .75))	### Finds where 75% timestamp is

	company_time_delta_DF = DataFrame()
	company_time_delta_DF["avg_time_dif_95"] = company_times_95
	company_time_delta_DF["avg_time_dif_90"] = company_times_90
	company_time_delta_DF["avg_time_dif_75"] = company_times_75


	### Returns Dict with mean, std for three percentages in dictionary format
	info = presentingTime.presentation(company_time_delta_DF)
	return info


#### Finds at what time x% of orders were placed, returns as timeDelt from closing.
def order_time_percentage(daily_company_orders, percent):
	length 	= daily_company_orders.shape[0]
	total 	= daily_company_orders['dish_count'].sum()
	val 	= percent * total

	#print("total:", total, "| val:", val)

	for i in range(length-1, -1, -1):
		total -= daily_company_orders.iloc[i, 0]
		if total <= val:
			delivery_date = dt.datetime.combine(daily_company_orders.iloc[0,1].date(), dt.time(10, 30))
			order_time = daily_company_orders.iloc[i, 2]

			tdelt = delivery_date - order_time
			return tdelt


#company_id = 117
#createTable(company_id)

