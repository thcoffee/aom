# -*- coding: utf-8 -*-
import salt.client
import traceback
import logging 
import logging.config
stdLogger = logging.getLogger('root')

class saltApi(object):

    def __init__(self,**kwages):
        
        self.input=kwages
        pass
        
    def run(self):
        try:
            #stdLogger.debug(self.input)
            client=salt.client.LocalClient()
            return(client.cmd(**self.input))
        except Exception as info:
            stdLogger.error(traceback.format_exc())
            return({'msg':'执行失败','std':''})
        
    def runbtch(self):
        pass
    
    def runasync(self):
        pass    
        