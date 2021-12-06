# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 17:09:19 2021

@author: ljz
"""

import pandas as pd
import os
import nltk
import matplotlib.pyplot as plt


path = r'E:\GitHub\CPED_V1.0'
path_full = os.path.join(path,'Full Data.xlsx')  
# numbers = 4058

df_basic = pd.read_excel(path_full, sheet_name='基本信息')
df_experience = pd.read_excel(path_full, sheet_name='全部经历')
#df_basic.describe()


Names = df_basic['姓名'].tolist()
df_corrup = df_basic[(df_basic['现状'] == '降/撤/辞职') | (df_basic['现状'] == '立案查处')]
df_nocorrup = df_basic[(df_basic['现状'] != '降/撤/辞职') & (df_basic['现状'] != '立案查处')]

#dfa = pd.pivot_table(df_basic,index=[u'性别',u'民族'],values=[u'现状'])

#pd.pivot_table(df,index=[u'主客场',u'胜负'],values=[u'得分',u'助攻',u'篮板'])
#词频统计
HomeTowns = df_basic['籍贯省'].tolist()
Freq_dist_nltk=nltk.FreqDist(HomeTowns)
#print(Freq_dist_nltk)
HomeDict = {}
for k,v in Freq_dist_nltk.items():
    HomeDict[str(k)] = v
print(HomeDict)

CorHomeTown = df_corrup['籍贯省'].tolist()
Freq_dist_Cor=nltk.FreqDist(CorHomeTown)
CorHomeDict = {}
for k,v in Freq_dist_Cor.items():
    CorHomeDict[str(k)] = v
    
def draw_from_dict(dicdata,RANGE, heng):
    #dicdata：字典的数据。
    #RANGE：截取显示的字典的长度。
    #heng=0，代表条状图的柱子是竖直向上的。heng=1，代表柱子是横向的。考虑到文字是从左到右的，让柱子横向排列更容易观察坐标轴。
    by_value = sorted(dicdata.items(),key = lambda item:item[1],reverse=True)
    x = []
    y = []
    for d in by_value:
        x.append(d[0])
        y.append(d[1])
    if heng == 0:
        plt.bar(x[0:RANGE], y[0:RANGE])
        plt.show()
        return 
    elif heng == 1:
        plt.barh(x[0:RANGE], y[0:RANGE],color = 'r' )
        plt.title("Corrupt_political leader's governing area") # remember to change
        plt.xlabel('Frequent')
        plt.ylabel('Provience')
        plt.colors('red')
        plt.figure(figsize=(10, 12))
        plt.show()
        plt.savefig('1.png')
        
        return 
    else:
        return "heng is 0 or 1"


#plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
#plt.rcParams['axes.unicode_minus']=False #用来正常显示负号)
# 籍贯  所在的省份  官员腐败的概率 
CorFrequentDict = {k : v/HomeDict[k] for k, v in CorHomeDict.items() if k in HomeDict} 
print(CorFrequentDict)
draw_from_dict(CorFrequentDict,len(CorHomeDict),heng=1)
# 计算平均中心地理位置
#每个人的初始位置index 和 末尾位置index
picklist_last = []
for i in range(2,len(df_basic)+1):
    try:
        picklist_last.append(df_experience['用户编码'].tolist().index(i)-1)
    except:
        continue

picklist_first = []
for i in range(len(df_basic)):
    try:
        picklist_first.append(df_experience['用户编码'].tolist().index(i))
    except:
        continue
#print(df_experience.iloc[41,:])

# 最后主政地区  所在的省份  官员腐败的概率 
last_GovTown = []
for i in picklist_last:
    last_GovTown.append(df_experience.at[i, '地方一级关键词'])

Freq_dist_Last=nltk.FreqDist(last_GovTown)
LastTownDict = {}
for k,v in Freq_dist_Last.items():
    LastTownDict[str(k)] = v
CorFrequentDict_Last = {k : v/LastTownDict[k] for k, v in CorHomeDict.items() if k in LastTownDict} 
CorFrequentDict_Last.pop('nan')

draw_from_dict(CorFrequentDict_Last,len(CorFrequentDict_Last),heng=1) #修改标题

biaozhiwei = list(set(df_experience['标志位'].tolist()))
daleibie = list(set(df_experience['基本大类别'].tolist()))
biaozhiwei.remove('无')

PersonTuple = list(zip(picklist_first,picklist_last))
Promotion = {}
for index in range(len(PersonTuple)):
    First = PersonTuple[index][0]
    Last = PersonTuple[index][1]
    PersonPromotion = []
    for j in range(First,Last+1):
        if df_experience.iloc[j,22] != '无': #标志位
            if not df_experience.iloc[j,22] in PersonPromotion:
                    PersonPromotion.append(df_experience.iloc[j,22])
    PersonNumber = df_experience.iloc[First,0] 
    Promotion[PersonNumber] =  PersonPromotion
    
#for i in range Promotion







