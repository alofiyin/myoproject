# -*- coding: utf-8 -*-
#falcon路由配置
import falcon
import traceback
import os
def route():
	res={}
	files = os.listdir("./controllers")
	for f in files:
		try:
			if f[:3] == 'ctl':
				m = __import__(f[:-3])
				arrt = dir(m)
				for n in arrt:
					if len(n)>6 and n[-6:]=='Action':
						p = "/%s/%s" % (f[4:-3],n[:-6])
						res[p]=eval('m.'+n)
				#exec("import %s" % )
		except Exception as e:
			traceback.print_exc()
	return res
				