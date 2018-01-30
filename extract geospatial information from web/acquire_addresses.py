# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:26:15 2017
《《《《《《 call the function load_file_data first, and then call other functions 》》》》》》
@author: yangpuhai
"""
import csv
import threading
import re
import os
import open_web as ow
import address_extract as ae
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

main_dir=''
street_file=''
street_type_file=''
city_file=''
state_file=''
country_file=''
type_file=''
types=[]
street=[]
city=[]

#The main body of a multithreaded function
class CustomTask: 
    def __init__(self): 
        self._result = [] 
    def run(self, *args, **kwargs):
        data = ow.open_normal_web(args[0])
        self._result.append([data,args[0]])
    def get_result(self):
        return self._result

#Retrieve the url from the href tag in google search results
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

#open file
def open_file(path):
    f1=open(path,'r')
    data=[s.strip('\n') for s in f1.readlines()]
    f1.close()
    return data

#Initialize the data
def load_file_data(main_dir1,street_file1,street_type_file1,city_file1,state_file1,country_file1,type_file1):
    global main_dir
    main_dir=main_dir1
    global street_file
    street_file=os.path.join(main_dir,street_file1)
    global street_type_file
    street_type_file=street_type_file1
    global city_file
    city_file=os.path.join(main_dir,city_file1)
    global state_file
    state_file=os.path.join(main_dir,state_file1)
    global country_file
    country_file=os.path.join(main_dir,country_file1)
    global type_file
    type_file=type_file1
    global types,street,city
    types=[' '.join(s.split('_')) for s in open_file(type_file)]
    street=open_file(street_file)
    city=open_file(city_file)
    

#access google search engine with the key word (type streetname city name),extract 100 urls in results
def acquire_url():
    city_name=city[0]
    search_keywords=[]
    for t in types:
        type_name=main_dir+'/'+t
        if os.path.exists(type_name)==False:
            os.mkdir(type_name)
        for s in street:
            sk=' '.join([t,s,city_name])
            search_keywords.append(sk)
            path=type_name+'/'+sk
            f=open(path,'a')
            web_data=ow.open_english_google(sk,100)
            soup = BeautifulSoup(web_data,'html.parser')
            for link in soup.find_all('h3',class_='r'):#寻找搜索结果的网址
                tmp_url = link.a["href"]
                tmped_url=extract_url(tmp_url)
                if re.match('^(https://maps.google.).*',tmped_url):
                    continue
                else:
                    f.write(tmped_url)
                    f.write('\n')
            f.close()

#delete urls
def del_acquire_url():
    city_name=city[0]
    for t in types:
        type_name=main_dir+'/'+t
        if os.path.exists(type_name):
            for s in street:
                sk=' '.join([t,s,city_name])
                path=type_name+'/'+sk
                if os.path.exists(path):
                    os.remove(path)
            os.rmdir(type_name)

#extract contant of the url
def acquire_web():
    city_name=city[0]
    for t in types:
        print t
        type_name=main_dir+'/'+t
        threaddata=[]
        for s in street:
            datas=[]
            print s
            sk=' '.join([t,s,city_name])
            path=type_name+'/'+sk
            path1=path+'_webdata'
            datas.append(path1)
            if os.path.isdir(path1)==False:
                os.makedirs(path1)
            f=open(path,'r')
            urls=f.readlines()
            urls1=[]
            for url in urls:
                    urls1.append(url)
            ct = CustomTask()
            datas.append(ct)
            threads=[]
            urldata=[]
            for u in urls1:
                urldata.append(u.strip('\n'))
                th=threading.Thread(target=ct.run, args=(u.strip('\n'),))
                threads.append(th)
                th.setDaemon(True)
            datas.append(threads)
            datas.append(urldata)
            threaddata.append(datas)
        for td in threaddata:
            for thr in td[2]:
                thr.start()
        #for td in threaddata:
            for thr in td[2]:
                thr.join()
        #for td in threaddata:
            result=td[1].get_result()
            path1=td[0]
            final_result=[]
            errorsum=0
            errordict={}
            for r in result:
                html=r[0]
                if html=='' or html==None:
                    html=''
                    errorsum+=1
                    errordict[r[1]]=0
                else:
                    final_result.append(html)
                    errordict[r[1]]=1
            count=errorsum
            url_count=len(td[3])/3.0
            while count>url_count:
                print "count>1/3 >>>>>>>>>>>>>>>>>>>>",count,len(td[3])
                ct1 = CustomTask()
                thread1=[threading.Thread(target=ct1.run, args=(ud,)) for ud in errordict if errordict[ud]==0]
                for thre in thread1:
                    thre.start()
                for thre in thread1:
                    thre.join()
                result1=ct1.get_result()
                for r1 in result1:
                    html=r1[0]
                    if html!='' and html!=None:
                        errordict[r1[1]]=1
                        final_result.append(html)
                count=len([1 for r in result1 if r[0]==''or r[0]==None ])
            print len(final_result)
            i=0
            for r in final_result:
                html=r
                web_path=path1+'/'+str(i)
                f1=open(web_path,'w')
                f1.write(html)
                f1.close()
                i+=1
            f.close()

#delete contant of the url
def del_acquire_web():
    city_name=city[0]
    for t in types:
        print t
        type_name=main_dir+'/'+t
        for s in street:
            print s
            sk=' '.join([t,s,city_name])
            path=type_name+'/'+sk
            path1=path+'_webdata'
            if os.path.exists(path1):
                for p in os.listdir(path1):
                    if os.path.exists(os.path.join(path1,p)): 
                        os.remove(os.path.join(path1,p))
                os.rmdir(path1)

#extract addresses from web contant
def acquire_address():
    ae.load_file_data(street_file,street_type_file,city_file,state_file,country_file)
    city_name=city[0]
    for t in types:
        print t
        type_name=main_dir+'/'+t
        for s in street:
            print s
            sk=' '.join([t,s,city_name])
            path=type_name+'/'+sk
            path1=path+'_webdata'
            path2=path+'_all_address.csv'
            path3=path+'_type_address.csv'
            webs=os.listdir(path1)
            address=[]
            t_address=[]
            for w in webs:
                w_path = os.path.join(path1,w)
                if os.path.isfile(w_path):
                    w_address=ae.address_extract4(w_path)
                    for w_a in w_address:
                        if w_a not in address:
                            address.append(w_a)
                    #f1=codecs.open(path, u'rb',encoding= u'utf-8',errors='ignore')
                    f1=open(w_path,'r')
                    d1 = f1.read()
                    tt=t.split()
                    f1.close()
                    if ' '+tt[-1]+' ' in d1:
                        for w_a in w_address:
                            if w_a not in t_address:
                                t_address.append(w_a)
            f=open(path2,'wb')
            writer = csv.writer(f)
            for a in address:
                print a
                writer.writerow(a)
            f.close()
            f2=open(path3,'wb')
            writer = csv.writer(f2)
            for a1 in t_address:
                print a1
                writer.writerow(a1)
            f2.close()

#delete addresses
def del_acquire_address():
    city_name=city[0]
    for t in types:
        print t
        type_name=main_dir+'/'+t
        for s in street:
            print s
            sk=' '.join([t,s,city_name])
            path=type_name+'/'+sk
            path2=path+'_all_address.csv'
            path3=path+'_type_address.csv'
            if os.path.exists(path2):
                os.remove(path2) 
            if os.path.exists(path3): 
                os.remove(path3)

#Merge the extracted address, the result in a file
def address_types_csv():
    city_name=city[0]
    path0=main_dir+'/address_types.csv'
    path00=main_dir+'/all_address_types.csv'
    data={}
    data00={}
    for t in types:
        print t
        type_name=main_dir+'/'+t
        for s in street:
            print s
            sk=' '.join([t,s,city_name])
            path=type_name+'/'+sk
            path3=path+'_type_address.csv'
            path4=path+'_all_address.csv'
            f1=open(path3,'r')
            reader=csv.reader(f1)
            for row in reader:
                if row[1] not in data:
                    data1={}
                    types_dict={}
                    types_dict[t]=1
                    data1['addr_num']=row[0]
                    data1['addr']=row[1]
                    data1['types']=types_dict
                    data[row[1]]=data1
                else:
                    if t not in data[row[1]]['types']:
                        data[row[1]]['types'][t]=1
                    else:
                        data[row[1]]['types'][t]+=1
            f1.close()
            f2=open(path4,'r')
            reader2=csv.reader(f2)
            for row2 in reader2:
                if row2[1] not in data00:
                    data1={}
                    types_dict={}
                    types_dict[t]=1
                    data1['addr_num']=row2[0]
                    data1['addr']=row2[1]
                    data1['types']=types_dict
                    data00[row2[1]]=data1
                else:
                    if t not in data00[row2[1]]['types']:
                        data00[row2[1]]['types'][t]=1
                    else:
                        data00[row2[1]]['types'][t]+=1
            f2.close()
    f0=open(path0,'wb')
    writer = csv.writer(f0)
    for a in data:
        writer.writerow([data[a]['addr_num'],data[a]['addr'],','.join([t1+':'+str(data[a]['types'][t1]) for t1 in data[a]['types']])])
    f0.close()
    f00=open(path00,'wb')
    writer00 = csv.writer(f00)
    for a in data00:
        writer00.writerow([data00[a]['addr_num'],data00[a]['addr'],','.join([t1+':'+str(data00[a]['types'][t1]) for t1 in data00[a]['types']])])
    f00.close()

 
    