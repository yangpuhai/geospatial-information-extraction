# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:25:06 2017

@author: yangpuhai
"""

import random
import time
import requests

user_agents = list()
proxy_ip_address=list()
google_domains=list()

#加载用户头
def load_user_agent():
    fp = open('user_agents', 'r')
    line=fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline().strip('\n')
    fp.close
#加载代理ip
def load_proxy_ip():
    fp = open('proxy_ip_address', 'r')
    line=fp.readline().strip('\n')
    while(line):
        proxy_ip_address.append(line)
        line = fp.readline().strip('\n')
    fp.close
#加载google域名集
def load_google_domain():
    fp = open('google_domain', 'r')
    line=fp.readline().strip('\n')
    while(line):
        google_domains.append(line)
        line = fp.readline().strip('\n')
    fp.close

english_google_url= "http://{domain}/search?hl=en&q={query}&btnG=Search&gbv=1&num={num}"

#打开url并存入文件
def open_english_google(query,num):
    html=''
    load_user_agent()
    #load_proxy_ip()
    load_google_domain()
    sleeptime =  random.randint(5, 30)
    time.sleep(sleeptime)
    while True:
        try:
            user_agent = random.choice(user_agents)
            #proxy_ip = random.choice(proxy_ip_address)
            #proxies = {"https": proxy_ip}
            google_domain = random.choice(google_domains)
            url = english_google_url
            url = url.format(domain=google_domain, query=query,num=num)
            req_header = {'User-Agent': user_agent,'referer': google_domain,'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
            html=requests.get(url,timeout=5,headers=req_header)
            html=html.content
            if 'Sometimes you may be asked to solve the CAPTCHA' in html:
                continue
            print google_domain
            break
        except:
            sleeptime =  random.randint(5, 30)
            time.sleep(sleeptime)
            continue
    return html

def open_normal_web(url):
    html=''
    load_user_agent()
    count=2
    while count>0:
        try:
            user_agent = random.choice(user_agents)
            req_header = {'User-Agent': user_agent,'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
            html=requests.get(url,timeout=5,headers=req_header,allow_redirects = True)
            html=html.content
            if 'Sometimes you may be asked to solve the CAPTCHA' in html:
                continue
            break
        except:
            count=count-1
            sleeptime =  random.randint(0, 5)
            time.sleep(sleeptime)
            continue
    return html

