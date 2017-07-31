# Noah M. Schumacher

sys.path.insert(0, '/Users/nschumacher/docs/smunchRoR/smunchData')
from helpers import *

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import seaborn as sns
from dateutil import parser

# Company categories
orderedIP_1W     = []
orderedIP_4W     = []
norderedIP_4W 	 = []
ordered1         = []
ordered2         = []
ordered3         = []
orderedM3        = []
one				 = []
twoA			 = []
threeA			 = []
threeB			 = []
fourA			 = []
fourB			 = []

categoriesFrame = DataFrame()

present = 736531

def main():

	df = getData()
	df = df.drop(['Restaurant'], axis=1)

	companies = getUniqueCompanies(df)
	companies = companies[companies != 'nan']

	Categorization(df, companies)


def Categorization(df, companies):

	#################  Iterating through each unique company ##################
	for company in companies:
		print("############### iteration", company, "################")
		print("Company:", company)
		companyDF = selectCompany(df, company).reset_index()
		companyDF = companyDF.drop(['index'], axis=1)

		############  Categorizing by number of Orders  ##############
		hits = companyDF.shape[0]
		print("Number of days ordered:", hits)
		numberOfOrders(company, hits)


		################  Categorizing by Recency #################
		for i in range(hits):
			stringDate = companyDF["Date"][i]
			structuredDate = parser.parse(stringDate)  #Converting dates to datetime
			companyDF["Date"][i] = structuredDate	   #Updating dates for each company to datetime

		dates = matplotlib.dates.date2num(companyDF["Date"]) #Converting dates to float
		dates = dates.tolist()
		dates = [int(i) for i in dates]
		companyDF["DateNumerical"] = dates
		print('\n',companyDF)
		companyDF.to_csv("inProg.csv", sep=",", index = False)

		orders = []
		for i in companyDF["Paying Orders"]:
			orders.append(round(float(i)))
		print("orders:", orders)
		cat = inPast(company, dates, present)   #Calling inpast and appending to appropriate list


		##################  Everyday  ####################
		if cat == "Week":
			everyDays = everyDay(dates, companyDF)
			if everyDay == True:
				one.append(company)

		##################  Same Days ####################
		elif cat == "Month":
			print("In Month")
			sameDays = sameDay(dates, companyDF)

		# Plot the orders from start to end
		# plot(dates, orders)

		yes = input("y or n: ")
		if yes == 'y':
			print(" ordered1:       ", ordered1,'\n',
				  "ordered2:       ", ordered2,'\n',
				  "ordered3:       ", ordered3,'\n',
				  "orderedM3:      ", orderedM3,'\n',
				  "orderedIP_1W:   ", orderedIP_1W, '\n',
				  "orderedIP_4W:   ", orderedIP_4W, '\n',
				  "norderedIP_4W:  ", norderedIP_4W, '\n')

		print(one)

	#################  Appending all categories to DataFrame  ####################
	'''categoriesFrame["orderedM3"]  	   = 	Series(orderedM3)
	categoriesFrame["ordered3"] 	   = 	Series(ordered3)
	categoriesFrame["ordered2"]    	   = 	Series(ordered2)
	categoriesFrame["ordered1"] 	   = 	Series(ordered1)
	categoriesFrame["orderedIP_Week"]  = 	Series(orderedIP_Week)
	categoriesFrame["orderedIP_4W"]    = 	Series(orderedIP_4W)
	categoriesFrame["norderedIP_4W"]    = 	Series(norderedIP_4W)

	return categoriesFrame'''

	#categoriesFrame.to_csv('CompanyCategories.csv', sep = ',')


def everyDay(dates, companyDF):
	endDay = dates[-1]
	startDay = dates[0]

	print("Start:", startDay, "End:", endDay)

	dayCount = 0
	print(dayCount)
	while endDay > startDay:
		#print("i:", endDay)
		if endDay in dates:
			dayCount += 1
			#print("Ordered for past:", dayCount, "Days")
			endDay -= 1
			if dayCount % 5 == 0:
				#print("exec")
				endDay = endDay - 2
		else:
			break
	if dayCount > 10:
		print("Orders Everyday!")
		return True


def sameDay(dates, companyDF):
	endDay = dates[-1]
	startDay = dates[0]

	dif = endDay - startDay
	dif_by_seven = int(dif/7)
	print("dif", dif_by_seven)
	iterations = 0
	if dif%7 == 0:
		print("start and end are same day")
		iterations = dif_by_seven

	print("Start:", startDay, "End:", endDay)

	ordersOnSameDay = 1
	for multiplyer in range(1, iterations+1):
		if (endDay - multiplyer*7) in dates:
			print("Ordered same day", multiplyer, "week ago")
			ordersOnSameDay += 1

	ordersOnDifDay = len(dates)-ordersOnSameDay

	print("Same Day:", ordersOnSameDay, "Dif Day:", ordersOnDifDay)


def other(companyDF):
	frequencyDF = companyDF["DateNumerical"].value_counts()
	print(frequencyDF)

	


def numberOfOrders(company, val):
	if val == 1:
		ordered1.append(company)
	elif val == 2:
		ordered2.append(company)
	elif val == 3:
		ordered3.append(company)
	else:
		orderedM3.append(company)


def inPast(company, dates, present):

	last = len(dates)-1
	if dates[last] >= (present - 7):
		orderedIP_1W.append(company)
		return "Week"
	elif dates[last] >= (present - 28):
		orderedIP_4W.append(company)
		return "Month"
	else:
		norderedIP_4W.append(company)
		return "MoreMonth"


def dateConverter():
	calendar = DataFrame([31,28,31,30,31,30,31,31,30,31,30,31], 
				index = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])

	print(calendar)


def plot(x, y):
		plt.plot(x, y, linestyle='--', marker='o', color='b')
		plt.gcf().autofmt_xdate()
		axes = plt.gca()
		axes.set_xlim([736075, 736531])
		plt.show()



main()
