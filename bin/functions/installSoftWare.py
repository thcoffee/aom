from functions import saltApi
import logging
import yaml
stdLogger = logging.getLogger('root')
class jdk(object):
    '''
    {'task':'installjdk','remotepath':'/home/deployuser/adcc/software/jdk1','localpath':'/home/deployuser/aom/software/jdk_7u72_linux_64.tar.gz','node':['test207']}
    '''
    
    def __init__(self,**kwages):
        self.taskDict=eval(kwages['taskcontent'])
        self.user='deployuser'
        self.group='deploygroup'
        self.remotepath=self.taskDict['localpath']
        self.localpath=self.taskDict['remotepath']
        self.node=self.taskDict['node']
        
        pass
        
    def install(self):
        s=saltApi.saltApi(**{'tgt':self.node,
                             'fun':'installsoftware.installjdk',
                             'timeout ':60,
                             'kwarg':{
                                      'remotepath':self.remotepath,
                                      'localpath':self.localpath,
                                      'user':self.user,
                                      'group':self.group,              
                                      },
                             'expr_form':'list'})
        #stdLogger.debug(yaml.dump(s.run(),default_flow_style=False))
        #stdLogger.debug(s.run())
        dict=s.run()
        for i in dict:
            for j in dict[i]: 
                stdLogger.debug(dict[i][j])
        pass