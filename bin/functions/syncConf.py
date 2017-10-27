# -*- coding: utf-8 -*-
from jinja2 import Template 
from functions import saltApi
import logging
import yaml
import pymysql
import os

stdLogger = logging.getLogger('root')

class syncNginxConf(object):

    def __init__(self,**kwages):
        self.taskDict=eval(kwages['taskcontent'])
        self.user='deployuser'
        self.group='deploygroup'
        #self.node=self.taskDict['node']
        self.db=kwages['db']
        self.taskid=kwages['taskid']
        
    def run(self):
        return_json={}
        return_json['listen']='80'
        sql="select domain from aom_environment where envid=%s"%(self.taskDict['envid'])   
        return_json['domain']= self.db.getData(sql=sql)[0]['domain']
        sql="SELECT a.appid,a.appname,b.`appRoot` FROM aom_app a LEFT JOIN aom_app_st b ON a.`appid`=b.`appid`  WHERE a.`appid` IN (SELECT appid FROM aom_app2jvm WHERE envid=%s GROUP BY appid)"%(self.taskDict['envid'])
        appdict=self.db.getData(sql=sql)
        stdLogger.debug(appdict)
        return_json['app']={}
        for i in appdict:
            return_json['app'][i['appname']]={}
            return_json['app'][i['appname']]['appRoot']=i['appRoot']
            return_json['app'][i['appname']]['upstream']="_".join([self.db.getCustom(customid=self.taskDict['customid']),
                                                          self.db.getProject(projectid=self.taskDict['projectid']),
                                                          self.db.getEnvironment(envid=self.taskDict['envid'])])     
            return_json['app'][i['appname']]['server']=[]     
            sql="SELECT c.`ip`,d.`http_port` FROM aom_app2jvm a LEFT JOIN aom_appserver b ON a.`appserverid`=b.`appserverid` LEFT JOIN aom_appserver_tomcat d ON b.`appserverid`=d.`appserverid`  LEFT JOIN aom_node c ON b.`nodeid`=c.`nodeid` WHERE `appid`=6"                               
            for j in self.db.getData(sql=sql):
                return_json['app'][i['appname']]['server'].append(":".join([j['ip'],str(j['http_port'])]))
        stdLogger.debug(return_json)
        stdLogger.debug(os.getcwd())
        with open('../templates/nginx/nginx.server','r') as myfile:
            template = Template(myfile.read())   
        stdLogger.debug(template.render(return_json))
       #   stdLogger.debug()
       #    pass