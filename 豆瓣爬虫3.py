import sys
sys.path.append('/home/aistudio/external-libraries')
import json
import re
import requests
import datetime
from bs4 import BeautifulSoup
import os

import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
url = 'https://read.douban.com/provider/all'

try:
    proxy_list = [
        {"http": "http://152.136.62.181:9999"},
        {"http": "http://39.84.114.140:9999"},
        {"http": "http://110.243.7.29:9999"},
        {"http": "http://27.188.65.244:8060"}
    ]
    response = requests.get(url,headers=headers,proxies=random.choice(proxy_list))
    # 将一段文档传入BeautifulSoup的构造方法,就能得到一个文档的对象, 可以传入一段字符串
    soup = BeautifulSoup(response.text, 'lxml')

    # 返回所有的<table>所有标签
    #
    publishes = soup.find_all('div', {'class': 'provider-group'})# 找到所有的<div class="provider-group">标签
    print(len(publishes))# 打印出来的是所有的<div class="provider-group">标签的个数
    pbs = []# 定义一个空列表
    for index, pb in enumerate(publishes):
        # if (index<=1): # 只取前两个
        if True:# 取所有
            pb_list = {}# 定义一个空字典
            pb_list['item_name'] = pb.find_next('div').text# 找到<div class="provider-group">标签的下一个<div>标签的内容
            item_list = []# 定义一个空列表
            p = pb.find_next('ul')# 找到<div class="provider-group">标签的下一个<ul>标签
            li_s = p.find_all('li')# 找到<ul>标签的所有<li>标签

            # print(l[0])
            for li in li_s:
                item_li = {}# 定义一个空字典
                item_li['href'] = 'https://read.douban.com' + li.find_next('a').get('href')#找到<li>标签的下一个<a>标签的href属性
                # item_li['others']=li.find_next('div').find_next('div').find_next_sibling('div')
                item_detail = li.find_next('div').find_next('div').find_next_sibling('div')# 找到<li>标签的下一个<div>标签的下一个<div>标签的下一个<div>标签的内容
                # print(item_detail)# 打印出来的是<div class="provider-item-detail">标签的内容
                pb_name = item_detail.find_next('div')
                item_li['pb_name'] = pb_name.text
                # print(pb_name.text)
                pb_count_str = pb_name.find_next_sibling('div').text
                idx = pb_count_str.find(' ')
                pb_count_str = pb_count_str[0:idx]
                # print(pb_count_str)
                item_li['pb_count'] = pb_count_str

                item_list.append(item_li)
                # print(li.find_next('div').find_next('div').find_next_sibling('div'))
                # print(li.find_next('div').find_next_sibling('div'))
            pb_list['item_list'] = item_list
            # print(pb_list)
            pbs.append(pb_list)# 将字典添加到列表中
    print(len(pbs))
    # json_data = json.loads(str(pbs))
    json_data = json.loads(str(pbs).replace("\'", "\"").replace("\\xa0", ""))# 将字符串转换成json格式
    with open('work/' + 'pbs.json', 'w', encoding='UTF-8') as f:# 将列表写入json文件中
        json.dump(json_data, f, ensure_ascii=False)# 将列表写入json文件中


except Exception as e:
    print(e)