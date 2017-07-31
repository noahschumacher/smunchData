# Noah M. Schumacher

sys.path.insert(0, '/Users/nschumacher/docs/smunchRoR/smunchData')
from helpers import *

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

orders1_same_day = []
orders_everyday  = []

def main():
	
	df = pd.read_csv("inProg.csv", skipinitialspace=True)
	print(df)

	company     = df["Customer"].iloc[0]
	firstDay    = df["DateNumerical"].iloc[0]
	lastDay     = df["DateNumerical"].iloc[-1]
	totalDays   = lastDay-firstDay
	totalWeeks  = int(totalDays/7)
	length      = df.shape[0]

	# How much of dataframe to look at
	df = df.ix[int(length-15):]
	print(df)

	countSeries = df["Day"].value_counts()
	print(countSeries)

	print("First Day:", firstDay, "| Last Day:", lastDay, "| Total Days:", totalDays, "| Total Weeks:", totalWeeks)

	days_of_week_ordered = countSeries.size
	print("Ordered,", days_of_week_ordered, "days of the week")

	sameDays = same_numb_of_orders_on_each_day(countSeries)

	orders_every_day(days_of_week_ordered, sameDays, company)

	orders_one_day(days_of_week_ordered, company)
	frequency(df, lastDay, 8)


def frequency(df, lastDay, weeks):
	count = 0
	for i in range(1, weeks):
		if (lastDay-(i*7)) in df["DateNumerical"]:
			count += 1
			print("count", count)

	if count == df.shape[0]:
		print("Every Week")
	elif count == df.shape[0]/4:
		print("Every Month")


def same_numb_of_orders_on_each_day(series):
	check_val = series[0]
	for val in series:
		if val != check_val:
			return False
			break
	return True


def orders_every_day(days_of_week_ordered, sameDays, company):
	if days_of_week_ordered == 5 and sameDays == True:
		print("Orders Everyday!!!! ===> Category: 1")
		orders_everyday.append(company)
		return True


def orders_one_day(days_of_week_ordered, company):
	if days_of_week_ordered == 1:
		print("Orders only one day  ===>  Category: 2A")
		orders1_same_day.append(company)

		return True

main()