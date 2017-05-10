import sys,os,time
import threading
import yaml
import logging

warLogger = logging.getLogger('warLog.test1')
stdLogger = logging.getLogger('root.test1')

def ddd():
    warLogger.debug('test') 
    stdLogger.debug('test')