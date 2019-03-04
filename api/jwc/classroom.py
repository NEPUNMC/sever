#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: qkyzs
@license: (C) Copyright 2017-2018, Node Supply Chain Manager Corporation Limited.
@contact: nepu1960@yeah.net
@file: classroom.py
@time: 2019/3/4 0004 14:19
@desc:
"""
import requests
from api.jwc.get_code import login_jwc,logout
from bs4 import BeautifulSoup
import re
import time
header={
    'Accept':'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.2)',
    'Accept-Encoding':'gzip, deflate',
    'Host':'jwgl.nepu.edu.cn'
}
global login
login=login_jwc()
def te():
    login=login_jwc()
    data={
        'typewhere':'xszq',
        'xnxqh':'2018-2019-2',
        'xqbh':'00001',
        'jxqbh':'',
        'jxlbh':'',
         'jsbh':'',
        'bjfh':'%3D',
        'rnrs':'',
        'jszt':'',
        'zc':'1',
        'zc2':'1',
        'xq':'1',
        'xq2':'1',
        'jc':'',
        'jc2':'',
    }
    back=login.post('http://jwgl.nepu.edu.cn/jiaowu/kxjsgl/kxjsgl.do?method=queryKxxxByJs&typewhere=xszq',data=data,headers=header).text
    soup=BeautifulSoup(back,'lxml')
    table=soup.find_all('table')
    lb=[]
    for i in table[:-3]:
        tr=i.find_all('tr')

        for i in tr[3:-2]:
            class_info = {}
            td=i.find_all('td')
            #print(td)
            jc = 0
            for i in td:
                text=i.get_text()
                # print(i.get_text('','\r\n\t\t\t\t\t\t\t\t'),jc)
                if jc==0:
                    try:
                        room_name = re.search('((1H-)|(2A-)|(1F-)|(主楼))[0-9]+',text).group()
                        roomID = re.search('ue=.\w+', str(i)).group()
                        # print(roomID[4:])
                        # print(room_name)
                        class_info['room'] = room_name
                        class_info['roomID']=roomID[4:]
                    except:
                          break
                else:
                    if '◆' in text:
                        class_info[jc]='正常上课'
                    elif 'Ｊ' in text:
                        class_info[jc]='借用'
                    elif 'Ｘ' in text:
                        class_info[jc]='锁定'
                    elif 'Κ' in text:
                        class_info[jc]='考试'
                    elif 'Ｇ' in text:
                        class_info[jc] = '固定调课'
                    elif 'Ｌ' in text:
                        class_info[jc] = '临时调课'
                    else:class_info[jc] = '空闲'
                jc = jc + 1
            if class_info:
                lb.append(class_info)
            else:
                pass
    print(lb)
def get_info_room(jsbh='00030'):
    '''查询教室占用情况'''
    url = 'http://jwgl.nepu.edu.cn/jiaowu/kxjsgl/kxjsgl.do?method=goQueryjszyqk&xnxqh=2018-2019-2&jsbh='+jsbh+'&kcsj=10304&typewhere=xszq&startZc=1&endZc=1&startJc=&endJc=&startXq=1&endXq=1&jszt=&type=add'
    room_info=login.get(url).text
    soup=BeautifulSoup(room_info,'lxml')
    tr=soup.find_all('tr')
    new_lb=[]
    for i in tr[2:3]:
        td=i.find_all('td')

        for i in td[1:]:
            new_lb.append(i.get_text('','\r\n\t\t\t\t\t\t\t\t\t\t'))
    print(new_lb)

    info={}
    a=0
    b=2
    for i in range(8):
        info[new_lb[a]]=new_lb[b]
        a=a+3
        b=b+3
    print(info)

if __name__ == '__main__':
    star=time.time()
    # te()
    get_info_room()
    logout()
    end=time.time()
    print(end-star)