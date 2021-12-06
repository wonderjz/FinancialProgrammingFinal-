# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 19:28:41 2021

@author: ljz
"""
import requests
import json
#e4GON5RMfylWGUosZLxPntA1IoTyDWJ4
path = r'E:\codes for 7033\Final Project\TomTom API geolocation\data'
import os 
import pandas as pd
path1 = os.path.join(path, 'coname_addresses.xlsx')
df = pd.read_excel(path1)  #读取数据时注意索引

addr = df['address'].tolist()
#addr1 = [i for i in df['address']]
df['lat'] = ''
df['lon'] = ''
#print(set(df.index.tolist())-set([i for i in range(len(df))])) # 只能找出missing 的数量 定位不了

# check the len(df) and index, there are some missing values.
for i in range(len(df)):
    
    #response = requests.get("https://api.tomtom.com/search/2/geocode/" +str(addr[i])+".json?contrySet=usa&minFuzzyLevel=1&maxFuzzyLevel=3&key=uQ4JeAGmQPOglcObkVFkOALdW46S0dNf")
    try:
        response = requests.get('https://api.tomtom.com/search/2/geocode/'+str(addr[i])+".json?&minFuzzyLevel=1&maxFuzzyLevel=3&key=9mc3DJ859nSBPw8e08L7lWUxRSEislCZ")
        res = json.loads(response.text)    
        df.iloc[i,2] = res['results'][0]['position']['lat']
        df.iloc[i,3]= res['results'][0]['position']['lon']
        del res
        print('finished_'+str(i))

    except:       
        print("An exception occurred")
df.to_csv(path + '\output_final.csv',index = False) # 不写入行名 
#
#https://<baseURL>/search/<versionNumber>/geocode/<query>.<ext>?key=<Your_API_Key>[&storeResult=<storeResult>][&typeahead=<typeahead>][&limit=<limit>][&ofs=<ofs>][&lat=<lat>][&lon=<lon>][&countrySet=<countrySet>][&radius=<radius>][&topLeft=<topLeft>][&btmRight=<btmRight>][&language=<language>][&extendedPostalCodesFor=<extendedPostalCodesFor>][&view=<view>][&mapcodes=<mapcodes>][&entityTypeSet=<entityTypeSet>]
#
#https://api.tomtom.com/search/2/geocode/台北市中正區羅斯福路一段15號.json?countrySet=TW&language=zh-TW&key=**your key**
#e4GON5RMfylWGUosZLxPntA1IoTyDWJ4
path = r'E:\codes for 7033\Final Project\TomTom API geolocation\data'
import os 
import pandas as pd
path1 = os.path.join(path, 'output_final.csv')
df = pd.read_csv(path1)  #读取数据时注意索引
#path1 = os.path.join(path, 'coname_addresses.xlsx')
#df = pd.read_excel(path1)  #读取数据时注意索引
from geopy import distance
import numpy as np

df['distance']=''
#lat 纬度
xlist = df['lat'].tolist()
ylist = df['lon'].tolist()
label = list(zip(xlist,ylist))
whitehouse = (38.8976763, -77.0387185)
aList = []
for i in range(len(label)):
    if df.iloc[i:3] is np.nan:
#        pd.isnull(df.iloc[890,4])
        continue
    else:
        try:
            print(distance.distance(whitehouse, label[i]))
            df['distance'][i] = str(distance.distance(whitehouse, label[i]))
            aList.append(str(distance.distance(whitehouse, label[i])))
            print('finished_' + str(i))
        except:
            print("An exception occurred")

#wellington = (-41.32, 174.81)
#salamanca = (40.96, -5.50)
#print(distance.distance(wellington, salamanca).km)
#19959.6792674
df_out = df
df_out.to_csv(path + '\output_final1.csv',index = False) # 不写入行名  