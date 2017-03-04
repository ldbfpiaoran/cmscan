import requests
from bs4 import BeautifulSoup
import re
# import base64
import rule
import sys
#from multiprocessing import Process


# favicon.ico  MD5识别功能（未作） 因为网站大部分会改favicon.ico


url = input('输入要识别的网址')
if url.startswith('http://'):
    url = url
else:
    url = 'http://'+url

#testurl = 'http://www.70018.cn/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.0.1471.914 Safari/537.36'}
response = requests.get(url=url,headers=headers)
    # 状态码  response.status_code
    # 用户头  headers.get（‘’）

bresponse = BeautifulSoup(response.text,"lxml")
title = bresponse.findAll('title')                            #title
for i in title:
    title = i.get_text()
head = response.headers
    #cookie = response.cookies
response = response.text


    #cookie = requests.utils.dict_from_cookiejar(cookie)
header = ''
for key in head.keys():                             #将 header集合
    header = header+key+':'+head[key]
    #print(header)
print('收集主页信息完毕')

def scan_title():
    titlerule = rule.title
    web_information = 0
    for key in titlerule.keys():
        req = re.search(key,title,re.I)
        if req:
            web_information = titlerule[key]
            break
        else:
            continue
    return web_information

def scan_head():
    headrule = rule.head
    web_information = 0
    for key in headrule.keys():
        if '&' in key:
            keys = re.split('&',key)
            if re.search(keys[0],header,re.I) and re.search(keys[1],response,re.I) :
                web_information = headrule[key]
                break
            else:
                continue
        else:
            req = re.search(key,header,re.I)
            if req:
                web_information = headrule[key]
                break
            else:
                continue
    return web_information




def scan_body():
    body = rule.body
    web_information = 0
    for key in body.keys():
        #print(key)   #排查哪条正则写错了
        if '&' in key:
            keys = re.split('&',key)
            if re.search(keys[0],response,re.I) and re.search(keys[1],response,re.I):
                web_information = body[key]
                break
            else:
                continue
        else:
            req = re.search(key,response,re.I)
            if req:
                web_information = body[key]
                break
            else:
                continue
    return web_information


def main():
    web_information = scan_title()
    if web_information == 0:
        web_information = scan_head()
        if web_information == 0:
            web_information = scan_body()
            if web_information == 0:
                print('无能为力了')
                sys.exit()
            else:
                print(web_information)
        else:
            print(web_information)
    else:
        print(web_information)


if __name__ == '__main__':
    main()

