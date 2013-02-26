#!/usr/bin/env python
"""
database.py
Author: Brian Boates

Take the YEAR-YEAR.scores files
and create a table for each inside 
a "hockey" database. Populate each 
table with its respective score data
"""
import glob
import MySQLdb as mdb

def dbRemove(db='hockey'):
    """
    WARNING! This function will drop current hockey database
    params:
            db: string | the name of the MySQL database
    """
    # connect to MySQL
    con = mdb.connect(host='localhost', user='root')
    
    # create cursor for MySQL
    cur = con.cursor()
    
    # check to see if database exists
    cur.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \'"+db+"\'")
    exists = cur.fetchone()
    
    # if database exists, remove it entirely
    if exists:
        cur.execute("DROP database "+db)


def dbCreate(db='hockey'):
    """
    Create the MySQL hockey database
    params:
            db: string | the name of the MySQL database
    """
    # connect to MySQL
    con = mdb.connect(host='localhost', user='root')
    
    # create cursor for MySQL
    cur = con.cursor()
    
    # create the hockey database if not already present
    cur.execute("CREATE SCHEMA IF NOT EXISTS "+db)
    
    # change to newly created hockey database
    cur.execute("USE "+db)
    
    # with connection to the hockey database
    with con:
        
        # create cursor to hockey database        
        cur = con.cursor()
        
        # find available season data
        seasons = sorted([s[7:16].replace('-','_') for s in glob.glob('scores/*.scores')])
        
        # create a table for each season
        for season in seasons:
            
            # each table has a date, home and away teams/goals and a result
            command  = "CREATE TABLE IF NOT EXISTS "+season+" (id INT PRIMARY KEY "
            command += "AUTO_INCREMENT, year INT, month INT, day INT, away CHAR(3), "
            command += "home CHAR(3), agoal INT, hgoal INT, result CHAR(2))"
            print command
            cur.execute(command)
            
            # populate the current season table
            dbPopulate(cur=cur, table=season)
                                
    # close cursor to skillrank database
    if cur: cur.close()
    
    # close connection to skillrank database
    if con: con.close()


def dbPopulate(cur, table):
    """
    Populate the MySQL hockey database for a given season
    params:
          cur: cursor to the MySQL hockey database
        table: string | the name of the database table
    """
    # create root string for MySQL insertions
    root = "INSERT INTO "+table+"(year,month,day,away,home,agoal,hgoal,result) "
    
    # open the corresponding .scores file
    scoresFile = open('scores/'+table.replace('_','-')+'.scores', 'rU')
    
    # loop through each line in .scores file
    for line in scoresFile:
        
        # split the line
        row = line.split()
        # assign date variables
        year, month, day = row[0].split('-')
        # assign away and home teams
        away, home = row[1], row[3]
        # assign away and home goals
        agoal, hgoal = row[2], row[4]
        # assign result
        result = row[5]
        
        # build the insertion command for current line
        command = root + "VALUES("+year+","+month+","+day+",\'"+away+"\',\'"+home+"\',"+ \
                                   agoal+","+hgoal+",\'"+result+"\')"
                                  
        cur.execute(command)


def main():
    """
    remove hockey database and create from scratch
    requires local scores/ directory with .scores files
    """
    dbRemove(db='hockey')
    dbCreate(db='hockey')


if __name__ == '__main__':
    main()