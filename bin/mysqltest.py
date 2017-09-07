# -*- coding: utf-8 -*-
import pymysql
def connect_wxremit_db():
    return pymysql.connect(host='test205',
                           port=3306,
                           user='root',
                           password='jljtmysql',
                           database='aom',charset='utf8')

db=connect_wxremit_db()             
cur=db.cursor()              
cur.execute('select * from aom_custom')
for i in cur.fetchall():
    temp=[]
    for j in i:
        print j
        temp.append(str(j))
    print "".join(temp)