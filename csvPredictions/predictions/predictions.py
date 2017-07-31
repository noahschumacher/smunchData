# Noah M. Schumacher

sys.path.insert(0, '/Users/nschumacher/docs/smunchRoR/smunchData')
from helpers import *

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def main():

	# DataFrame to create predictions
	df = getData()

	####################   Companies to predict   #########################
	df_predictions = pd.read_clipboard()
	df_predictions.columns = ["Day", "Restaurant", "Customer"]

	print("###########  Companies to predict  ###############\n", df_predictions)

	######### columns added to df_predictions ##########
	predictions       = Series()
	dataPointsDay     = Series()
	dataPointsRest    = Series()
	trendDay          = Series()
	trendRest         = Series()

	length = df_predictions.shape[0]

	########## iteration through companies ###########
	for i in range(length):
		print("##############.  iteration: ", i, "################")


		##################   Read Info   ######################
		day = df_predictions["Day"][i].lower()
		restaurant = df_predictions["Restaurant"][i].lower()
		company = df_predictions["Customer"][i].lower()
		print("READ INFO\n",day, company, restaurant)
		# selecting company dataframe
		selectedCompanyDF = selectCompany(df, company)



		################   Orders on Weekday Info   ####################
		dayofweekDF = independentVariable(selectedCompanyDF, "Day", day)
		weekdayInfo = calulations(dayofweekDF, day, company)
		weekdayInfo[0] = bound(selectedCompanyDF, weekdayInfo[0])
		dataPointsDay = dataPointsDay.set_value(i, weekdayInfo[2])
		trendDay = trendDay.set_value(i, weekdayInfo[1])



		##############   Orders from Restaurant info   ##################
		restaurantDF = independentVariable(selectedCompanyDF, "Restaurant", restaurant)

		if restaurantDF.empty:
			predictedAvg = weekdayInfo[0]
			dataPointsRest = dataPointsRest.set_value(i, 0)

		else:
			restaurantInfo = calulations(restaurantDF, restaurant, company)
			restaurantInfo[0] = bound(selectedCompanyDF, restaurantInfo[0])

			############   Creating Prediction Series   ################
			predictedAvg = (weekdayInfo[0] + restaurantInfo[0])/2
			dataPointsRest = dataPointsRest.set_value(i, restaurantInfo[2])
			trendRest = trendRest.set_value(i, restaurantInfo[1])


		print("The predicted orders for", company.title(), "on", day.title(), "from", restaurant.title(), "is:\n", predictedAvg, "\n\n")
		predictions = predictions.set_value(i, predictedAvg)

		del dayofweekDF
		del selectedCompanyDF
		del restaurantDF


	print("Prediction Frame:")

	# Adding columns to frame
	df_predictions["Predicted Orders"] = predictions
	df_predictions["Data Points on Day"] = dataPointsDay
	df_predictions["Day trend Slope"] = trendDay
	df_predictions["Data Points on Rest"] = dataPointsRest
	df_predictions["Rest trend Slope"] = trendRest


	print(df_predictions)
	print(df_predictions["Predicted Orders"].sum())

	#sumCompany(df_predictions)

	df_predictions.to_csv('prediction.csv', sep = ',')



# plots frame
def calulations(df, param, company):

	info = [0,0,0]

	x = df.index.values
	if len(x) < 1:
		print("x less than 1")
		info[0] = 0
		return info
	#print("x array: \n", x)


	y = []
	for i in df["Paying Orders"]:
		y.append(float(i))
	#print("y array: \n", y)

	if len(y) == 1:
		print("y equals 1")
		info[0] = y[0]
		info[2] = 1
		return info
	elif len(y) == 0:
		print("y equal 0?")
		info[0] = 0
		return info

	z = np.polyfit(x, y, 1)
	print("y =",z[0],"x + ", z[1])

	m=round(z[0], 3)
	b=round(z[1], 3)

	#plotORno = input("plot? (yes?): " )
	#if plotORno == "yes":
	#	plot(x, y, m, b, param, company)

	print("Based on the previous amount of orders on", param.title(), ", the predicted number of order for next", param, "is:")
	prediction = round(m*(len(y)) + b)
	print(prediction,"\n")

	info = [prediction, m, len(x)]

	return info

def plot(x, y, m, b, param, company):

	plt.plot(x, y, 'b-', label = param.title())
	plt.plot(x, m*x + b, 'r', label = "Best Fit")
	plt.xlabel("Date")
	plt.ylabel("Orders")
	title = "Orders from "+company.title()+" on "+param.title()+" vs. Date"
	plt.title(title)
	plt.legend()
	plt.show()


def sumCompany(df):

	df = df.fillna(0)
	restaurant = np.unique(df["Restaurant"])
	print(restaurant)

	total = [0,0,0]
	for i in df.index:
		if df["Restaurant"][i] == restaurant[0]:
			total[0] = total[0] + df["Predicted Orders"][i]
		elif df["Restaurant"][i] == restaurant[1]:
			total[1] = total[1] + df["Predicted Orders"][i]
		elif df["Restaurant"][i] == restaurant[2]:
			total[2] = total[2] + df["Predicted Orders"][i]
		#elif df["Restaurant"][i] == restaurant[3]:
		#	total[3] = total[3] + df["Predicted Orders"][i]

	for i in range(len(restaurant)):
		print("Predicted orders for,", restaurant[i], "are:", total[i])


main()







