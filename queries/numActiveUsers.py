# Noah M. Schumacher, Aug 18, 2017
# Number of active users in x previous days
# 

## UNUSEFULL DATA!!!!!!!!!!!!!!!!!!!!!!
# Inherent nature of graph is flawed for company model


#####################################################################################
#############	  					NOTES		  						#############
#####################################################################################
''' Currently this file is a single run file so I did write it with the intention
of making a it a minimal memory, cpu load file. In the future if this is delpoyed on
the website it should be modified with smarter logic as to mitigate the extensive
quarries and looping done to complete. '''

import psycopg2
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt



#####################################################################################
#############	  			CONNECT TO SMUNCH DB   						#############
#####################################################################################
def get_connections():
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
#### General format for sql query and dataForm
def sql_Query(cursor, dataForm, query):
	if dataForm == "Series":
		get_command = query
		cursor.execute(get_command)
		data = Series(cursor.fetchall())
		data = data
		return data
	else:
		get_command = query
		cursor.execute(get_command)
		data = DataFrame(cursor.fetchall())
		return data

def getActiveUsersInXDays(cursor, days):
	activeUsers = sql_Query(cursor, "Series", "SELECT DISTINCT user_id FROM choices WHERE updated_at > (CURRENT_DATE - interval '%s' day) AND menue_dish_id IS NOT null" %days)
	return activeUsers


#####################################################################################
#############  					WORKING WITH DATA   					#############
#####################################################################################
def countUsers(activeUsers):
	totalUsers = activeUsers.count()
	return totalUsers

def plot(activeUsers):
	y = list(activeUsers.values)
	x = list(activeUsers.index)
	count = 0
	for val in x:
		x[count] = -val
		count += 1


	#### Trying to put threee thigns on same plot
	plt.plot(x, y, 'b', label='plot')
	plt.xlabel("X Days Ago")
	plt.ylabel("Active Users")
	plt.title("Active Users VS X Previous Days")
	plt.xticks(np.arange(-400, 0, 15))
	plt.legend()

	plt.grid(b=True, which='major', color='r', linestyle='--')

	plt.show()


def main():
	cursor = get_connections()

	days = int(input("Enter number of days in question: "))

	usersOrdered = Series()
	for i in range(days, 0, -1):

		activeUsers = getActiveUsersInXDays(cursor, str(i))
		count = countUsers(activeUsers)
		if count == 0:
			break
		usersOrdered = usersOrdered.set_value(i, count)
		

	print(usersOrdered)
	plot(usersOrdered)

	print("The count of total users who have ordered in the past %s days is:" %days)
	print(count)


main()



