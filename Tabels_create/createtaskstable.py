# -*- coding: utf-8 -*-
"""
Created on :
2016-06-16 15:44:53.289000

@author: Yasin_Yousif
"""

import sys
import MySQLdb
conn = MySQLdb.connect(host='127.0.0.1', user = 'root' ,passwd = 'roben',
                       db= 'lgls')

cursor = conn.cursor()

try :
    cursor.execute("""
                   create table Tasks (Task_class char(20),
                                       Task_title char(50),
                                       Task_shortcut char(15),
                                    Task_isUrg tinyint(1),
                                    Task_isImp tinyint(1),
                                    Task_isInsatnce tinyint(1),
                                    Task_period smallint,
                                    Task_start char(15),
                                    Task_end char(15),
                                    Task_hardness tinyint,
                                    Task_notes char(110));
                    """)

except MySQLdb.Error:
    print("Error in Creating Products table")
    sys.exit(1)

cursor.close()
conn.close()

