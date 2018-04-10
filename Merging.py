## -*- coding: utf-8 -*-
#"""
#Created on Wed Mar 14 11:45:11 2018
#
#@author: miche
#"""
#
import pandas as pd
import os
#0xb0.encode('utf-8').strip()
#datasettime = pd.read_csv('2015-02.csv', encoding = 'ISO-8859-1')

files = [f for f in os.listdir('.') if os.path.isfile(f)]

merged = []

for f in files:
    filename, ext = os.path.splitext(f)
    if ext == '.csv':
        read = pd.read_csv(f, encoding = 'ISO-8859-1')
        merged.append(read)

result = pd.concat(merged)

result.to_csv('Climate.csv')


