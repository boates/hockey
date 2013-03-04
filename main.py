#!/usr/bin/env python
"""
main.py
Author: Brian Boates

Main script for running hockey analysis
"""
import MySQLdb as mdb
from objects import Game, Season
from database import *



def main():
    
    # connect to MySQL db and get cursor
    con = mdb.connect(host='localhost', db='hockey', user='root')
    cur = con.cursor()
    
    # get all available season names
    seasonNames = getSeasonNames(cur)
    
    print seasonNames
    
    
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()