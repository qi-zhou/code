#!/usr/bin/env python3
from  urllib import request
import json


def search(value):
    MCC = value.split(",")[0]
    MNC = value.split(",")[1]
    LAC = value.split(",")[2]
    CI = value.split(",")[3]
    bs = MCC + ',' + MNC + ',' + LAC + ',' + CI
    url = 'http://api.gpsspg.com/bs/?oid=2940&bs=' + bs + '&output=json'
    print(url)
    with request.urlopen(url) as f:
        data = f.read()
        data_dict = json.loads(data.decode('utf-8'))
        if data_dict["status"] == 200:
            result = data_dict["result"][0]
            lat = result["lat"]
            lng = result["lng"]
            address = result["address"]
            print('INSERT INTO barn(a,b,c) values({0},{1},{2})'.format(lat, lng, address))
        elif data_dict["status"] == 404:
            print("未收录次数据")
        elif data_dict["status"] == 702:
            print("订阅过期,请继续订阅")
        elif data_dict["status"] == 100:
            print("站点数据维护中")
        elif data_dict["status"] == 110:
            print("参数格式错误")
        elif data_dict["status"] == 300:
            print("执行数据查询时出错")
        elif data_dict["status"] == 701:
            print("未订阅该api服务,订阅后才可以使用")
        elif data_dict["status"] == 709:
            print("违规暂停,账户违规锁定或因违规当天暂停")
        elif s["status"] == 900:
            print("拒绝请求,KEY不正确或IP / 网址未绑定")
        elif data_dict["status"] == 901:
            print("超过套餐限额,可第二天使用或升级套餐")
        else:
            print("位置错误")


if __name__ == '__main__':
    txt = open('/home/zhouqi/code/config.txt', 'r')
    for a in txt.readlines():
        search(a.split()[0])
    txt.close()
