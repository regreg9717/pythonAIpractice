# import requests
#
# target_url = 'https://www.tiobe.com/tiobe-index/'
#
# response=requests.get(target_url)
#
# print(response.text)

from lxml import html
with open("仙逆人物志.html","r",encoding="UTF-8") as f:
    html_text=f.read()
    document=html.fromstring(html_text)

    #解析表头
    th_list=document.xpath("//table/thead/tr/th/text()")
    print(th_list)
    #获取所有行的数据
    tr_list=document.xpath("//table/tbody/tr")
    for tr in tr_list:
        td_list=tr.xpath("./td/text()")
        print(td_list)

