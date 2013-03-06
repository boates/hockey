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
    
    # loop over all seasons
    for seasonName in seasonNames:
        
        # get Season for seasonName
        S = getSeason(cur, seasonName)
        
        # loop over all teams in Season
        for team in S.teams():
            
            # get TeamSeason object
            tS = S[team]
            
            # get games list for team
            games = tS.getGames(loc='all', result='all')
            
            
        
        
    
    print allSeasons[0].getTeam('DET')
    print allSeasons[0].season
    
    
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()