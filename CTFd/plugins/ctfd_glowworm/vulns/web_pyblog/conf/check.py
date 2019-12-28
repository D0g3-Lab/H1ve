# -*- coding:utf8 -*-

import sys, re
# reload(sys)
# sys.setdefaultencoding('utf-8')
import requests as rq
my_time = "AAAA"
debug = False
host = 'localhost'
port = 80
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

class check():
    def __init__(self):
        a = 1
    def index_check(self):
        res = rq.get('http://%s:%s/' % (host,port),headers=headers)
        if "蜀ICP备1111111111114号-1" in res.text:
            return True
        if debug:
            print("[fail!] index_check_fail")
        return False

    def search_check(self):
        res = rq.get('http://%s:%s/blog/search/?key=123' % (host,port),headers=headers)
        if '搜索到' in res.text:
            return True
        if debug:
            print("[fail!] search_check")
        return False
    def admin_login(self):
        s = rq.Session()
        rqq = s.get('http://%s:%s/admin/login/?next=/admin/' % (host,port),headers=headers).text
        token = re.findall(r'name=\'csrfmiddlewaretoken\' value=\'(.*)\' />',rqq)
        data = {'username':'root','password':'roottoor','csrfmiddlewaretoken':token}
        res = s.post('http://%s:%s/admin/login/?next=/admin/' % (host,port),data=data)
        if r'站点管理' in res.text:
            return True
        if debug:
            print("[fail!] admin_login")
        return False
    



def server_check():

    a = check()
    try:
        if not a.index_check():
            return False  
        if not a.search_check():
            return False  
        if not a.admin_login():
            return False
        return True
    except Exception as e:
        return False


if __name__ == '__main__':
    host = sys.argv[1]
    port = sys.argv[2]

    if server_check():
        # print("Host: "+host+" seems ok")
        print("")
        pass
    else:
        # 10180 11080
        print("team"+port[1:3])
        # print("Host: "+host+" seems down")


