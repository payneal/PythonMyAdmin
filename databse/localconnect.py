#this is used to loginto root so that you can create a user

#I worote this to run on my mac computer 
#I state this because I cannot run terminal call 'mysql' to get to mysql to run 
#instead I must use "/usr/local/mysql/bin/mysql " now all of this can be temporaryly changed on a mac 
#with the following terminal call '/usr/local/mysql/bin/mysql ' but even if this takes place on the 
#python call I still must use "/usr/local/mysql/bin/mysql" rather than 'mysql' so if you are testing this on
#your machine adjust the machine accordingly 

# for operating system calls 
import subprocess

#for mysql db 
import mysql.connector
from mysql.connector import errorcode

#once establed a user in system we can use this
class users:
    def __init__(self, dbname, username , password , host , connection = None ):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.connection= connection


    def connectToDB(self):
        try:
            cnx = mysql.connector.connect(user= self.username, password= self.password, host= self.host, database= self.dbname )
            self.connection = cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def closeDB(self):
        if self.connection == None:
            print "you are not connecte dto databse"
        else:
            self.connection.close()
            print "the connection has been closed"



#used this not the comment line below fell free to ignore windows warning
#https://docs.python.org/2/library/subprocess.html
def system_output(command):
	p = subprocess.check_output([command], stderr=subprocess.STDOUT, shell=True)
	return p

#used to connect to local mysql host
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



# when ran as main test will test to see if this program is valid, with your entered setting can run
# on your system, and or if the information you input is correcct
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

	









