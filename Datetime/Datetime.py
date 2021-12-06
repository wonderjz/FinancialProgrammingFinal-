# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:24:17 2021

@author: ljz
"""

import os 
import pandas as pd
#from datetime import datetime
import calendar

path = 'E:\codes for 7033\Final Project\Datetime\data'
path1 = os.path.join(path,'ukpound_exchange.csv')
df = pd.read_csv(path1)
df.head(3)
df.info()

#df["Date"]= pd.to_datetime(df["Date"]) # 10/11/1983 (string) to 1983-11-10

def Whether_lastday(date):

        date = pd.to_datetime(date) #string to datetime
        year = date.strftime('%Y') #f format 格式化 to string
        month = date.strftime('%m') # type(year&month) is string
        return date.strftime('%d')== str(calendar.monthrange(int(year), int(month))[1]) 
'''
year, month = 2016, 12
calendar.monthrange(year, month)[1]
[1] 返回此月的天数 [0] 返回第一天是星期几 
'''
           
df['Islast'] = ''    
df['Islast'] = df['Date'].apply(Whether_lastday) #true or false
#add a new column to record whether the date is the last day of a month
df1 = df[(df['Islast']==True)]
df_output = df1.iloc[:,[0,1,2,3]]
df_output.to_csv(path + '\output.csv',index = False) # 不写入行名




