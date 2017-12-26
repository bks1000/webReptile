# coding=utf-8

#种子文件处理

import bencode
import chardet

btfile = open('F:/HW/OCU27Fz.torrent','rb')
btinfo = bencode.bdecode(btfile.read())
btfile.close()

info = btinfo['info']
print type(info) # info(dict类型) ,info['files'](list类型),info['files'][0](dict类型)
btlist = []
for f in info['files']:
    #if len(ls['path']) > 1:
    #    btlist[ls['path'][0]] = {'path':ls['path'][0]+'/'+ls['path'][1],'size':ls['length']}
    #else:
    #    btlist[ls['path'][0]] = {'path':ls['path'][0],'size':ls['length']}
    for key in f:
        if key=="path":
            p = f['path']
            extend = p[0][-3:]
            print extend
            if extend!="url" and extend!="rar" and extend!="txt" and extend!="URL" and extend!="mht" and extend!="jpg" and extend!="gif":
                pass
            else:
                btlist.append(f)

raise Exception

print len(btlist)
for f in btlist:
    print f



info['files']=btlist
newinfo = bencode.bencode(info)
btfile = open('F:/HW/NEWOCU27Fz.torrent','wb')
btfile.write(newinfo)
btfile.close()
#print btlist
