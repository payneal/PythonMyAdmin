#!/usr/bin/env python3
################################################################################
#                           Instructions                                       #
#       Include this file to do the following with a local mysql Databse:      #
#                                                                              #
#                                                                              #
################################################################################
#                      *LOGIN/CHECK MYSQL CREDIENTIALS*
#   function: loginMysql(pythonDic):
#
#   pythonDic => { "database": <string>, "user": <string>, "host": '127.0.0.1', "password": '', "query":<string> }
#
#   returns =>     on succes = {'success': 'db was connected'}
#
#   returns=>       on failure = {'fail': mysql error message}
#
#------------------------------------------------------------------------------
#                       *ADD OR DELETE MYSQLDB TABLE*
#   function: addOrDeleteMydqlTable(pythonDic, table):
#
#   pythonDic => { "database": <string>, "user": <string>, "host": '127.0.0.1', "password": '', "query":<string> }
#
#   table => <string>
#
#   ex. Delete
#   DROP TABLE pet
#
#   ex. Add
#   CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20) DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1
#
#   returns =>      on succes = {'success':'created new table or deleted {table}}
#
#   returns=>       on failure = {'fail':'mysql error message}'}
#
#------------------------------------------------------------------------------
#                      *SHOW ALL TABLES IN A DATABASE*
#   function: showAllTablesInAMysqlDB(pythonDic):
#
#   pythonDic => { "database": <string>, "user": <string>, "host": '127.0.0.1', "password": '', "query":<string> }
#
#   returns =>      on succes ex =  {'success': [{'Tables_in_[nameoftable]': [nameoftable1]}, {'Tables_in_[nameoftable]': [nameoftable2]}]}
#
#   returns =>      on failure = {'false':mysql error message}
#
#
#------------------------------------------------------------------------------
#                      *DELETE/INSERT DATA IN TABLE*
#
#   function: deleteInsertDataToTable(pythonDic, iData):
#
#   pythonDic => { "database": <string>, "user": <string>, "host": '127.0.0.1', "password": '', "query":<string> }
#
#   iData => <string>
#   ex.
#       INSERT INTO pet(name, owner) Values('buddy', 'jack')
#
#   returns =>      on succes =  {'success': 'created new table or deleted {callmade}}
#
#   returns =>      on failure = {'false':mysql error message}
#
#
#------------------------------------------------------------------------------
#                      *RETURN PYTHON DICTIONARY FROM QUERY*
#
#   function: pythonDicFromQuery(pythonDic, query):
#
#   pythonDic => { "database": <string>, "user": <string>, "host": '127.0.0.1', "password": '', "query":<string> }
#
#   query => <string>
#
#   ex.
#       select name, owner from pet
#
#   returns =>      on succes =  [{'owner': 'jack', 'name': 'buddy'}, {'owner': 'jack', 'name': 'buddy'}]
#
#   returns =>      on failure = {'false':mysql error message}
#
################################################################################
#RESOURCES:
#   1.) http://www.thegeekstuff.com/2008/08/get-quick-info-on-mysql-db-table-column-and-index-using-mysqlshow/
#   2.) http://mysql-python.sourceforge.net/MySQLdb.html#using-and-extending
#   3.) https://dev.mysql.com/doc/refman/5.1/en/index.html
#   4.) http://zetcode.com/db/mysqlpython/
#   5.) http://stackoverflow.com/questions/1451782/python-mysql-selects-work-but-not-deletes
#        *used alot of various stackover flow articles
#   6.) http://www.tutorialspoint.com/python/python_database_access.htm
#   7.) http://www.mikusa.com/python-mysql-docs/index.html
#   8.) https://media.readthedocs.org/pdf/mysqldb/latest/mysqldb.pdf
#   9.) http://www.cs.columbia.edu/~hgs/teaching/ap/examples/scripts_python_dbapi.pdf
#



