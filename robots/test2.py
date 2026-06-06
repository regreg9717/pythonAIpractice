import requests
from lxml import html


target_url = 'https://www.tiobe.com/tiobe-index/'

response=requests.get(target_url)

document=html.fromstring(response.text)

#解析数据
th_list=document.xpath("//table[@id='top20']/thead/tr/th/text()")
print(th_list)

tr_list=document.xpath("//table[@id='top20']/tbody/tr")
for td in tr_list:
    td_list=td.xpath("./td/text()")
    print(td_list)