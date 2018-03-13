#!/usr/bin/python
# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import os
import time, datetime, random


""" 使用 Python3.5
    爬取妹子图(www.mzitu.com)
"""


class Mzitu():

    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            # 'Host': 'i.meizitu.net',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

    def request(self, url):
        content = requests.get(url, headers=self.headers)
        return content

    def mkdir(self, path):
        path = os.path.join("/home/daimx/图片/Mzitu", path.strip())
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            os.chdir(path)
            print(u"文件夹%s建立成功！" % path)
            return True
        else:
            print(u"文件夹%s已存在" % path)
            return False

    # 获取所有套图
    def all_url(self, url):
        html = self.request(url)
        all_ul = BeautifulSoup(html.text, 'lxml').find_all('ul', class_="archives")
        for ul in all_ul:
            all_a = ul.find_all('a')
            for a in all_a:
                # 获取文本内容
                title = a.get_text()
                # 获取地址
                href = a['href']
                # ？在windows中不能创建文件夹所以替换掉
                path = str(title).replace("?", "_")

                # print(title, href)
                self.mkdir(path)
                self.html(href)

    # 获取每套图的单张显示地址
    def html(self, href):
        html = self.request(href)
        self.headers["Referer"] = href
        # 获取套图的总页数
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            # 获取每张图片的显示页面
            page_url = href + "/" + str(page)
            self.img(page_url)

    # 获取图片的真实地址
    def img(self, page_url):
        img_html = self.request(page_url)
        img_href = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.headers["Referer"] = page_url
        print('爬取图片地址：%s' % img_href)
        self.save(img_href)

    # 保存图片
    def save(self, img_url):
        name = img_url[-9:-4]
        img = self.request(img_url)
        with open(name + ".jpg", 'ab') as f:
            f.write(img.content)


if __name__ == '__main__':
    mzitu = Mzitu()
    mzitu.all_url('http://www.mzitu.com/all')
