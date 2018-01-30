# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:45:09 2017

@author: yangpuhai
"""
import os
import re
from bs4 import BeautifulSoup
from open_webpage2 import *

base_url= 'https://www.zillow.com/homes/for_sale/globalrelevanceex_sort/35.146862,-116.578675,32.893425,-120.0943_rect/7_zm'

#extract addresses from real-estate wensite 'zillow'
def extract_zillow(filename):
    list1=[]
    html_file = open(filename,'r')
    html_data = html_file.read()
    soup = BeautifulSoup(html_data,'html.parser')
    for link in soup.find_all('span',class_='zsg-photo-card-address'):
        address=link.text
        if re.match('^[0-9]',address):
            list1.append(address)
    return list1

#acquire real-estate addresses
def acquire_real_estate_address(base_url,num,filename):
    acquired_page=0
    page=0
    f=open(filename,'w')
    while acquired_page<=num:
        page+=1
        url=base_url+'/%d_p/'%(page)
        open_url(url,'training_data/zillow/test_data_%d'%(page))
        list1=extract_zillow('training_data/zillow/test_data_%d'%(page))
        while len(list1)==0:
            open_url(url,'training_data/zillow/test_data_%d'%(page))
            list1=extract_zillow('training_data/zillow/test_data_%d'%(page))
        for l in list1:
            f.write(l)
            f.write('\n')
            acquired_page+=1
            if acquired_page>num:
                break
    f.close()


def extractUrl(href):
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

#acquire real-estate urls
def acquire_real_estate_webpage(address_file,webpage_url,webpage_data_dir):
    f1=open(address_file,'r')
    address=f1.readlines()
    f1.close()
    count=0
    f2=open(webpage_url,'a')
    for a in address:
        query = urllib2.quote(a)#关键词编码
        html=open_english_google(query,10)
        while html==None or len(html)<3000:
            print 'error open\n'
            html=open_english_google(query,10)
        
        fn='%s/%d'%(webpage_data_dir,count)
        f=open(fn,'w')
        f.write(html)
        f.close() 
        
        soup = BeautifulSoup(html,'html.parser')
        for link in soup.find_all('h3',class_='r'):#寻找搜索结果的网址
            count+=1
            tmp_url = link.a["href"]
            tmped_url=extractUrl(tmp_url)
            if re.match('^(http[s]?://maps.google.com).*',tmped_url):
                continue
            else:
                print count
                f2.write(tmped_url)
                f2.write('\n')
    f2.close()

        
if __name__ == '__main__':
    if os.path.exists('training_data')==False:
        os.mkdir('training_data')
    if os.path.exists('training_data/zillow')==False:
        os.mkdir('training_data/zillow')
    if os.path.exists('training_data/data')==False:
        os.mkdir('training_data/data')
    acquire_real_estate_address(base_url,400,'training_data/real_estate_address_2')
    acquire_real_estate_webpage('training_data/real_estate_address_2','training_data/webpage_url_2','training_data/data')





