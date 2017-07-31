# Noah M. Schumacher
# First attempt at grabbing data from Smunch DB using sql in python

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

def get_connection():
	try:
		connection = psycopg2.connect(
			"dbname='smunch_development_pricing' user='nschumacher' host='localhost' password='12' port='5432'")
		connection.autocommit = True
		cursor = connection.cursor()
	except:
		print("Did not connect to database")
	return cursor

def get_unique_companies_as_sorted_list(cursor):
	get_command = "SELECT DISTINCT name FROM companies"
	cursor.execute(get_command)
	companies = cursor.fetchall()
	companies = convert_to_array(companies)
	sort_list_of_strings(companies)
	print(companies)

def get_unique_restaurants_as_sorted_list(cursor):
	get_command = "SELECT DISTINCT name FROM restaurants"
	cursor.execute(get_command)
	restaurants = cursor.fetchall()
	restaurants = convert_to_array(restaurants)
	sort_list_of_strings(restaurants)
	print(restaurants)

def get_unique_companies_ordered_inP_2M(cursor):
	get_command = "SELECT DISTINCT companies.name, closings.company_id FROM closings INNER JOIN companies ON closings.company_id = companies.id WHERE (closings.delivered_at > CURRENT_DATE - interval '60 days')"
	cursor.execute(get_command)
	inP_2M_companies = DataFrame(cursor.fetchall(), columns = ["name", "company_id"])
	inP_2M_companies = inP_2M_companies.sort_values(["company_id"])
	print(inP_2M_companies)
	return inP_2M_companies

def get_order_history_for_company(cursor, company_id):
	get_command = "SELECT dish_count, transaction_type, company_id, daily_restaurant_id, delivered_at FROM closings WHERE company_id = %d" %company_id
	cursor.execute(get_command)
	company_order_history = DataFrame(cursor.fetchall(), columns = ['dish_count', 'order_type', 'company_id', 'restaurant_id', 'delivered_at'])
	print("Here is a companies order history\n", company_order_history)



def convert_to_array(oneD_data):
	ll = []
	for item in oneD_data:
		for first_item in item:
			ll.append(first_item)
	return ll

def sort_list_of_strings(data):
	data = data.sort()
	return data




def main():
	cursor = get_connection()

	#print("\nHere are all the companies:")
	#get_unique_companies_as_sorted_list(cursor)

	#print("\nHere are all the restaurants:")
	#get_unique_restaurants_as_sorted_list(cursor)

	print("\nHere are companies ordered in past 2 months:")
	companies_ordered_inP_2M_DF = get_unique_companies_ordered_inP_2M(cursor)

	day_of_week = input("Enter the day of the week you want to look at [mon, tue, wed, thu, fri]:")
	restaurant = input("Enter the restraunt you want to look at:")

	print("\ncompanies order history:")
	get_order_history_for_company(cursor, 163)



main()