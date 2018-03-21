#!/usr/bin/python3
# -*- coding:utf-8 -*-
import urllib
from urllib import request
from bs4 import BeautifulSoup


class CSND_Spider():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
        }

    def get_user_info(self, url):
        req = request.Request(url=url, headers=self.headers)
        response = request.urlopen(req)
        print(response.read().decode('utf-8'))


if __name__ == '__main__':
    spider = CSND_Spider()
    spider.get_user_info('https://my.csdn.net/qianjin036a')