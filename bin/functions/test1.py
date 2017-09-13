import sys,os,time
import threading
import yaml
import logging

#warLogger = logging.getLogger('warLog.test1')
stdLogger = logging.getLogger('root')

def ddd():
    #warLogger.debug('test') 
    stdLogger.debug('test111')
    
class test1(object):
    
    def __init__(self,**kwages):
        self.msg=eval(kwages['taskcontent'])['msg']
        pass
        
    def run(self):
        time.sleep(20)
        stdLogger.debug(self.msg+' chuliwan.')
        pass