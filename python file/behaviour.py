"""
Created By: Dhiraj Kumar
"""
# importing libraries
from dateutil import parser
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import NullFormatter
from matplotlib.dates import MonthLocator, DateFormatter


class weather:

    @staticmethod
    def behaviour(file, frq):

        df = pd.read_csv(file)

        row_no = 1
        columns = df.columns.values

        print(df.head())

        df['obstime'] = df['obstime'].apply(parser.parse)

        # sorting data and dropping duplicate values
        df.sort_values("obstime", inplace=True)
        df.drop_duplicates(keep=False, inplace=True)

        df = df.set_index(df['obstime'])

        plt.figure(figsize=(15, 30))

        for column in columns[1:]:
            data = df[column]

            # removing incorrect data i.e. -999 and assigning color for different data
            if column == "temperature":
                data = data[data > -273]
                color = "orange"
            else:
                data = data[data > 0]
                if column == "wind_speed":
                    color = "blue"
                elif column == "wind_direction":
                    color = "red"
                elif column == "pressure":
                    color = "green"
                elif column == "relative_humidity":
                    color = "yellow"

            data = data.groupby(pd.Grouper(freq=frq)).mean().dropna()

            if not data.empty:
                # getting maximum and minimum of the data
                maxm = str(round(max(data), 2))
                minm = str(round(min(data), 2))

                # assigning graph position
                ax1 = plt.subplot(5, 1, row_no)
                plt.grid(True)
                # plotting graph
                plt.plot(data, color=color)

                ax1.xaxis.set_major_locator(MonthLocator())
                ax1.xaxis.set_minor_locator(MonthLocator(bymonthday=28))
                ax1.xaxis.set_major_formatter(NullFormatter())
                ax1.xaxis.set_minor_formatter(DateFormatter('%b'))

                plt.ylabel(column)

                max_patch = mpatches.Patch(color='red')
                min_patch = mpatches.Patch(color='green')

                plt.legend(loc=1, handles=[max_patch, min_patch], labels=['Max Value : ' + maxm, 'Min Value : ' + minm])

                row_no += 1

        plt.show()
        return 0


w = weather()

print('Behaviour Analysis')

input_file = "weather.csv"
year = '2017'
freq = 'd'
w.behaviour(input_file, freq)
