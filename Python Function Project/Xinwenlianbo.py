# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 11:57:37 2021

@author: ljz
"""

import tushare as ts
import pandas as pd
import time,os
import jieba
import nltk
import matplotlib.pyplot as plt
from numpy import random

pro = ts.pro_api()
ts.set_token('947370352888ee063dd8b3259bef941510dc39d8f4552156ce3b896e')
pro = ts.pro_api('947370352888ee063dd8b3259bef941510dc39d8f4552156ce3b896e')


df_1 = pro.cctv_news(date='20200101')
#https://developer.huawei.com/consumer/cn/forum/topic/0201438450459330292
content1 = []
content1.append(df_1['content'].tolist())
str_content1 = str(content1[0])
#seg_list111 = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
#print(", ".join(seg_list111)) #搜索引擎模式
seg_list1 = jieba.cut(str_content1,cut_all=False) #generator 
# True means retain all the meaning ful cut, False only retain one format
list1=[]
for i in seg_list1:
    list1.append(i)
#seg_list1 = jieba.cut(str_content1, cut_all=False)
#print(" ".join(seg_list1))#join and convert to a str
                                 

text1=nltk.text.Text(list1)  
text1.concordance('新年') #搜索指定词语
text1.dispersion_plot(["新","新年","国家","欢乐","健康"])# 画图
fdist1=nltk.FreqDist(text1)
plt.rcParams['font.sans-serif']=['SimHei']
fdist1.plot(35,cumulative=True)
#==============================================================================

#选取本年(0101)到任意一天(1120)新闻联播数据
date_data = pd.period_range("2021-01-01","2021-11-20")
date_data = date_data.to_series().astype(str) # '2021-01-01' series

for i in date_data:
    date_data[i] = str(date_data[i])

date_data = date_data.tolist()
for i in range(len(date_data)):
    date_data[i] = date_data[i].replace("-",'')
    
path = r'E:\codes for 7033\Final Project\CCTVnews'
for i in date_data:
    path_date = os.path.join(path,i)
    os.mkdir(path_date)  

pro = ts.pro_api()
ts.set_token('947370352888ee063dd8b3259bef941510dc39d8f4552156ce3b896e')
pro = ts.pro_api('947370352888ee063dd8b3259bef941510dc39d8f4552156ce3b896e')


for i in date_data:
    df = pro.cctv_news(date=i)
    pathone = os.path.join(path,i)
    pathtwo = str(i)+".csv"
    thepath = os.path.join(pathone,pathtwo)
    df.to_csv(thepath)
    print("have written {} news".format(i))
    del df
    time.sleep(random.uniform(31,33))
#接口访问频率限制 30秒一次



#content1 = []
#content1.append(df_1['content'].tolist())
#str_content1 = str(content1[0])
import os
import pandas as pd
import nltk
path = r'E:\codes for 7033\Final Project\CCTVnews'


for i in date_data:
    path_date = os.path.join(path,i)
    df_date = pd.read_csv(path_date + os.sep + i + ".csv") 
    
    content = []
    content.append(df_date['content'].tolist())
    str_content = str(content[0])
    
    file = open(path_date + os.sep + i + ".txt",'w',encoding='utf-8')
    file.write(str_content)
    file.close()
        
    del df_date
    print(str(i) + " .txt have finished ")



from pyecharts import options as opts
from pyecharts.charts import Map
#from pyecharts.faker import Faker
import jieba
import json, os
import pandas as pd
path = r'E:\codes for 7033\Final Project\CCTVnews'
provinces = ['北京','天津','河北','山西','内蒙古','辽宁','吉林','黑龙江','上海','江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','广东','广西','海南','重庆','四川','贵州','云南','陕西','甘肃','青海','宁夏','新疆','香港','澳门','台湾','西藏']
All_dict = {}
for var in provinces:
    All_dict[var] = 0 

# half year data
date_data = pd.period_range("2021-01-01","2021-06-30")
date_data = date_data.to_series().astype(str) # '2021-01-01' series

for i in date_data:
    date_data[i] = str(date_data[i])

date_data = date_data.tolist()
for i in range(len(date_data)):
    date_data[i] = date_data[i].replace("-",'')

#读取txt并统计
for i in date_data:
    path_date = os.path.join(path,i)

    file = open(path_date + os.sep + i + ".txt", 'r',encoding="utf-8")
    date_content = []    
    date_content = list(jieba.cut(str(file.read()), cut_all = True))         
    count_dict = {}
    for word in date_content:
        if word in provinces:
            count_dict[word] = count_dict.get(word,0) + 1
    
#    All_dict.update(count_dict)
    for k,v in count_dict.items():
        All_dict[k] += v
    
    file = open(path_date + os.sep + i + "_dict.txt",'w',encoding="utf-8")
    file.write(json.dumps(count_dict,ensure_ascii=False))
    file.close()
    del date_content
    print(i)


province = list(All_dict.keys())
values = [i/10 for i in All_dict.values()]
#{'西藏'：150,'北京': 968, '天津': 136, '河北': 252, '山西': 94, '内蒙古': 124, '辽宁': 78, '吉林': 93, '黑龙江': 120, '上海': 349, '江苏': 191, '浙江': 253, '安徽': 128, '福建': 150, '江西': 188, '山东': 182, '河南': 94, '湖北': 130, '湖南': 139, '广东': 190, '广西': 116, '海南': 191, '重庆': 160, '四川': 169, '贵州': 154, '云南': 117, '陕西': 139, '甘肃': 116, '青海': 115, '宁夏': 80, '新疆': 390, '香港': 591, '澳门': 123, '台湾': 27}
c = (
    Map()
    .add("CCTV1 新闻联播 from 2021-01-01 to 2021-06-30 (numbders divided by 10)", [list(z) for z in zip(province, values)], "china")
    .set_global_opts(title_opts=opts.TitleOpts(title="中国地图"),visualmap_opts=opts.VisualMapOpts())
    .render("CCTV_provience_map.html")
)


os.system("CCTV_provience_map.html")










#V=nltk.(text)
#sorted(V.keys())
#from nltk.tokenize import sent_tokenize
#mytext = "Hello Adam, how are you? I hope everything is going well. Today is a good day, see you dude."
#print(sent_tokenize(mytext,True))
#
#from nltk.corpus import stopwords
#tokens=[ 'my','dog','has','flea','problems','help','please',
#         'maybe','not','take','him','to','dog','park','stupid',
#         'my','dalmation','is','so','cute','I','love','him'  ]
# 
#clean_tokens=tokens[:]
#stwords=stopwords.words('english')
#for token in tokens:
#    if token in stwords:
#        clean_tokens.remove(token)
# 
#print(clean_tokens)

#
#fdist = nltk.FreqDist(text1)
#fdist.plot(10) # plot the most 10
#fdist1.most_common(15) #return a list of tuple
#from nltk.corpus import stopwords
#tokens=[ 'my','dog','has','flea','problems','help','please',
#         'maybe','not','take','him','to','dog','park','stupid',
#         'my','dalmation','is','so','cute','I','love','him'  ]
# 
#clean_tokens=tokens[:]
#stwords=stopwords.words('english')
#for token in tokens:
#    if token in stwords:
#        clean_tokens.remove(token)
# 
#print(clean_tokens)

