import csv
import requests
from lxml import html

BASE_URL="https://doc.hnumi.com"
BASE_URL_REDIS="https://doc.hnumi.com/bd/redis"

def main():
    response=requests.get(BASE_URL,timeout=60)
    document=html.fromstring(response.text)
    title_list=document.xpath("")


if __name__=='__name__':
    main()
