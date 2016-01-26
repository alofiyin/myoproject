# -*- coding: utf-8 -*-
#$Id: SrvEventlet.py 3316 2015-08-02 10:27:53Z fyin $
# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
#ip 地理位置解析

import net

def ip2lc(kw):
    ip = kw['ip']
    print("++++++++ ",len(net.IP_DIST))
    return net.ip2lct(ip)



    

    