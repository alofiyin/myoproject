#_*_coding:utf-8_*_
import zkwrap
import kazoo.protocol.states
import traceback
from kazoo.client import KazooState

def proxy(kw):
	if 'cmd' not in kw:
		return [-1,"cmd not set"]
	args = kw.get('args',[])
	kwargs = kw.get('kwargs',{})
	for i in range(0,len(args)):
		if args[i] == 'True':
			args[i]=True
		elif args[i] == 'False':
			args[i]=False

	for k,v in kwargs.items():
		if v == 'True':
			kwargs[k]=True
		elif v == 'False':
			kwargs[k]=False
	zk = zkwrap.get()
	try:
		if hasattr(zk,kw['cmd']):
			f = getattr(zk,kw['cmd'])
			if args and kwargs:
				res = f(*args,**kwargs)
			elif args:
				res = f(*args)
			else:	
				res = f()
			#ÖØ¹¹ obj->dist
			if kw['cmd'] == 'get_children':
				return get_children(args)
			if kw['cmd'] in ['get','get_acls','set_acls','set']:
				_res=[]
				for i in range(0,len(res)):
					if isinstance(res[i],kazoo.protocol.states.ZnodeStat) and hasattr(res[i],'_fields'):
						tmp={}
						for field in res[i]._fields:
							tmp[field]= getattr(res[i],field)
						_res.append(tmp)
					else:
						_res.append(res[i])
				return 0,_res			
						
			return [0,res]
		
		return [-3,"has no attribute:%s"%kw['cmd']] 
	except Exception as e:
		traceback.print_exc()
		print(e)
		return [-2,""]

def get_children(kw):

	try:
		zk = zkwrap.get()
		res = zk.get_children(*kw)
		if len(kw)==3 and kw[2]:
			_tm = []
			print(res[1])		
			for i in range(0,len(res[1])):
				if isinstance(res[1][i],kazoo.protocol.states.ZnodeStat) and hasattr(res[1][i],'_fields'):
					tmp={}
					for field in res[1][i]._fields:
						tmp[field]= getattr(res[1][i],field)
						_tm.append(tmp)
					else:
						_tm.append(res[1][i])
			res[1]=_tm
		return 0,res
	except :
		traceback.print_exc()
		return [-2,""]
	return res				