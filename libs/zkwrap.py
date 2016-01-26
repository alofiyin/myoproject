#_*_coding:utf-8_*_
from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging,time
logging.basicConfig(
    level = logging.DEBUG,
    format = "[%(asctime)s] %(levelname)-8s %(message)s"
)

log = logging
POOL = {
    'default': None
}
def setup(name,args):
    """
    注册zk
    """
    hosts = args.pop('hosts')
    if args:
        zk = KazooClient(hosts,**args)
    else:
        zk = KazooClient(hosts)
    zk.start()
    POOL[name]=zk

def get(name='default'):
    if name in POOL:
        return POOL[name]
    return None
    

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        print("zkserver is lost!")
    elif state == KazooState.SUSPENDED:
            # Handle being disconnected from Zookeeper
        print("disconnected! ")
    else:
        print("isconnected!")
        # Handle being connected/reconnected to Zookeeper
            


#zk.add_listener(my_listener)

