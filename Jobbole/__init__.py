#!/usr/bin/python3
# -*- coding:utf-8 -*-
import ProxiesSpiders
import requests
from bs4 import BeautifulSoup
import pymongo


class Jobbole():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['jobbole']
        self.table = self.db['jobbole']

    def save_mongodb(self, result):
        r = self.table.insert(result)
        return r

    def update_mongodb(self, result):
        r = self.table.update(result)
        return r

    def delete_mongodb(self, result):
        r = self.table.delete_many(result)
        return r

    def get_html(self, url):
        html = None
        try:
            response = requests.get(url=url, headers=self.headers, timeout=10)
            html = response.text
        except requests.HTTPError as e:
            print('爬取报错', e.args)
            if hasattr(e, 'code') and 500 <= e.code < 600:
                html = self.get_html(url)
        finally:
            return html

    def get_context(self, html):
        a_all_tag = BeautifulSoup(html, 'lxml').find_all('a', class_='archive-title')
        for a_tag in a_all_tag:
            href = a_tag['href']
            title = a_tag['title']
            j = {
                'href': href,
                'title': title
            }
            print('href=={}==title=={}'.format(href, title))
            self.save_mongodb(j)


if __name__ == '__main__':
    j = Jobbole()
    j.table.drop()
    table = j.table.find().sort('title', pymongo.DESCENDING)

    for t in table:
        print(t)
    for i in range(1, 100):
        html = j.get_html('http://python.jobbole.com/all-posts/page/{0}/'.format(i))
        print('解析第{}页'.format(i))
        j.get_context(html)