# -*- coding: utf-8 -*-
import os
import salt.client
import traceback
import subprocess 
import tarfile
import shutil
from pwd import getpwnam 
import logging
stdLogger = logging.getLogger()

def installjdk(**kwages):
    try:
        i=_installjdkObj(**kwages)
        return(i.install())        
    except Exception as info:
        return({'msg':'安装失败','std':str(traceback.format_exc())})
    
class _installjdkObj(object):
    
    def __init__(self,**kwages):
        self.user='deployuser'
        self.group='deploygroup'
        self.remotepath=kwages['remotepath']
        self.localfiles=kwages['localfiles']
        self.localpath=kwages['localpath']
        self.msg={}
        
    def install(self):
        msg=[]
        std=[]
        if os.path.exists(self.remotepath):
            msg.append('jdk已经安装，无需再次安装.')
        else:
            caller = salt.client.Caller()
            a=caller.cmd('cp.get_file',os.path.join('salt://',self.localpath,self.localfiles),os.path.join('/tmp',self.localfiles))
            stdLogger.warning(str(a))
            tar = tarfile.open(os.path.join('/tmp',self.localfiles), "r:gz")
            file_names = tar.getnames()
            for file_name in file_names:
                tar.extract(file_name, '/tmp')
            tar.close()
            if os.path.exists('/tmp/jdk'):
                shutil.move('/tmp/jdk', self.remotepath)
                os.system("".join(['chown ',self.user,':',self.group,' -R ',self.remotepath]))
                if os.path.exists(os.path.join('/tmp',self.localfiles)):
                    os.remove(os.path.join('/tmp',self.localfiles))
                if os.path.exists('/tmp/jdk'):
                    shutil.rmtree('/tmp/jdk')
                msg.append(self.remotepath)
                msg.append('jdk安装成功。')
            else:
                msg.append('jdk解压失败。')
        return({'msg':"".join(msg),'std':"".join(std)})    

def installnginx(**kwages):
    try:
        i=_installnginxObj(**kwages)
        return(i.install())        
    except Exception as info:
        return({'status':False,'msg':'安装失败','std':str(traceback.format_exc())})
    
class _installnginxObj(object):
    
    def __init__(self,**kwages):
        self.user='deployuser'
        self.group='deploygroup'
        self.remotepath=kwages['remotepath']
        self.localfiles=kwages['localfiles']
        self.localpath=kwages['localpath']
        self.msg={}        
    
    def install(self):
        msg=[]
        std=[]
        
        if os.path.exists(self.remotepath):
            status=False
            msg.append('jdk已经安装，无需再次安装.')    
        else:
            caller = salt.client.Caller()
            a=caller.cmd('cp.get_file',os.path.join('salt://',self.localpath,self.localfiles),os.path.join('/tmp',self.localfiles))
            stdLogger.warning(str(a))  
            tar = tarfile.open(os.path.join('/tmp',self.localfiles), "r:gz")            
            file_names = tar.getnames()
            for file_name in file_names:
                tar.extract(file_name, '/tmp')
            tar.close()
            if os.path.exists('/tmp/nginx'):
                shellStr="".join(['cd /tmp/nginx/&&./configure --prefix=',self.remotepath,'&&make&&make install'])
                rm=subprocess.Popen(shellStr,shell=True,universal_newlines=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE) 
                stdout=rm.stdout.read()
                stderr=rm.stderr.read()
                stdLogger.warning(stdout+stderr)
                if os.path.exists(self.remotepath):
                    if os.path.exists(os.path.join('/tmp',self.localfiles)):
                        os.remove(os.path.join('/tmp',self.localfiles))
                    if os.path.exists('/tmp/nginx'):
                        shutil.rmtree('/tmp/nginx')
                    msg.append('nginx安装成功。')
                    status=True
                else:
                    status=False
                    msg.append('nginx编译安装失败。')   
            else:
                status=False
                msg.append('nginx解压失败。')
        return({'msg':"".join(msg),'std':"".join(std)})  

def installtomcat(**kwages):
    try:
        i=_installtomcatObj(**kwages)
        return(i.install())        
    except Exception as info:
        return({'status':False,'msg':'tomcat安装失败','std':str(traceback.format_exc())})
    
class _installtomcatObj(object):
    
    def __init__(self,**kwages):
        self.user='deployuser'
        self.group='deploygroup'
        self.remotepath=kwages['remotepath']
        self.localfiles=kwages['localfiles']
        self.localpath=kwages['localpath']
        self.serverxml=kwages['serverxml']
        self.catalina=kwages['catalina']
        self.msg={}
        
    def install(self):
        msg=[]
        std=[]
        if os.path.exists(self.remotepath):
            msg.append('tomcat已经安装，无需再次安装.')
            status=False
        else:
            caller = salt.client.Caller()
            a=caller.cmd('cp.get_file',os.path.join('salt://',self.localpath,self.localfiles),os.path.join('/tmp',self.localfiles))
            stdLogger.warning(str(a))
            tar = tarfile.open(os.path.join('/tmp',self.localfiles), "r:gz")
            file_names = tar.getnames()
            for file_name in file_names:
                tar.extract(file_name, '/tmp')
            tar.close()
            if os.path.exists('/tmp/tomcat'):
                shutil.move('/tmp/tomcat', self.remotepath)
                with open(os.path.join(self.remotepath,'conf','server.xml'),'w') as serverfile:
                    serverfile.write(self.serverxml)
                with open(os.path.join(self.remotepath,'bin','catalina.sh'),'w') as catalinafile:
                    catalinafile.write(self.catalina)
                os.system("".join(['chown ',self.user,':',self.group,' -R ',self.remotepath]))
                if os.path.exists(os.path.join('/tmp',self.localfiles)):
                    os.remove(os.path.join('/tmp',self.localfiles))
                if os.path.exists('/tmp/tomcat'):
                    shutil.rmtree('/tmp/tomcat')
                msg.append(self.remotepath)
                msg.append('tomcat安装成功。')
                status=True
            else:
                status=False
                msg.append('tomcat解压失败。')
        return({'status':status,'msg':"".join(msg),'std':"".join(std)})           