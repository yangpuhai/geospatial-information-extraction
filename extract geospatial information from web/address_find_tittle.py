# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 19:13:52 2017

@author: yangpuhai
"""

import re
from bs4 import BeautifulSoup
from open_webpage2 import *
from web_page_prediction_model import *

#解析谷歌网页中的网址
def extract_url(href):
    url = href
    pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
    url_match = pattern.search(href)
    if(url_match and url_match.lastindex > 0):
        url = url_match.group(1)
    com_str='http://www.google.com/url?url='
    length=len(com_str)
    pos=url.find(com_str)
    if(pos>-1):
        url=url[length:]
    return url

#对提取的title进行处理
def extract_tittle(tmp_tittle,address_head):
    s=''+address_head+'.*'
    s1=' - .*'
    s2=' \| .*'
    partten=re.compile(s)
    partten1=re.compile(s1)
    partten2=re.compile(s2)
    res=partten.sub('',tmp_tittle)
    res1=partten1.sub('',res)
    res2=partten2.sub('',res1)
    return res2

#提取谷歌搜索网页中的地图数据
def extract_google_inf(html):
    inf=[]
    name=''
    business=''
    address=''
    status=''
    soup=BeautifulSoup(html,'html.parser')
    soup10=soup.find('span',id='_Gtg')
    if soup10:
        status=soup10.get_text()
    soup11=soup.find('div',id="rhs_title")
    if soup11:
        name=soup11.find('span').get_text()
    for soup12 in soup.find_all('span',class_='_eMw'):
        business+=soup12.get_text()
    soup2=soup.find('div',class_='_G1d _wle _xle')
    if soup2:
        address=soup2.find('span',class_='_Xbe').get_text()
    if name=='':
        soup31=soup.find('div',class_='_B5d')
        if soup31:
            name=soup31.get_text()
        soup32=soup.find('div',class_='_POh')
        if soup32:
            for soup321 in soup32.find_all('span'):
                business+=soup321.get_text()
        soup33=soup.find('span',class_='_tA')
        if soup33:
            address=soup33.get_text()
        soup34=soup.find('div',class_='_zdb _Pxg')
        if soup34:
            status=soup34.get_text()
    inf.append(name)
    inf.append(business)
    inf.append(address)
    inf.append(status)
    return inf

#从搜索地址的结果中提取50个title，并对其进行处理，输出处理后的title
def new_acquire_not_estate_tittles(address,city):
    address_head=''
    if address.split():
        address_head=address.split()[0]
    model=load_model()
    tittles={}
    results_per_page=50
    query = urllib2.quote(address)#关键词编码
    html=open_english_google(query,results_per_page)
    if html=='':
        return None
    soup = BeautifulSoup(html,'html.parser')
    street_addr=' '+city.lower()+'.*'
    parten=re.compile(street_addr)
    for link in soup.find_all('h3',class_='r'):#寻找搜索结果的网址
        tmp_url = link.a["href"]
        tmp_tittle=link.a.get_text()
        tmped_url=extract_url(tmp_url)
        tmped_tittle=extract_tittle(tmp_tittle,address_head)
        #print tmped_url
        if re.match('^(https://maps.google.).*',tmped_url):
            continue
        else:
            if model_prediction(model,tmped_url)[0]==-1 and len(tmped_tittle)!=0 and parten.sub('',address.lower()) in tmp_tittle.lower():
            #if model_prediction(model,tmped_url)[0]==-1 and len(tmped_tittle)!=0 and address_head in tmp_tittle:
                print tmp_tittle
                print tmped_tittle
                if tmped_tittle not in tittles:
                    tittles[tmped_tittle]=1
    for t1 in tittles:
        for t2 in tittles:
            if t1!=t2 and t2 in t1:
                tittles[t1]=0
    titles=[]
    for t3 in tittles:
        if tittles[t3]==1:
            titles.append(t3)
    return titles

def new_acquire_place_names_closed_inf(name_key,address,state):
    address_head=''
    if address.split():
        address_head=address.split()[0]
    model=load_model()
    close=0
    google_inf=['','','']
    tittles=[]
    results_per_page=10
    query = urllib2.quote(name_key+' '+address)#关键词编码
    html=open_english_google(query,results_per_page)
    if html=='':
        return None,close,google_inf
    google_inf=extract_google_inf(html)
    print google_inf
    soup = BeautifulSoup(html,'html.parser')
    street_addr=' '+state.lower()+'.*'
    parten=re.compile(street_addr)
    for link in soup.find_all('div',class_='g'):#寻找搜索结果的网址
        url_title=link.find('h3',class_='r')
        if url_title:
            tmp_url = url_title.a["href"]
            tmp_tittle=url_title.a.get_text()
            tmp_abstract=''
            abstract=link.find('span',class_='st')
            if abstract:
                tmp_abstract=abstract.get_text()
            tmped_url=extract_url(tmp_url)
            tmped_tittle=extract_tittle(tmp_tittle,address_head)
            if re.match('^(https://maps.google.).*',tmped_url):
                continue
            else:
                ss=parten.sub('',address.lower()).split(' ')
                st=(tmp_tittle+tmp_abstract).lower()
                tag=1
                for s in ss:
                    if s not in st:
                        tag=0
                if model_prediction(model,tmped_url)[0]==-1 and len(tmped_tittle)!=0 and tag==1:
                    tittles.append(tmped_tittle)
                    if 'close' in tmp_tittle.lower():
                        close=1
    return tittles,close,google_inf


