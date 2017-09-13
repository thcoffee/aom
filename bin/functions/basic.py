# -*- coding: utf-8 -*-
import threading
import logging
import traceback
import time
stdLogger = logging.getLogger('root')

#刷新数据字典数据
class  refreshSystemDictObject(threading.Thread):
    
    def __init__(self,**kwages):
        threading.Thread.__init__(self);    
        self.systemDict=kwages['systemDict']
        self.baseParams=kwages['baseParams']
        self.threadList=kwages['threadList']
        self.name=kwages['name']
        self.daemon = True
        self.start()
        pass
        
    def run(self):
        try:
            self._run()
        except Exception as info:
            self.systemDict['thread'][self.name]['threadStatus']=False
            stdLogger.error(traceback.format_exc())
            stdLogger.error('The thread refreshSystemDict collapse')
            
    def _run(self):
        while 1:
            self._refreshSystemDict()
            import time
            time.sleep(1)

    
    def _refreshSystemDict(self):
        for i in self.threadList.keys():
            if i=='task':
                for j in self.threadList[i].keys():
                    self.systemDict['thread'][i][j]['threadStatus']=self.threadList[i][j].isAlive()                 
            else:
                self.systemDict['thread'][i]['threadStatus']=self.threadList[i].isAlive()
        
     