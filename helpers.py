# Noah M. Schumacher

import pandas as pd
from pandas import Series, DataFrame
import numpy as np

# This page is for helper functions in analyzing the data

# Aquires and somewhat organizes data from clipboard
def getData():

	cols = ['Date', 'Day', 'Restaurant', 'Customer', 'Paying Orders']
	df = pd.read_csv('csvPredictions/predictions/smunchDataHistorical.csv', skipinitialspace=True, usecols=cols)

	# Changing the Colmn Names
	df.columns = ['Date', 'Day', 'Restaurant', 'Customer', 'Paying Orders']
	df = df.apply(lambda x: x.astype(str).str.lower())
	return df


# Prints out company names
def getUniqueCompanies(df):

	companies = Series(np.unique(df["Customer"]))
	print(companies)
	return companies


# removes all rows with different company name than provided
def selectCompany(df, companyName):

	# Only taking rows with customer matching companyName
	companydf = df.loc[df["Customer"] == companyName]
	print("##################### SELECTCOMPANY\n ", companydf)
	return companydf


# Gets only the Date, Day, Paying Orders columns of df rows with specified day
def independentVariable(df, varTitle, var):

	# Gets rid of all other columns besides date, varTitle, paying orders
	df = df[["Date", varTitle, "Paying Orders"]]

	# Selects rows that contain certain var in varTitle
	df = df.loc[df[varTitle] == var].reset_index()

	print("#############. ", varTitle, " frame\n", df)

	return df

def bound(companyDF, predictionVal):
	orders = Series()
	count = 0
	for i in companyDF["Paying Orders"]:
		val = float(i)
		orders.set_value(count, val)
		count += 1

	minVal = orders.min()
	maxVal = orders.max()

	print("Prediction: ", predictionVal, "Min: ", minVal, "Max: ", maxVal)

	if predictionVal < minVal:
		print("less")
		return minVal
	elif predictionVal > (maxVal + maxVal*.2):
		print("more")
		predictionVal = (maxVal + maxVal*.2)
		return predictionVal
	else:
		print("else")
		return predictionVal




