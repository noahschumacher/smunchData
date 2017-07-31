# Noah Schumacher

sys.path.insert(0, '/Users/nschumacher/docs/smunchRoR/smunchData')
from helpers import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



from pandas import Series, DataFrame

def main():
	getWeather()
	getCompany()
	plotWeather()

def getWeather():

	df = pd.read_clipboard()

	date 	= df["Jun"]
	avgT	= df["avg"]
	avgW	= df["avg.5"]
	event	= df[" "]

	weatherDF = DataFrame()
	weatherDF["May"]	  = date
	weatherDF["Avg Temp"] = avgT
	weatherDF["Avg Wind"] = avgW
	weatherDF["Event"]	  = event

	print(weatherDF)

	weatherDF.to_csv('theweather.csv', sep=',')


def getCompany():
	df = getData()
	getUniqueCompanies(df)
	companyName = input("Enter company name: ") # Reads in company name and reduces df to only rows with company name in it
	selectedCompany = selectCompany(df, companyName)

	selectedCompany.to_csv("withWeather.csv", sep=',')


def plotWeather():
	df = pd.read_clipboard()

	y = []
	for i in df["Paying Orders"]:
		y.append(float(i))
	y = y[:-1]
	print("y array: \n", y)

	x = []
	for i in df["Avg Wind"]:
		x.append(float(i))
	x = x[:-1]

	z = np.polyfit(x, y, 1)
	print("y =",z[0],"x + ", z[1])

	m=z[0]
	b=z[1]


	prediction = round(m*(len(y)+1) + b)


	plt.scatter(x, y, c='b')
	plt.show()
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


main()