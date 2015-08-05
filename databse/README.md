#connecting to database 

This will connect to mysql databse but the issue is that: 
you cannot connect to a databse direcly through flip so I guess we are back to the drawing board 


No need to go to drawing board we are connecting to local host mysql/postgress 

steps to set up mysql are in progress.doc


#issue - trying to have python script that can either make system call to access root of mysql 



1.) connect.py - This is first attempt 

    error = 

    2003: Can't connect to MySQL server on 'localhost:3306' (61 Connection refused)


    entered localhost, test, admin , ''


2.) connect2.py - this is 2nd attempt

error = 

Traceback (most recent call last):
File "localconnect.py", line 3, in <module>
subprocess.check_output(["mysql",  "-u admin -host localhost"])
File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 566, in check_output
process = Popen(stdout=PIPE, *popenargs, **kwargs)
File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 709, in __init__
errread, errwrite)
File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 1326, in _execute_child
raise child_exception
OSError: [Errno 2] No such file or directory

    


3.) connection3.py - This is the 3rd attempt 


    error = 

Traceback (most recent call last):
File "localconnect.py", line 21, in <module>
cnx = mysql.connector.connect(**config) 
File "/Library/Python/2.7/site-packages/mysql/connector/__init__.py", line 162, in connect
return MySQLConnection(*args, **kwargs)
File "/Library/Python/2.7/site-packages/mysql/connector/connection.py", line 129, in __init__
self.connect(**kwargs)
File "/Library/Python/2.7/site-packages/mysql/connector/connection.py", line 454, in connect
self._open_connection()
File "/Library/Python/2.7/site-packages/mysql/connector/connection.py", line 417, in _open_connection
self._socket.open_connection()
File "/Library/Python/2.7/site-packages/mysql/connector/network.py", line 475, in open_connection
errno=2003, values=(self.get_address(), _strioerror(err)))
mysql.connector.errors.InterfaceError: 2003: Can't connect to MySQL server on 'localhost:3306' (61 Connection refused)


4.) connection4.py 

error = same as 3 



