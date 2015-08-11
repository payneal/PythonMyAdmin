#!/usr/bin/env python3

#http://www.thegeekstuff.com/2008/08/get-quick-info-on-mysql-db-table-column-and-index-using-mysqlshow/

# for operating system calls
import subprocess
#for mysql db
import MySQLdb
#used to return json data
import json

import itertools

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

############################################
# connects to mysql database
#once establed a user in system we can use this
############################################
class curseMySqlDB:
    def __init__(self, dbname, username , password, host, connection = None):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.connection= connection

    #connects to the database
    def connectToDB(self):
        try:
            con = MySQLdb.connect(user= self.username, passwd= self.password, host= self.host, db= self.dbname)
            self.connection = con
            return {'success': 'db was connected'}
        except MySQLdb.Error as err:
            conn.rollback()
            return {'fail': err}

    #return database results in a dictionary
    def queryMysql(self, query):
        if self.connection:
            c= self.connection.cursor()
            try:
                c.execute(query)
                results = self.dictfetchall(cursor)

                #json the results
                #json_results = json.dumps(results)
                return {'success': json_results}
            except:
                return {'error':"unable to fetch data"}
        else:
            return {'error':'must be connect to db to query'}

    #"""Returns all rows from a cursor as a list of dicts"""
    def dictfetchall(self, cursor):
        desc = cursor.description
        return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]

    #used to create db, delete, update, or insert
    def insertDeleteUpdateMysql(self, info):
        if self.connection:
            c= self.connection.cursor()
            try:
                c.execute(info)
                self.connection.commit()
                return {'true':'insert, delete, or update worked'}
            except:
                self.connection.rollback()
                return {'false':"unable insert, delete, update"}
        else:
            return {'error':'must be connect to db to query'}

    #dont know if this is really needed I think Insert or delete would work
    def createOrDeleteTableMysql(self, table):
        if self.connection:
            c= self.connection.cursor()
            try:

                print "thi sis the table var: {}".format(table)
                #might have to check if table exist

                #then drop if table does exist
                c.execute(table)

                return {'true':'created new table or deleted table'}
            except MySQLdb.Error as err:
                self.connection.rollback()
                return {'false':err}
        else:
            return {'error':'must be connect to db to query'}

    def MySQLshowTables(self):
        if self.connection:
            c= self.connection.cursor()
            try:
                c.execute("Use {}".format(self.dbname))
                c.execute("SHOW TABLES")
                results = self.dictfetchall(c)
                #json the results
                json_results = json.dumps(results)
                return {'success': results}
                #return (results, json_results)
            except MySQLdb.Error as err:
                self.connection.rollback()
                return {'false':err}
        else:
            return {'error':'must be connect to db to query'}

    #closes the database
    def closeDB(self):
        if self.connection == None:
            #print "you are not connecte dto databse"
            return{'fail':'you are not connected to any db to close'}
        else:
            self.connection.close()
            #print "the connection has been closed"
            return{'success':'db was closed'}

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

