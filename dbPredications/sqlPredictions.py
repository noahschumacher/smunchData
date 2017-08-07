# Noah M. Schumacher
# Calculates the predicted orders for a company bases on DayOfWeek and assigned Restaurant

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np


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
def get_unique_companies_as_series(cursor):
	get_command = "SELECT DISTINCT name FROM companies"
	cursor.execute(get_command)
	companies = Series(cursor.fetchall())
	return companies

def get_unique_restaurants_as_DF_if_active(cursor):
	get_command = "SELECT DISTINCT name, id FROM restaurants WHERE fsm_state = 'active'"
	cursor.execute(get_command)
	all_restaurants_df = DataFrame(cursor.fetchall(), columns = ['name', 'id'])
	all_restaurants_df = all_restaurants_df.sort_values(['name'])
	return all_restaurants_df

def get_unique_companies_ordered_inP_2M(cursor):
	get_command = "SELECT DISTINCT companies.name, closings.company_id FROM closings INNER JOIN companies ON closings.company_id = companies.id WHERE (closings.delivered_at > CURRENT_DATE - interval '60 days')"
	cursor.execute(get_command)
	inP_2M_companies_df = DataFrame(cursor.fetchall(), columns = ["name", "company_id"])
	inP_2M_companies_df = inP_2M_companies_df.sort_values(["company_id"])
	return inP_2M_companies_df

def get_company_order_history(cursor, company_id):
	get_command = "SELECT dish_count, transaction_type, company_id, daily_restaurant_id, delivered_at FROM closings WHERE company_id = %d" %company_id
	cursor.execute(get_command)
	company_order_history_df = DataFrame(cursor.fetchall(), columns = ['dish_count', 'order_type', 'company_id', 'restaurant_id', 'delivered_at'])
	return company_order_history_df

def get_company_orderHistory_on_specific_day(cursor, company_id, DoW):
	get_command = "SELECT dish_count, delivered_at FROM closings WHERE extract(dow from  delivered_at) = %d AND company_id = %d" %(DoW, company_id)
	cursor.execute(get_command)
	company_orders_DoW_df = DataFrame(cursor.fetchall(), columns = ['dish_count', 'delivered_at'])
	return company_orders_DoW_df

def get_company_orderHistory_from_restaurant(cursor, company_id, restaurant_id):
	get_command = "SELECT dish_count, delivered_at FROM closings WHERE company_id = %d AND restaurant_id = %d" %(company_id, restaurant_id)
	cursor.execute(get_command)
	company_orders_Restaurant_df = DataFrame(cursor.fetchall(), columns = ['dish_count', 'delivered_at'])
	return company_orders_Restaurant_df


#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################

##### Aggregating the total orders on specific Date or Restaurant
def orders_on_param_from_company(df):
	length = df.shape[0]
	orders_on_param_list = []
	orders_on_param = 0

	for i in range(length):
		#### Handling last data point
		if i == length-1:
			if df.iloc[i, 1] == df.iloc[i-1, 1]:
				orders_on_param_list.append(orders_on_param + df['dish_count'][i])
				break
			else:
				orders_on_param_list.append(df['dish_count'][i])
				break
		#### Checking if delivery date matches next delivery date and if so adding val to orders_on_param
		if df.iloc[i, 1] == df.iloc[i+1, 1]:
			orders_on_param += df['dish_count'][i]
		else:
			orders_on_param += df['dish_count'][i]
			orders_on_param_list.append(orders_on_param)
			orders_on_param = 0

	# NOT ENOUGH DATA // Error handling
	if len(orders_on_param_list) == 0:
		return [0, 0]
	elif len(orders_on_param_list) == 1:
		return [orders_on_param_list, 1]
	elif len(orders_on_param_list) == 2:
		return [sum(orders_on_param_list)/2, 2]

	prediction = predict_orders_vs_param(orders_on_param_list)
	return [prediction, 3]


#### Takes list of orders and creates finds linear regression equation then predicts
def predict_orders_vs_param(orders):

	x = list(range(len(orders)))
	print(x)
	print(orders)

	z = np.polyfit(x, orders, 1)
	print("y =",z[0],"x + ", z[1])

	m=z[0]
	b=z[1]

	prediction = round(m*len(orders) + b)
	print("Predicted Orders:", prediction,"\n")

	return prediction

#### Attempts to weight the parameter predictions.
def weighting(pred1, pred2):
	pred1_valid = pred1[1] == 3
	pred2_valid = pred2[1] == 3
	if pred1_valid and pred2_valid:
		weighted_prediction = (pred1[0] + pred2[0])/2
	elif pred1_valid:
		weighted_prediction = pred1[0]
	else:
		weighted_prediction = pred2[0]
	print("Final weighted prediction is:")
	print(weighted_prediction)


#####################################################################################
#############  				   		MAIN 		 						#############
#####################################################################################
def main():
	cursor = get_connection()

	print("Getting all the companies...\n")
	unique_companies_all = get_unique_companies_as_series(cursor)

	print("Getting all the restraunts...\n")
	unique_restraunts_all = get_unique_restaurants_as_DF_if_active(cursor)

	print("Getting all companies ordered in past 2 moths...\n")
	companies_ordered_inP_2M_DF = get_unique_companies_ordered_inP_2M(cursor)

	DoW = 1
	company = 90
	restaurant = 20

	print("Getting specific company complete order history...\n")
	company_order_history_all = get_company_order_history(cursor, company)

	print("Getting specific company specific Day of Week order history...\n")
	company_order_hisotry_DoW = get_company_orderHistory_on_specific_day(cursor, company, DoW)
	print(company_order_hisotry_DoW)

	print("Getting specific company specific restaurant order history...\n")
	company_order_history_Restaurant = get_company_orderHistory_from_restaurant(cursor, company, restaurant)

	print("Predicting...\n")
	predicted_orders_for_DoW = orders_on_param_from_company(company_order_hisotry_DoW)

	print("Predicting...\n")
	predicted_orders_for_Restaurant = orders_on_param_from_company(company_order_history_Restaurant)

	print("Weighting...\n")
	weighting(predicted_orders_for_DoW, predicted_orders_for_Restaurant)

main()