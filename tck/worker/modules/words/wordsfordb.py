#_*_coding:utf-8_*_

# Copyright (c) 2015 fiyin <alofiyin@gmail.com>
# All rights reserved
#非法关键词查找模块
#$Id: wordsfordb.py 649 2015-06-12 fiyin $#

#from wbsp_process import WBProcess
#from threading import Thread
import base64
import mysqlwrap
import traceback
import jobstatus
import global_list
from utils import get_process_count
import logging,sys,json,time
import multiprocessing as mp
import eventlet
from threading import Thread
from datamodel import get_result_queue,get_conn_hash
logger = logging.getLogger('worker.WordsForDB')

KW_TABLE = 'wbsp.keywords'
KW_FIELDS = 'word,group'
KWORDS = None
def fielt(item,kwords,kweight,fweight,q=None):
    """对单条记录进行关键词匹配，并计算权重，结果压入输出队列
    multiprocessing.Pool.apply_async不支持类成员函数，所以这个处理
    函数要单独出来
    参数说明:
    @item dict 要处理的数据库记录
    @kwords list 关键词列表
    @kweight dict 关键词权重
    @fweight dict 字段权重
    @q Queue      输出队列
    """
    res ={}
    k_dict={}
    _kw = 0
    id = item.pop('id')
    
    for i,s in item.items():
        try:
            ks = [k for k in kwords if k in s]           
            if ks:
                k_dict[i]=ks
                _kw += sum([kweight[k] for k in ks])
                _kw+=fweight[i]
        except:
            print(s)
            traceback.print_exc() 
    if k_dict: 
        res['id'] = id
        res['weight'] = _kw
        res['content'] = k_dict
        if q : q.put(res)
        return res

def fielt_srv(kwords,kweight,fweight,in_q,out_q,exit_flag):
    """对单条记录进行关键词匹配，并计算权重，结果压入输出队列
    multiprocessing.Pool.apply_async不支持类成员函数，所以这个处理
    函数要单独出来
    参数说明:
    @kwords list 关键词列表
    @kweight dict 关键词权重
    @fweight dict 字段权重
    @in_q Queue      输入队列
    @out_q Queue     输出队列
    @exit_flag Event 退出标记
    """
    while 1:
        if exit_flag.is_set() and in_q.qsize()==0:
            import os
            print('child %s exit...' % os.getpid())
            break
        if in_q.qsize()==0:
            time.sleep(1)
            continue
        #print(exit_flag.is_set(),in_q.qsize())
        item = in_q.get()   
        res ={}
        k_dict={}
        _kw = 0
        id = item.pop('id')
        
        for i,s in item.items():
            try:
                ks = [k for k in kwords if k in s]           
                if ks:
                    k_dict[i]=ks
                    _kw += sum([kweight[k] for k in ks])
                    _kw+=fweight[i]
            except:
                print(s)
                traceback.print_exc() 
        if k_dict: 
            res['id'] = id
            res['weight'] = _kw
            res['content'] = k_dict
            out_q.put(res)

 
