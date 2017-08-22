# Noah M. Schumacher	Aug2, 2017
# File presents the normal distribution for 75%, 90%, 95% of ordes placed
# It aggregates all the companies ordered in the past two months and to form distributions
# Reads in csv file in same directory in read_in() function

import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import re
from datetime import timedelta

### Reads in general companies orderTimes_% and formats.
def read_in():
	df = pd.read_csv("order_placed_percentage_times.csv", skipinitialspace = True)

	df = format_times(df, 1)
	df = format_times(df, 2)
	df = format_times(df, 3)

	return df

### Formats the times in DF col by excluding negative times and calls stringTD_to_TD
def format_times(df, col):
	
	count = 0
	col_name = df.columns[col]
	for time in df[col_name]:
		if time[0] == '-':
			df = df.set_value(count, col_name, stringTD_to_TD("0 days 0:00:00"))
		else:
			timeD = stringTD_to_TD(time)
			df = df.set_value(count, col_name, timeD)
		count += 1

	return df

### converts string timedelta to datetime.timedelta
def stringTD_to_TD(s):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]* (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return timedelta(**{key: float(val) for key, val in m.groupdict().items()})

### Reads in timeDF and presents three bells curves for 75,90,95%
def presentation(timeDF):

	times_in_hours_95 = convert_times(timeDF, "avg_time_dif_95")
	times_in_hours_90 = convert_times(timeDF, "avg_time_dif_90")
	times_in_hours_75 = convert_times(timeDF, "avg_time_dif_75")


	mu_95 = round(np.mean(times_in_hours_95),3)
	mu_90 = round(np.mean(times_in_hours_90),3)
	mu_75 = round(np.mean(times_in_hours_75),3)

	std_D_95 = round(np.std(times_in_hours_95),3)
	std_D_90 = round(np.std(times_in_hours_90),3)
	std_D_75 = round(np.std(times_in_hours_75),3)

	variance_95 = round(std_D_95**2,3)
	variance_90 = round(std_D_90**2,3)
	variance_75 = round(std_D_75**2,3)

	#print("Mu_95:", mu_95, " | Std_D_95:", std_D_95, " | variance_95:", variance_95)
	#print("Mu_90:", mu_90, " | Std_D_90:", std_D_90, " | variance_90:", variance_90)
	#print("Mu_75:", mu_75, " | Std_D_75:", std_D_75, " | variance_75:", variance_75)

	info = [[0.95, mu_95, std_D_95], [0.90, mu_90, std_D_90], [0.75, mu_75, std_D_75]]

	return info

### Converts timeDeltas into an hours count and return list of hours
def convert_times(timeDF, col):
	times_in_hours = []
	for i in timeDF[col]:
		days, seconds = i.days, i.seconds
		hours = days * 24 + seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60

		total_hours = hours + minutes/60

		if 0 < total_hours < 48:
			times_in_hours.append(total_hours)

	return times_in_hours


def main():
	df = read_in()
	presentation(df)