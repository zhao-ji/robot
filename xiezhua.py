#!/usr/bin/env python
#coding=utf-8

import web ,sys
import urllib ,urllib2

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

def xiezhua(xiezhua_id ,status ,source ,type):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if type == 'talk':        
        status = status.decode('utf-8').encode('gbk')
        source = source.decode('utf-8').encode('gbk')
        type   =   type.decode('utf-8').encode('gbk')
        data   = {'status':status,'source':source,'status_type':type}
        data  = urllib.urlencode(data)

        headers   = 'Basic' + ' ' + xiezhua_id.encode('base64')[:-1]
        headers  = {'Authorization':headers}
        url = 'http://weilairiji.com/api/statuses/update.xml'
        
        req = urllib2.Request(url,data=data,headers=headers)
        try:
            f=urllib2.urlopen(req)
            d=f.getcode()
            if d == 200:
                c=f.read()
                f.close()
                return d,c
            else:
                f.close()
                return d,'fail'
        except urllib2.HTTPError:
            return 0,0

    if type == 'photo':
        register_openers()
        source = source.decode('utf-8').encode('gbk')
        type   =   type.decode('utf-8').encode('gbk')
        status = open('picture/1.jpg','rb')
        values = {'status':status,'source':source,'status_type':type}
        data, headers = multipart_encode(values)
        
        Authorization = 'Basic' + ' ' + xiezhua_id.encode('base64')[:-1]
        headers.update({'Authorization':Authorization})
        
        url    = 'http://weilairiji.com/api/statuses/update.xml'
        
        req    = urllib2.Request(url,data=data,headers=headers)
        try:
            f=urllib2.urlopen(req)
            d=f.getcode()
            if d == 200:
                c=f.read()
                f.close()
                print d,c
            else:
                c=f.read()
                f.close()
                print d,c
        except urllib2.HTTPError:
            print 0,0

if __name__ == '__main__':
    xiezhua('shijunzi@myopera.com:sxjzz7wIyel' ,'status' ,'python' ,'talk')
