# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 18:17:36 2021

@author: ljz
"""

import datetime
starttime = datetime.datetime.now()
import pandas as pd
import os
import numpy as np

path = r'E:\codes for 7033\Final Project\Data transformation\data'
path_input = os.path.join(path,'deal_level_data.csv')

df_old = pd.read_csv(path_input,float_precision='round_trip')

# starting from quarter -12 
def Numbers(inputString):
    return any(var.isdigit() for var in inputString)

# create a list contains the columns of quarter
# get cols without numbers and Acq
my_quarter_level_col = []
for col in df_old.columns: 
    if not Numbers(col) and "Acq_" not in col:
        my_quarter_level_col.append(col)
#        print(col) 
#print(len(my_quarter_level_col)) 41
my_quarter_level_data = my_quarter_level_col.copy() #41
quarter_level_col = my_quarter_level_data[15:]  #13
my_quarter_level_data.insert(14,'quarter_to_the_event_date') #42
my_quarter_level_data = pd.DataFrame(columns=my_quarter_level_data) #create a df
quarter_date_string = ['__12', '__11', '__10', '__9', '__8', '__7', '__6', '__5', '__4', '__3', '__2', "__1",
                '', '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8', '_9', '_10', '_11', "_12"]
quarter_date_number = [i for i in range(-12,13)]
#quarter_date_number = [-12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1,
#                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
col_14 = my_quarter_level_col[:14] # first 14
#np.repeat(df)
df_new1 = pd.DataFrame(np.repeat(df_old.iloc[:,0:14].values,25,axis=0),columns = col_14 ) # top 14 finished

# add 15th columns
count = 0 
for index, row in df_new1.iterrows():
    df_new1.at[count, 'quarter_to_the_event_date'] = quarter_date_number[count%25]
    count +=1
    if count > len(df_new1):
        break
   
df_new1['quarter'] = ''
df_13month = df_old.iloc[:,14:27] # last 13 columns
df_13month_r = df_13month.iloc[:,::-1] # reversed 
df_quarter_data  = pd.concat([df_13month_r,df_old.iloc[:,27:39] ], axis=1) #左右拼接

#add 16th columns
df_quarter_data_array = df_quarter_data.values
df_quarter_data_array1 = df_quarter_data_array.reshape(1,-1) #flat by row
df_quarter_data_list = df_quarter_data_array1.tolist() #1d array [[1,2,4,6]]
df_quarter_data_list = [i for i in df_quarter_data_list[0]]
#解释这部分
#import itertools
#df_quarter_data_list1 = list(itertools.chain.from_iterable(df_quarter_data_list))
#df_new1['quarter'] = df_quarter_data_list1

#last 26th columns label and sort to new
#quarter_level_newcol = []
#for i in range(10,23):
#    quarter_level_newcol.append(quarter_level_col[i])
#del quarter_level_col[10 : 23]
#quarter_level_newcol = quarter_level_newcol + quarter_level_col 
quarter_level_newcol = ['Com_Net_Charge_Off', 'Com_Insider_Loan', 'Com_NIE', \
                         'Com_NII', 'Com_NIM', 'Com_ROA', 'Com_Total_Assets', \
                         'Com_AvgSalary', 'Com_EmployNum', 'Com_TtlSalary',\
                         'Com_AvgSalary_log', 'Com_EmployNum_log', 'Com_TtlSalary_log',\
                         'Tar_Net_Charge_Off', 'Tar_Insider_Loan', 'Tar_NIE', 'Tar_NII', \
                         'Tar_NIM', 'Tar_ROA', 'Tar_Total_Assets','Tar_AvgSalary', 'Tar_EmployNum', 'Tar_TtlSalary',\
                         'Tar_AvgSalary_log', 'Tar_EmployNum_log', 'Tar_TtlSalary_log']
#pick useful cols in the old for the last 26th cols    
quarter_col_inold = []
for j in quarter_date_string:    
    for i in quarter_level_newcol:
            quarter_col_inold.append(str(i+j))
#list of list 25*26
quarter_col_inold_dim2 = np.array(quarter_col_inold).reshape(25,26).tolist()

df_pick =  df_old.loc[:, quarter_col_inold]
#numpy array 2 dimensions
df_pickdim3 = (df_pick.values).reshape(3005,25,26) #
#(3005,650) -> (3005*25,26)

df_2 = df_pickdim3.reshape(-1, df_pickdim3.shape[-1])
df2 = pd.DataFrame(df_2, index = df_new1.index, columns = quarter_level_newcol)
# align by line 
df_end = pd.concat([df_new1,df2], axis = 1, ignore_index = False, join = "outer")
df_end.to_csv(path + '\output.csv',index = False) # 不写入行名
endtime = datetime.datetime.now()
print('You spend '+ str((endtime - starttime).seconds) + ' seconds to finish it.')
