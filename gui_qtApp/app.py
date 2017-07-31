# Noah M. Schumacher



import appPredictions
import sys

sys.path.insert(0, '/Users/nschumacher/docs/smunchRoR/smunchData')
import helpers

import pandas as pd
from pandas import Series, DataFrame

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class App(QWidget):

	def __init__(self, parent = None):
		super(App, self).__init__(parent)
		self.setWindowTitle("Predictions")
		self.initWidgets()
		self.show()

	def initWidgets(self):
		parameters = ["mon", "", False]
		day = 'mon'
		rest = ''
		calc = False

		layout = QVBoxLayout()
		dayLayout = QHBoxLayout()
		buttonLayout = QHBoxLayout()
		restaurantLayout = QHBoxLayout()
		tableLayout = QVBoxLayout()

		########## Creating Select Day Section #################
		dayGroup = QGroupBox("Day of the Week")

		self.btn_Mon = QRadioButton("Monday")
		self.btn_Tue = QRadioButton("Tuesday")
		self.btn_Wed = QRadioButton("Wednesday")
		self.btn_Thu = QRadioButton("Thursday")
		self.btn_Fri = QRadioButton("Friday")

		self.btn_Mon.setChecked(True)

		self.btn_Mon.toggled.connect(lambda:self.dayRadioBtnState(self.btn_Mon, parameters))
		self.btn_Tue.toggled.connect(lambda:self.dayRadioBtnState(self.btn_Tue, parameters))
		self.btn_Wed.toggled.connect(lambda:self.dayRadioBtnState(self.btn_Wed, parameters))
		self.btn_Thu.toggled.connect(lambda:self.dayRadioBtnState(self.btn_Thu, parameters))
		self.btn_Fri.toggled.connect(lambda:self.dayRadioBtnState(self.btn_Fri, parameters))

		dayLayout.addWidget(self.btn_Mon)
		dayLayout.addWidget(self.btn_Tue)
		dayLayout.addWidget(self.btn_Wed)
		dayLayout.addWidget(self.btn_Thu)
		dayLayout.addWidget(self.btn_Fri)

		dayGroup.setLayout(dayLayout)
		########################################################


		########## Creating Restaurant Selector ################
		restrauntGroup = QGroupBox("Restaurant")

		self.restrauntSelector = QComboBox()
		self.restrauntSelector.addItems(self.getUniqueRestraunts())
		self.restrauntSelector.currentIndexChanged.connect(self.restSelectionChange) ####### How to store resraunt changed too?

		restaurantLayout.addWidget(self.restrauntSelector)

		restrauntGroup.setLayout(restaurantLayout)
		########################################################


		#############   Add Calculate Button   #################
		buttonGroup = QGroupBox("Calculate")

		self.button = QPushButton("Calculate Predicted Orders", self)
		self.button.clicked.connect(lambda:self.calculateBtnState(self.button, parameters))

		buttonLayout.addWidget(self.button)

		buttonGroup.setLayout(buttonLayout)
		########################################################


		##########  Creating Prediction Table   ################
		tableGroup = QGroupBox("Predictions")

		companies = self.companyList()
		#predictions = self.createPredictions(parameters, companies)
		rows = len(companies)
		cols = 2

		self.tableWidget = QTableWidget()
		self.tableWidget.setRowCount(rows)			###### Setting Row count
		self.tableWidget.setColumnCount(cols)		###### Set col count

		for row in range(rows):
			self.tableWidget.setItem(row, 0, QTableWidgetItem(companies[row].title()))
			self.tableWidget.setItem(row, 1, QTableWidgetItem("prediction for"))

		tableLayout.addWidget(self.tableWidget)

		tableGroup.setLayout(tableLayout)
		########################################################


		##############   Putting it all togeather   ############
		layout.addWidget(dayGroup)
		layout.addWidget(restrauntGroup)
		layout.addWidget(buttonGroup)
		layout.addWidget(tableGroup)

		layout.addStretch(0)

		self.setLayout(layout)


	###############      Helper Functions      #################
	def getUniqueRestraunts(self):
		df = helpers.getData()
		restaurants = Series(np.unique(df["Restaurant"].map(lambda x: x.strip())))
		for ind in range(len(restaurants)):
			restaurants[ind] = restaurants[ind].title()
		restaurants = restaurants.sort_values()

		del df
		print(restaurants)
		return restaurants


	def companyList(self):
		relevantColumns = ["orderedIP_Week", "orderedIP_1M", "orderedIP_2M"]
		relevantCompanies = pd.read_csv("/Users/nschumacher/docs/smunchRoR/smunchData/csvPredictions/chanceOfOrder/CompanyCategories.csv", skipinitialspace = True, usecols = relevantColumns)
		companyL = []
		for i in relevantCompanies["orderedIP_Week"]:
			if type(i) == str:
				companyL.append(i)
		for i in relevantCompanies["orderedIP_1M"]:
			if type(i) == str:
				companyL.append(i)
		for i in relevantCompanies["orderedIP_2M"]:
			if type(i) == str:
				companyL.append(i)

		return companyL

	def restSelectionChange(self, i):
		currentText = self.restrauntSelector.currentText()
		print("selection changed to", currentText.title())
		print(currentText, "only being hit here")
		return currentText

	def dayRadioBtnState(self, b, parameters):
		if b.text() == "Monday":
			if b.isChecked() == True:
				print(b.text(), "is selected")
				parameters[0] = 'mon'
		elif b.text() == "Tuesday":
			if b.isChecked() == True:
				print(b.text(), "is selected")
				parameters[0] = 'tue'
		elif b.text() == "Wednesday":
			if b.isChecked() == True:
				print(b.text(), "is selected")
				parameters[0] = 'wed'
		elif b.text() == "Thursday":
			if b.isChecked() == True:
				print(b.text(), "is selected")
				parameters[0] = 'thu'
		elif b.text() == "Friday":
			if b.isChecked() == True:
				print(b.text(), "is selected")
				parameters[0] = 'fri'
		print(parameters)

	def calculateBtnState(self, b, parameters):
		if not self.button.isChecked():
			print("Button released")
			parameters[2] = True
		print(parameters)
		#createPredictions(parameters)


	def createPredictions(self, parameters, companies):
		bigDF = helpers.getData()
		day = parameters[0]
		rest = parameters[1]
		companies = companies

		predictions = appPredictions.getPredictions(bigDF, day, rest, companies)

		predList = []
		for i in predictions:
			predList.append(i)

		del predictions
		return predList


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())