# for operating system calls
import subprocess
#for mysql db
import MySQLdb
#used to return json data
import json
#used to create dictionaty
import itertools
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
############################################
# connects to mysql database and does basically everything
#
# user in system uses this
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
        con= None
        try:
            con = MySQLdb.connect(user= self.username, passwd= self.password, host= self.host, db= self.dbname)
            self.connection = con
            return {'success': 'db was connected'}
        except MySQLdb.Error as err:
            con.rollback()
            return {'fail': err}

    #return database results in a dictionary
    def queryMysql(self, query):
        if self.connection:
            c= self.connection.cursor()
            try:
                #c.execute("Use {}".format(self.dbname))
                c.execute(query)
                results = self.dictfetchall(c)
                return {'success': results}
            except MySQLdb.Error as err:
                return {'fail':err}
        else:
            return {'fail':'must be connect to db to query'}

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
                return {'success':'insert, delete, or update worked: {}'.format(info)}
            except MySQLdb.Error as err:
                self.connection.rollback()
                return {'fail':err }
        else:
            return {'fail':'must be connect to db to query'}

    #dont know if this is really needed I think Insert or delete would work
    def createOrDeleteTableMysql(self, table):
        if self.connection:
            c= self.connection.cursor()
            try:
                #print "this is the table var: {}".format(table)
                #might have to check if table exist
                #then drop if table does exist
                c.execute(table)
                self.connection.commit()

                return {'success':'created new table or deleted {}'.format(table)}
            except MySQLdb.Error as err:
                self.connection.rollback()
                return {'fail':err}
        else:
            return {'fail':'must be connect to db to query'}

    def MySQLshowTables(self):
        if self.connection:
            c= self.connection.cursor()
            try:
                c.execute("Use {}".format(self.dbname))
                c.execute("SHOW TABLES")
                results = self.dictfetchall(c)
                #json the results
                #json_results = json.dumps(results)
                return {'success': results}
                #return (results, json_results)
            except MySQLdb.Error as err:
                self.connection.rollback()
                return {'false':err}
        else:
            return {'false':'must be connect to db to query'}

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
#function to log into mysql
def loginMysql(pythonDic):
    con = None
    database= pythonDic['database']
    user = pythonDic['user']
    host = pythonDic['host']
    password = pythonDic['password']

    con = curseMySqlDB(database, user, password, host)
    result = con.connectToDB()
    con.closeDB
    return result
#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#function to add or delete a table as user
def addOrDeleteMydqlTable(pythonDic, theTable):
    con = None
    database= pythonDic['database']
    user = pythonDic['user']
    host = pythonDic['host']
    password = pythonDic['password']
    table = theTable
    con = curseMySqlDB(database, user, password, host)
    con.connectToDB()
    result = con.createOrDeleteTableMysql(table)
    con.closeDB()
    return result


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#function to call when what to query the database
def showAllTablesInAMysqlDB(pythonDic):
    con = None
    database= pythonDic['database']
    user = pythonDic['user']
    host = pythonDic['host']
    password = pythonDic['password']
    con = curseMySqlDB(database, user, password, host)
    con.connectToDB()
    result = con.MySQLshowTables()
    con.closeDB()
    return result

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#function to call when what to query the database
def deleteInsertDataToTable(pythonDic, iData):
    con = None
    database= pythonDic['database']
    user = pythonDic['user']
    host = pythonDic['host']
    password = pythonDic['password']
    con = curseMySqlDB(database, user, password, host)
    con.connectToDB()
    result = con.insertDeleteUpdateMysql(iData)
    con.closeDB()
    return result

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#function to call when what to query the database
def pythonDicFromQuery(pythonDic, query):
    con = None
    database= pythonDic['database']
    user = pythonDic['user']
    host = pythonDic['host']
    password = pythonDic['password']
    con = curseMySqlDB(database, user, password, host)
    con.connectToDB()
    query = query
    result= con.queryMysql(query)
    con.closeDB()
    return result

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all rows from table
def getAllRowsFromTable(pythonDic, tablename):
    #"Select * FROM `tablename`

    #already have query, so idk if this is needed

    return False

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


###############################################################################
# for the three calls below one woudl need to access admin in
# mysql but the closest I could get with scrit was the following:

# for operating system calls
#import subprocess
#system_output('mysql -u root -p -h localhost -P 3306')

#hit enter for password

#did find way to talk to command like ex:
#def system_output(command):
#	p = subprocess.check_output([command], stderr=subprocess.STDOUT, shell=True)
#	return p

#but coudldnt get pass 'Enter Password:' in python script to work

