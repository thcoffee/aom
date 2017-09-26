# -*- coding: utf-8 -*-
from functions import saltApi
import logging
import yaml
import pymysql
stdLogger = logging.getLogger('root')
class jdk(object):
    '''
    {'task':'installsoftware','name':'jdk','remotepath':'/home/deployuser/adcc/software/jdk1','localpath':'/home/deployuser/aom/software/jdk_7u72_linux_64.tar.gz','node':['test207']}
    '''
    
    def __init__(self,**kwages):
        self.taskDict=eval(kwages['taskcontent'])
        self.user='deployuser'
        self.group='deploygroup'
        self.node=self.taskDict['node']
        self.db=kwages['db']
        self.cur=kwages['cur']
        self.taskid=kwages['taskid']
        
        pass
        
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
            stdLogger.debug("".join([str(self.taskid),'no return.']))
        for i in dict:
            for j in dict[i]: 
                if j=='msg' and dict[i]['msg']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("".join([str(i),':',dict[i]['msg']]),self.taskid)
                    #stdLogger.debug(sql)
                    self.cur.execute(sql) 
                    self.db.commit()
                elif j=='std' and dict[i]['std']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)" %("".join([str(i),':',pymysql.escape_string(dict[i]['std'])]),self.taskid)
                    #stdLogger.debug(sql)
                    self.cur.execute(sql) 
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
        self.cur=kwages['cur']
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
            stdLogger.debug("".join([str(self.taskid),'no return.']))
        for i in dict:
            for j in dict[i]: 
                if j=='msg' and dict[i]['msg']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),1,'%s',%s)" %("".join([str(i),':',dict[i]['msg']]),self.taskid)
                    #stdLogger.debug(sql)
                    self.cur.execute(sql) 
                    self.db.commit()
                elif j=='std' and dict[i]['std']!='':
                    sql="insert into aom_msg (msgdate,msgtype,msgcontent,taskid)values (now(),2,'%s',%s)" %("".join([str(i),':',pymysql.escape_string(dict[i]['std'])]),self.taskid)
                    #stdLogger.debug(sql)
                    self.cur.execute(sql) 
                    self.db.commit()
                
                stdLogger.debug(dict[i][j])