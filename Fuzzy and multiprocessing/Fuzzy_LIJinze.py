# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 12:50:23 2021

@author: ljz
"""
#from joblib import Parallel, delayed
import time, os
#from multiprocessing import Pool
from fuzzywuzzy import fuzz
import pandas as pd

base_path = r'E:\codes for 7033\Final Project\Fuzzy and multiprocessing\data'

acquirers_data = pd.read_excel(base_path + os.sep + 'acquirers.xlsx')
banks_data = pd.read_csv(base_path + os.sep + 'bank_names.csv')
saved_file_name = base_path + os.sep + 'output.csv'

acquirers_data['acquirers'] = ''
acquirers_data['acquirers'] = acquirers_data['Acquirer Name'] + ' ' + acquirers_data['Acquirer State']
origin_firms = acquirers_data['acquirers']
#add new columns
#for i in range(5):
#    acquirers_data[str(i+1)] = ''

def Scores(aTuple):
    sc1 = fuzz.ratio(aTuple[0].lower(),aTuple[1].lower())
    sc2 = fuzz.partial_ratio(aTuple[0].lower(),aTuple[1].lower())
    sc3 = fuzz.token_sort_ratio(aTuple[0].lower(),aTuple[1].lower())
    sc4 = fuzz.token_set_ratio(aTuple[0].lower(),aTuple[1].lower())
    sc = (sc1 + sc2 + sc3 + sc4)/4
    return sc


def SortedSimilarity(aList,bList,num=5): 
    match_list = list(zip(aList,bList))  # list of tuple
    scored_list = list(map(lambda x: Scores(x), match_list))
    scored_dict = dict(zip(bList,scored_list)) #keys = bList / values = scroed_list
    sorted_list = sorted(scored_dict.items(), key=lambda x: x[1], reverse=True) # sorted by values        
    out_list = [v for v in sorted_list[0:num]]
    output_list = list(dict(out_list).keys())
    return output_list # bList and scores list of tuple 
        
start_time = time.time()
#def mainFunction(ticker):
#pd.DataFrame()
Total_list = []
for index in range(len(acquirers_data)):
    
    firm = acquirers_data.at[index,'acquirers'] #pick a firm    
    acquirer_list = []
    acquirer_list = [str(firm)]*len(banks_data['bank_names'].tolist())
    banks_list = banks_data['bank_names'].tolist()
    #use a list of tuple preparing for matching
    if index % 10 == 0:
        print("matched "+str(index+1)+ 'firms')
    try:
        Total_list.append(SortedSimilarity(acquirer_list,banks_list,num=5))
    except:
        continue

df2 = pd.DataFrame(Total_list)#list of list to dataframe by rows
df_out = pd.concat([origin_firms.to_frame(), df2], axis=1)
df_out.to_csv(saved_file_name,index = False)


#if __name__ == '__main__':
#    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
#p = Pool(processes=3)
#acquirers_dataout = p.map(mainFunction, range(len(acquirers_data)))
#p.close()
#p.join()  
#Parallel(n_jobs=3)(delayed(mainFunction)(ticker) for ticker in range(len(acquirers_data)))       
#    df_out = acquirers_dataout
#    df_out.to_csv(saved_file_name,index = False) # 不写入行名  
#print("--- %s seconds ---" % (time.time() - start_time))