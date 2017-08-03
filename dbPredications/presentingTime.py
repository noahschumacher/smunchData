# Noah M. Schumacher
# First attempt at grabbing data from Smunch DB using sql in python

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab 

def presentation(timeDF):
	timeDF = timeDF[timeDF.avg_time_dif != 0]
	print("Fixed time DF:\n", timeDF)

	times_in_mins = convert_times(timeDF)


	mu = np.mean(times_in_mins)
	sigma = np.std(times_in_mins)
	variance = sigma**2
	print("Mu:", mu, " | Sigma:", sigma, " | variance:", variance)
	x = np.linspace(-50, 120, 100)


	#nine5 = plt.plot(x, mlab.normpdf(x, mu, sigma), color= 'r', label = "95%")
	nine = plt.plot(x, mlab.normpdf(x, mu, sigma), color= 'b', label = "90%")
	#seven5 = plt.plot(x, mlab.normpdf(x, mu, sigma), color= 'g', label = "75%")


	plt.grid(b=True, which='both')


	plt.show()

def convert_times(timeDF):
	times_in_mins = []
	for i in timeDF["avg_time_dif"]:
		days, seconds = i.days, i.seconds
		hours = days * 24 + seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60

		total_min = (hours*60 + minutes)/60

		times_in_mins.append(total_min)
	print(times_in_mins)
	return times_in_mins
