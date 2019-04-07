import matplotlib.pyplot as plt
import pandas as pd
import datetime
from abstractAnalytics import AbstractAnalytics

class ScatterPlot(AbstractAnalytics):

	def generatePNG(self):

		#gets the current day in the same format as stored in csv
		date_today = datetime.date.today().strftime('%d/%m/%Y')
			
		a = pd.read_csv('temp.csv')				
		#only use data as todays date
		a = a.loc[a["Date"] == date_today]

		x = "Humidity"		
		a.plot(x, y="Temperature",kind="scatter",color="g")

		#save the png
		plt.savefig('scatterplot.png')