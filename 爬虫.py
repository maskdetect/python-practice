import requests
from lxml import etree
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import json
import matplotlib.font_manager as font_manager


proxy_list = [
    { "http": "http://113.195.23.2:9999" },
    { "http": "http://39.84.114.140:9999" },
    { "http": "http://110.243.7.29:9999" },
    { "http": "http://27.188.65.244:8060" }]

#//div[@class="sub-Aritst-Area"]/dl//li/a/text()
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
url = 'https://amma.artron.net/artronindex_artist.php'

page_text = requests.get(url=url,headers=headers,proxies=random.choice(proxy_list)).content.decode('utf-8')
#把网页便变成xpath结构
tree = etree.HTML(page_text)
artlist = tree.xpath('//div[@class="sub-Aritst-Area"]/dl//li/a/text()')

#https://baike.baidu.com/item/%E6%9D%8E%E5%8F%AF%E6%9F%93/331468?fr=aladdin
a=0
artlist_nn=[]
dfz=pd.DataFrame(columns=['n','r','m'])

for i in artlist :
    try:
        #time.sleep(1)
        url = 'https://baike.baidu.com/item/'+i
        page_text = requests.get(url=url,headers=headers,proxies=random.choice(proxy_list)).content.decode('utf-8')
        #把网页便变成xpath结构
        tree = etree.HTML(page_text)
        re =tree.xpath('//div[@class="lemma-relation-module viewport"]/ul/li/a/div/span[@class="name"]/text()')
        na =tree.xpath('//div[@class="lemma-relation-module viewport"]/ul/li/a/div/span[@class="title"]/text()')
        if len(re) != 0:
            artlist_nn.append(i)
            df = pd.DataFrame()
            a=a+1
            print(a)
            df['n']=0
            df['r']=re
            df['n']=i
            df['m']=na
            dfz=pd.concat([dfz,df],axis=0,ignore_index=True)
            #df.to_csv('result/'+i+'.csv',encoding='utf-8')
            dfz.to_csv('result.csv',encoding='utf-8')
    except:
        print('爬取失败')
        pass
    continue




