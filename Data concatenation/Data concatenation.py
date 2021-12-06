# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 15:04:49 2021

@author: ljz
"""
import os
import pandas as pd
import numpy as np

path = r'E:\codes for 7033\Final Project\Data concatenation\data'
path1 = os.path.join(path,'2014.csv')
path2 = os.path.join(path,'2015.csv')

df1 = pd.read_csv(path1)
df2 = pd.read_csv(path2)
#print(df1.shape[0])
#print(df2.shape[0])
df_output = df1.append(df2, ignore_index=True)
#print(df_output.shape[0]) # count the rows 

df_output.to_csv(path + '\output.csv',index = False) # 不写入行名