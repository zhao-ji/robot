#!/usr/bin/env python
#coding=utf-8

import web ,sys
import urllib ,urllib2

def xiezhua(xiezhua_id ,status ,source ,type):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if type == 'talk':        
        status = status.decode('utf-8').encode('gbk')
        source = source.decode('utf-8').encode('gbk')
        type   =   type.decode('utf-8').encode('gbk')
        head   = {'status':status,'source':source,'status_type':type}
        head1  = urllib.urlencode(head)

        user   = 'Basic' + ' ' + xiezhua_id.encode('base64')[:-1]
        user1  = {'Authorization':user}
        url='http://weilairiji.com/api/statuses/update.xml'
        
        send=urllib2.Request(url,head1,user1)
        try:
            f=urllib2.urlopen(send)
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
        source = source.decode('utf-8').encode('gbk')
        type   =   type.decode('utf-8').encode('gbk')
        head   = {'status':status,'status_type':type}
        head1  = urllib.urlencode(head)

        user   = 'Basic' + ' ' + xiezhua_id.encode('base64')[:-1]
        user1  = {'Authorization':user}
        url='http://weilairiji.com/api/statuses/update.xml'
        
        send=urllib2.Request(url,head1,user1)
        try:
            f=urllib2.urlopen(send)
            d=f.getcode()
            if d == 200:
                c=f.read()
                f.close()
                return d,c
            else:
                c=f.read()
                f.close()
                return d,c
        except urllib2.HTTPError:
            return 0,0

