# -*- encoding: utf-8 -*-

from rediswrap import *
from datamodel import *
import task_reg_model

def hello():
    return "hello !!!!!!!!!"

def get_reg_task():
    """
    返回注册的任务信息
    """
    task={}
    for k,v in task_reg_model.task_list.items():
        if 'callback' in k:
            continue
        task[k]=v
    return task
    
def get_reg_task_info(*ag, **kw):
    """
    参数 
    @func 任务函数名
    返回 注册任务参数说明
    """
    func = kw.pop('func','')
    return task_reg_model.task_list[func]['info']
    
def get_workers():
    """返回在线工人的编号
    """
    res = get_online_worker()
    return res

def get_task_workers(*ag,**kw):
    """
    参数
    @job  string workers.jobs 中注册的job
    @cpu_usage cpu的使用率上限
    返回符合条件的 worker 以cpu使用率降序
    """
    job = kw.pop('job')
    cpu_usage = kw.pop('cpu_usage',80)
    workes = get_workers()
    reg = get_workers_reg()
    worke_doing_max=10 #工作站正在执行任务上限
    
    wk = {k:reg[k]['sysinfo']['cpu'][0] * (100-reg[k]['sysinfo']['cpu'][1]) for k in workes if reg[k]['sysinfo']['cpu'][1] < cpu_usage and len(reg[k]['doing']) <worke_doing_max and job in reg[k]['jobs_registry'] }

    sorted_wk = sorted(wk.items(),key=lambda asd:asd[1]*asd[0], reverse=False)
    return [k[0] for k in sorted_wk]
    
def get_workers_reg(*ag,**kw):
    """返回工人注册信息
    """
    res = {}
    name = kw.pop('name','')
    if name:
        res[name]=get_reg_list().get(name)
        return res
    for k, v in get_reg_list().items():
        k = check_key(k)
        res[k] = v
    return res

def getall_sub_task():
    """返回所有的子任务
    """  
    res = {}

    for k, v in get_sub_hash().items():
        k = check_key(k)
        res[k] = v
    return json_dumps(res) 
    
def get_sub_task(*ag,**kw):
    """根据主任务id返回子任务
    """
    id = kw.pop('id','')
    hostry = kw.pop('hostry','')
    res = {}
    if hostry:
        ids = get_task_hitory_list().get(id)['subtaskes']
        stasks_rd = get_sub_history_hash()
    else:
        ids = get_task_list().get(id)['subtaskes']
        stasks_rd = get_sub_hash() 
    try:
        tasks=stasks_rd.mget(ids)
        for i in range(0,len(ids)):
            if tasks[i] is None:
                continue
            res[ids[i]]= check_key(tasks[i])
    except Exception as e:
        print(e)

    return res
    
def get_tasks(*ag, **kw):
    """返回任务列表
    """
    res = []
    hostry = kw.pop('hostry',"")
    if hostry:
        stasks_rd = get_sub_history_hash()
        tasks_rd = get_task_hitory_list()
    else:
        tasks_rd = get_task_list()
        stasks_rd = get_sub_hash() 
    id = kw.pop('id','')
    if id:
        return [tasks_rd.get(id)]
    
    for k, v in tasks_rd.items():
        ids = v.pop('subtaskes')
        v['subtaskes']=[]
        for stk in stasks_rd.mget(ids) :
            if stk:
                v['subtaskes'].append({'id':stk['id'].split('-')[-1],'status':stk['status']})    
        res.append(v)
    return res
 

def taskcmd(*ag, **kw):
    """向worker发送任务指令
        @_cmd 
         0 subtaskes  暂停任务
         1 goon     继续任务
         2 cancel       取消/中止任务
         3 flush        重新执行任务 
         4 redo     重新分配任务
        @ids  主任务号，多个任务号之间以','分隔
    """
    ids = kw.pop('ids','').split(',')
    status = int(kw.pop('status',''))
    stasks_rd = get_sub_hash()    
    mtasks_rd = get_task_list()
    if ids:
        if status==4:
            task = stasks_rd.get(ids[0])
            workers = get_task_workers(job=task['func'])
            if not workers:
                return {'status':-1}
            w=""
            for ww in workers:
                if ww != task['worker']:
                    w = ww
                    break
            task['errinfo']=""
            get_task_queue(w).push(task)
            cmd={'command':'task_status','id':task['id'],'status':2}
            get_command_queue(task['worker']).push(cmd)
            stasks_rd.__delitem__(ids[0])
            return {'status':1}
        if status==3:
            task = stasks_rd.get(ids[0])
            stasks_rd.__delitem__(ids[0])
            task['errinfo']=""
            get_task_queue(task['worker']).push(task)
            return {'status':1}
        task = mtasks_rd.mget(ids)
        for tk in task:
            subtask = stasks_rd.mget(tk['subtaskes'])
            for sk in  subtask:
                cmd={'command':'task_status','id':sk['id'],'status':status}
                get_command_queue(sk['worker']).push(cmd)
    return {'status':1}
        
def get_conn_info(*ag, **kw):
    """获取数据库连接信息
    """
    key = kw.pop('key','')
    if key:
        return get_conn_hash().get(key)
    conn=[]
    for k,v in get_conn_hash().items():
        conn.append(v)
    return conn

def set_conn(*ag, **kw):
    """设置/修改数据库连接
    """
    key  = kw.pop('key','')
    info = kw.pop('info','')
    
    if not key or not info:
        return  {'status':-1}
    import time
    info['uptime'] = int(time.time())
    get_conn_hash().set(key, info)
    return  {'status':0}

def del_conn(*ag, **kw):
    """删除数据库连接
    """ 
    k  = kw.pop('k','').split(',')
    if k:
        rd = get_conn_hash()
        for kk in k:
             rd.__delitem__(kk)
    
    return  {'status':0}
        
def get_cron_task(*ag, **kw):
    """返回定时任务列表
    """
    func = kw.pop('func','')
    biz  = kw.pop('biz','')
    res = []
    for cron in get_cron_set():
        if func and biz and cron['func']==func and cron['biz']==biz:
            return cron
        res.append(cron)
    return res
    
#--------------代理ip-------------
def get_proxyip(*ag, **kw):
    t = kw.pop('t',0)
    res = []
    for k,v in get_tb_prod().items():
        if t:
            res.append({v[1]:"%s:%s"%(k,v[0])})
        else:
            res.append('%s:%s' % (k,v[0]))
    return res
    
    