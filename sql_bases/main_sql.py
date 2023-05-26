import pymysql.cursors
con = pymysql.connect(
            host='localhost',
            port=3306,
            user='droping',
            password='locomotive39',
            database='frolovscake')

cur = con.cursor(pymysql.cursors.DictCursor)

import datetime 
now = datetime.datetime.now()
str_now = now.strftime('%Y-%m-%d %H:%M:%S')
print(str_now)

con.commit()



    
    

