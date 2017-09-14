import os,time
import salt.client
import dayin
import salt.config
import salt.loader

def getpid(msg):
    time.sleep(10)
    return(msg+str(os.getpid()))

def zu(**msg):
    #__opts__ = salt.config.minion_config('/etc/salt/minion')
   # __grains__ = salt.loader.grains(__opts__)
   # return({'a':'b','c':['a','b'],'id':__grains__['id']})
   caller = salt.client.Caller()
   return({'a':'b','c':['a','b'],'id':caller.sminion.functions['grains.items']('shenme')}) 
def get_file():
    caller = salt.client.Caller()
    a=caller.cmd('cp.get_file','salt://Python-3.4.6.tgz','/root/Python-3.4.6.tgz')
    return a

#1
def getdate():
    return _getDate()

def _getDate():
    return(str(time.time()))    

def wait():
    a=str(time.time())
    time.sleep(int(a[-1]))
    return

def mark(taskid):
    with open('/root/test.log','a') as myfile:
        myfile.write(taskid+' begin\n')
        myfile.flush()
        time.sleep(10)
        myfile.write(taskid+' end\n')
        myfile.flush()

def dy():
    return(dayin.dayin())

def getDict(self):
    return({'date':str(time.time)})
