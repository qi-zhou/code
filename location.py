#!/usr/bin/env python3
from  urllib import request
import json


def search(value):
    mcc = value.split(",")[0]
    mnc = value.split(",")[1]
    lac = value.split(",")[2]
    ci = value.split(",")[3]
    bs = mcc + ',' + mnc + ',' + lac + ',' + ci
    url = 'http://api.gpsspg.com/bs/?oid=2940&bs=' + bs + '&output=json'
    print(url)
    with request.urlopen(url) as f:
        data = f.read()
        s = json.loads(data.decode('utf-8'))
        if s.get("status") == 200:
            result = s["result"][0]
            lat = result.get("lat")
            lng = result.get("lng")
            address = result.get("address")
            print('INSERT INTO gsm_location(mnc,lac,lng,lat,address,expire_time) values({0},{1},{2},{3},{4},{5},)'.format(mnc, lac, lng, lat, address, "2017-6-20"))
        elif s.get("status") == 404:
            print("未收录次数据")
        elif s.get("status") == 702:
            print("订阅过期,请继续订阅")
        elif s.get("status") == 100:
            print("站点数据维护中")
        elif s.get("status") == 110:
            print("参数格式错误")
        elif s.get("status") == 300:
            print("执行数据查询时出错")
        elif s.get("status") == 701:
            print("未订阅该api服务,订阅后才可以使用")
        elif s.get("status") == 709:
            print("违规暂停,账户违规锁定或因违规当天暂停")
        elif s.get("status") == 900:
            print("拒绝请求,KEY不正确或IP / 网址未绑定")
        elif s.get("status") == 901:
            print("超过套餐限额,可第二天使用或升级套餐")
        else:
            print("位置错误")


if __name__ == '__main__':
    txt = open('/home/zhouqi/code/config.txt', 'r')
    for a in txt.readlines():
        search(a.split()[0])
    txt.close()
