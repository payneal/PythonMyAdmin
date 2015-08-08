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

#input: json strong with username, database, password(optional), query
#output: results of query, or False if error. 
def queryPostgres(json_login):
	con = None
	json_login_parsed = json.loads(json_login)

	try:
	    	con = psycopg2.connect(database=json_login_parsed['database'], user=json_login_parsed['username'], password=json_login_parsed['password']) 
	    	cur = con.cursor() #cursor can be used to execute SQL
	        if json_login_parsed['query_string']:
			cur.execute(json_login_parsed['query_string'])
			return {'True':cur.fetchall()}       
	except psycopg2.DatabaseError, e: 
	    	return {'False':e}
	       
	finally:
	    	if con:
			con.close()

# JAM (DEBUG): this version takes a dictionary instead of json object
def queryPostgresDict(json_login_dict, q_str=None):
    con = None
    try:
        con = psycopg2.connect(database =json_login_dict['database'], 
                               user     =json_login_dict['username'], 
                               password =json_login_dict['password'])
        cur = con.cursor() #cursor can be used to execute SQL
        if q_str == None:
            q_str = "SELECT * FROM COUNTRY LIMIT 3"
	    cur.execute(q_str) 
        return { 'True' :cur.fetchall() }       
    except psycopg2.DatabaseError, e: 
	    return { 'False':e }	       
    finally:
	    if con:
		    con.close()

# JAM (DEBUG): moved these into function since they were getting called
#   automatically when importing module
def tests():
    print "Should be success:"
    json_to_pass = '{ "username" : "postgres", "password": "", "database": "world", "query_string": "SELECT * FROM COUNTRY LIMIT 3" }'
    print queryPostgres(json_to_pass)

    print "Should fail:"
    json_to_pass = '{ "username" : "postgres", "password": "", "database": "world", "query_string": "SELECT * FROM COUNTR" }'
    print queryPostgres(json_to_pass)

    print "Should fail:"
    json_to_pass = '{ "username" : "postgres", "password": "", "database": "worl", "query_string": "SELECT * FROM COUNTRY" }'
    print queryPostgres(json_to_pass)

    print "Should fail:"
    json_to_pass = '{ "username" : "postgre", "password": "", "database": "world", "query_string": "SELECT * FROM COUNTRY" }'
    print queryPostgres(json_to_pass)
