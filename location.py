#!/usr/bin/env python
#coding: utf-8
import urllib2
import json
 
html = urllib2.urlopen(r'http://api.gpsspg.com/bs/?oid=2940&bs=460,01,40977,2205409&output=json')
 
hjson = json.loads(html.read())

print hjson
 
