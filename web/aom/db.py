import pymysql
from django.conf import settings
class opMysqlObj(object):
    def __init__(self,**kwages):
        self.databases=kwages['dbname']
        self._getdb()
        pass
        
    def _getdb(self):
        temp=settings.DATABASES[self.databases]
        temp2={}
        temp2['user'],temp2['password'],temp2['host'],temp2['database'],temp2['port']=temp['USER'],temp['PASSWORD'],temp['HOST'],temp['NAME'],int(temp['PORT'])
        temp2['charset']='utf8'
        self.db=pymysql.connect(**temp2)
    
    def getLaseID(self):
        return(self.getData(**{'sql':'SELECT LAST_INSERT_ID()'})[0][0])
    
    def getData(self,**kwages):     
        cur=self.db.cursor()
        cur.execute(kwages['sql'])
        return(cur.fetchall())
        
    def commit(self):
        self.db.commit()    
        
    def putData(self,**kwages):
        cur=self.db.cursor() 
        cur.execute(kwages['sql'])
        
    def close(self):
        self.db.close()
    
    def getNodes(self):
        temp=[]
        for i in self.getData(**{'sql':'select nodeid from aom_node'}):
            temp.append(i[0])
        return(temp)
        
    def getDefaultPath(self,**kwages):
        return(self.getData(**{'sql':'select defaultpath from aom_softtype where softtypeid=%s'%(kwages['softtypeid'])})[0][0])
    
    def getCustoms(self,**kwages):
        return(self.getData(**{'sql':'select customid,customname from aom_custom'}))
        
    def getCustom(self,**kwages):
        return(self.getData(**{'sql':'select customname from aom_custom where customid=%s'%(kwages['customid'])})[0][0])
        
    def getProject(self,**kwages):
        return(self.getData(**{'sql':'select projectname from aom_project where projectid=%s'%(kwages['projectid'])})[0][0])
        
    def getEnvironment(self,**kwages):
        return(self.getData(**{'sql':'select envname from aom_environment where envid=%s'%(kwages['envid'])})[0][0])        