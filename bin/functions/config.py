import yaml,os

class configObject(object):
    def __init__(self):
        self.filename='../conf/base.yaml'
        self.config={}
        self._defaultConf()
        
        
    def getConf(self):
        a=self._loadConf()   
        return(a)
    
    def _loadConf(self):
        try:
            f = open(self.filename)  
            config = yaml.load(f)         
            if isinstance(config,dict):             
                return(dict(dict(self.config, **config),**self.configStatic))
            else:
                return(dict(self.config,**self.configStatic)) 
        except IOError,e:
            return(dict(self.config,**self.configStatic))
        
    def _defaultConf(self):
       
        self.config={                    
                     }
        self.configStatic={
                           'pidFile':'../conf/aom.pid',
                           'IPCFile':'../tmp/ipc',
                            }
