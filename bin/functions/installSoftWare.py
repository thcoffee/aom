# -*- coding: utf-8 -*-
from jinja2 import Template 
from functions import saltApi
import logging
import yaml
import pymysql

stdLogger = logging.getLogger('root')
class jdk(object):
    '''    {'task':'installsoftware','name':'jdk','remotepath':'/home/deployuser/adcc/software/jdk1','localpath':'/home/deployuser/aom/software/jdk_7u72_linux_64.tar.gz','node':['test207']}
    '''
    
    def __init__(self,**kwages):
        self.taskDict=eval(kwages['taskcontent'])
        self.user='deployuser'
        self.group='deploygroup'
        self.node=self.taskDict['node']
        self.db=kwages['db']
        self.taskid=kwages['taskid']
       
    def install(self):
        s=saltApi.saltApi(**{'tgt':self.node,
                             'fun':'installsoftware.installjdk',
                             'timeout ':60,
                             'kwarg':{
                                      'remotepath':self.taskDict['remotepath'],
                                      'localpath':self.taskDict['localpath'],
                                      'localfiles':self.taskDict['localfiles'],
                                      'user':self.user,
                                      'group':self.group,                                      
                                      },
                             'expr_form':'list'})
        #stdLogger.debug(yaml.dump(s.run(),default_flow_style=False))
        #stdLogger.debug(s.run())
        dict=s.run()
        if dict =={}:
            sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)"%('无信息返回.',self.taskid)
            self.db.putData(sql=sql)
            self.db.commit()
            stdLogger.debug("".join([str(self.taskid),'no return.']))
        for i in dict:
            for j in dict[i]: 
                if j=='msg' and dict[i]['msg']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("".join([str(i),':',dict[i]['msg']]),self.taskid)
                    #stdLogger.debug(sql)
                    self.db.putData(sql=sql) 
                    self.db.commit()
                elif j=='std' and dict[i]['std']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)" %("".join([str(i),':',pymysql.escape_string(dict[i]['std'])]),self.taskid)
                    #stdLogger.debug(sql)
                    self.db.putData(sql=sql) 
                    self.db.commit()
                
                stdLogger.debug(dict[i][j])
             
class nginx(object):
    '''
    {'task':'installsoftware','name':'jdk','remotepath':'/home/deployuser/adcc/software/jdk1','localpath':'/home/deployuser/aom/software/jdk_7u72_linux_64.tar.gz','node':['test207']}
    '''
    
    def __init__(self,**kwages):
        self.taskDict=eval(kwages['taskcontent'])
        self.user='deployuser'
        self.group='deploygroup'
        self.node=self.taskDict['node']
        self.db=kwages['db']
        self.taskid=kwages['taskid']
        
        pass
        
    def install(self):
        s=saltApi.saltApi(**{'tgt':self.node,
                             'fun':'installsoftware.installnginx',
                             'timeout ':60,
                             'kwarg':{
                                      'remotepath':self.taskDict['remotepath'],
                                      'localpath':self.taskDict['localpath'],
                                      'localfiles':self.taskDict['localfiles'],
                                      'user':self.user,
                                      'group':self.group,              
                                      },
                             'expr_form':'list'})
        #stdLogger.debug(yaml.dump(s.run(),default_flow_style=False))
        #stdLogger.debug(s.run())
        dict=s.run()
        if dict =={}:
            sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)"%('无信息返回.',self.taskid)
            self.db.putData(sql=sql)
            self.db.commit()
            stdLogger.debug("".join([str(self.taskid),'no return.']))
        for i in dict:
            for j in dict[i]: 
                if j=='msg' and dict[i]['msg']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("".join([str(i),':',dict[i]['msg']]),self.taskid)
                    #stdLogger.debug(sql)
                    self.db.putData(sql=sql) 
                    self.db.commit()
                elif j=='std' and dict[i]['std']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)" %("".join([str(i),':',pymysql.escape_string(dict[i]['std'])]),self.taskid)
                    #stdLogger.debug(sql)
                    self.db.putData(sql=sql) 
                    self.db.commit()  
            if dict[i]['status']:
                self._addNginxServer(i)
            else:
                pass                     
                #stdLogger.debug(dict[i][j])
                
    def _addNginxServer(self,i):                
        #sql='select appserver_type_id from aom_appserver_type where softtypeid=%s'%(self.taskDict['softtypeid'])     
        sql="insert into aom_nginx (node_id,basedir)  values ('%s','%s')"%(str(i),self.taskDict['remotepath'])  
        #stdLogger.debug(sql)
        self.db.putData(sql=sql) 
        self.db.commit()       
        
