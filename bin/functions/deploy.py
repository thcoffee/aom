import sys,os,time
import threading
import yaml
import logging
import traceback

stdLogger = logging.getLogger('root.deploy')


class deployAntWar(threading.Thread):
    
    def __init__(self,**kwages):
        threading.Thread.__init__(self)
        self.systemDict=kwages['systemDict']
        self.threadList=kwages['threadList']
        self.daemon = True
        self.start()
        
    def run(self):
        try:
            self._run()
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread deployAntWar collapse')
            self.systemDict['thread']['deployAntWar']['switch']['state']='off'
    
    def _run(self):
        while 1:
            if self.systemDict['thread']['deployAntWar']['switch']['target']=='off':
                self.systemDict['thread']['deployAntWar']['switch']['state']='off'
                stdLogger.info('The thread deployAntWar has stopped.')
                break
            time.sleep(1)