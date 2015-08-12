#Test that postgres and mysql modules are functioning correctly

from cursesPostgres import queryPostgresDict


login_info = {'username': 'postgres', 'password': '', 'database': 'world'}
print "Testing Postgres module:"
print "Should be success:"
print queryPostgresDict(login_info, "SELECT * FROM COUNTRY LIMIT 3")

print "Should fail:"
print queryPostgresDict(login_info, "SELECT * FROM COUNTR")

print "Should fail:"
print queryPostgresDict(login_info, "SELECT * FROM COUNTRY")

print "Should fail:"
print queryPostgresDict(login_info, "SELECT * FROM COUNTRY")

#Queries to use for testing:

#get all tables from database
#MySQL: SHOW TABLES from world
#postgres: SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'

#get all rows from table
#MySQL: SELECT * FROM Cities
#postgres: SELECT * FROM Cities

#drop/add table from database
#MySQL:CREATE TABLE test_table LIKE Cities
#postgres:

#drop/add row to table
#MySQL:
#postgres:
