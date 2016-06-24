# -*- coding: utf-8 -*-
"""
Created on :
2016-06-16 22:28:13.613000

@author: Yasin_Yousif
"""

import sys
import MySQLdb
conn = MySQLdb.connect(host='127.0.0.1', user = 'root' ,passwd = 'roben',
                       db= 'lgls')

cursor = conn.cursor()

try :
    cursor.execute("""
                   create table prodictivty (hours char(20),hardness tinyint(4))
                    """)

    for x in range(24):
        cursor.execute("""
                       insert into prodictivty values('%02d:00:00',0)
                       """%x)
except MySQLdb.Error:
    print("Error in Creating Products table")
    sys.exit(1)

conn.commit()
cursor.close()
conn.close()

