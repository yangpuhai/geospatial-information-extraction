# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:50:56 2017

@author: yangpuhai
"""
import re
import difflib
key_words1='el segundo'
key_words2='california'
def break_up_url(url):  #将url分解
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

def delete_noisy_data(url_data):  #清除url中的干扰数据
    separator3=re.compile(r'(^http[s]?\W|^www\W|^com\W|[0-9]+)')
    #separator4=re.sub(' ','',key_words1).lower()
    separator4=re.compile(r'el[\s]?segundo')   #去除搜索关键词
    separator5=re.sub(' ','',key_words2).lower()
    result_data=[]
    for data in url_data:
        str1=''
        for d in data:
            str1+=d
            str1+=' '
        s1=re.sub(separator3,'',str1)
        s2=re.sub(separator4,'',s1)
        s3=re.sub(separator5,'',s2)
        if len(s3)!=0:        
            result_data.append(s3)
    return result_data
        

def str_longest_match(str1,str2):  #得到两个字符串的最长公共子串
    str1+='0'  #添加后缀字符，消除函数已知bug
    str2+='1'
    s = difflib.SequenceMatcher(None, str1, str2)
    #print len(str1), len(str2)
    star_a, start_b, length = s.find_longest_match(0, len(str1)-1, 0, len(str2)-1)
    #print star_a, start_b, length
    return str1[star_a:star_a + length]

def extract_name_from_two_urls(url1,url2):  #提取两个url中的名称
    str1=delete_noisy_data(break_up_url(url1.lower()))
    str2=delete_noisy_data(break_up_url(url2.lower()))
    max_str=''
    for s in str2:
        for w in str1:
            str3=str_longest_match(s,w)
            if len(str3)>len(max_str):
                max_str=str3
    return max_str

def extract_name_from_several_urls(urls):  #提取多个url中的名称
    if urls==None:
        return 0
    a=0.5   #名称长度权重
    b=0.5   #名称出现次数权重
    length=len(urls)
    name_dict={}
    name_list=[]
    for i in range(0,length):
        for j in range(i+1,length):
            name1=extract_name_from_two_urls(urls[i],urls[j])
            if name1 not in name_dict:
                name_list.append(name1)
                name_dict[name1]=1
            else:            
                name_dict[name1]+=1
    if len(name_list)==0:
        return 0
    max_value=len(name_list[0])*a+name_dict[name_list[0]]*b
    name=name_list[0]
    for name2 in name_list:
        value=len(name2)*a+name_dict[name2]*b
        if max_value<value:
            max_value=value
            name=name2
    return name

def url_feature_extract(url):  #提取url的特征参数
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

