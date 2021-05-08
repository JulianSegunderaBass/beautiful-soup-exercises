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

html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2018')

bsyc = BeautifulSoup(html.read(), "lxml")

# tables with class="t-chart"
tc_table_list = bsyc.findAll('table',
                      { "class" : "t-chart" } )

# only 1 t-chart table, so grab it
tc_table = tc_table_list[0]

# ------ My Code ------

# Reference: https://stackoverflow.com/questions/2870667/how-to-convert-an-html-table-to-an-array-in-python

daily_yield_curves = []

allrows = tc_table.findAll('tr', limit=10)

for row in allrows:
    daily_yield_curves.append([])
    delete_headers = row.findAll('th', text="2 mo")
    delete_empty = row.findAll('td', text="\n\t\t\tN/A\n\t\t")
    for match in delete_headers:
        match.decompose()
    for match in delete_empty:
        match.decompose()
    allcols = row.findAll('th') + row.findAll('td')
    for col in allcols:
        try:
            daily_yield_curves[-1].append(float(col.text))
        except:
            daily_yield_curves[-1].append(col.text)
        
#for row in daily_yield_curves:
#    print(row)

# ------ For matplotlib plotting ------

interest_rates_np = np.array(daily_yield_curves)

interest_rates_np[0] = ['Date', 1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]

print(pd.DataFrame(interest_rates_np))

print(interest_rates_np.dtype)

# days since 01/02/18
#x = interest_rates_np[1:, :1]
# months of maturity
#y = interest_rates_np[:1, 1:]
# rates
#z = interest_rates_np[1:, 1:].astype(float)

x = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9]])
y = np.array(interest_rates_np[:1, 1:].astype(int))
z = np.array(interest_rates_np[1:, 1:].astype(float))

print("Days since 01/02/18: ")
print(pd.DataFrame(x), "\n")
print("Months of Maturity: ")
print(pd.DataFrame(y), "\n")
print("Interest Rates: ")
print(pd.DataFrame(z), "\n")

# Method 1
fig = plt.figure(figsize = [12,8])
ax = fig.gca(projection = '3d')

# Plot the surface.
surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax.set_xlabel('Trading days since 01/02/18')
ax.set_ylabel('Months to maturity')
ax.set_zlabel('Rate')

# Method 2
#f = lambda x, y: np.sin(x) * np.cos(y)
#X, Y = np.meshgrid(x, y)
#F = f(X, Y)

#fig = plt.figure(figsize = [12,8])
#ax = fig.gca(projection = '3d')
#ax.plot_surface(X, Y, F, cmap = cm.coolwarm)

#ax.set_xlabel('trading days since 01/02/18')
#ax.set_ylabel('months to maturity')
#ax.set_zlabel('rate')


# ------ Saving to File ------

df_list = pd.DataFrame(daily_yield_curves)

# Creating an output file
output_file = open('scraped_table.txt', 'wt',
		encoding='utf-8')

# Saving tc table to output file  
output_file.write(str(df_list))    
output_file.close()

# print(tc_table.prettify())