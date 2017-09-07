#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import subprocess
import sys,os,time
import zmq
import threading
import socket
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
#print(path)
#print(os.popen('pwd').read())

#设置日志格式
#os.makedirs("../log", exist_ok=True)
logging.config.fileConfig("../conf/logging.conf")
stdLogger = logging.getLogger("root")
warLogger = logging.getLogger("warLog")

from functions import test1
from functions import deploy
from functions import task
#获取基础参数
baseParams=config.configObject()
baseParams=baseParams.getConf()

#线程池
threadList={
            'test':'',
            'deployAntWar' :'' ,
            'task':''            
             }

#系统字典
systemDict={'main':
                  {'target':'on','state':'on'},
            'thread':{
                      'test':{
                              'switch':{'target':'off','state':'off'},
                              'threadStatus':'',
                             },
                       'deployAntWar':{
                              'switch':{'target':'on','state':'on'},
                              'threadStatus':'',
                             } , 
                        'task':{
                                'switch':{'target':'on','state':'on'},
                                'threadStatus':'',
                                } ,                            
                     },
            }

#通讯工作线程
class IPCInterface(threading.Thread):
    def __init__(self,worker_url, context):
        threading.Thread.__init__(self)
        self.worker_url=worker_url
        self.context=context
        self.flag=True
        self.daemon = True
        self.start()
        
    def run(self): 
        try:
            self._run()
        except Exception as info:
            systemDict['main']['target']='off'  
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread IPCInterface collapse')
        
    
    def _run(self):
        socket = self.context.socket(zmq.REP)   
        socket.connect(self.worker_url)
        while 1:
            if self.flag:     
                self._ipcFun(socket)
            else:
                break
    
    def _ipcFun(self,socket):

        
        message = socket.recv_json()
        if message['action']=='status':
            #systemDict['thread']['test']['threadStatus']=threadList['test'].isAlive() 
            systemDict['thread']['deployAntWar']['threadStatus']=threadList['deployAntWar'].isAlive() 
            systemDict['thread']['task']['threadStatus']=threadList['task'].isAlive() 
            socket.send_json({'data':{"server response! PID:"+str(os.getpid()):systemDict}})
        elif message['action']=='stop':  
            self.flag=False
            self._checkProcessEnd()
            socket.send_json({'data':'Process stop completion.'})
            systemDict['main']['target']='off' 

        elif message['action']=='forcestop':   
            self.flag=False        
            socket.send_json({'data':'Process forcestop completion.'})
            #time.sleep(5)
            systemDict['main']['target']='off' 
        elif message['action']=='start':
            socket.send_json({'data':"Start to finish,pid:"+str(os.getpid())})
        elif message['action']=='addlog':
            stdLogger.info(message['data'])
            socket.send_json({'data':'addlog completion.'})
        else:
            socket.send_json({'data':'unknow parameter'})

        
#给所有线程下关闭指令 检测所有线程是否停止    
    def _checkProcessEnd(self):
        for i in systemDict['thread']:
            systemDict['thread'][i]['switch']['target']='off'
          
        for j in systemDict['thread']:
            for x in range(360):
                if systemDict['thread'][j]['switch']['state']=='off':
                    break
                time.sleep(1)

 #测试线程            
class test(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon=True
        self.start()
 
    def run(self):
        try:
            self._run()
        except Exception as info:
            systemDict['main']['target']='off'  
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread startIPCInterface collapse')
            
    def _run(self):
        while 1:
            if systemDict['thread']['test']['switch']['target']=='off':
                systemDict['thread']['test']['switch']['state']='off'
                stdLogger.info('The thread test has stopped.')
                break
            a=b+c
            time.sleep(1)   
    
#通讯启动线程
class startIPCInterface(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
        
    def run(self): 
        try:
            self._run()
        except Exception as info:
            systemDict['main']['target']='off'  
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread startIPCInterface collapse')

    
    def _run(self):
        url_worker = "inproc://workers"  
        url_client = baseParams['tcpaddr']
        context = zmq.Context(1) 
        clients = context.socket(zmq.XREP)   
        clients.bind(url_client)   
       
        workers = context.socket(zmq.XREQ)   
        workers.bind(url_worker) 
        for i in range(5):
            t=IPCInterface(url_worker, context)
        zmq.device(zmq.QUEUE, clients, workers) 
        
#守护进程    
class serverDaemon(object): 
    def __init__(self):
        pass

        
    def run(self):   
        stdLogger.info("Start to finish,pid:"+str(os.getpid()))
        #启动通讯线程
        t=startIPCInterface()
        
        dAW=deploy.deployAntWar(**{'threadList':threadList,'systemDict':systemDict})
        threadList['deployAntWar']=dAW
        
        #启动任务处理线程
        taskThread=task.taskThreadObj(**{'threadList':threadList,'systemDict':systemDict,'baseParams':baseParams})
        threadList['task']=taskThread
        stdLogger.debug('wanshi')
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
        if len(self.param)<2:
            print(self._help())
        elif self.param[1]=='start':
            self._start({'action':self.param[1],'data':''})
        elif self.param[1]=='-d':
            self._demon()
        elif self.param[1]=='status':
            self._status({'action':self.param[1],'data':''})
        elif self.param[1]=='stop':
            self._stop({'action':self.param[1],'data':''})
        elif self.param[1]=='forcestop':
            self._stop({'action':self.param[1],'data':''})
        elif self.param[1]=='restart':
            self._stop({'action':'stop','data':''})
            self._start({'action':'start','data':''})
        elif len(self.param)==3:
            if self.param[1]=='addlog' and self.param[2]:
                self._addlog({'action':self.param[1],'data':self.param[2]})
        else:
            print(self._help())
    

    def _addlog(self,flag):
        if self._ipcExists():
            print('The process is addlog. Please wait.')
            print(self._getIPCMsg(flag)['data'])
        else:
            print('Process has not started')    

    #启动进程
    def _start(self,flag):
        if self._ipcExists():
            print('Process has been started')
        else:
            subprocess.Popen([baseHome,'-d'])
            print(self._getIPCMsg(flag)['data'])
            
    #守护进程
    def _demon(self):
        s=serverDaemon()
        s.run()
        
            
    def _stop(self,flag):
        if self._ipcExists():
            print('The process is stopping. Please wait.')
            print(self._getIPCMsg(flag)['data'])
        else:
            print('Process has not started')
            
    def _status(self,flag):
        if self._ipcExists():
            print(yaml.dump(self._getIPCMsg(flag)['data'],default_flow_style=False))
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
        #socket.connect("ipc://"+baseParams['IPCFile'])
        socket.connect(baseParams['tcpaddr'])
        socket.send_json(flag)
        poller = zmq.Poller()  
        poller.register(socket, zmq.POLLIN)  
        if poller.poll(360*1000): # 10s timeout in milliseconds     
            return (socket.recv_json())
        else:  
            return('The process has no response')
            #raise IOError("Timeout processing auth request")             
    
    #帮助
    def _help(self):
        msg= baseParams['help']      
        return(yaml.dump(msg,default_flow_style=False))
    
    #判断端口是否被占用
    def _ipcExists(self):
        s=socket.socket()       #建立soket对象
        s.settimeout(2)   #设置超时时间
        try:
            s.connect(baseParams['checktcpaddr'])#连接目标
            return True
        except Exception,e:
            return False
    
if __name__ == '__main__':
    run=serverInit(sys.argv)
    run.run()
