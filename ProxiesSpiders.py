#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
代理池爬虫
"""
import urllib.request
from bs4 import BeautifulSoup
import MyConst
import random
import csv


class Spider():
    # 初始化
    def __init__(self):
        self.user_agent_list = MyConst.MY_USER_AGENT
        self.headers = {
            'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
        }

    # 获取网页内容
    def get_html(self, url):
        try:
            req = urllib.request.Request(url, headers=self.headers)
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')
            return html
        except urllib.request.URLError as e:
            e.reason

    def analysis(self, html):
        content = BeautifulSoup(html, 'lxml')
        proiexs_tag = content.find('div', id='list').find('tbody').find_all('tr')
        proiexs_list = []
        for proiex_tag in proiexs_tag:
            ip = proiex_tag.find('td', attrs={'data-title': 'IP'})
            port = proiex_tag.find('td', attrs={'data-title': 'PORT'})
            ip_type = proiex_tag.find('td', attrs={'data-title': '类型'})
            address = proiex_tag.find('td', attrs={'data-title': '位置'})
            end_time = proiex_tag.find('td', attrs={'data-title': '最后验证时间'})
            proiexs_list.append([ip.get_text(), port.get_text(), ip_type.get_text(), address.get_text(), end_time.get_text()])
        self.save_csv(proiexs_list)

    def save_csv(self, data):
        with (open('./proiexs.cvs', 'w')) as f:
            writer = csv.writer(f)
            writer.writerows(data)


if __name__ == '__main__':
    spider = Spider()
    html = spider.get_html('https://www.kuaidaili.com/free/inha/1/')
    spider.analysis(html)