#!/usr/bin/env python3
from urllib import request
import re, json
import os

def search(value):
    reqheaders = {
        'Referer': "http://www.gpsspg.com/bs.htm",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36"
    }

    mnc = re.search(r"mnc:(\d+).*?,",value).group(1)
    cell = re.search(r"cell:(\d+).*?",value).group(1)
    lac = re.search(r"lac:(\d+).*?",value).group(1)

    bs = '460' + ',' + mnc + '0' + ',' + lac + ',' + cell
    url = 'http://api.gpsspg.com/bss/?oid=159&bs={}' \
          '&hex=10&type=&to=1&output=jsonp' \
          '&callback=jQuery11020563021744484645_1467786333143&_=1467786333144'.format(bs)
    req = request.Request(url, headers=reqheaders)
    status_dict = {404: '未收录此数据', 100: '站点数据维护中', 110: '参数格式错误', 300: '执行数据查询时出错', 900: '拒绝请求'}
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
        elif status_dict.__contains__(s.get("status")):
            print(bs + ':' + status_dict.get(s.get("status")))
        else:
            print(bs + ':' + "位置错误")


if __name__ == '__main__':
    values_list = []
    maildata_file = 'config.txt'
    with open(os.path.join(os.getcwd(), maildata_file), 'r') as f:
        for line in f.readlines():
            tmp = search(line)
            if tmp is None:
                continue
            values_list.append(tmp)
try:
    values_str = ", ".join(values_list)
    out_sql = "INSERT INTO barn.gsm_location (mnc,lac,cell,lng,lat,address,expire_time) VALUES {};".format(values_str)

    print(out_sql)
except Exception:
    pass
