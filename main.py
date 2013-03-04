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
    
    # create list of all seasons
    allSeasons = [getSeason(cur, seasonName) for seasonName in seasonNames]
    
    print allSeasons[0].getTeam('DET')
    print allSeasons[0].season
    
    
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()