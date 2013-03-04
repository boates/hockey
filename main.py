#!/usr/bin/env python
"""
main.py
Author: Brian Boates

Main script for running hockey analysis
"""
import MySQLdb as mdb
from objects import Game
from objects import TeamSeason
from objects import Season
from database import *



def main():
    
    # connect to MySQL db and get cursor
    con = mdb.connect(host='localhost', db='hockey', user='root')
    cur = con.cursor()
    
    # get all available season names
    seasonNames = getSeasonNames(cur)
    
    # loop over all available seasons
    allSeasons = []
    for seasonName in seasonNames:
        allSeasons.append( getSeason(cur, seasonName) )
    

    print allSeasons[0].getTeam('DET')
    
    
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()