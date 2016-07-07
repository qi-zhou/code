#!/usr/bin/env python3
from urllib import request
import re, json


def search(value):
    reqheaders = {
        'Referer': "http://www.gpsspg.com/bs.htm",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36"
    }
    tmp = value.split(",")[0]
    mnc = '0{0}'.format(int(eval(tmp)))
    cell = int(eval(value.split(",")[1]))
    equipmentId = int(eval(value.split(",")[2]))
    lac = int(eval(value.split(",")[3]))
    bs = '460' + ',' + str(mnc) + ',' + str(lac) + ',' + str(cell)
    url = 'http://api.gpsspg.com/bss/?oid=159&bs={}' \
          '&hex=10&type=&to=1&output=jsonp' \
          '&callback=jQuery11020563021744484645_1467786333143&_=1467786333144'.format(bs)
    req = request.Request(url, headers=reqheaders)
    with request.urlopen(req) as f:
        data = f.read().decode('utf-8')
        jieguo = re.findall(r'{.*}', data)
        s = json.loads(jieguo[0])
        if s.get("status") == 200:
            result = s["result"][0]
            lat = result.get("lat")
            lng = result.get("lng")
            address = result.get("address")
            value_list = [mnc, str(lac), str(cell), "'" + lng + "'",
                          "'" + lat + "'", "'" + address + "'", "'2020-12-31'"]
            single_value = "(" + ", ".join(value_list) + ")"
            return single_value
        elif s.get("status") == 404:
            print("未收录次数据")
        elif s.get("status") == 100:
            print("站点数据维护中")
        elif s.get("status") == 110:
            print("参数格式错误")
        elif s.get("status") == 300:
            print("执行数据查询时出错")
        elif s.get("status") == 900:
            print("拒绝请求")
        else:
            print("位置错误")


if __name__ == '__main__':
    values_list = []
    with open('/home/zhouqi/PycharmProjects/location-ui/fail.txt', 'r') as f:
        for line in f.readlines():
            values_list.append(search(line))

    values_str = ", ".join(values_list)
    out_sql = "INSERT INTO barn.gsm_location (mnc,lac,lng,lat,address,expire_time) VALUES {};".format(values_str)
    print(out_sql)
