# -*- coding: utf-8 -*-
import os
import salt.client
import traceback
import subprocess 
import tarfile
import shutil
from pwd import getpwnam 

def installjdk(**kwages):
    try:
        i=_installjdkObj(**kwages)
        return(i.install())        
    except Exception as info:
        return({'msg':'安装失败','std':traceback.format_exc()})
    
class _installjdkObj(object):
    
    def __init__(self,**kwages):
        self.user='deployuser'
        self.group='deploygroup'
        self.remotepath=kwages['localpath']
        self.localpath=kwages['remotepath']
        self.msg={}
        
    def install(self):
        msg=[]
        std=[]
        if os.path.exists(self.remotepath):
            msg.append('jdk已经安装，无需再次安装.')
        else:
            #os.makedirs(self.remotepath, exist_ok=True)
            caller = salt.client.Caller()
            a=caller.cmd('cp.get_file','salt://software/jdk_7u72_linux_64.tar.gz','/tmp/jdk_7u72_linux_64.tar.gz')
            tar = tarfile.open('/tmp/jdk_7u72_linux_64.tar.gz', "r:gz")
            file_names = tar.getnames()
            for file_name in file_names:
                tar.extract(file_name, '/tmp')
            tar.close()
            shutil.move('/tmp/jdk1.7.0_72', self.remotepath)
            #os.chown(self.remotepath, self.user, self.group)
            os.system('chown deployuser:deploygroup -R '+self.remotepath)
            if os.path.exists('/tmp/jdk_7u72_linux_64.tar.gz'):
                os.remove('/tmp/jdk_7u72_linux_64.tar.gz')
            if os.path.exists('/tmp/jdk1.7.0_72'):
                shutil.rmtree('/tmp/jdk1.7.0_72')
            msg.append(self.remotepath)
            msg.append('安装成功。')
        return({'msg':"".join(msg),'std':"".join(std)})    
        