class WordsForDB(Thread):
    """
        参数说明
       @dbsource    数据库源（考虑加密方式）
       {type:数据类型 mysql,
       server:服务器连接信息
       {标识名:{host:ip地址, port:端口号, user:用户名, passwd:密码, dbname:数据库名,charset:字符编码}
       }
       
       @input 输入数据
        {server:标识名,data:{table:表名, 'fields':字段, 'where':条件,'range':id范围,weight:权重{字段名:权重值}}
       @output输出数据
       {server:标识名,data:{table:表名, 'fields':字段}
       
       @kwsource关键词来源
       {server:标识名,data:{table:表名,'fields':字段,'where'条件}
       
       @keywords 关键词
       []
       @return:是否返回结果 False or True
       
    """
    def __init__(self,*_args,**_kw ):
        super(WordsForDB, self).__init__()
        self._dbsource  = {}
        self._input     = _kw.pop('input',None)
        self._output    = _kw.pop('output',{})
        self._kwsource  = _kw.pop('kwsource',None)
        self._keywords  = _kw.pop('keywords',None)
        self._return    = _kw.pop('return',False)
        self._args      = _args
        self._kw        = _kw
        self.taskid     = _kw.pop('id')
        self.powerlevel = _kw.pop('powerlevel','mid')
        self.pid        = _kw.pop('pid')
        self.exit_flag  = mp.Event()#退出标志
        self.keyweight  = {}        #关键词权重
        self.keywords   = []        #关键词 
        self.rowstep    = 10000     #单次从数据库取的记录数
        self.result     = []        #存放返回结果
        
        self.init()
    def init(self):         
        global KWORDS
        if self._input is None:
            raise Exception("not set input config!")
        if self._kwsource is None and self._keywords is None:
            raise Exception("not set keywords!")
        
        if self._dbsource is None:
            raise Exception("not set dbsource!")
        #注册数据库连接
        conn_rd = get_conn_hash()
        info = conn_rd.get(self._input['dbserver'])['info']
        info['dbname']=self._input['data']['dbname']
        mysqlwrap.setup_db(self._input['dbserver'],info)
        
        info = conn_rd.get(self._kwsource['dbserver'])['info']
        info['dbname']=self._kwsource['data']['dbname']
        mysqlwrap.setup_db(self._kwsource['dbserver'],info) 

        info = conn_rd.get(self._output['dbserver'])['info']
        info['dbname']=self._output['dbname']
        mysqlwrap.setup_db(self._output['dbserver'],info)    
        
        mysqlwrap.pool_monitor()
        
        #生成keywords
        if self._keywords:
            self.keywords = self._keywords
            KWORDS = self.keywords
            
        else:
            db = mysqlwrap.get_db(self._kwsource['dbserver'])
            res,desc = db.query(self._kwsource['data'])

            if res == -1 or not desc:
                print(res,desc)
                raise Exception("no keywords!")
            
            for row in desc:
                if row['k_word']:
                    self.keywords.append(row['k_word'])
                    self.keyweight[row['k_word']]=row['k_weight']
   
    def output_data(self,queue,exit_flag):
        """输出结果到数据库
        """
        kword_stat={}
        kcount = 0
        out_db = mysqlwrap.get_db(self._output['dbserver'])
        #插入sql模版，如果记录存在则更新
        tb = self._output['table']      
        insert_sql = "insert into " + tb + "(rowid,contents,tb_name,k_weight) values('%s','%s','" + self._input['data']['table'] + "','%s') on DUPLICATE KEY UPDATE contents='%s',k_weight='%s'"

        while 1:
            if exit_flag.is_set() and queue.qsize()==0:
                import os
                print("out_db exit...",os.getpid())
                #sql = "insert into illegal_log(kcount,taskid,contents)values('%s','%s','%s')" % \
                #(kcount,self.taskid,mysqlwrap.addslashes(json.dumps(kword_stat)))
                
                #res,desc = out_db.query(sql,1)
                get_result_queue(self.pid).push(kword_stat)
                break
            #print("im waiting for data.....",queue.qsize())
            try:
                try:
                    row = queue.get(timeout=5)
                except:
                    continue
                
                id = row.pop('id')
                weight = row.pop('weight')
                #小于或等设置的输出权重，刚放弃
                if weight <= self._output['weight']:
                    continue
                #统计关键匹配数量
                for ks in row['content'].values():
                    for k in ks:
                        kcount+=1
                        if k in kword_stat:
                            kword_stat[k]+=1
                        else:
                            kword_stat[k]=1
                            
                content = mysqlwrap.addslashes(json.dumps(row.get('content')))
                
                res, desc = out_db.query(insert_sql % (id, content, weight,content, weight))
                
            except Exception as e:
                
                logger.error(str(e))
    def data_source(self,db,q_pool,sql_item):
        stime = time.time()
        print(mysqlwrap.structure_sql(sql_item))
        res, desc = db.query(sql_item)
        print("select user time",time.time()-stime,len(desc),mysqlwrap.structure_sql(sql_item))
        if res == -1:
            time.sleep(3)
        q_index = 0
        for row in desc:
            if q_index == len(q_pool):q_index=0
            q_pool[q_index].put(row)
            q_index+=1
                
                                
    def close(self):
        self.exit_flag.set()
            
    def run(self):
        manager = mp.Manager()
        queue = manager.Queue()
        in_queue = manager.Queue()
        out_db_exit = mp.Event()
        input_db = mysqlwrap.get_db(self._input['dbserver'])
        sql_item = self._input['data']
        #设置id范围
        if 'range' in sql_item and sql_item['range']:
            minid, maxid = sql_item.pop('range')
        else:
            res, desc = input_db.query("select min(id) as min,max(id) as max from %s" % sql_item['table'])
            minid, maxid = desc[0]['min'], desc[0]['max']
        sql_where = sql_item.pop('where','')
        
        #字段权重
        weight = sql_item.pop('weight')
        
        if sql_where:   sql_where+= " and "
        
        #定义运行级别取得进程数
        #pool = mp.Pool(get_process_count(self.powerlevel))
        """以守护的方式运行"""
        pnum = get_process_count(self.powerlevel)
        pool = []
        q_pool=[]
        for i in range(0,pnum):
            q = manager.Queue()
            q_pool.append(q)
            pool.append(mp.Process(target=fielt_srv, args=(self.keywords,self.keyweight,weight,q,queue,self.exit_flag)))
            pool[i].daemon = True
            pool[i].start()
        """-"""
        p = None
        #启动输出线程
        if self._output:
            
            p=mp.Process(target=self.output_data, args=(queue,out_db_exit))
            p.start()
            #pool.append(p)
            #pool.apply_async(output_data,(self,queue,self.exit_flag))
            #output_data(self,queue,self.exit_flag)
        p_start = time.time()
        #e_pool = eventlet.GreenPool(10)
        item=[]
        while minid < maxid:
            #检查退出状态
            if self.exit_flag.is_set() or global_list.G_EXIT:
                pool.close()
                pool.join()
                self.close()
                break
            #检查任务状态
            if global_list.TASK_STAUS[self.taskid] == 1: #暂停状态
                time.sleep(1)
                continue
            if global_list.TASK_STAUS[self.taskid] == 2: #退出状态
                #pool.close()
                #pool.join()
                #self.close()
                break
            stop_id = minid + self.rowstep
            if stop_id > maxid : stop_id = maxid
            _sql_item=sql_item.copy()
            _sql_item['where'] = "%s id >= %s and id < %s" % (sql_where, minid, stop_id)
            res, desc = input_db.query(_sql_item)
            """这里sql_item存在同步问题，有共享冲突"""
            #e_pool.spawn_n(self.data_source,input_db,q_pool,_sql_item)
            #item.append(_sql_item)
            minid = stop_id
            if res == -1:
                print(desc)
                time.sleep(3)
                continue
            #result = []
            q_index = 0
            for row in desc:
                #ps = pool.apply_async(func=fielt,args=(row,self.keywords,self.keyweight,weight,queue))
                
                #fielt(row,self.keywords,self.keyweight,weight,queue)
                #if self._return: result.append(ps)      
                #数据队列模式
                if q_index == len(q_pool):q_index=0
                q_pool[q_index].put(row)
                q_index+=1
            
            """返回结果的代码
            if 1:#self._return:
                for i in result:
                    _res = i.get()
                    print(_res)
                    if _res:
                        self.result.append(_res)
            
            """  

        #任务完成
        #pool.close()
        #pool.join()
        self.close()
        #if p: p.join()
        #import pdb
        #pdb.set_trace()
        
        print(len(pool))
        for i in range(0,len(pool)):
            print('join..',pool[i].pid)
            if global_list.TASK_STAUS[self.taskid] == 2:
                pool[i].terminate()
            else:
                pool[i].join()
        print("is done")
        out_db_exit.set()
        if p: p.join()
        print("finish job user :" ,time.time()-p_start)
        jobstatus.done(self.taskid)    
        