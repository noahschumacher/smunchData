# Noah M. Schumacher
# First attempt at grabbing data from Smunch DB using sql in python

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

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
def get_company_order_hisotry_on_day(cursor, daily_company_id):
	get_command = "SELECT dish_count, transaction_type, company_id, updated_at FROM closings WHERE daily_company_id = %d" %daily_company_id
	cursor.execute(get_command)
	company_order_history_df = DataFrame(cursor.fetchall(), columns = ['dish_count', 'order_type', 'company_id', 'updated_at'])
	company_order_history_df = company_order_history_df.sort_values(["updated_at"])
	return company_order_history_df	


#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################
def order_time_percentage(daily_company_orders):
	total = daily_company_orders['dish_count'].sum()
	print("total:", total)
	
	orderArray = []
	count = 0
	for i in daily_company_orders['dish_count']:
		orderArray.append(i)
		if count > 0:
			orderArray[count] = (orderArray[count-1] + i)
		print(orderArray)
		
		if .75 > (orderArray[count] / total) >= .50:
			print("Hit 50% of order at", daily_company_orders.iloc[count, 3])

		if .90 > (orderArray[count] / total) >= .75:
			print("Hit 75% of order at", daily_company_orders.iloc[count, 3])
			
		if (orderArray[count] / total) >= .90:
			print("Hit 90% of order at", daily_company_orders.iloc[count, 3])

		count += 1




#####################################################################################
#############  				   		MAIN 		 						#############
#####################################################################################
def main():
	cursor = get_connection()

	company = 4581

	print("Getting specific company complete order history...\n")
	company_order_history = get_company_order_hisotry_on_day(cursor, company)
	print(company_order_history, '\n')

	#orderPercentageTimes = DataFrame(,columns = [50, 75, 90])
	order_time_percentage(company_order_history)




main()