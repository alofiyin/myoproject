#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#ip解析
#$Id: jobexecute.py 649 2015-06-08 fiyin $#
__author__ = 'fiyin <alofiyin@gmail.com>'
__version__ = '$Revision: 0.1 $'

import httpwrap
from lxml import etree
import gzip


SF_Dist = {'BJ':'北京','GD':'广东','SD':'山东','ZJ':'浙江','JS':'江苏','SH':'上海','LN':'辽宁','SC':'四川','HA':'河南','HB':'湖北','FJ':'福建','HN':'湖南','HE':'河北','CQ':'重庆','SX':'山西','JX':'江西','SN':'陕西','AH':'安徽','HL':'黑龙江','GX':'广西','JL':'吉林','YN':'云南','TJ':'天津','NM':'内蒙','XJ':'新疆','GS':'甘肃','GZ':'贵州','HI':'海南','NX':'宁夏','QH':'青海','XZ':'西藏','HK':'香港'}
def get_ipview(sf):
    ip=[]
    url  = "http://ips.chacuo.net/view/s_%s" %sf
    http = httpwrap.HttpWrap()
    html = http.request(url).read()
    html = gzip.decompress(html).decode()
    tree = etree.HTML(html) 
    fp   = open('./data/%s'%sf,'w')
    for item in tree.xpath('//dd'):
        node = item.xpath('span')
        #ip.append((node[0].text,node[1].text))
        fp.write('%s %s\n'%(node[0].text,node[1].text))
    fp.close()
    return ip
    

if __name__ == "__main__":
   for sf in SF_Dist.keys():
       get_ipview(sf)   
   
