import requests
import csv
from  lxml import html

#常量
TMDB_BASE_URL="https://www.themoviedb.org"
TMDB_TOP_URL="https://www.themoviedb.org/movie/top-rated"

# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
# }

#保存电影数据为csv文件
def save_all_movies(all_movies):
    pass

#获取电影详情
def get_movie_info(movie_info_urls):
    movie_response=requests.get(movie_info_urls,timeout=60)
    print(movie_response)
    movie_doc=html.fromstring(movie_response.text)
    print(movie_doc)
    movie_name=movie_doc.xpath("//*[@id='original_header']/div[2]/section/div[1]/h2/a/text()")
    print(movie_name)

def main():
    #1.发送请求，获取高分电影榜单数据
    response=requests.get(TMDB_TOP_URL,timeout=60)

    #2.解析数据，获取电影列表
    document=html.fromstring(response.text)
    movie_list=document.xpath("//*[@id='4bc88d49017a3c122d005189']/div/div[2]/div/a/h2/span")

    #3.遍历电影列表，获取电影详情
    all_movies=[]
    for movie in movie_list:
        movie_urls =movie.xpath("./div/div/a/@href")
        if movie_urls:
            #电影详情的url
            movie_info_url=TMDB_BASE_URL+movie_urls[0]
            #发送请求，获取电影的详情数据
            movie_info=get_movie_info(movie_info_url)
            all_movies.append(movie_info)


    #4.保存数据，保存为csv文件
    save_all_movies(all_movies)

if __name__ =='__main__':
    main()

