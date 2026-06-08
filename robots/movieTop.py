import requests
import csv
from  lxml import html

#常量
TMDB_BASE_URL="https://www.themoviedb.org"
TMDB_TOP_URL="https://www.themoviedb.org/movie/top-rated"

#获取电影详情
def get_movie_info(movie_info_url):
    pass

def main():
    #发送请求，获取高分电影榜单数据
    response=requests.get(TMDB_TOP_URL,timeout=60)

    #解析数据，获取电影列表
    document=html.fromstring(response.text)
    movie_list=document.xpath("//*[@id='page_1']/div[@class='card style_1']")

    #遍历电影列表，获取电影详情
    for movie in movie_list:
        movie_urls =movie.xpath("./div/div/a/@href")
        if movie_urls:
            #电影详情的url
            movie_info_urls=TMDB_BASE_URL+movie_urls[0]

    #保存数据，保存为csv文件

if __name__ =='__name__':
    main()

