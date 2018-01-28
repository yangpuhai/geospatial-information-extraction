# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 09:48:24 2017

@author: yangpuhai
"""
import random
import time
import requests

user_agents = list()
proxy_ip_address=list()
google_domains=list()
#base_url='https://www.google.com/'
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

english_google_url= "https://{domain}/search?hl=en&q={query}&btnG=Search&gbv=1&num={num}"

#打开url并存入文件
def open_english_google(query,num):
    html=''
    load_user_agent()
    load_proxy_ip()
    load_google_domain()
    sleeptime =  random.randint(15, 30)
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
                print 'detect CAPTCHA'
                continue
            break
        except:
            print 'error'
            sleeptime =  random.randint(15, 30)
            time.sleep(sleeptime)
            continue
    return html


def open_url(url,filename):
    html=''
    load_user_agent()
    load_proxy_ip()
    sleeptime =  random.randint(15, 30)
    time.sleep(sleeptime)
    while True:
        try:
            user_agent = random.choice(user_agents)
            #proxy_ip = random.choice(proxy_ip_address)
            #proxies = {"https": proxy_ip}
            req_header = {'User-Agent': user_agent,'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
            html=requests.get(url,timeout=5,headers=req_header)
            html=html.content
            if 'Please verify you\'re a human to continue' in html:
                print 'detect verify'
                continue
            break
        except:
            print 'error'
            sleeptime =  random.randint(15, 30)
            time.sleep(sleeptime)
            continue
    f=open(filename,'w')
    f.write(html)
    f.close()


