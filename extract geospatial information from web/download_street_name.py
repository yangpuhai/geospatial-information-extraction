# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 11:18:09 2017

@author: yangpuhai
"""
import os
import requests
from bs4 import BeautifulSoup

Houston_box='houston,-95.41870,29.71465,-95.41464,29.71930'
New_York_box='New York,-74.0119,40.7253,-74.0044,40.7303'
Chicago_box='Chicago,-87.65490,41.88257,-87.64660,41.88615'
San_Francisco_box='San Francisco,-122.42700,37.77525,-122.42013,37.77920'
box=[Houston_box,New_York_box,Chicago_box,San_Francisco_box]

error_response='You requested too many nodes (limit is 50000). Either request a smaller area, or use planet.osm'

def download_street_name(left,bottom,right,top):
    street=[]
    city=[]
    state=[]
    country=[]
    mid_l_r=(left+right)/2.0
    mid_b_t=(bottom+top)/2.0
    url='http://api.openstreetmap.org/api/0.6/map?bbox=%s,%s,%s,%s'%(left,bottom,right,top)
    data=requests.get(url).content
    if data!=error_response:
        soup=BeautifulSoup(data,'html.parser')
        way=soup.find_all('way')
        street_type=[]
        f2=open('street_type','r')
        street_type_data=f2.readlines()
        f2.close()
        for s_t in street_type_data:
            for s in s_t.strip('\n\t').split(' '):
                street_type.append(s.lower())
        for w in way:
            name=w.find('tag',k='name')
            if name:
                n=name.get('v')
                if n not in street and n.split(' ')[-1].lower() in street_type:
                    street.append(n)
        info=soup.find_all()
        for i in info:
            name1=i.find('tag',k='addr:street')
            if name1:
                n1=name1.get('v')
                if n1 not in street and n1.split(' ')[-1].lower() in street_type:
                    street.append(n1)
        
        city_data=soup.find_all('tag',k='addr:city')
        for c in city_data:
            city.append(c.get('v'))
            break
        state_data=soup.find_all('tag',k='addr:state')
        for s in state_data:
            state.append(s.get('v'))
            break
        country_data=soup.find_all('tag',k='addr:country')
        for co in country_data:
            country.append(co.get('v'))
            break
    else:
        for a in download_street_name(left,mid_b_t,mid_l_r,top)+download_street_name(left,bottom,mid_l_r,mid_b_t)+download_street_name(mid_l_r,bottom,right,mid_b_t)+download_street_name(mid_l_r,mid_b_t,right,top):
            for st in a[0]:
                if st not in street:
                    street.append(st)
            for cit in a[1]:
                if cit not in city:
                    city.append(cit)
            for sta in a[2]:
                if sta not in state:
                    state.append(sta)
            for cou in a[3]:
                if cou not in country:
                    country.append(cou)
    return [[street,city,state,country]]

def save_street_inf(box):
    for b in box:
        bb=b.split(',')
        name=bb[0]
        left=float(bb[1])
        bottom=float(bb[2])
        right=float(bb[3])
        top=float(bb[4])
        inf=download_street_name(left,bottom,right,top)
        if os.path.exists(name)==False:
            os.mkdir(name)
        f1=open(name+'/street','a')
        f2=open(name+'/city','a')
        f3=open(name+'/state','a')
        f4=open(name+'/country','a')
        for n in inf:
            for s in n[0]:
                f1.write(s)
                f1.write('\n')
            for c in n[1]:
                f2.write(c)
                f2.write('\n')
            for st in n[2]:
                f3.write(st)
                f3.write('\n')
            for co in n[3]:
                f4.write(co)
                f4.write('\n')
            f1.close()
            f2.close()
            f3.close()
            f4.close()
            
if __name__ == '__main__':
    save_street_inf(box)