#if one can, from there the functions below are easy ... see steps in main

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all databases that belong to a user (less important, since right now we're logging in to a single database instead of an account)
def mysqlGetAllDBsofUser(user):
    return False


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- create A db
def mysqlCreateADb(host, user, passw):
    return False

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- create A db
#http://stackoverflow.com/questions/8932261/create-mysqldb-database-using-python-script
def grantPrivsToMySqlDB(host, user, passw):
    return False


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
############################################
# steps on how to set up mysql and settings to trst program as well
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
        #to do this go again go to the command line and enter:
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
    #connect to db
    test.connectToDB()
    print ("we will add the following table: ")
    table = '''CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20) {}'''.format("DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1");
    print table
    result = test.createOrDeleteTableMysql(table)
    test.closeDB()
    if result['success']:
        print result['success']
        print "test#2 - passed"
    else:
        print results['fail']
        exit()

    print ('3.) show tables to see if last table was created')
    test.connectToDB()
    result = test.MySQLshowTables()
    test.closeDB()
    if result['success']:
        intable = result['success'][0]
        if intable['Tables_in_menagerie'] == 'pet':
            print "tables in db= {}".format(intable['Tables_in_menagerie'])
            print "test#3 - passed"
    else:
        print results['fail']
        exit()

    print("4.) Insert data to a table")
    test.connectToDB()
    print("lets insert data to the pet table")
    insert = "INSERT INTO pet(name, owner) Values('buddy', 'jack')"
    print "here is the statement"
    print insert
    result = test.insertDeleteUpdateMysql(insert)
    test.closeDB()
    if result['success']:
        print result['success']
        print "test#4 - passed"
    else:
        print results['fail']
        exit()

    print ("5.) delete data from table")
    test.connectToDB()
    delete = "DELETE FROM pet WHERE name='buddy'"
    print("lets delete row from the pet db")
    print "here is the statement"
    print delete
    result = test.insertDeleteUpdateMysql(delete)
    test.closeDB()
    if result['success']:
        print result['success']
        print "test#5 - passed"
    else:
        print results['fail']
        exit()

    print('6.) return python dic of query')
    test.connectToDB()
    print("to check if query works lets input two rows to pet")
    insert1 = "INSERT INTO pet(name, owner) Values('buddy', 'jack')"
    insert2 = "INSERT INTO pet(name, owner) Values('ron', 'smalls')"
    print("here is insert one: ")
    print insert1
    test.insertDeleteUpdateMysql(insert1)
    print("here is insert 2: ")
    print insert2
    test.insertDeleteUpdateMysql(insert1)
    query = "select name, owner from pet"
    print("this is the query")
    print query
    results = test.queryMysql(query)
    test.closeDB()
    print("now we will return a python dictionary")
    if results['success']:
        print results['success']
        print "test#6 - passed"
    else:
        print results['fail']
        exit()

    print('7.) delete table')
    test.connectToDB()
    print ("we will now delete the table pet with this call: ")
    table = "DROP TABLE pet"
    print "here is the statement"
    print table
    result = test.createOrDeleteTableMysql(table)
    test.closeDB()
    if result['success']:
        print result['success']
        print "test#7 - passed"
    else:
        print results['fail']
        exit()

    print ("8.)\ntest all functions that program will use")
    check = loginMysql(data)
    print "Testing function loginMysql(pythondic)"
    if check['success']:
        print check
        print "function loginMysql(pythondic) - passed"
    else:
        print check['fail']
        print "function loginMysql(pythondic) - failed"
        exit()

    print "\nTesting function addOrDeleteMydqlTable(pythondic, table)"
    table = '''CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20) {}'''.format("DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1");
    check = addOrDeleteMydqlTable(data, table)
    if check['success']:
        print check
        print "function addOrDeleteMydqlTable(pythondic, table) - passed for add"
    else:
        print check['fail']
        print "function addOrDeleteMydqlTable(pythondic, table)) - failed for add"
        exit()

    print "\nTesting function showAllTablesInAMysqlDB(pythonDic):"
    #adding additional table
    table = '''CREATE TABLE state (name VARCHAR(20), id VARCHAR(20) {}'''.format("DEFAULT NULL) ENGINE=MyISAM DEFAULT CHARSET=latin1");
    addOrDeleteMydqlTable(data, table)
    #now calling function
    check = showAllTablesInAMysqlDB(data)
    if check['success']:
        print check
        print "function showAllTablesInAMysqlDB(pythonDic)) - passed"
    else:
        print check['fail']
        print "function showAllTablesInAMysqlDB(pythonDic)) - failed"
        exit()

    print "\nTesting function: deleteInsertDataToTable(pythonDic, iData):"
    insert = "INSERT INTO pet(name, owner) Values('buddy', 'jack')"
    check = deleteInsertDataToTable(data, insert)
    if check['success']:
        print check
        print "function: deleteInsertDataToTable(pythonDic, iData) - passed"
    else:
        print check['fail']
        print "function: deleteInsertDataToTable(pythonDic, iData) - failed"
        exit()

    print "\nTesting function: pythonDicFromQuery(pythonDic, query):"
    query = "select name, owner from pet"
    #adding a couple more queries
    insert = "INSERT INTO pet(name, owner) Values('duke', 'sandy')"
    deleteInsertDataToTable(data, insert)
    insert = "INSERT INTO pet(name, owner) Values('paul', 'mj')"
    deleteInsertDataToTable(data, insert)
    result = pythonDicFromQuery(data, query)
    if check['success']:
        print result
        print "function: pythonDicFromQuery(pythonDic, query) - passed"
    else:
        print check['fail']
        print "function: pythonDicFromQuery(pythonDic, query) - failed"
        exit()
