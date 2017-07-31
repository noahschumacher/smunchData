# Noah M. Schumacher
import os
import sys

sys.path.insert(0, '/Users/nschumacher/docs/smunchRoR/smunchData')
from helpers import *

print(os.getcwd())
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():


	###############  Read in and select specific Companies data  #################
	df = getData()
	getUniqueCompanies(df)
	companyName = input("Enter company name: ") # Reads in company name and reduces df to only rows with company name in it
	selectedCompany = selectCompany(df, companyName)


	#####################   Orders on Weekday   ###########################
	day = input("Select day in question: ")
	dayofweek = independentVariable(selectedCompany, "Day", day)
	weekdayOrders = plotOrders_and_BestFit(dayofweek, day, companyName)


	####################   Orders from Restaurant   ########################
	restaurant = input("Select restaurant in question: ")
	dayofweek = independentVariable(selectedCompany, "Restaurant", restaurant)	
	restaurantOrders = plotOrders_and_BestFit(dayofweek, restaurant, companyName)


	del dayofweek
	del selectedCompany

	predictedAvg = (weekdayOrders + restaurantOrders)/2
	print("The predicted orders for", companyName.title(), "on", day.title(), "from", restaurant.title(), "is:\n", predictedAvg)

# plots frame
def plotOrders_and_BestFit(df, param, company):

	x = df.index.values
	print("x array: \n", x)
	x = x[:-1]

	y = []
	for i in df["Paying Orders"]:
		y.append(float(i))
	y = y[:-1]
	print("y array: \n", y)

	z = np.polyfit(x, y, 1)
	print("y =",z[0],"x + ", z[1])

	m=z[0]
	b=z[1]


	print("Based on the previous amount of orders on", param.title(), ", the predicted number of order for next", param, "is:")
	prediction = round(m*(len(y)+1) + b)
	print(prediction,"\n")


	plt.scatter(x, y, c='b')
	plt.plot(x, m*x + b, 'r', label = "Best Fit")
	plt.xlabel("Date")
	plt.ylabel("Orders")
	title = "Orders from "+company.title()+" on "+param.title()+" vs. Date"
	plt.title(title)
	plt.legend()

	axes = plt.gca()
	axes.set_xlim([0,len(x)+5])
	axes.set_ylim([0,max(y)+10])

	plt.show()

	return prediction


main()







