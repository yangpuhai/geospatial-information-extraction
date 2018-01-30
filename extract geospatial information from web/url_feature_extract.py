# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:50:56 2017

@author: yangpuhai
"""
import re

#break down url
def break_up_url(url):
    url_data=[]
    separator1=re.compile(r'[(://)(\.)(/)]')
    separator2=re.compile(r'[^a-zA-Z0-9]+')
    url_1=re.sub(separator1,' ',url)
    i=0
    for u in url_1.split():
        url_data.append([])
        url_2=re.sub(separator2,' ',u)
        for w in url_2.split():
            url_data[i].append(w)
        i+=1
    return url_data

#extract features from url
def url_feature_extract(url):
    f1=0
    f21=0
    f22=0
    f3=0
    f4=0
    #f5=0
    f6=0
    f7=0
    url_data=break_up_url(url)
    f1=len(url_data)
    i=0
    k=0
    max_str=[]
    max_str_i=0
    for u in url_data:
        i+=1
        j=0
        if len(u)>len(max_str):
            max_str=u
            max_str_i=i
        for w in u:
            j+=1
            if re.match(r'[0-9]+',w):
                if k<1:
                    f21=i
                    f22=j
                k+=1
            #if re.match(r'http[s]?',w):
            #    f5=i
            if re.match(r'www',w):
                f6=i
            if re.match(r'com',w):
                f7=i
    f4=len(max_str)
    if f21==max_str_i:
        f3=1
    return [f1,f21,f22,f3,f4,f6,f7]

