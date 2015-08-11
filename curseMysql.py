#!/usr/bin/env python

#http://www.thegeekstuff.com/2008/08/get-quick-info-on-mysql-db-table-column-and-index-using-mysqlshow/

# for operating system calls
import subprocess
#for mysql db
import MySQLdb
#used to return json data
import json

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
            con = MySQLdb.connect(user= self.username, password= self.password, host= self.host, database= self.dbname
            self.connection = con
            return {'success': 'connected'}
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
                json_results = json.dumps(results)
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
                #might have to check if table exist

                #then drop if table does exist
                c.execute(table)

                return {'true':'created new table or deleted table'}
            except:
                self.connection.rollback()
                return {'false':"unable to create this table"}
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

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all rows from table
def getAllRowsFromTable(json_login, query_statment = None, tablename = None):
#"Select * FROM `tablename`

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- drop/add table from database
def dropOrAddTableMySql(json_loin, delete_statement = None, tableToDelet= None):

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- drop/add row to table
def dropOrAddRowMysql (json_loin, delete_statement = None, RowToDelete = None, tableOfRow = None):



############################################
# this is used to loginto root so that you can create a user
# which allows us to create new user on local server
# also can grant priovilages to user
#
# mac cannot run terminal call 'mysql' to get to mysql to
# run instead w/ "/usr/local/mysql/bin/mysql "
# can temporialy be changed with the following terminal call
# '/usr/local/mysql/bin/mysql'
# but still for this progam must enter "/usr/local/mysql/bin/mysql"
#
##################################################
class connectAsRoot:
    def __init__(self, howYouCallTerminalMysql=None, username= None, port=None, password=None, host=None):

    	self.howYouCallTerminalMysql = None
        #if your on windows and termical call for accesing mysql is 'mysql' just enter as s
        #but check this out 'http://stackoverflow.com/questions/13752424/how-to-connect-from-windows-command-prompt-to-mysql-command-line'

        #if linux see: http://stackoverflow.com/questions/6200215/how-to-log-in-to-mysql-and-query-the-database-from-linux-terminal
        #but for most part works same as windows so 'mysql'

         #keep in mine created on the system type below
        #for mac (OS X 10.10 (Yosemite)) => '/usr/local/mysql/bin/mysql
        # http://stackoverflow.com/questions/14235362/mac-install-and-open-mysql-using-terminal

        self.username= 'root'
        #we are login in at root which is the defealt administrated with all grant provilage

        self.port= '3306'
        #https://dev.mysql.com/doc/refman/5.1/en/connecting.html
        #ocnnections to remote servers always use TCP/IP. This command connects to the server running on remote.example.com using the default port number (3306)

        self.password = None
        #Windows = think there may also be a password not 100%
		#linux At the Enter password: prompt, well, enter root's password :)
		#macs root has no password set so '' is fine

      	#changing passowrd in mysql =
      	#https://dev.mysql.com/doc/refman/5.0/en/set-password.html

      	#once loged in as root show host root password for all users=
      	# 'select host, user, password from mysql.user;'

      	#once logged in so all info:
      	#'select * from mysql.user;'

      	self.host = "localhost"
      	#local host works on mac
      	# if this doesnt work check out '127.0.0.1'


    def setPassword(self):
    	password  = raw_input("what is password?\n")
    	self.password = password

    def setSysCall(self):
    	usersCall = raw_input("how do you call mysql?\n")
    	self.howYouCallTerminalMysql = usersCall


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

#This is used to make system calls
#https://docs.python.org/2/library/subprocess.html
def system_output(command):
	p = subprocess.check_output([command], stderr=subprocess.STDOUT, shell=True)
	return p


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all databases that belong to a user (less important, since right now we're logging in to a single database instead of an account)


#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#- get all tables from database



#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
############################################
# when ran as main test will test to see if this program is valid
# allows one to enter there own testing settings
#
#
#
############################################
if __name__ == "__main__":

	#test the command line first;
	testsys= 'ps'
	check = system_output(testsys)
	if "PID TTY" not in  check:
		print "terminal call: fail"
		exit()
	else:
		print "termail call: success"
		#contine

	#establish the objetct
	tester = connectAsRoot()
	#set the password
	tester.setPassword()
	#set how you make terminal Mysql call
	tester.setSysCall()

	#personal error check to make sure we have correcty inputs
	#print "this is the password {}".format(tester.password)
	#print "this is the call that needs to be made {}".format(tester.howYouCallTerminalMysql)

	mysqlLocation = tester.howYouCallTerminalMysql
	username = tester.username
	password = tester.password
	host = tester.host
	port = tester.port


	#creat command to root acces mysql
	command = mysqlLocation + " -u " + username + " -p " + password + " -h " + host + " -P " + port

	print "this is the command we will be sending to command line: {}".format(command)

	check = system_output(command)

	#stuck here you can log into console if you just go to python interperter and entere
	#what command is (keep in mind 'myslq' for windows '/usr/local/mysql/bin/mysql' or mac)

	#stuck because you  get an error im thinking, need to go back to:
	#https://docs.python.org/2/library/subprocess.html

	#and find out how to instead return standard out message I need to communicate
	# I say this because "enter password: " come up which your prompted to do on mysql
	#root acces but I prolly have to write back  command line but then again im now in mysql
	# so im not %100%  that is what writing to command line will do ???


	# after under stand how to create a new user then easy to connect with db useing
	# the user Object
