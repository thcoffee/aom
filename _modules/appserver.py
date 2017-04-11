import os,time
import salt.client
import dayin
def getpid(msg):
    time.sleep(10)
    return(msg+str(os.getpid()))

def zu(**msg):
    return(msg['name'])
    
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
