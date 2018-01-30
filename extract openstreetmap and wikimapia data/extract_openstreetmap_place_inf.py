# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:21:07 2017

@author: yangpuhai
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

reload(sys)
sys.setdefaultencoding('utf-8')

Houston_box='houston,-95.41870,29.71465,-95.41464,29.71930'
Chicago_box='Chicago,-87.65490,41.88257,-87.64660,41.88615'
error_response='You requested too many nodes (limit is 50000). Either request a smaller area, or use planet.osm'
box=[Houston_box,Chicago_box]

def download_place_inf(left,bottom,right,top):
    inf=[]
    mid_l_r=(left+right)/2.0
    mid_b_t=(bottom+top)/2.0
    url='http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s'%(left,bottom,right,top)
    data=requests.get(url).content
    if data!=error_response:
        soup=BeautifulSoup(data,'html.parser')
        nodes=soup.find_all('node')
        for node in nodes:
            name=node.find('tag',k='name')
            if name:
                place=[]
                n=name.get('v')
                place.append(n)
                typ=node.find('tag',k='amenity')
                if typ:
                    t=typ.get('v')
                    place.append(t)
                else:
                    place.append('')
                lon=node.get('lon')
                lat=node.get('lat')
                place.append(lon)
                place.append(lat)
                if n not in [i[0] for i in inf]:
                    inf.append(place)
    else:
        for a in download_place_inf(left,mid_b_t,mid_l_r,top)+download_place_inf(left,bottom,mid_l_r,mid_b_t)+download_place_inf(mid_l_r,bottom,right,mid_b_t)+download_place_inf(mid_l_r,mid_b_t,right,top):
            if a[0] not in [i[0] for i in inf]:
                inf.append(a)
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
        f=open(name+'_openstreetmap_inf.csv','wb')
        writer = csv.writer(f)
        writer.writerow(['name','type','lon','lat'])
        for i in inf:
            writer.writerow(i)
        f.close()

if __name__ == '__main__':
    save_place_inf(box)
    
    
    
    
    
    