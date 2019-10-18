# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 07:14:42 2019

@author: motoi
"""

import json

"""xxxを書き換えて使う"""
api_data = {"bf": { "key": 'xxx', "secret": 'xxx' },"mex": { "key": 'xxx', "secret": 'xxx' },"finex":{"key": 'xxx',"secret":'xxx'}}

"""windowsならデフォルトでDesktopにjsonデータが作成される...はず"""
fw = open("api_file.json","w")
json.dump(api_data,fw)