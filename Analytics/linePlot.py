import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from abstractAnalytics import AbstractAnalytics

class LinePlot(AbstractAnalytics):

	def generate_PNG(self):

		#gets the current day in the same format as stored in csv
		date_today = datetime.date.today().strftime('%d/%m/%Y')
		
		#reads csv
		sensehat_data = pd.read_csv('data.csv')

		#get the latest data the past 15 minutes
		sensehat_data = sensehat_data.tail(15)		
		
		#only use data as todays date
		sensehat_data = sensehat_data.loc[sensehat_data["Date"] == date_today]

		#change size of the graph
		sns.set(rc={'figure.figsize':(15,10)})

		#remove background grid
		sns.set_style("whitegrid", {'axes.grid' : False})		

		#plot the data
		axes = sns.lineplot(x="Time", y="Temperature",label="Temperature",legend=False,data=sensehat_data, color="g")
		second_axes = axes.twinx()
		
		sns.lineplot(x="Time", y="Humidity",label="Humidity",ax=second_axes,legend=False,data=sensehat_data, color="r")
		
		#shows legend
		axes .figure.legend()
		figure = axes.get_figure()

		#saves the graph into png
		figure.savefig('lineplot.png')
