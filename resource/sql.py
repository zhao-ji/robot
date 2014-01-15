#!/usr/var/env python
#coding=utf-8
import web ,sys

db = web.database(dbn='mysql', user='root', pw='password', db='info')

def select():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    a=db.select('info',what="sendfrom",where="id=24579")
    b=a[0].sendfrom.encode('raw_unicode_escape')
    print b
    print sys.getdefaultencoding()
if __name__ == '__main__':
    select()
