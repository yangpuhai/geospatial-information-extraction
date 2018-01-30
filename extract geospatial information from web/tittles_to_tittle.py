# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 19:47:56 2017

@author: yangpuhai
"""
import re
import difflib

#Get the longest common substring of two strings
def str_longest_match(str1,str2):  
    str1+='0'
    str2+='1'
    s = difflib.SequenceMatcher(None, str1, str2)
    star_a, start_b, length = s.find_longest_match(0, len(str1)-1, 0, len(str2)-1)
    return star_a,star_a + length

#Extract the longest substring of two tittles
def extract_tittle_from_two_tittles(t1,t2):  
    str1=t1.lower()
    str2=t2.lower()
    a,b=str_longest_match(str1,str2)
    return t1[a:b]

#Extract place name from several tittles
def extract_tittle_from_several_tittles(tittles):  
    if tittles==None:
        return 0
    if len(tittles)==0:
        return 0
    a=0.5   
    b=0.5   
    length=len(tittles)
    name_dict={}
    name_list=[]
    for i in range(0,length):
        for j in range(i+1,length):
            name1=extract_tittle_from_two_tittles(tittles[i],tittles[j])
            if name1 not in name_dict:
                name_list.append(name1)
                name_dict[name1]=1
            else:            
                name_dict[name1]+=1
    if len(name_list)==0:
        return 0
    tittle_list=[]
    for name2 in name_list:
        value=len(name2)*a+name_dict[name2]*b
        #value=len(re.findall(r'[0-9A-Za-z]+',name2))*a+name_dict[name2]*b
        tittle_list.append([name2,value])
    tittle_list=sorted(tittle_list, key=lambda a:a[1],reverse=True)
    result=''
    num=0
    #print tittle_list
    for t in tittle_list:
        num+=1
        ls='^'+re.escape(t[0])
        partten=re.compile(ls)
        if len([1 for ts in tittles if partten.findall(ts)])!=0:
            result=t[0]
            break
    if num>3 or result=='' or len(result)<4:
        return 0
    else:
        return result

#Extract place name from several tittles,send some information
def extract_tittle_from_several_tittles_closed_inf(tittles,close,google_inf):
    if tittles==None:
        return 0,close,google_inf
    if len(tittles)==0:
        return 0,close,google_inf
    a=0.5   
    b=0.5   
    length=len(tittles)
    name_dict={}
    name_list=[]
    for i in range(0,length):
        for j in range(i+1,length):
            name1=extract_tittle_from_two_tittles(tittles[i],tittles[j])
            if name1 not in name_dict:
                name_list.append(name1)
                name_dict[name1]=1
            else:            
                name_dict[name1]+=1
    if len(name_list)==0:
        return 0,close,google_inf
    tittle_list=[]
    for name2 in name_list:
        value=len(name2)*a+name_dict[name2]*b
        #value=len(re.findall(r'[0-9A-Za-z]+',name2))*a+name_dict[name2]*b
        tittle_list.append([name2,value])
    tittle_list=sorted(tittle_list, key=lambda a:a[1],reverse=True)
    result=''
    num=0
    #print tittle_list
    for t in tittle_list:
        num+=1
        ls='^'+re.escape(t[0])
        partten=re.compile(ls)
        if len([1 for ts in tittles if partten.findall(ts)])!=0:
            result=t[0]
            break
    if num>3 or result=='' or len(result)<4:
        return 0,close,google_inf
    else:
        return result,close,google_inf