#function to call when what to query the database
def queryMysql(json_login, q_string):
    con = None
    loginInfo =  json.loads(json_login)

    database= loginInfo['database']
    user = loginInfo['user']
    host = '127.0.0.1'
    password = ''
    query = loginInfo['user']
    if loginInfo['password']:
        password = loginInfo['password']

    con = users(database, user, pasword, host)
    result = con.connectToDB()
    result =  json.loads(result)
    if result['success']:
        #start the query
        feedback = con.insertDeleteUpdateMysql(q_string)
        feedback =  json.loads(result)
        #close the
        check = con.closeDB()
        check =  json.loads(check)
        return feedback
    else:
        return result

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#function to call when you want to change mysql database
def changeMysql(json_login, c_srting):
    con = None
    loginInfo =  json.loads(json_login)

    database= loginInfo['database']
    user = loginInfo['user']
    host = '127.0.0.1'
    password = ''
    query = loginInfo['user']
    if loginInfo['password']:
        password = loginInfo['password']

    con = users(database, user, pasword, host)
    result = con.connectToDB()
    result =  json.loads(result)
    if result['success']:
        #start the query
        feedback = con.Mysql(q_string)
        feedback =  json.loads(result)
        #close the
        check = con.closeDB()
        check =  json.loads(check)
        return feedback
    else:
        return result

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#function to call when want to getall dbs for a user
def getAllUsersTablesMysql(json_login):
    #something like show tables
    return True

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all rows from table
def getAllRowsFromTable(json_login, query_statment = None, tablename = None):
#"Select * FROM `tablename`
    return True
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- drop/add table from database
def dropOrAddTableMySql(json_loin, delete_statement = None, tableToDelet= None):
    return True
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- drop/add row to table
def dropOrAddRowMysql (json_loin, delete_statement = None, RowToDelete = None, tableOfRow = None):
    return True


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all databases that belong to a user (less important, since right now we're logging in to a single database instead of an account)
def mysqlGetAllDBsofUser(user):
    return True

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#-for testing program
def getmysqlDBLoginInfo():
    host = raw_input("what is the Hostname? ")
    host = host.strip()
    dbname = raw_input("what is the DatabaseName? ")
    dbname = dbname.strip()
    username = raw_input("what is the username? ")
    username = username.strip()
    password= raw_input("what is the password? ")
    password= password.strip()
    return (host, dbname, username, password)

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all databases that belong to a user (less important, since right now we're logging in to a single database instead of an account)
def mysqlGetAllDBsofUser(user):
    return True

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- create A db
def mysqlCreateADb(host, user, passw):
    return True

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- create A db
#http://stackoverflow.com/questions/8932261/create-mysqldb-database-using-python-script
def grantPrivsToMySqlDB(host, user, passw):
    return True


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
############################################
# steps on how to set up prorgam and test as well
#
#
#
#
############################################
if __name__ == "__main__":
    #1. we need to Create a user in mysql

        #download mysql: https://dev.mysql.com/downloads/mysql/
        #install it
        #go to setting and make sure local server is up and running
        #go to command line
            #for mac
                # terminal call => "/usr/local/mysql/bin/mysql"
            #for windows
                #terminal call => 'mysql'
            #for linux
                #terminal call => 'mysql'

        #once mysql is up and running in the terminal ex 'mysql>'
        #we want to acces admin so exit mysql with exit ex. 'mysql>exit'

        #now we want to log in as a user that can make changes to localhost
        #to do this go again to the comman line and enter:
        #mac ex.
        # /usr/local/mysql/bin/mysql -u root -p -h localhost -P 3306
        # to quickly explain this string:
            #we are login in at root which is the defealt administrated with all grant provilage

            # local host is where we are running the program if this doesnt work check out '127.0.0.1'

            #connection to local host server run on port(3306)

        # you will then be asked for the password
        #ex. 'Enter password:'
            #the defealt password is ''
            #http://forums.mysql.com/read.php?34,140320,140324

        #now that we are loged in a root user we can create a new user in the db

        #https://dev.mysql.com/doc/refman/5.1/en/adding-users.html
        #ex.
        # creates user with password
        # mysql> CREATE USER 'fake'@'localhost' IDENTIFIED BY 'admin_pass';
        # create a user without a password (not recommended)
        # mysql> CREATE USER 'dummy'@'localhost';

    #2.) create a Database
        #ex. => mysql> CREATE DATABASE menagerie;

        #verify databse was creaded with:
        #ex. => mysql> show databases;

    #3.) give the created user acces to this db
        #ex. =>  mysql> GRANT ALL PRIVILEGES ON menagerie.* To 'fake'@'localhost'


    #4.) Now that we have a user = 'fake' , password= 'admin_pass' host = 'localhost' , and databse = 'menagerie'
        #we can finiially use the created command line

    print "Now that you have completed steps 1-4 and have a username, host, and database we can now move on!"

    #host, dbname, username, password = getmysqlDBLoginInfo()

    answer = None

    answer= raw_input('have you created the test steps exactly as walkthrough states meaning \nuser = fake , password= admin_pass host = localhost , and databse = menagerie:\n y/n => ')

    if answer != 'y':
        print ('test is set up for this information please use forresults')
        answer= raw_input('would you like to enter your already established connection\ny/n: ')
        if answer == 'y':
            host, dbname, username, password = getmysqlDBLoginInfo()
        else:
            print("set up test and come back, good bye")
            exit()


    host = 'localhost'
    dbname = 'menagerie'
    username = 'fake'
    password = 'admin_pass'

    #create a json string
    data = {'database': dbname, 'user': username, 'host': 'localhost', 'password': password}
    json_logInfo = json.dumps(data)

    if isinstance(data, str) == False:
        print "data is python dictionary"
        print data['user']

    print "\n"

    if isinstance(json_logInfo, str):
        print "json_logInfo is a string"
        print json_logInfo

    print("now that we have a python dictionary lets start testing")
    #create a mysql db
    test = curseMySqlDB(data['database'],data['user'], data['password'], data['host'])

    print('1.) can we connect to and close db')
    result = test.connectToDB()
    if result['success']:
        print result['success']
        result = test.closeDB()
        if result['success']:
            print result['success']
            print "test#1 - passed"
        else:
            print result['fail']
            print "test#1 - failed"
            exit()
    else:
        print result['fail']
        print "test#1 - failed"
        exit()

    print ('2.)Can we ceate a table in the db')
    connect to db
    test.connectToDB()
    print ("we will add the following table: ")
    table = '''CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20) {}'''.format("DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1");
    print table
    result = test.createOrDeleteTableMysql(table)
    test.closeDB()
    if result['success'];
        print result['success']
        print "test#2 - passed"
    else:
        print results['fail']
        exit()

    print ('3. show tables to see if last table was created')
    test.connectToDB()
    result = test.MySQLshowTables()
    test.closeDB()
    if result['success']:
        intable = result['success'][0]
        if intable['Tables_in_menagerie'] == 'pet':
            print "tables in db= {}".format(intable['Tables_in_menagerie'])
            print "test#2 - passed"
    else:
        print results['fail']
        exit()
