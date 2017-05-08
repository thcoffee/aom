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



#ipc通讯接口
class IPCInterface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
        
    def run(self): 
        
        while 1:
            self._run()
    
    def _run(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        rc = socket.bind("ipc://"+baseParams['IPCFile'])
        message = socket.recv()
        if message=='status':
            socket.send("server response! PID:"+str(os.getpid()))
        elif message=='stop':   
            socket.send("Stop to finish")
            stdLogger.info('Stop to finish')
            sys.exit(1)
        elif message=='start':
            socket.send("Start to finish,pid:"+str(os.getpid()))

            
class serverDaemon(object): 
    def __init__(self):
        pass
        
    def run(self):
        pass

#服务端初始化
class serverInit(object):
    def __init__(self,param):
        self.param=param
        self.threadList={}
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
        stdLogger.info("Start to finish,pid:"+str(os.getpid()))
        #self._setPidFile()
        t=IPCInterface()
        t.run()
        while 1:
            time.sleep(1)
            
    def _stop(self,flag):
        if self._ipcExists():
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
        if poller.poll(10*1000): # 10s timeout in milliseconds     
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
