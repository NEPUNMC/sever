#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: qkyzs
@license: (C) Copyright 2017-2018, Node Supply Chain Manager Corporation Limited.
@contact: nepu1960@yeah.net
@file: get_kb.py
@time: 2019/3/6 0006 08:52
@desc:获取课表
"""
from bs4 import BeautifulSoup
from main.api.jwc.zhouchuli import get_zhou_list
from ..queue import celery
header={
    'Accept':'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; InfoPath.2)',
    'Accept-Encoding':'gzip, deflate',
    'Host':'jwgl.nepu.edu.cn'
}
@celery.task
def get_kb(login,username,xnxqh='2018-2019-2'):
    '''获取课表'''
    url='http://jwgl.nepu.edu.cn/tkglAction.do?method=goListKbByXs&istsxx=no&xnxqh='+xnxqh+'&zc=&xs0101id='+username
    get_info = login.get(url,headers=header).text
    soup=BeautifulSoup(get_info,'lxml')
    table=soup.find_all('table')
    total=[]
    for i in table[:-3]:
        tr=i.find_all('tr')
        jieci = 0
        for i in tr[1:-1]:
            td=i.find_all('td',)
            week = 0
            jieci=jieci+1
            for i in td:
                div=i.find_all('div',id=str(jieci)+'-'+str(week)+'-'+str(2))
                for i in div:
                    test=i.get_text(' ', '<br/>')
                    h = test.split(' ')
                    width=len(h)/5
                    if width<1:
                        kong=[]
                        info={
                            'weekday':week,
                            'jieci':jieci,
                            'name':'',
                            'teacher':'',
                            'classroom':'',
                            'week':'',
                            'class':'',
                        }
                        kong.append(info)
                        total.append(kong)
                        pass
                    else:
                        js=0
                        print(h)
                        taday_class=[]
                        for i in range(int(width)):
                            info={
                                'weekday': week,
                                'jieci': jieci,
                                'name': h[js],
                                'teacher': h[js+2],
                                'classroom': h[js+4],
                                'week': get_zhou_list(h[js+3]),
                                'class': h[js+1],
                            }
                            js+=5
                            taday_class.append(info)
                        total.append(taday_class)
                week = week + 1

    return total