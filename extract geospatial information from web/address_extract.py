#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:40:35 2017
《《《《《《 call the function load_file_data first, and then call other functions 》》》》》》
@author: hadoop
"""
import re
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

street_file=''
street_type_file=''
city_file=''
state_file=''
country_file=''
street={}
street_type=[]
street_direction=[]
max_street=0
    
#create street dictionary
def create_street_dict(street_file,street_type_file):#获得街道字典、街道类型和街道方向矩阵、街道名最大长度
    street_direction=[['n','north'],['s','south'],['w','west'],['e','east']]
    street_type=[]
    street={}
    max_street=0
    f1=open(street_type_file,'r')
    for s_t in f1:
        street_type.append(s_t.lower().split())
    f2=open(street_file,'r')
    num=0
    for s in f2:
        s_g=s.lower().split()
        size=len(s_g)
        if max_street<size:
            max_street=size
        s_street={}
        i=0
        for st in street_type:
            if s_g[-1]==st[0] or s_g[-1]==st[1]:
                s_street['type']=i
            i+=1
        j=0
        k=0
        for sd in street_direction:
            if s_g[0]==sd[0] or s_g[0]==sd[1]:
                s_street['direction']=j
                k=1
            j+=1
        name=''
        if k==0:
            name=' '.join(s_g[0:size-1])
            s_street['direction']=None
        if k==1:
            name=' '.join(s_g[1:size-1])
        while 1:
            if name in street:
                name+=' '
            else:
                break
        s_street['num']=num
        street[name]=s_street
        num+=1
    f1.close()
    f2.close()
    return street,street_type,street_direction,max_street

#load city name
def create_city_array(city_file):
    city=[]
    f=open(city_file,'r')
    data=f.readline()
    for d in data.split(' '):
        city.append(d)
    f.close()
    return city

#load state name
def create_state_array(state_file):
    state=[]
    f=open(state_file,'r')
    data=f.readline()
    for d in data.split(' '):
        state.append(d)
    f.close()
    return state
    
#load country name
def create_country_array(country_file):
    country=[]
    f=open(country_file,'r')
    data=f.readline()
    for d in data.split(' '):
        country.append(d)
    f.close()
    return country

#Initialize the data
def load_file_data(street_file1,street_type_file1,city_file1,state_file1,country_file1):
    global street_file
    street_file=street_file1
    global street_type_file
    street_type_file=street_type_file1
    global city_file
    city_file=city_file1
    global state_file
    state_file=state_file1
    global country_file
    country_file=country_file1
    global street,street_type,street_direction,max_street
    street,street_type,street_direction,max_street=create_street_dict(street_file,street_type_file)#得到街道字典数据

#extract address except extra information
def address_extract3(path):
    addresses=[]
    city=create_city_array(city_file)
    state=create_state_array(state_file)
    country=create_country_array(country_file)
    candidate_address=[]
    html_file=open(path,'r')
    html_data = html_file.read()
    raw = BeautifulSoup(html_data).get_text('\n','br/')
    temp2=re.compile(r'[^0-9a-zA-Z]')
    words=' '.join(re.sub(temp2,' ',raw).split())
    words1=words.split()
    pattern = re.compile(r'^[0-9]')
    i=0
    k=0
    n=0
    for w in words1:
        k=n
        if w.lower()==city[k].lower():
            n+=1
            if n==len(city):
                c_a=[]
                for j in range(max(0,i-max_street-len(city)-3),i+1):
                    c_a.append(words1[j])
                candidate_address.append(c_a)
                n=0
        i+=1
    for cand_add in candidate_address:
        for st1 in street:
            street_arr=[]
            street_arr.append(street[st1]['num'])
            st1_num=''
            st1_direction=''
            st1_name=''
            st1_type=''
            st1_city=' '.join(a for a in city)
            st1_state=' '.join(b for b in state)
            st1_country=' '.join(c for c in country)
            s_n_s=0
            s_n_e=0
            st=st1.split()
            i=0
            k=0
            n=0
            for c_ad in cand_add:
                k=n
                if c_ad.lower()==st[k]:
                    n+=1
                    if n==len(st):
                        s_n_s=i-len(st)+1
                        s_n_e=i+1
                    n=0
                i+=1
            st1_name=' '.join(i.capitalize() for i in st)
            if s_n_s>0 and s_n_e<len(cand_add):
                find_type=0
                find_direction=0
                find_num=0
                s_direction=street[st1]['direction']
                s_type=street[st1]['type']
                for s_t in street_type[s_type]:
                    if cand_add[s_n_e].lower()==s_t:
                        find_type=1
                st1_type=street_type[s_type][0].capitalize()
                if s_direction==None:
                    find_direction=1
                    if pattern.match(cand_add[s_n_s-1]):
                        find_num=1
                    if find_type==1 and find_direction==1 and find_num==1:
                        st1_num=cand_add[s_n_s-1]
                        address=' '.join(c for c in [st1_num,st1_direction,st1_name,st1_type,st1_city,st1_state,st1_country] if c!='')
                        street_arr.append(address)
                        addresses.append(street_arr)
                if s_direction!=None and s_n_s>1:
                    if pattern.match(cand_add[s_n_s-2]):
                        find_num=1
                    for s_d in street_direction[s_direction]:
                        if cand_add[s_n_s-1].lower()==s_d:
                            find_direction=1
                    if find_type==1 and find_direction==1 and find_num==1:
                        st1_num=cand_add[s_n_s-2]
                        st1_direction=street_direction[s_direction][0].capitalize()
                        address=' '.join(c for c in [st1_num,st1_direction,st1_name,st1_type,st1_city,st1_state,st1_country] if c!='')
                        street_arr.append(address)
                        addresses.append(street_arr)
    addresses1=[]
    for addres in addresses:
        if addres not in addresses1:
            addresses1.append(addres)
    return addresses1

#extract address contains extra information
def address_extract4(path):
    addresses=[]
    city=create_city_array(city_file)
    state=create_state_array(state_file)
    country=create_country_array(country_file)
    candidate_address=[]
    html_file=open(path,'r')
    html_data = html_file.read().decode('utf-8','ignore')
    raw = BeautifulSoup(html_data).get_text('\n','br/')
    temp2=re.compile(r'[^#0-9a-zA-Z]')
    #temp2=re.compile(r' ')
    words=' '.join(re.sub(temp2,' ',raw).split())
    words1=words.split()
    pattern = re.compile(r'^[0-9]')
    i=0
    k=0
    n=0
    for w in words1:
        k=n
        if w.lower()==city[k].lower():
            n+=1
            if n==len(city):
                c_a=[]
                for j in range(max(0,i-max_street-len(city)-3),i+1):
                    c_a.append(words1[j])
                candidate_address.append(c_a)
                n=0
        i+=1
    for cand_add in candidate_address:
        for st1 in street:
            street_arr=[]
            street_arr.append(street[st1]['num'])
            st1_num=''
            st1_direction=''
            st1_name=''
            st1_type=''
            st1_city=' '.join(a for a in city)
            st1_state=' '.join(b for b in state)
            st1_country=' '.join(c for c in country)
            s_n_s=0
            s_n_e=0
            st=st1.split()
            i=0
            k=0
            n=0
            for c_ad in cand_add:
                k=n
                #print c_ad.lower(),st[k]
                if c_ad.lower()==st[k]:
                    n+=1
                    if n==len(st):
                        s_n_s=i-len(st)+1
                        s_n_e=i+1
                        n=0
                i+=1
            #print cand_add
            st1_name=' '.join(i.capitalize() for i in st)
            if s_n_s>0 and s_n_e<len(cand_add):
                find_type=0
                find_direction=0
                find_num=0
                s_direction=street[st1]['direction']
                s_type=street[st1]['type']
                for s_t in street_type[s_type]:
                    if cand_add[s_n_e].lower()==s_t:
                        find_type=1
                st1_type=street_type[s_type][0].capitalize()
                if s_direction==None:
                    find_direction=1
                    if pattern.match(cand_add[s_n_s-1]):
                        find_num=1
                    if find_type==1 and find_direction==1 and find_num==1:
                        st1_num=cand_add[s_n_s-1]
                        ste=' '.join(cand_add[s_n_e+1:len(cand_add)-len(city)])
                        if ste!='':
                            if '#' not in ste and 'ste' not in ste.lower() and 'suite' not in ste.lower():
                                ste=''
                        address=' '.join(c for c in [st1_num,st1_direction,st1_name,st1_type,ste,st1_city,st1_state,st1_country] if c!='')
                        street_arr.append(address)
                        addresses.append(street_arr)
                if s_direction!=None and s_n_s>1:
                    if pattern.match(cand_add[s_n_s-2]):
                        find_num=1
                    for s_d in street_direction[s_direction]:
                        if cand_add[s_n_s-1].lower()==s_d:
                            find_direction=1
                    if find_type==1 and find_direction==1 and find_num==1:
                        st1_num=cand_add[s_n_s-2]
                        st1_direction=street_direction[s_direction][0].capitalize()
                        ste=' '.join(cand_add[s_n_e+1:len(cand_add)-len(city)])
                        if ste!='':
                            if '#' not in ste and 'ste' not in ste.lower() and 'suite' not in ste.lower():
                                ste=''
                        address=' '.join(c for c in [st1_num,st1_direction,st1_name,st1_type,ste,st1_city,st1_state,st1_country] if c!='')
                        street_arr.append(address)
                        addresses.append(street_arr)
    addresses1=[]
    for addres in addresses:
        if addres not in addresses1:
            addresses1.append(addres)
    return addresses1


    