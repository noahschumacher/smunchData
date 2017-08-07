# Noah M. Schumacher
# Gets average time a company has placed 75%, 90%, 95% of its orders
# Writes to CSV file at end of get_company_order_percent_times()

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib
import presentingTime

#####################################################################################
#############	  			CONNECT TO SMUNCH DB   						#############
#####################################################################################
def get_connection():
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

def get_unique_companies_ordered_inP_2M(cursor):
	inP_2M_companies = sql_Query(cursor, "Series", "SELECT DISTINCT closings.company_id FROM closings INNER JOIN companies ON closings.company_id = companies.id WHERE (closings.delivered_at > CURRENT_DATE - interval '60 days')")
	inP_2M_companies = inP_2M_companies.sort_values()
	return inP_2M_companies

def get_company_delivery_dates(cursor, company_id):
	deliverys_dates = sql_Query(cursor, "Series", "SELECT DISTINCT delivered_at FROM closings WHERE company_id = %d" %company_id)
	deliverys_dates = deliverys_dates.sort_values()
	return deliverys_dates

def get_order_times_and_count(cursor, company_id, delivered_at):
	order_times_count_df = sql_Query(cursor, "DataFrame", "SELECT closings.dish_count, closings.delivered_at, choices.updated_at FROM closings INNER JOIN choices ON closings.choice_id = choices.id WHERE choices.menue_dish_id IS NOT null AND closings.company_id = %d AND closings.delivered_at = '%s'" %(company_id, delivered_at))
	return order_times_count_df


#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################
def get_company_order_percent_times(cursor):
	#### List declarations
	avg_time_dif_95 = []
	avg_time_dif_90 = []
	avg_time_dif_75 = []
	ran_through_companies = []

	#### Get companies that have ordered in past 2Months
	companies = get_unique_companies_ordered_inP_2M(cursor)			### SQL Query
	print("\nHere are the companies:\n",companies)

	#### Cycling through these companies
	count = 0
	for company_id in companies:
		count += 1
		#if count > 12:
		#	break
		print("\nHere is the NEW company_id:", company_id[0])

		#### Getting the dates this company had a scheduled delivery
		delivery_dates = get_company_delivery_dates(cursor, company_id[0]) 		### SQL Query

		#input("new company?")

		company_times_95 = []	#### List of time deltas for company
		company_times_90 = []
		company_times_75 = []

		#### Cycling through delivery dates
		for delivered_at in delivery_dates:
			print("\nCompany ID: ", company_id[0]," | Delivery Date:", delivered_at[0])

			daily_company_orders = get_order_times_and_count(cursor, company_id[0], delivered_at[0])	### SQL query

			### Checking if no orders placed
			if daily_company_orders.empty == True:
				print("Empty DF: didnt order on this day")
			else:
				daily_company_orders = DataFrame(daily_company_orders.values, columns = ['dish_count', 'delivered_at', 'updated_at'])
				daily_company_orders = daily_company_orders.sort_values('updated_at')
				print(daily_company_orders)
				company_times_95.append(order_time_percentage(daily_company_orders, .95))	### Finds where 95% timestamp is
				company_times_90.append(order_time_percentage(daily_company_orders, .90))	### Finds where 90% timestamp is
				company_times_75.append(order_time_percentage(daily_company_orders, .75))	### Finds where 75% timestamp is

		print(company_times_95)
		print(company_times_90)
		print(company_times_75)
		#### Finding avg time before cutoff time % of orders were placed
		avg_time_dif_95.append(avg_time_deltas(company_times_95))
		avg_time_dif_90.append(avg_time_deltas(company_times_90))
		avg_time_dif_75.append(avg_time_deltas(company_times_75))
		ran_through_companies.append(company_id[0])


	company_time_delta_DF = DataFrame()
	company_time_delta_DF["company_id"] = ran_through_companies
	company_time_delta_DF["avg_time_dif_95"] = avg_time_dif_95
	company_time_delta_DF["avg_time_dif_90"] = avg_time_dif_90
	company_time_delta_DF["avg_time_dif_75"] = avg_time_dif_75

	print("1111111", company_time_delta_DF)

	company_time_delta_DF = clean_up(company_time_delta_DF, cursor)
	

	print("RESULT")
	print(company_time_delta_DF)

	company_time_delta_DF.to_csv("order_placed_percentage_times.csv", sep = ",", index = False)
	return company_time_delta_DF


def order_time_percentage(daily_company_orders, percent):

	length 		= daily_company_orders.shape[0]
	total 		= daily_company_orders['dish_count'].sum()
	val 		= percent * total

	print("total:", total, "| val:", val)

	for i in range(length-1, -1, -1):
		total -= daily_company_orders.iloc[i, 0]

		if total <= val:
			delivery_date = datetime.datetime.combine(daily_company_orders.iloc[0,1].date(), datetime.time(9, 30))
			order_time = daily_company_orders.iloc[i, 2]

			tdelt = delivery_date - order_time

			return tdelt

def avg_time_deltas(times):
	if len(times) == 0:
		print("len == 0?")
		return 0
	avg = sum(times, datetime.timedelta(0)) / len(times)
	print("Avg:", avg)

	return avg

def clean_up(df, cursor):
	df = df[df.avg_time_dif_95 != 0]
	df = df.reset_index(drop=True)

	print("222222", df)

	company_names = []

	names = sql_Query(cursor, "data frame", "SELECT DISTINCT name, id FROM companies")
	names = DataFrame(names.values, columns = ['name', 'id'])
	names = names.sort_values('id')
	for i in df["company_id"]:
		if i in names['id']:
			index = names[names['id'] == i].index[0]
			company_names.append(names.ix[index, 'name'])
		else:
			company_names.append("no name?")
	print("len company names", len(company_names))
	df['names'] = company_names
	return df

#####################################################################################
#############  				   		MAIN 		 						#############
#####################################################################################
def main():
	cursor = get_connection()
	timeDF = get_company_order_percent_times(cursor)


main()