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
    
    # loop over all seasons
#    for seasonName in seasonNames:
    for seasonName in seasonNames[-1:]:
        
        # get Season for seasonName
        S = getSeason(cur, seasonName)
        
        # compute projections for games in season
        S.getProjections(N=5, loc='all', result='all', scheme='constant')
        
    ts = S.getTeam('DET')
    
    for g in ts.getGames():
        print '--------------'
#        print g
        
        print S.getTeam(g.home).gameOnDate(g.date())
        print S.getTeam(g.away).gameOnDate(g.date())
        
#        S.getTeam(g.home).getGoalsLists(N=5, loc='all', result=result, before=date)
#        print g.features
        
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()