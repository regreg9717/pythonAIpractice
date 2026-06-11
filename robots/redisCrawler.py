import csv
import requests
from lxml import html

BASE_URL="https://doc.hnumi.com"
BASE_URL_REDIS="https://doc.hnumi.com/bd/redis"

#这是一个爬取云枢智库的爬虫代码
def main():
    response=requests.get(BASE_URL,timeout=60)
    document=html.fromstring(response.text)
    title_list=document.xpath("")


if __name__=='__name__':
    main()
