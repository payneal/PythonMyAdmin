#if we decide to do things locally check this out
#http://zetcode.com/db/mysqlpython/
#http://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
import mysql.connector
from mysql.connector import errorcode

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

    def showhowtogetinfo():
        print "must collect your login information to use Command LineInterface"
        print "1.) go to the following website: http://onid.oregonstate.edu/ "
        print "2.)Click Log in to ONID (to bypass: https://secure.onid.oregonstate.edu/cgi-bin/my?type=want_auth)"
        print "3.) Type in user name and password amd click login"
        print "4.) Click on Web Database"
        print "5.) The following info needs to be provided"
        host = raw_input("what is the Hostname? ")
        host = host.strip()
        dbname = raw_input("what is the DatabaseName? ")
        dbname = dbname.strip()
        username = raw_input("what is the username? ")
        username = username.strip()
        password= raw_input("what is the password? ")
        password= password.strip()
        return (host, dbname, username, password)

    print("test this thing out")
    host, dbname, uname, passw = showhowtogetinfo()
    print "the value entered for host; ", host
    test = users(dbname, uname, passw, host)
    test.connectToDB()
    test.closeDB()