# Noah M. Schumacher
# First attempt at grabbing data from Smunch DB using sql in python

import psycopg2

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

#def get_order_history_for_company(cursor):

#def get_order_history_for_restaurant(cursor):

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

	print("\nHere are the companies:")
	get_unique_companies_as_sorted_list(cursor)

	print("\nHere are the restaurants:")
	get_unique_restaurants_as_sorted_list(cursor)



main()