# -*- coding: utf-8 -*-
"""
Created on Sat May  1 23:12:34 2021

@author: Julian Bass
"""

from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2018')

bsyc = BeautifulSoup(html.read(), "lxml")

# tables with class="t-chart"
tc_table_list = bsyc.findAll('table',
                      { "class" : "t-chart" } )

# only 1 t-chart table, so grab it
tc_table = tc_table_list[0]

# what are this table's components/children?
#for c in tc_table.children:
#    print(str(c)[:50])

# tag tr means table row, containing table data
# what are the children of those rows?
#for c in tc_table.children:
#    for r in c.children:
#        print(str(r)[:50])

# we have found the table data!
# just get the contents of each cell
#for c in tc_table.children:
#    for r in c.children:
#        print(r.contents)

# ------ My Code ------

# Reference: https://stackoverflow.com/questions/2870667/how-to-convert-an-html-table-to-an-array-in-python

daily_yield_curves = []

allrows = tc_table.findAll('tr', limit=10)

for row in allrows:
    daily_yield_curves.append([])
    allcols = row.findAll('th') + row.findAll('td')
    for col in allcols:
        daily_yield_curves[-1].append(col.text)
        
for row in daily_yield_curves:
    print(row)

# ------ Saving to File ------

# Creating an output file
output_file = open('scraped_table.txt', 'wt',
		encoding='utf-8')

# Saving tc table to output file  
output_file.write(str(tc_table))    
output_file.close()

# print(tc_table.prettify())