class tomcat(object):
    
    def __init__(self,**kwages):
        self.taskDict=eval(kwages['taskcontent'])
        self.user='deployuser'
        self.group='deploygroup'
        self.node=self.taskDict['node']
        self.db=kwages['db']
        self.taskid=kwages['taskid']
        self.serverxml=self._getServerXml()
        self.catalina=self._getCatalina()
        
    def _getServerXml(self):
        with open('/home/deployuser/aom/templates/tomcat/server.xml','r') as myfile:
            template = Template(myfile.read()) 
        arg={'httpport':self.taskDict['httpport'],
             'shutdownport':self.taskDict['shutdownport'],
             'ajpport':self.taskDict['ajpport'],
             'appbase':self.taskDict['appbase'],
             'app':[],
             }    
        return(template.render(arg))
    def _getCatalina(self):
        with open('/home/deployuser/aom/templates/tomcat/catalina.sh','r') as myfile:
            template = Template(myfile.read()) 
        arg={'javahome':self.taskDict['javahome'],
             'javaopt':self.taskDict['javaopt']
             }    
        return(template.render(arg))  
        
    def install(self):
        s=saltApi.saltApi(**{'tgt':self.node,
                             'fun':'installsoftware.installtomcat',
                             'timeout ':60,
                             'kwarg':{
                                      'remotepath':self.taskDict['remotepath'],
                                      'localpath':self.taskDict['localpath'],
                                      'localfiles':self.taskDict['localfiles'],
                                      'user':self.user,
                                      'group':self.group,   
                                      'serverxml':self.serverxml,
                                      'catalina':self.catalina,                                       
                                      },
                             'expr_form':'list'})
        dict=s.run()    
        if dict =={}:
            sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)"%('无信息返回.',self.taskid)
            self.db.putData(sql=sql)
            self.db.commit()
            stdLogger.debug("".join([str(self.taskid),'no return.'])) 
        for i in dict:
            for j in dict[i]: 
                if j=='msg' and dict[i]['msg']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("".join([str(i),':',dict[i]['msg']]),self.taskid)
                    self.db.putData(sql=sql) 
                    self.db.commit()
                elif j=='std' and dict[i]['std']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)" %("".join([str(i),':',pymysql.escape_string(dict[i]['std'])]),self.taskid)
                    self.db.putData(sql=sql) 
                    self.db.commit()
            stdLogger.debug(dict[i])     
            if dict[i]['status']:
                self._addAppServer(i)
            else:
                pass                
                                   
    def _addAppServer(self,i):                
        sql='select appserver_type_id from aom_appserver_type where softtypeid=%s'%(self.taskDict['softtypeid'])     
        sql="insert into aom_appserver (appserver_type_id,nodeid)  values (%s,'%s')"%(self.db.getData(sql=sql)[0]['appserver_type_id'],str(i))  
        self.db.putData(sql=sql) 
        sql="insert into aom_appserver_tomcat(appserverid,http_port,shutdown_port,ajp_port,basedir,docbase,appbase,javahome,javaopts) values(%s,%s,%s,%s,'%s','%s','%s','%s','%s')"%(self.db.getLastID(),self.taskDict['httpport'],self.taskDict['shutdownport'],self.taskDict['ajpport'],self.taskDict['remotepath'],self.taskDict['docbase'],self.taskDict['appbase'],self.taskDict['javahome'],pymysql.escape_string(self.taskDict['javaopt']))
        #stdLogger.debug(sql)
        self.db.putData(sql=sql)
        self.db.commit()            