#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import subprocess
import sys,os,time
import zmq
import threading
import yaml
import psutil
import logging
import logging.config
import traceback
from functions import config

#获取基础路径
baseHome=os.path.realpath(__file__)

#修改默认路径
os.chdir(os.path.split(os.path.realpath(__file__))[0])

#获取基础参数
baseParams=config.configObject()
baseParams=baseParams.getConf()

#设置日志格式
#os.makedirs("../log", exist_ok=True)
logging.config.fileConfig("../conf/logging.conf")
stdLogger = logging.getLogger("root")

threadList={'test':''}
systemDict={'main':
                  {'target':'on','state':'on'},
            'thread':{
                      'test':{
                              'switch':{'target':'on','state':'on'},
                              'threadStatus':'',
                             }
                     },
            }

#ipc通讯接口
class IPCInterface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.flag=True
        self.daemon = True
        self.start()
        
    def run(self): 
        try:
            self._run()
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread IPCInterface collapse')
        
    
    def _run(self):
        while 1:
            if self.flag:
                self.ipcFun()
            else:
                break
    
    def ipcFun(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        rc = socket.bind("ipc://"+baseParams['IPCFile'])
        message = socket.recv()
        if message=='status':
            systemDict['thread']['test']['threadStatus']=threadList['test'].isAlive() 
            socket.send("server response! PID:"+str(os.getpid())+'\n'+yaml.dump(systemDict,default_flow_style=False))
        elif message=='stop':  
            self.flag=False
            self.checkProcessEnd()
            socket.send('Process stop completion.')
            systemDict['main']['target']='off'                   
        elif message=='start':
            socket.send("Start to finish,pid:"+str(os.getpid()))
            
    def _stop(self,socket):
        pass
            
    def checkProcessEnd(self):
        for i in systemDict['thread']:
            systemDict['thread'][i]['switch']['target']='off'
          
        for j in systemDict['thread']:
            for x in range(5):
                if systemDict['thread'][j]['switch']['state']=='off':
                    break
                time.sleep(1)

 #测试进程               
class test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon=True
        self.start()
 
    def run(self):
        try:
            self._run()
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread test collapse')
            systemDict['thread']['test']['switch']['state']='off'
            
    def _run(self):
        while 1:
            if systemDict['thread']['test']['switch']['target']=='off':
                systemDict['thread']['test']['switch']['state']='off'
                stdLogger.info('The thread test has stopped.')
                break
            a=b+c
            time.sleep(1)   
    
            
class serverDaemon(object): 
    def __init__(self):
        pass

        
    def run(self):   
        stdLogger.info("Start to finish,pid:"+str(os.getpid()))
        t=IPCInterface()
        t1=test()
        threadList['test']=t1
        while 1:
            if systemDict['main']['target']=='off':
                stdLogger.info('Process stop completion.')
                break
            time.sleep(1)

#服务端初始化
class serverInit(object):
    def __init__(self,param):
        self.param=param
        pass

    def run(self):
        if len(self.param)!=2:
            print(self._help())
        elif self.param[1]=='start':
            self._start(self.param[1])
        elif self.param[1]=='-d':
            self._demon()
        elif self.param[1]=='status':
            self._status(self.param[1])
        elif self.param[1]=='stop':
            self._stop(self.param[1])
        elif self.param[1]=='restart':
            self._stop('stop')
            self._start('start')
        else:
            print(self._help())
    
    #启动进程
    def _start(self,flag):
        if self._ipcExists():
            print('Process has been started')
        else:
            subprocess.Popen([baseHome,'-d'])
            print(self._getIPCMsg(flag))
            
    #守护进程
    def _demon(self):
        s=serverDaemon()
        s.run()
        
            
    def _stop(self,flag):
        if self._ipcExists():
            print('The process is stopping. Please wait.')
            print(self._getIPCMsg(flag))
        else:
            print('Process has not started')
            
    def _status(self,flag):
        if self._ipcExists():
            print(self._getIPCMsg(flag))
        else:
            print('Process has not started')
            
    def _setPidFile(self):
        with open(baseParams['pidFile'],'w') as myfile:
            myfile.write(str(os.getpid()))
    
    #服务端ipc获取    
    def _getIPCMsg(self,flag):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 0) 
        socket.connect("ipc://"+baseParams['IPCFile'])
        socket.send(flag)
        poller = zmq.Poller()  
        poller.register(socket, zmq.POLLIN)  
        if poller.poll(360*1000): # 10s timeout in milliseconds     
            return (socket.recv())
        else:  
            return('The process has no response')
            #raise IOError("Timeout processing auth request")             
    
    def _help(self):
        msg= baseParams['help']      
        return(yaml.dump(msg,default_flow_style=False))
    
    def _ipcExists(self):
        if os.path.exists(baseParams['IPCFile']):
            return(True)
        else:
            return(False)
    
if __name__ == '__main__':
    run=serverInit(sys.argv)
    run.run()
