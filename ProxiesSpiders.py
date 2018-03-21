#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
代理池爬虫
"""
from urllib import request
import requests
from bs4 import BeautifulSoup
import MyConst
import pymongo

import csv


class Spider():
    # 初始化
    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client['proxies_db']
        self.collection = self.db['proxies']

        self.user_agent_list = MyConst.MY_USER_AGENT
        self.headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
        }

    def insert_result(self, proxies):
            result = self.collection.insert(proxies)
            return result

    # 获取网页内容
    def get_html(self, url):
        try:
            req = request.Request(url, headers=self.headers)
            response = request.urlopen(req, timeout=10)
            html = response.read().decode('utf-8')
            return html
        except request.URLError as e:
            e.reason

    def analysis(self, html):
        content = BeautifulSoup(html, 'lxml')
        proxies_tag = content.find('div', id='list').find('tbody').find_all('tr')
        proxies_list = []
        for proxie_tag in proxies_tag:
            ip = proxie_tag.find('td', attrs={'data-title': 'IP'})
            port = proxie_tag.find('td', attrs={'data-title': 'PORT'})
            ip_type = proxie_tag.find('td', attrs={'data-title': '类型'})
            address = proxie_tag.find('td', attrs={'data-title': '位置'})
            end_time = proxie_tag.find('td', attrs={'data-title': '最后验证时间'})
            proxies_list.append([ip.get_text(), port.get_text(), ip_type.get_text(), address.get_text(), end_time.get_text()])
        self.save_csv(proxies_list)

    def save_csv(self, data):
        with (open('./proxies.cvs', 'w')) as f:
            writer = csv.writer(f)
            writer.writerows(data)

# if __name__ == '__main__':
#     spider = Spider()
#     html = spider.get_html('https://www.kuaidaili.com/free/inha/1/')
#     spider.analysis(html)
#     lis = spider.read_csv('./proxies.cvs')
#     with (open('./proxies.cvs', 'r')) as f:
#         reader = csv.reader(f)
#         for l in reader:
#             print(l)
#             proxies = {l[3]: '{}://{}:{}'.format(l[3], l[1], l[2])}
#             response = requests.get(url='https://httpbin.org/ip', proxies=proxies)
#             print(response)
#             if response.status_code != 200:
#                 reader.
