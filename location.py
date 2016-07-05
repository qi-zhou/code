#!/usr/bin/env python3
from  urllib import request
import json
#MCC = '460'
MCC = input('输入MCC，中国mcc=460:')
#MNC = '01'
MNC = input('输入mnc:')
LAC = '40977'
CI = '2205409'
bs = MCC + ',' + MNC + ',' + LAC + ',' + CI 
#url = 'http://api.gpsspg.com/bs/?oid=2940&bs=460,01,40977,2205409&output=json'
url = 'http://api.gpsspg.com/bs/?oid=2940&bs=' + bs + '&output=json'
print(url)
with request.urlopen(url) as f:
  data = f.read()
  s = json.loads(data.decode('utf-8'))
  result = s["result"][0]
  lat = result["lat"]
  lng = result["lng"]
  address = result["address"]
print('INSERT INTO barn(a,b,c) values({0},{1},{2})'.format(lat,lng,address))
