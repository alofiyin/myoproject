# -*- coding: utf-8 -*-
#Copyright  2015/4/21  fiyin
import dbclass
    	
	
def savedata(data,table):
	db = dbclass.dbclass(1)
	res, desc = db.connect()
	if res==-1:
		return (res,desc)
	fields = []
	values = []
	for k,v in data.items():
		fields.append(k)
		#v = db.escape_string(v)
		v=v.replace('"'," ")
		values.append('"%s"' % v)
	sql = "insert into %s(%s)values(%s)" % (table,','.join(fields),','.join(values))

	res,desc = db.query(sql,1)
	return (res,desc)
	

