#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from html.parser import HTMLParser

class MyParser(HTMLParser):
    switch = False
    result=[]
    def __init__(self):
        HTMLParser.__init__(self)
    def handle_starttag(self,tag,attrs):
        if tag == 'div' and ('class','content') in attrs:
            self.switch = True
    def handle_endtag(self,tag):
        if tag == 'div':
            self.switch = False
    def handle_data(self,data):
        if self.switch:
            self.result.append(data.strip())
        self.result=list(filter(lambda x:x != '', self.result))
    def out(self):
        for i in self.result:
            yield i


class Pool():
    __res=[]
    __wasted=[]
    __header={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Encoding':'gzip, deflate, sdch, br','Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 ()X11; Linux x86_64) AppleWebKit/537.36 ()KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36'}
    def __init__(self):
        for page in range(1,36):
            try:
                f=requests.get('http://www.qiushibaike.com/textnew/page/'+str(page),headers=self.__header)
            except ConnectionError :
                print('ConnectionError\n')
            print("Status %s: %s"%(f.status_code,f.reason))
            parser=MyParser()
            parser.feed(f.text)
            for i in parser.out():
                self.__res.append(i)
            parser.close()
        self.__res=list(set(self.__res))
        self.__pool=self.__pripoo()
    def refresh(self):
        try:
            f=requests.get('http://www.qiushibaike.com/textnew/',headers=self.__header)
        except ConnectionError :
            print('ConnectionError\n')
        print("Status %s: %s"%(f.status_code,f.reason))
        parser=MyParser()
        parser.feed(f.text)
        for i in parser.out():
            if not (i in self.__res):
                self.__res.append(i)
    def __pripoo(self):
        for i in self.__res :
            if not (i in self.__wasted):
                self.__wasted.append(i)
                yield i
    def poo(self):
        return next(self.__pool)
    def reset(self):
        self.__wasted=[]
    def ignore(self,str):
        self.__wasted=self.__wasted+list(str)
