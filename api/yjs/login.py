#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: qkyzs
@license: (C) Copyright 2017-2018, Node Supply Chain Manager Corporation Limited.
@contact: nepu1960@yeah.net
@file: login.py
@time: 2019/3/5 0005 16:14
@desc:
"""
import requests
from bs4 import BeautifulSoup
import re
from api.yjs.jx import get_list
session=requests.session()
header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        #'Host': '172.16.199.2:8008',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
def get_login(xh,pwd):
    '''登陆'''
    data={
        'userName': xh,
        'password': pwd,
        'radiovalue':'student'
    }

    url='http://wenepu.imwork.net:43504/yjsjwgl/login.do'

    back_info=session.post(url,data=data,headers=header)
    if back_info.status_code!=200:
        return 404
    elif '用户名或密码不正确' in back_info.text:

        return '学号或密码错误'
    else:
        return session
def get_info(xh):
    '''获取个人信息'''
    url='http://wenepu.imwork.net:43504/yjsjwgl/xsxxwh.do?method=xsgrxxwh'
    info=session.get(url,headers=header).text
    soup=BeautifulSoup(info,'lxml')
    name=str(soup.find_all('input')[5])
    zjhm=str(soup.find_all('input')[8])
    name=re.search('value=.+',name).group().replace('value="','').replace('"/>','')
    zjhm = re.search('value=.+', zjhm).group().replace('value="','').replace('"/>','')
    info={
        'xh':xh,
        'name':name,
        'zjhm':zjhm
    }
    print(name,zjhm)
def get_score(xn='',xq=''):
    '''成绩获取'''
    url='http://wenepu.imwork.net:43504/yjsjwgl/xscjcx.do?act=find'
    data={
        'xn':xn,
        'xq':xq
    }
    '''研究生成绩查询'''
    info=session.post(url,data=data,headers=header).text
    #print(info)
    soup=BeautifulSoup(info,'lxml')
    div=soup.find_all('div')
    score=[]
    for i in div:
        tr=i.find_all('tr')
        for i in tr[1:]:
            td=i.find_all('td')
            score_info={
                '学年':td[0].get_text('','\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t'),
                '学期':td[1].get_text('','\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t'),
                '课程名称':td[2].get_text('','\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t'),
                '课程性质':td[3].get_text('','\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t'),
                '学分':td[4].get_text('','\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t'),
                '正考成绩':td[5].get_text('','\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t'),
            }
            score.append(score_info)
    print(score)
def get_class(xn='2018-2019',xq='1'):
    '''课表获取'''
    data={
        'dm':'',
        'xn':xn,
        'xq': xq
    }
    url='http://wenepu.imwork.net:43504/yjsjwgl/xsgrkbck.do'
    info=session.post(url,data=data,headers=header).text
    soup=BeautifulSoup(info,'lxml')
    div=soup.find_all('div')
    list=[]
    for i in div[3:]:
        tr=i.find_all('tr')
        for i in tr[1:]:
            td=i.find_all('td')
            fen=td[4].string
            te=fen.split('/')
            # print(te)
            for i in te:
                print(i)
                week = re.search('周.', i).group()

                jc = re.search('[0-9].*节', i).group()
                didian = re.search('【.+】', i).group()
                zhouci = re.search('】.+周', i).group()
                info_class={
                    'name':td[0].string,
                    'xuefen':td[1].string,
                    'teacher':td[2].string,
                    'xingzhi':td[3].string,
                    'week':week,
                    'jc':get_list(jc[:-1]),
                    'didian':didian,
                    'zhouci':get_list(zhouci[1:-2]),
                }
                list.append(info_class)
    print(list)
if __name__ == '__main__':
    get_login('188002070322','xinjiyuan18')
    get_class()
    get_info('188002070322')

