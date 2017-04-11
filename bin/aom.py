#!/usr/bin/python2.6
import subprocess
import sys,os,time
import zmq
import threading
import yaml

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
        rc = socket.bind("ipc:///tmp/"+str('0'))
        message = socket.recv()
        if message=='status':
            socket.send("server response! PID:"+str(os.getpid()))
        elif message=='stop':   
            socket.send("Stop to finish")
            sys.exit(1)
        elif message=='start':
            socket.send("Start to finish,pid:"+str(os.getpid()))

            
class serverDaemon(object): 
    def __init__(self):
        pass
        
    def run(self):
        pass

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

    def _start(self,flag):
        if self._ipcExists():
            print('Process has been started')
        else:
            path=os.path.realpath(__file__)
            subprocess.Popen([path,'-d'])
            print(self._getIPCMsg(flag))
            
    def _demon(self):
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
            
    def _getIPCMsg(self,flag):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.setsockopt(zmq.LINGER, 0) 
        socket.connect("ipc:///tmp/0")
        socket.send(flag)
        poller = zmq.Poller()  
        poller.register(socket, zmq.POLLIN)  
        if poller.poll(10*1000): # 10s timeout in milliseconds     
            return (socket.recv())
        else:  
            return('The process has no response')
            #raise IOError("Timeout processing auth request")             
    
    def _help(self):
        msg={'help':{'da.py $parameter':[
                     'da.py start    *Start the process',
                     'da.py stop     *Stop the process',
                     'da.py restart  *Restart the process',
                     'da.py status   *Check the process status']}}          
    
        return(yaml.dump(msg,default_flow_style=False))
    
    def _ipcExists(self):
        if os.path.exists('/tmp/0'):
            return(True)
        else:
            return(False)
    
if __name__ == '__main__':
    run=serverInit(sys.argv)
    run.run()
