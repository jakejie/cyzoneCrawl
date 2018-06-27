# -*- coding:utf-8 -*-
__author__ = "jake"
__email__ = "jakejie@163.com"
"""
Project:创业邦网站数据爬虫
FileName = PyCharm
Version:1.0
CreateDay:2018/6/25 11:05
"""
from scrapy import cmdline

if __name__ == "__main__":
    cmdline.execute("scrapy crawl zone".split())
    # cmdline.execute("scrapy crawl zone --nolog".split())
