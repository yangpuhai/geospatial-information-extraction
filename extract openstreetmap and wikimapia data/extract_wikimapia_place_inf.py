# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 00:36:28 2018

@author: yangpuhai
"""
import sys
import requests
from bs4 import BeautifulSoup
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

Houston_box='houston,-95.41870,29.71465,-95.41464,29.71930'
New_York_box='New York,-74.0119,40.7253,-74.0044,40.7303'
Chicago_box='Chicago,-87.65490,41.88257,-87.64660,41.88615'
San_Francisco_box='San Francisco,-122.42700,37.77525,-122.42013,37.77920'
box=[Houston_box,New_York_box,Chicago_box,San_Francisco_box]

base_url='http://api.wikimapia.org/?function=box&bbox=%s,%s,%s,%s&format=xml&key=8A006943-3013DFAE-AB18C1B2-288DEE68-6101AAA6-4DAE7C05-25836D72-6695F122&count=%s&page=%s'

def download_place_inf(left,bottom,right,top):
    inf=[]
    url_test=base_url%(left,bottom,right,top,1,1)
    data_test=requests.get(url_test).content
    soup_test=BeautifulSoup(data_test,'html.parser')
    count=soup_test.find('folder').get('found')
    url=base_url%(left,bottom,right,top,count,1)
    data=requests.get(url).content
    soup=BeautifulSoup(data,'html.parser')
    nodes=soup.find_all('place')
    for node in nodes:
        place=[]
        place.append(node.get('id'))
        place.append(node.find('name').get_text())
        place.append(node.find('lon').get_text())
        place.append(node.find('lat').get_text())
        inf.append(place)
    return inf


def save_place_inf(box):
    for b in box:
        bb=b.split(',')
        name=bb[0]
        left=float(bb[1])
        bottom=float(bb[2])
        right=float(bb[3])
        top=float(bb[4])
        inf=download_place_inf(left,bottom,right,top)
        f=open(name+'_wikimapia_inf.csv','wb')
        writer = csv.writer(f)
        writer.writerow(['id','name','lon','lat'])
        for i in inf:
            writer.writerow(i)
        f.close()

if __name__ == '__main__':
    save_place_inf(box)

