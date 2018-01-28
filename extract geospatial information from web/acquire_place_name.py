# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 15:40:21 2017
《《《《《《调用函数请先调用load_file_data，再调用其它函数》》》》》》
@author: yangpuhai
"""
import sys
import csv
import os
import re

from address_find_tittle import new_acquire_not_estate_tittles as nanet
from address_find_tittle import new_acquire_place_names_closed_inf as napnci
from tittles_to_tittle import extract_tittle_from_several_tittles_closed_inf as etfstci


reload(sys)
sys.setdefaultencoding('utf-8')

city_file=''
state_file=''
filter_words_file=''
main_dir=''
city=[]
state=[]
filter_words=[]


#打开文件
def open_file(path):
    f1=open(path,'r')
    data=[s.strip('\n') for s in f1.readlines()]
    f1.close()
    return data

#设定各个文件夹的路径,初始化数据
def load_file_data(main_dir1,city_file1,state_file1,filter_words_file1):
    global main_dir
    main_dir=main_dir1
    global city_file
    city_file=os.path.join(main_dir,city_file1)
    global city
    city=open_file(city_file)
    global state_file
    state_file=os.path.join(main_dir,state_file1)
    global state
    state=open_file(state_file)
    global filter_words_file
    filter_words_file=filter_words_file1
    global filter_words
    filter_words=open_file(filter_words_file)
    

#提取title的可能关键词，以便下一步联合搜索
def new_acquire_titles_key_word():
    city_name=city[0]
    if main_dir!='':
        path=main_dir+'/all_address_types.csv'
        f=open(path,'r')
        reader=csv.reader(f)
        for row in reader:
            path1=main_dir+'/all_address_titles.csv'
            f1=open(path1,'ab')
            writer=csv.writer(f1)
            addr=row[1]
            titles=nanet(addr,city_name)
            print addr
            print titles
            data=[]
            data.append(addr)
            for title in titles:
                data.append(title.decode('utf-8').encode('GB2312','ignore'))
            #title=title.decode('utf-8').encode('GB2312','ignore')
            writer.writerow(data)
            f1.close()

#联合搜索名称关键字和地址，得到更精确的名称,并提取搜索时可能出现的google地图数据
def new_acquire_place_name():
    state_name=state[0]
    if main_dir!='':
        path=main_dir+'/all_address_titles.csv'
        f=open(path,'r')
        reader=csv.reader(f)
        count=0
        for row in reader:
            if len(row)>1:
                for name_key in row[1:]:
                    if len(name_key)!=0:
                        addr_name_data=[]
                        addr_name_data.append(row[0])
                        search_key=name_key+' '+row[0]
                        count+=1
                        print search_key
                        tittles,closed,g_inf=napnci(name_key,row[0],state_name)
                        place_name,close,google_inf=etfstci(tittles,closed,g_inf)
                        print place_name
                        if place_name!=0:
                            addr_name_data.append(place_name.decode('utf-8').encode('GB2312','ignore'))
                            if close==0:
                                addr_name_data.append('open')
                            if close==1:
                                addr_name_data.append('closed')
                            for g in google_inf:
                                addr_name_data.append(g)
                            path1=main_dir+'/all_address_place_name.csv'
                            f1=open(path1,'ab')
                            writer=csv.writer(f1)
                            writer.writerow(addr_name_data)
                            f1.close()

#合并相同的名称，过滤一部分非地点名称，输出最终结果
def new_combine_place_name():
    if main_dir!='':
        parten1=re.compile(r'[^a-zA-Z0-9]')
        path=main_dir+'/all_address_place_name.csv'
        f=open(path,'r')
        reader=csv.reader(f)
        same_addr=[]
        final_addr=[]
        for row in reader:
            if len(same_addr)==0:
                same_addr.append(row)
                continue
            if len(same_addr)!=0:
                if row[0]==same_addr[0][0]:
                    same_addr.append(row)
                else:
                    for sa in same_addr:
                        sa.append(1)
                    for sa in same_addr:
                        if len([1 for fw in filter_words if fw.lower() in sa[1].lower()])!=0:
                            sa[-1]=0
                            print sa[1]
                        if sa[1].lower() in sa[0].lower():
                            sa[-1]=0
                            print sa[1]
                        if parten1.sub('',sa[1]).isdigit():
                            sa[-1]=0
                            print sa[1]
                    for n1 in range(len(same_addr)):
                        for n2 in range(len(same_addr)):
                            if n1!=n2 and same_addr[n1][1].lower() in same_addr[n2][1].lower() and same_addr[n2][-1]==1 and same_addr[n1][-1]==1:
                                same_addr[n1][-1]=0
                                if same_addr[n2][3]=='' and same_addr[n1][3]!='':
                                    same_addr[n2][3:7]=same_addr[n1][3:7]
                    for sa in same_addr:
                        if sa[-1]==1:
                            final_addr.append(sa[:-1])
                    same_addr=[row]
        path1=main_dir+'/handled_all_address_place_name.csv'
        f1=open(path1,'ab')
        writer=csv.writer(f1)
        writer.writerow(['address','name','status','google_name','google_type','google_address','google_status'])
        for fa in final_addr:
            writer.writerow(fa)
        f1.close()
