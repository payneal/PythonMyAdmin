
#CS 419 Project: Curses-based UI for Database Access


Background
Databases are rather interesting beasts, but the UIs available for them tend to fall into one of 3 camps:
• web based
• simple command line interface
• custom, heavyweight, arcane GUIs that rarely look native
While there are exceptions to the above (such as FileMaker Pro), DB interfaces are lacking one major flavor
of interface: an ncurses based command line tool.
Project Description
What I am looking for is relatively straightforward to describe: something along the lines of phpMyAdmin,
but CLI/ncurses based. This means a well implemented interface, with proper pagination of results, full
listing of tables, likely multiple screen ports (think frames on a web site), etc.
Unlike phpMyAdmin, this tool should work for either mysql or postgresql (preferred). Ideally, you will
implement both, and more grading consideration will be given if both are provided, but only one is required.
Database
No DB will be provided for this project, but you will need to create your own test DBs locally.
Useful information
• These tools will be entirely written in python. That means the curses based CLI and any testing tools
you need to write.
• postgreSQL and mysql are very similar. But not quite the same.
• While mysql is rarely used in production environments in larger corporations(at least as far as I can
find), postgresql is relatively common.

------------------------------------------------------------------

CS419 Group 6
Ali Payne
Joshua Alexander McQueen
Tyler Hadley

Group Requirements: 
Written entirely in Python (including tests)
UI utilizes the nurses library for displaying graphics and receiving user input
UI will display data with proper pagination
UI will use multiple windows/frames as appropriate
UI will show full listings of tables
UI is compatible with both mysql and/or postgresql
UI will support the following database actions:
create/drop databases
create/drop/alter tables,views
delete/edit/add fields
execute SQL (Post and My) 
manage keys, privileges, triggers, etc
export data in .txt, .csv or sql formats
Software testing will be performed using test query sets and will assess the basic sql execution functionality of the application and whether the displayed output is behaving as expected
Database sample data is based off of the publicly available “world” database, 
for which there are mySQL and postgresql versions:
http://dev.mysql.com/doc/world-setup/en/
http://pgfoundry.org/projects/dbsamples/


decent manual: http://www.tldp.org/HOWTO/NCURSES-Programming-HOWTO/
flow chart: https://drive.draw.io/#G0BwlWZfoKk28SRmUzNl9zZlpUUDQ

-------------------------------------------------
due dates: 

Design document:
This will be due the Wednesday of week 4. This document should contain your entire design, as well as a timeline with
milestones. The “how” and the “when”.
Weekly progress reports:
Due Sunday night of each week, these will contain 3 specific sections:
• Progress during the past week.
• Plans for the upcoming week. 
• Any problems you encountered during the past week.
These progress reports will be submitted via TEACH.

Midterm demo:
Your midterm progress report will be during week 5, and will a group video. At this point, you will demonstrate
your progress to date. Any functional code, screen mockups, etc. will be shown during this demo. You are certainly
not expected to have a functional product at this point, it is simply a way to determine where you are, a chance
offer advice on how to move forward, and a checkpoint in your progress.
Final report:
Your final report is a written document detailing your project, including changes to your design, problems you
overcame, a group evaluation, and any other interesting project related details you want to include. Specific
format guidelines and requirements will be posted during week 8. 
-------------------------------------------------

Not all req's were meet but here is the finished result:
[![CS419 - Curses-based UI for Database Access(python)  ](http://img.youtube.com/vi/unBNGDBV_no/0.jpg)](http://www.youtube.com/watch?v=unBNGDBV_no)


