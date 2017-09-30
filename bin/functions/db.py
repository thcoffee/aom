import pymysql

class opMysqlObj(object):
    def __init__(self,**kwages):
        self.databases=kwages
        self.db=pymysql.connect(**self.databases)
        pass
        
    def getLastID(self):
        return(self.getData(**{'sql':'SELECT LAST_INSERT_ID()'})[0]['LAST_INSERT_ID()'])
    
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
            temp.append(i['nodeid'])
        return(temp)
        
    def getDefaultPath(self,**kwages):
        return(self.getData(**{'sql':'select defaultpath from aom_softtype where softtypeid=%s'%(kwages['softtypeid'])})[0][0])