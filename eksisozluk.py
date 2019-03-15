#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 16:24:13 2019

@author: aybukeozkan
"""

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
from string import punctuation

url = 'https://eksisozluk.com'
useragent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get(url)

gundemPage = 1
while(gundemPage <= 5):
    h = requests.get(url + '/basliklar/gundem?p=' + str(gundemPage), headers=useragent)
    soup = bs(h.content, 'html.parser')
    titles = soup.find(id = 'content-body')
    titles = titles.find(class_ = 'topic-list').find_all('a')
        
    for title in titles:
        link = title.get('href')
        pageNum = 1
        link = requests.get(url + link, headers=useragent)
        if link.status_code == 200:
            soup2 = bs(link.content, 'html.parser')
            pageUrl = soup2.find(itemprop = 'url')['href']   
            page = requests.get(url + pageUrl, headers=useragent)
            if page.status_code == 200:
                soup3 = bs(page.content, 'html.parser')
                maxPageNum = soup3.find(id = 'topic').find(class_ = 'pager')
                if maxPageNum is not None:
                    maxPageNum = (int)(maxPageNum['data-pagecount'])
                else:
                    maxPageNum = 1
                baslik = soup3.find('span', attrs={'itemprop': 'name'})\
                    .get_text().translate(str.maketrans('', '', punctuation))
                with open('{}.json'.format(baslik), 'wb') as file:
                    while pageNum <= maxPageNum:
                        r = requests.get(url + pageUrl + '?p=' + str(pageNum), headers=useragent)
                        if r.status_code == 200:
                            soup4 = bs(r.content, 'html.parser')
                            entries = soup4.find(id = 'entry-item-list').find_all('li')
                            for entry in entries:
                                try:
                                    data = {}
                                    data ['content'] = entry.find(class_ = 'content').get_text(strip=True)
                                    data ['author'] = entry.find(class_ = 'entry-author').get_text(strip=True)
                                    data ['date'] = entry.find(class_ = 'entry-date').get_text(strip=True)
                                    file.write(json.dumps('{} , '.format(data), ensure_ascii=False).encode("utf-8"))
                                except:
                                    continue    
                        pageNum = pageNum + 1
    gundemPage = gundemPage + 1