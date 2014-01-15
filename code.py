#!/usr/bin/env python
#coding=utf-8

import web
import hashlib, time, re
import urllib, urllib2
import MySQLdb
from lxml import etree
from xiezhua import xiezhua
import hanzi

db = web.database(dbn='mysql',user='root',pw='password',db='info')
render = web.template.render('templates/')

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        token = "xiezhua"
        params = web.input()
        args = [token, params['timestamp'], params['nonce']]
        args.sort()
        if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
            if params.has_key('echostr'):
                return params['echostr']

    def POST(self):
        str_xml = web.data() 
        xml     = etree.fromstring(str_xml)
        msgType = xml.find("MsgType").text
        fromUser= xml.find("FromUserName").text
        toUser  = xml.find("ToUserName").text
        if   msgType == 'event':
            event = xml.find("Event").text
            if   event == 'subscribe'  :
                return render.weixin(fromUser,toUser,int(time.time()),hanzi.hello)
            elif event == 'unsubscribe':
                db.delete('info', where="weixin_id=$fromUser",vars=locals())
            else:
                pass
        elif msgType == 'text' :
            content  = xml.find("Content").text
            id       = db.select('info' ,what="id"      ,where="weixin_id=$fromUser",vars=locals())
            if len(id) == 0:
                if len(content) > 50:
                    return render.weixin(fromUser,toUser,int(time.time()),hanzi.hello)
                else:
                    code,xiezhua_xml = xiezhua(content.strip(),hanzi.bind_ok,hanzi.weixin,'talk')
                    if code != 200:
                        return render.weixin(fromUser,toUser,int(time.time()),str(code)+hanzi.hello)
                    else:
                        xml0 = etree.fromstring(xiezhua_xml)
                        id   = xml0[0][6][0].text
                        db.insert('info', id=id ,weixin_id=fromUser ,xiezhua_id=content ,sendfrom=hanzi.weixin)
                        return render.weixin(fromUser,toUser,int(time.time()),hanzi.bind_ok)
            else:
                xiezhua_id = db.select('info' ,what="xiezhua_id",where="weixin_id=$fromUser" ,vars=locals())
                sendfrom   = db.select('info' ,what="sendfrom"  ,where="weixin_id=$fromUser" ,vars=locals())
                if   content == 'help':
                    return render.weixin(fromUser,toUser,int(time.time()),hanzi.help)
                elif content[0:8:] == 'sendfrom':
                    sendfrom = content[8::]
                    db.update('info' ,where="weixin_id=$fromUser" ,sendfrom=sendfrom ,vars=locals())
                    sendfrom = db.select('info',what="sendfrom"  ,where="weixin_id=$fromUser" ,vars=locals())
                    if sendfrom[0].sendfrom == content[8::]:
                        code,xiezhua_xml = xiezhua(xiezhua_id[0].xiezhua_id,hanzi.sendfrom_ok+content[8::],content[8::],'talk')
                        return render.weixin(fromUser,toUser,int(time.time()),hanzi.sendfrom_ok+content[8::])
                    else:
                        return render.weixin(fromUser,toUser,int(time.time()),hanzi.sendfrom_fail)
                        code,xiezhua_xml = xiezhua(xiezhua_id[0].xiezhua_id,hanzi.sendfrom_fail,sendfrom[0].sendfrom.encode('raw_unicode_escape'),'talk')

                else:
                    code,xiezhua_xml = xiezhua(xiezhua_id[0].xiezhua_id,content,sendfrom[0].sendfrom,'talk')
                    if code == 200:
                        return render.weixin(fromUser,toUser,int(time.time()),hanzi.send_ok)
                    else:
                        db.delete('info', where="weixin_id=$fromUser" ,vars=locals())
                        return render.weixin(fromUser,toUser,int(time.time()),hanzi.hello)

        elif msgType == 'image' :
            picurl   = xml.find("PicUrl").text
            id       = db.select('info' ,what="id"      ,where="weixin_id=$fromUser",vars=locals())
            if len(id) == 0:
                return render.weixin(fromUser,toUser,int(time.time()),hanzi.hello)
            else:
                xiezhua_id = db.select('info' ,what="xiezhua_id",where="weixin_id=$fromUser" ,vars=locals())
                sendfrom   = db.select('info' ,what="sendfrom"  ,where="weixin_id=$fromUser" ,vars=locals())
                pic        = urllib2.urlopen(picurl).read()
                code,xiezhua_xml = xiezhua(xiezhua_id[0].xiezhua_id,'''[img]'''+picurl+'''[/img]''',sendfrom[0].sendfrom,'talk')
                if code == 200:
                    return render.weixin(fromUser,toUser,int(time.time()),hanzi.send_ok)
#                else:
#                    return render.weixin(fromUser,toUser,int(time.time()),picurl)



if __name__ == "__main__":
    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app = web.application(urls, globals())
    time.sleep(0.01)
    app.run()
