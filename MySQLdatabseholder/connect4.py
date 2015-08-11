import mysql.connector

cnx = mysql.connector.connect(user='admin', password='',
                              host='localhost',
                              database='test')
cnx.close()