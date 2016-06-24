# -*- coding: utf-8 -*-
"""
Created on :
2016-06-17 03:40:56.708000

@author: Yasin_Yousif
"""

import sys
import MySQLdb
conn = MySQLdb.connect(host='127.0.0.1', user = 'root' ,passwd = 'roben',
                       db= 'lgls')

cursor = conn.cursor()

try :
    cursor.execute("""
                   create table Timesheet (daydate char(45),
                    `08:00-am` char(100),
                    `09:00-am` char(100),
                    `10:00-am` char(100),
                    `11:00-am` char(100),
                    `00:00-pm` char(100),
                    `01:00-pm` char(100),
                    `02:00-pm` char(100),
                    `03:00-pm` char(100),
                    `04:00-pm` char(100),
                    `05:00-pm` char(100),
                    `06:00-pm` char(100),
                    `07:00-pm` char(100),
                    `08:00-pm` char(100),
                    `09:00-pm` char(100),
                    `10:00-pm` char(100),
                    `11:00-pm` char(100),
                    `00:00-am` char(100),
                    `01:00-am` char(100),
                    `02:00-am` char(100),
                    `03:00-am` char(100),
                    `04:00-am` char(100),
                    `05:00-am` char(100),
                    `06:00-am` char(100),
                    `07:00-am` char(100)
                   )
                    """)

except MySQLdb.Error:
    print("Error in Creating Products table")
    sys.exit(1)

cursor.close()
conn.close()

