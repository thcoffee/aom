from django.db import models
from . import db

# Create your models here.

#应用配置
class AomApp(models.Model):
    appid = models.AutoField(primary_key=True)
    appname = models.CharField(max_length=50, blank=True, null=True)
    appcname = models.CharField(max_length=50, blank=True, null=True)
    projectid = models.ForeignKey('AomProject', models.DO_NOTHING, db_column='projectid', blank=True, null=True)
    percentdep = models.IntegerField(db_column='percentDep', blank=True, null=True)  # Field name made lowercase.
    codectrl = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_app'
    def __str__(self):
        return(str(self.projectid)+'/'+self.appname)

#应用对jvm
class AomApp2Jvm(models.Model):
    app2jvmid = models.AutoField(primary_key=True)
    appid = models.ForeignKey(AomApp, models.DO_NOTHING, db_column='appid', blank=True, null=True)
    appserverid = models.ForeignKey('AomAppserver', models.DO_NOTHING, db_column='appserverid', blank=True, null=True)
    envid = models.ForeignKey('AomEnvironment', models.DO_NOTHING, db_column='envid', blank=True, null=True)
    status = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_app2jvm'
    
    def __str__(self):
        return("/".join([str(self.appid),str(self.appserverid),str(self.envid.envname)]))


#应用对应starteam配置        
class AomAppSt(models.Model):
    appid = models.ForeignKey(AomApp, models.DO_NOTHING, db_column='appid', primary_key=True)
    stproject = models.CharField(db_column='stProject', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stview = models.CharField(db_column='stView', max_length=50, blank=True, null=True)  # Field name made lowercase.
    stfolder = models.CharField(db_column='stFolder', max_length=50, blank=True, null=True)  # Field name made lowercase.
    mvnprofile = models.CharField(db_column='mvnProfile', max_length=50, blank=True, null=True)  # Field name made lowercase.
    appwar = models.CharField(db_column='appWar', max_length=50, blank=True, null=True)  # Field name made lowercase.
    approot = models.CharField(db_column='appRoot', max_length=50, blank=True, null=True)  # Field name made lowercase.
    checkpage = models.CharField(db_column='checkPage', max_length=50, blank=True, null=True)  # Field name made lowercase.
    checkkey = models.CharField(db_column='checkKey', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aom_app_st'

#应用服务器配置
class AomAppserver(models.Model):
    appserverid = models.AutoField(primary_key=True)
    appserver_type = models.ForeignKey('AomAppserverType', models.DO_NOTHING, blank=True, null=True)
    nodeid = models.ForeignKey('AomNode', models.DO_NOTHING, db_column='nodeid', blank=True, null=True)
    
    def path(self):
        sql="select appservername from aom_appserver_type where appserver_type_id=%s"%(self.appserver_type.appserver_type_id)
        print(sql)
        dbcon=db.opMysqlObj(**{'dbname':'default'})
        apptype=dbcon.getData(**{'sql':sql})
        if apptype[0][0]=='tomcat':
            sql="select baseDir from aom_appserver_tomcat where appserverid=%s"%(self.appserverid)
            temp=dbcon.getData(**{'sql':sql})[0][0]
        else:
            temp='Null'
        dbcon.close()
        return(temp)
    
    class Meta:
        managed = False
        db_table = 'aom_appserver'
        #permissions = (
        #    ('views_aomappserver_list', '查看学员信息表'),
        #    ('views_aomappserver_info', '查看学员详细信息'),
        #)
    def __str__(self):
        return("/".join([str(self.appserver_type),str(self.nodeid)]))


#应用服务器tomcat配置       
class AomAppserverTomcat(models.Model):
    appserverid = models.ForeignKey(AomAppserver, models.DO_NOTHING, db_column='appserverid', primary_key=True)
    http_port = models.IntegerField(blank=True, null=True)
    shutdown_port = models.IntegerField(blank=True, null=True)
    ajp_port = models.IntegerField(blank=True, null=True)
    basedir = models.CharField(db_column='baseDir', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    docbase = models.CharField(db_column='docBase', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    appbase = models.CharField(db_column='appBase', max_length=1024, blank=True, null=True)  # Field name made lowercase.
    javahome = models.CharField(max_length=1024, blank=True, null=True)
    javaopts = models.TextField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'aom_appserver_tomcat'
        #permissions = (
        #    ('views_aomappserver_list', '查看学员信息表'),
        #    ('views_aomappserver_info', '查看学员详细信息'),
        #)

#应用服务器类型        
class AomAppserverType(models.Model):
    appserver_type_id = models.AutoField(primary_key=True)
    appservername = models.CharField(max_length=50, blank=True, null=True)
    appserverversion = models.CharField(max_length=50, blank=True, null=True)
    softtypeid = models.ForeignKey('AomSofttype', models.DO_NOTHING, db_column='softtypeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_appserver_type'
    
    def __str__(self):
        return(str(self.softtypeid))

#软件类型
class AomSofttype(models.Model):
    softtypeid = models.AutoField(primary_key=True)
    softname = models.CharField(max_length=50, blank=True, null=True)
    softversion = models.CharField(max_length=50, blank=True, null=True)
    softpath = models.CharField(max_length=1000, blank=True, null=True)
    softfiles = models.CharField(max_length=1000, blank=True, null=True)
    defaultpath = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_softtype'   

    def __str__(self):
        return("/".join([self.softname,self.softversion]))        

#客户配置        
class AomCustom(models.Model):
    customid = models.AutoField(primary_key=True)
    customname = models.CharField(max_length=50, blank=True, null=True)
    customcname = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_custom'
        verbose_name_plural='客户设置'  
        verbose_name='客户设置'
        
    def __str__(self):
        return(self.customname)
class test(models.Model):
    tid = models.AutoField(primary_key=True)

#nginx配置    
class AomNginx(models.Model):
    nginx_id = models.AutoField(primary_key=True)
    node = models.ForeignKey('AomNode', models.DO_NOTHING, blank=True, null=True)
    basedir = models.CharField(db_column='baseDir', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'aom_nginx'
    
    def __str__(self):
        return("".join([str(self.node),':nginx']))

#环境配置        
class AomEnvironment(models.Model):
    envid = models.AutoField(primary_key=True)
    envname = models.CharField(max_length=50, blank=True, null=True)
    envcname = models.CharField(max_length=50, blank=True, null=True)
    projectid = models.ForeignKey('AomProject', models.DO_NOTHING, db_column='projectid', blank=True, null=True)
    domain = models.CharField(max_length=50, blank=True, null=True)
    nginx=models.ManyToManyField(AomNginx,verbose_name='nginxServer',blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'aom_environment'
    
    def __str__(self):
        return(str(self.projectid)+'/'+self.envname)




#节点配置        
class AomNode(models.Model):
    nodeid = models.CharField(primary_key=True, max_length=50)
    osid = models.ForeignKey('AomOs', models.DO_NOTHING, db_column='osid', blank=True, null=True)
    customid = models.ForeignKey(AomCustom, models.DO_NOTHING, db_column='customid', blank=True, null=True)
    ip = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_node'

    def __str__(self):
        return(self.nodeid+'/'+self.ip)

#操作系统配置        
class AomOs(models.Model):
    osid = models.IntegerField(primary_key=True)
    osname = models.CharField(max_length=50, blank=True, null=True)
    osversion = models.CharField(max_length=50, blank=True, null=True)
    osbit = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_os'
    
    def __str__(self):
        return(self.osname+self.osversion+self.osbit)

#项目配置        
class AomProject(models.Model):
    projectid = models.AutoField(primary_key=True)
    projectname = models.CharField(max_length=50, blank=True, null=True)
    projectcname = models.CharField(max_length=50, blank=True, null=True)
    customid = models.ForeignKey(AomCustom, models.DO_NOTHING, db_column='customid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'aom_project'
    
    def __str__(self):
        return(str(self.customid)+'/'+str(self.projectname))
