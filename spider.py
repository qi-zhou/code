#!/usr/bin/env python3
from urllib import request
reqheaders = {
            'Referer': 'http://www.gpsspg.com/bs.htm',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36'
}
bs = '460,00,34860,62041'
url = 'http://api.gpsspg.com/bss/?oid=159&bs={}&hex=10&type=&to=1&output=jsonp&callback=jQuery11020563021744484645_1467786333143&_=1467786333144'.format(bs)
#url = "http://localhost:8000"
req = request.Request(url, headers=reqheaders)
req.add_header('Referer', 'http://www.gpsspg.com/bs.htm')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
