# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:12:34 2021

@author: Julian Bass
"""

from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2018')

bsyc = BeautifulSoup(html.read(), "lxml")

# tables with class="t-chart"
tc_table_list = bsyc.findAll('table',
                      { "class" : "t-chart" } )

# only 1 t-chart table, so grab it
tc_table = tc_table_list[0]

# ------ A.1 Creating the Daily Yield Curves Array ------

# Reference: https://stackoverflow.com/questions/2870667/how-to-convert-an-html-table-to-an-array-in-python

# Creating empty array
daily_yield_curves = []

# Finding all row tags inside the table + limiting to first 15 rows
allrows = tc_table.findAll('tr', limit=10)

# Iterating through each row
for row in allrows:
    # Appending that row to the array
    daily_yield_curves.append([])
    # Identifying the '2 mo' table header
    delete_headers = row.findAll('th', text="2 mo")
    # Identifying empty table data cells
    delete_empty = row.findAll('td', text="\n\t\t\tN/A\n\t\t")
    # Removing these tags and data
    for match in delete_headers:
        match.decompose()
    for match in delete_empty:
        match.decompose()
    # Finding columns (table headers and table data tags) in the current row
    allcols = row.findAll('th') + row.findAll('td')
    # Iterating through each column
    for col in allcols:
        try:
            # Try to convert the tag's text to a float
            daily_yield_curves[-1].append(float(col.text))
        except:
            # If not possible, simply add the text
            daily_yield_curves[-1].append(col.text)
        
#for row in daily_yield_curves:
#    print(row)
            
# ------ A.2 Saving to File ------

df_list = pd.DataFrame(daily_yield_curves)

# Creating an output file
output_file = open('scraped_table.txt', 'wt',
		encoding='utf-8')

# Saving tc table to output file  
output_file.write(str(df_list))    
output_file.close()

# print(tc_table.prettify())

# ------ B. For matplotlib plotting ------

# Converting the daily_yield_curves array into a NumPy array
interest_rates_np = np.array(daily_yield_curves)

# Changing the header row according to month format
interest_rates_np[0] = ['Date', 1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]

print(pd.DataFrame(interest_rates_np))
print(interest_rates_np.dtype)

# Slicing to get the column of dates (days)
original_dates = interest_rates_np[1:, :1]

counted_days = []
day = 0

# Looping through original column of dates
# to create a new array with day counts
for day in range(len(original_dates)):
    day = day + 1
    counted_days.append([day])

# Converting the counted days into a NumPy array
counted_days = np.array(counted_days)

print("Counted days since 01/02/18: ")
print(counted_days)

# Identifying coordinates for plotting
x = counted_days # Array of days
y = interest_rates_np[:1, 1:].astype(int) # Sliced array of months
z = interest_rates_np[1:, 1:].astype(float) # Sliced array of rates converted to float

print("Days since 01/02/18: ")
print(pd.DataFrame(x), "\n")
print("Months of Maturity: ")
print(pd.DataFrame(y), "\n")
print("Interest Rates: ")
print(pd.DataFrame(z), "\n")

# Plot display settings
# Reference: https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
fig = plt.figure(figsize = [12,8])
ax = fig.gca(projection = '3d')

# Plotting axes
# Surface and wireframe are combined
surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

wire = ax.plot_wireframe(x, y, z, color='black')

# Setting labels
ax.set_xlabel('Trading days since 01/02/18')
ax.set_ylabel('Months to maturity')
ax.set_zlabel('Rate')