# Noah M. Schumacher
# Calculates the predicted orders for a company bases on DayOfWeek and assigned Restaurant

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import timePrediction
import datetime as dt


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
		return [orders_on_param_list[0], 1]
	elif len(orders_on_param_list) == 2:
		return [sum(orders_on_param_list)/2, 2]

	prediction = predict_orders_vs_param(orders_on_param_list)
	return [prediction, 3]


#### Takes list of orders and creates finds linear regression equation then predicts
def predict_orders_vs_param(orders):

	x = list(range(len(orders)))
	#print(x)
	#print(orders)

	z = np.polyfit(x, orders, 1)
	print("y =",z[0],"x + ", z[1])

	m=z[0]
	b=z[1]

	prediction = round(m*len(orders) + b)
	print("Predicted Orders:", prediction,"\n")

	return prediction

#### The x% of orders time prediction, weighting
def x_percent_orders(company_id, DofW, currentOrders, delivery_date):
	### info = [[.95, mu_95, std_95], [.90, mu_90, std_90]...]
	info = timePrediction.createTable(company_id, DofW)

	time_to_closure = time_From_closure(delivery_date)

	timeDif = []
	for i in range(3):
		timeDif.append(round(abs(time_to_closure - info[i][1]), 2))

	print("\ntimeDif:", timeDif)

	min_index = timeDif.index(min(timeDif))
	print("\nMin Index:", min_index)

	timeDif = []
	for i in range(3):
		timeDif.append(round(time_to_closure - info[i][1], 2))

	time_prediction = currentOrders / info[min_index][0]
	print("time Prediction: ", time_prediction)

	w_away = 9-(2**(min_index+1))
	wT_avg = 4
	wT_std = 8

	w_T = abs(w_away / ((timeDif[min_index] * (1/wT_avg)) + info[min_index][2] * (1/wT_std)))
	print("\nw_T =", w_away, "/ ((", timeDif[min_index], "* (1/", wT_avg, ")) +", info[min_index][2],"* (1/", wT_std,")) =", w_T)
	#print("time weighting:", w_T)

	return [time_prediction, w_T]

def time_From_closure(delivery_date):

	### Method allows for prediction from any day but needs 'delivery_date' as string passed in
	current_dateTime = dt.datetime.now()
	print("\nCurrent Time:", current_dateTime)
	time_to_closure = dt.datetime.combine(delivery_date.date(), dt.time(9,50)) - current_dateTime
	days, seconds = time_to_closure.days, time_to_closure.seconds
	hours = (days * 24) + round((seconds / 3600), 3)
	if hours <= 0:
		print("IN PAST!!")
		return 1000000
	print("\nTime From Closure:", hours)
	return hours
	

#### Attempts to weight the parameter predictions.
def weighting(pred_DofW, pred_Rest, time_pred_weight):
	pred_DofW_valid = pred_DofW[1] == 3
	pred_Rest_valid = pred_Rest[1] == 3
	print("DoW Valid?:", pred_DofW_valid, " | Rest Valid?:", pred_Rest_valid,)

	w_T = time_pred_weight[1]
	w_D = 1
	w_R = 1

	if pred_DofW_valid and pred_Rest_valid:
		weighted_prediction = (pred_DofW[0]*w_D + pred_Rest[0]*w_R + time_pred_weight[0]*w_T)/(w_D+w_R+w_T)
	elif pred_DofW_valid:
		weighted_prediction = ((pred_DofW[0]*w_D)+(time_pred_weight[0]*w_T))/(w_D+w_T)
	elif pred_Rest_valid:
		weighted_prediction = ((pred_Rest[0]*w_R)+(time_pred_weight[0]*w_T))/(w_R+w_T)
	else:
		weighted_prediction = time_pred_weight[0]

	return weighted_prediction

#####################################################################################
#############  				   		MAIN 		 						#############
#####################################################################################
def main(company_id, restaurant_id, current_Orders, delivery_date):
	cursor = get_connection()
	DoW = delivery_date.weekday()

	print("Getting specific company specific Day of Week order history...\n")
	company_order_hisotry_DoW = get_company_orderHistory_on_specific_day(cursor, company_id, DoW+1)
	print("PREDICTING from DAYOFWEEK...\n")
	predicted_orders_for_DoW = orders_on_param_from_company(company_order_hisotry_DoW)
	if predicted_orders_for_DoW[0] == 0:
		print("NEVER ORDERED ON THIS DOW")
		return 0
	elif predicted_orders_for_DoW[0] <= current_Orders - (current_Orders*.15):
		predicted_orders_for_DoW[1] = False

	print("Getting specific company specific restaurant order history...\n")
	company_order_history_Restaurant = get_company_orderHistory_from_restaurant(cursor, company_id, restaurant_id)
	print("PREDICTING from RESTAURANT...\n")
	predicted_orders_for_Restaurant = orders_on_param_from_company(company_order_history_Restaurant)
	print()
	if predicted_orders_for_Restaurant[0] <= current_Orders + (current_Orders*.15):
		predicted_orders_for_Restaurant[1] = False

	print("Getting % Time Weighting...")
	time_pred_weight = x_percent_orders(company_id, DoW, current_Orders, delivery_date)

	print("Weighting...\n")
	PREDICTION = weighting(predicted_orders_for_DoW, predicted_orders_for_Restaurant, time_pred_weight)
	return PREDICTION