# Note (Example is valid for Python v2 and v3) 
from __future__ import print_function 

import sys 

#sys.path.insert(0, 'python{0}/'.format(sys.version_info[0])) 

import mysql.connector 
from mysql.connector.constants import ClientFlag 

config = { 
    'user': 'admin', 
    'password': '', 
    'host': 'localhost', 
    'client_flags': [ClientFlag.SSL], 
    'ssl_ca': '/opt/mysql/ssl/ca.pem', 
    'ssl_cert': '/opt/mysql/ssl/client-cert.pem', 
    'ssl_key': '/opt/mysql/ssl/client-key.pem', 
} 

cnx = mysql.connector.connect(**config) 
cur = cnx.cursor(buffered=True) 
cur.execute("SHOW STATUS LIKE 'Ssl_cipher'") 
print(cur.fetchone()) 
cur.close() 
cnx.close() 