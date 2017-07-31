# Noah M. Schumacher

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def getData():

	# Find better way to read in certain data
	df = pd.read_clipboard()
	return df



def selectCompany(df, companyName):

	#Changing the Colmn Names
	df.columns = ['Date', 'Day', 'Restaurant', 'Location', 'Company Paying', 'Customer', 'Acquisition month', 'Paying Orders']

	companydf = df.loc[df["Customer"] == companyName]
	return companydf

# Gets only the Date, Day, Paying Orders columns of whole df, calls total_average...
def dayOfTheWeekFrame(df, day):

	df = df[["Date", "Day", "Paying Orders"]]

	# Creating data frames for certain each day of week
	frame = df[df["Day"].str.contains(day)].reset_index()
	totalAverage = total_and_average_per_day(frame)
	return totalAverage



def total_and_average_per_day(df):

	ordersPerDay = pd.DataFrame(columns = ["Date", "Total Orders", "Average"])

	checkIndex = 0
	iteration = 0
	ordersOnDay = 0
	total = 0
	for i in df["Date"]:
		
		#print("-----------START Loop------------------------")
		#print("Iteration: ", iteration, "   Check index: ", checkIndex, '\n')
		#print("i in df: ", i, "    Total = ", total)

		if i == df.loc[checkIndex, "Date"]:

			#print("-------IF Loop-------")

			total += df.loc[iteration, "Paying Orders"]

			#print("Iteration: ", iteration, "   Check index: ", checkIndex, '\n')
			#print("total = ", total)

			ordersOnDay += 1
			#print("orders On Day = ", ordersOnDay)

			
		else:
			#print("--------ELSE loop--------")
			#print("total = ", total)
			average = total / ordersOnDay
			ordersPerDay.loc[checkIndex] = [df.loc[checkIndex, "Date"], total, average]

			#total = 0
			ordersOnDay = 1

			# Reassigns the index to check to the new date entry and sets total equal to the first entry
			checkIndex = iteration
			total = df.loc[checkIndex, "Paying Orders"]

			#ordersPerDay.loc[checkIndex] = [df.loc[checkIndex, "Date"], total, average]

		iteration += 1

	ordersPerDay = ordersPerDay.reset_index()
	del ordersPerDay["index"]
	return ordersPerDay


def plotTotalOrders(df1, df2, df3, df4, df5):
	plt.plot(df1.index.values, df1["Total Orders"], 'r-', label = "Monday")
	#plt.plot(df2.index.values, df2["Total Orders"], 'b-', label = "Tuesday")
	#plt.plot(df3.index.values, df3["Total Orders"], 'g-', label = "Wednesday")
	#plt.plot(df4.index.values, df4["Total Orders"], 'y-', label = "Thursday")
	#plt.plot(df5.index.values, df5["Total Orders"], 'p-', label = "Friday")

	plt.xlabel("Index")
	plt.ylabel("Total Number of Payed Orders")
	plt.title("Total Orders on Weekday vs Date")
	plt.legend()

	plt.show()

def plotAverageOrders(df1, df2, df3, df4, df5):
	plt.plot(df1.index.values, df1["Average"], 'r-', label = "Monday")
	plt.plot(df2.index.values, df2["Average"], 'b-', label = "Tuesday")
	plt.plot(df3.index.values, df3["Average"], 'g-', label = "Wednesday")
	plt.plot(df4.index.values, df4["Average"], 'y-', label = "Thursday")
	plt.plot(df5.index.values, df5["Average"], 'p-', label = "Friday")

	plt.xlabel("Index")
	plt.ylabel("Average Number of Payed Orders")
	plt.title("Average Orders on Weekday vs Date")
	plt.legend()

	plt.show()


everythingFrame = getData()
companyFrame = selectCompany(everythingFrame, "Mahren Immobilien")

monFrame = dayOfTheWeekFrame(companyFrame, "Mon")
tueFrame = dayOfTheWeekFrame(companyFrame, "Tue")
wedFrame = dayOfTheWeekFrame(companyFrame, "Wed")
thuFrame = dayOfTheWeekFrame(companyFrame, "Thu")
friFrame = dayOfTheWeekFrame(companyFrame, "Fri")

plotTotalOrders(monFrame, tueFrame, wedFrame, thuFrame, friFrame)
#plotAverageOrders(monFrame, tueFrame, wedFrame, thuFrame, friFrame)




