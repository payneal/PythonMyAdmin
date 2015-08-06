#test script to connect to postgres db
#need to execute as the user that has permission for the db

import psycopg2
import sys


con = None

try:
     
    con = psycopg2.connect(database='mydb', user='postgres') 
    cur = con.cursor() #cursor can be used to execute SQL
    cur.execute('SELECT version()')          
    q = cur.fetchone()
    print q    
    

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
