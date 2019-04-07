import matplotlib.pyplot as plt
import pandas as pd
import datetime
from abstractAnalytics import AbstractAnalytics

class ScatterPlot(AbstractAnalytics):

	def generatePNG(self):

		#gets the current day in the same format as stored in csv
		date_today = datetime.date.today().strftime('%d/%m/%Y')
			
		sp = pd.read_csv('data.csv')				
		#only use data with current date
		sp = sp.loc[sp["Date"] == date_today]

		x = "Humidity"		
		sp.plot(x, y="Temperature",kind="scatter",color="g")

		#save the png
		plt.savefig('scatterplot.png')