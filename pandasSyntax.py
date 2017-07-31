# Noah M. Schumacher
# noahschumacher14@gmail.com

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from numpy.random import randn

######################################################################
# SERIES
######################################################################

#Crearting a Series
# First part are the values of the series and second part are the corresponding indexs
my_series = Series(['val1', 'val2', 'val3'], index=[0,1,2,3])

# Get the index's of a Series
my_index = my_series.index

# Grab and index value , Cant change and index value easily
my_value = my_index[3]

# Reindex a series
# Creates a second series with same values as first but new index's, if no val fills with NaN
my_series2 = my_series.reindex(['A', 'B','C','D','E'])

# Reindex and fill new Index with specified value
my_series2.reindex(['A','B','C','D','E','F'], fill_value=0)

# Get specific value
my_series2.loc["index", "col"]

# Get the values of a series

######################################################################
# CREATING DATA FRAMES
######################################################################

# From a dictionary
cityPop = {"City":['SF', 'LA', 'NYC'], "Population":[200000, 2342222, 838383883]}
# Passing in dictionary to dataframe
cityFrame = DataFrame(cityPop)

# Read a frame from the clipboard
frame = pd.read_clipboard()

# Creating dataframe
dframe = DataFrame(randn(25).reshape((5,5)), index=['A','B','D','E','F'], columns = ['col1','col2','col3','col4','col5']


# Website Ref: http://pandas.pydata.org/pandas-docs/dev/generated.pandas.DataFrame.html

######################################################################
# READING AND WRITING TO DATA FRAMES
######################################################################

# Read frame colmns: outputs the titles of each colmn
frame.columns

# Read the values in particular colmn or multiple with ,...,...
frame["Title", "Title 2"]

# Read in TOP 10 rows from dataframe, if no number specified reads in 5 rows/ does not include title
frame.head(10)

# Read in BOTTOM x rows from dataframe, same as above
frame.tail(10)

# Read information of particular colmn with titles
frame.ix[3]		# 3 specifies row index to read (starts at 0)

# Asign values to colmn (fills in all rows with the info)
frame["title"] = "Row info"

# Asign certain values to a certain colmn
frame["title"] = np.arange(20)        # Will add 0-19 to each row sequestianly

# Create a series with certain values and index
series = Series(["Info1", "Info2"], index=[4,0])

# Add a row to a data frame
frame.loc[0] = ["col1 info", "col2 info"]

# Add series to data frame
frame["frame title"] = series 	# places the series info into column with that title at series specifed index

# Delete a coln of row
del frame["row title"]


######################################################################
# REINDEX DATA FRAMES
######################################################################

# Have the data frame
dframe = DataFrame(randn(25).reshape((5,5)), index=['A','B','D','E','F'], columns = ['col1','col2','col3','col4','col5']
dframe.reindex(['A','B','C','D','E','F']) 	# Adds the C index with NaN values


######################################################################
# DROP ENTRIES
######################################################################

# This will create series and then delete the value at index b
ser1 = Series(np.arange(3), index['a','b','c'])
ser1.drop('b')

# Creates and then drops LA row from the data frame (DOES NOT PERMENTALY DELETE)
dframe1 = DataFrame(np.arange(9).reshape((3,3)), index=['SF','LA','NY'], columns=['pop','size','year'])
dframe1.drop('LA')

# Drops the colmn year, axis=1 specifies it is colmn
dframe1.drop('year', axis=1)



######################################################################
# SELECTING ENTRIES
######################################################################

# Create series with values 0,1,2
ser2 = Series(np.arange(3),index=['A','B','C'])
val1 = ser2['B'] 	# Would store 1 in val1
val2 = ser2[1] 		# Would also store 1 in val2

# This will return all the values from index
ser2[0:3]

# Grab by logic
ser2[ser2>1] 		# Returns part of series greater than 1


# Example data frame (5x5 dataframe going from 0-24)
dframe2 = DataFrame(np.arange(25).reshape((5,5)), index=['SF','LA','NY','DC','Chi'], 
	columns=['A','B','C','D','E'])

# Return Colm or colms
dframe2['B']
dframe2[['B','E']]

# Return dataframe where C colm values are over specified param
dframe2[dframe2['C']>5]

# Boolean Data Frame, here returns true or false in each value location depending on condition
dframe2 > 10

# Read information of particular colmn with titles
dframe2.ix[3]		# 3 specifies row index to read (starts at 0)


######################################################################
# DATA ALIGNMENT
######################################################################

# Adding series
series3 = series1 + series2 	# Will add entries at index if both contain values at that index

# Adding dataframes, will only add values if there is a value at particular location in both frames
dataframe3 = dataframe1 + dataframe2     # Also rearranges colm order / returns NaN for empty

# Adding and filling
dataframe3 = dataframe1.add(dataframe2, fill_value=0)

# Adding series and dataframes
dframe = dframe1-ser2 	# Sees if index matches with dataframe and persorms operation or particilar row or colm


######################################################################
# SUMMARY STATISTICS
######################################################################

# Will return the sum for each colm, ignores NaN
dframe.sum()

# Will return sum of Rows
dframe.sum(axis=1)

# Min/max val for each col
dframe.min()

# Min/max val index for each col
dframe.idxmin()

# Cumulation sum
dframe.cumsum()

# Describe method creates summary statistics for each colm
dframe.descirbe() 	#count, mean, std, min, ....

# Covariance and Correlation
import pandas.io.data as pdweb
import datetime


# Getting the stock data from the internet and displaying the first 5 sets
prices = pdweb.get_data_yahoo(['CVX', 'XOM', 'BP'],start=datetime.datetime(2010,1,1),
	end=datetime.datetime(2013,1,1))['Adj Close']
prices.head()


# Getting unique values in series
ser1.unique()
# Getting the count of each value in a series
ser1.value_count()


######################################################################
# MISSING DATA
######################################################################

# Suppose data is a series
# to return a a series filled with true or false depending on if NaN
data.isnull()

# To drop empty data use
data.dropna()

# In data frame will drop whole row if contains NaN so specify otherwise
dframe.dropna(how='all')		# Will only drop rows where all data is NaN

# To drop columns instead of rows
dframe.dropna(axis=1)

 # Drop rows that have less than a certain number of data points
 dframe.dropna(thresh=2) 	# Will drop rows that have more than two NaN in it

 # Fill all NaN with something
 dframe.fillna(1) 	# Fills of NaN with 1

 # Want to fill certain places with certain things dframe.fillna({col:cal})
dframe.fillna({0:4, 1:3, 3:100})

# Modify something inline
dframe.fillna(0, inplace = True)


######################################################################
# INDEX HIERARCHY
######################################################################

# Create a series with two level index
ser = Series(randn(6), index = [[1,1,1,2,2,2], ['a','b','c','a','b','c']])

# Convert multiple indexed series to data frame
dframe = ser.unstack()

# Create a dataframe with multiple index levels
dframe2 = DataFrame(np.arange(16).reshape(4,4),index=[['a','a','b','b'],[1,2,1,2]], columns = [['NY','NY','LA','SF']])



######################################################################
# READING AND WRITING TEXT FILES
######################################################################

# To read in a .csv file, takes top row to be header and , to be delimeter
dframe = pd.read_csv('file.csv'). 	# Requires file to be in same directory as script

# Read in .csv with no header 
dframe.read_csv('file.csv', header = None)

# Another way to import .csv files (More genaric way to read in data have to specify delimeter)
dframe = pd.read_table('file.csv', sep',',header=None)

# Indicate number of rows want to read in
dframe = pd.read_csv('file.csv', header=None, nrows=2)

# Export out to csv file
dframe.to_csv('mynewFile.csv')


######################################################################
# READING AND WRITING JSON FILES AND DATA
######################################################################

import json

# Suppose you have a json object
json_obj = """
{
	"zoo_animal": "Lion",
	"food": ["Meat", "Veggies", "Honey"],
	"clothes": null,
	"diet": [{"zoo_animal": "Gazelle", "food": "grass", "fur": "Brown"}]
} """

# To work with data transfer it to data
data = json.loads(json_obj)

# To get the diet of above json object into data frame use
dframe = DataFrame(data['diet'])


######################################################################
# READING AND WRITING WITH HTML
######################################################################

from pandas import read_html

# Need to pip install beautiful-soup
# and pip install html5lib
url = 'website url goes here'

# creating a list bject with html data from url and then
dframe_list = pd.io.html.read_html(url)
# specifically grabs tabled data in the second line
dframe = dframe_list[0]

# If you want to only grab the column titles
dframe_list.columns.values


######################################################################
# MERGING DATA
######################################################################

# Creating two data frames of different sizes
dframe1 = DataFrame({'key':['X','Z','Y','Z','X','X'], 'data_set_1':np.arange(6)})

dframe2 = DataFrame({'key':['Q','Y','Z'], 'data_set_2':[1,2,3]})

# Calling the merge function will merge these two different sized data frames and align them based
	# on the key values that they share
merged = pd.merge(dframe1, dframe2)

# To specify which colm to merge on
pd.merge(dframe1, dframe2, on = 'key')
 
# To merge and creare null values where on dataframe doesnt share values
pd.merge(dframe1, dframe2, on='key', how='left')


# Many to Many merging
# This will merge two mutiple colmn data frames and will return NaN where there is no value for certain key combination
pd.merge(df_left, df_right, on= ['key1','key2'], how= 'outer')


# Merging based on index
# Suppose you have two data frames 'df_left', 'df_right'. 
# Below we will merge the left one on the column name key
pd.merge(df_left, df_right, left_on='key',right_index=True)



######################################################################
# CONCATENATE
######################################################################

# Creating a matrix with numpy
arr1 = np.arange(9).reshape(3,3) 	# 3x3 matrix with values 0-8

# Will return a 3x6 matrix with 0,1,2,0,1,2 on one row
np.concatenate([arr1, arr1], axis=1)

# To concatenate top to bottom
np.concatenate([arr1,arr1],, axis=0)


# Concatenating in pandas with series
# This will simply put series two information after series1 information
pf.concat([series1, series2])

# Want to concatenate into a dataframe (each series will have seperate column)
pd.concat([series1, series2], axis=1)

# Concatenate two series into a double indexed sereis
pd.concat([series1, series2], keys=['cat1','cat2']) 	# the leys are the second indexing

# Simply concat dataframe
pd.concat([df1, df2])


































