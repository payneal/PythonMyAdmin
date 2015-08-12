#test script to connect to postgres db
#need to execute as the user that has permission for the db
#installation instructions for postgres and world db:
#	sudo apt-get install postgresql postgresql-contrib
#	sudo -u postgres psql postgres
#	download world sample database from http://pgfoundry.org/projects/dbsamples/
#	navigate to world.sql
#	sudo -u postgres createdb world
#	sudo -u postgres psql -f world.sql -d world

import psycopg2
import sys
import json
import ast
import psycopg2.extras
import decimal

#input: python dict with username, database, password(optional), query
#output: results of query, or False if error.
def queryPostgresDict(login_dict, q_str=None):
	con = None
	try:
		con = psycopg2.connect(database =login_dict['database'], 
		                       user     =login_dict['username'], 
		                       password =login_dict['password'])
		dict_cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		#dict_cur = con.cursor()  
		if q_str == None:
	    		q_str = "SELECT * FROM COUNTRY LIMIT 3"
		dict_cur.execute(q_str) 
		results = dict_cur.fetchall()
		#ast.literal_eval(results)
		#results = [dict((dict_cur.description[i][0], value) \
               	#	for i, value in enumerate(row)) for row in dict_cur.fetchall()]
		json_results = json.dumps(results)
		return { 'True' :json_results }       
	except psycopg2.DatabaseError, e: 
	    	return { 'False':e }	       
	finally:
	    	if con:
		    	con.close()


