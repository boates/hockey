#!/usr/bin/env python
"""
main.py
Author: Brian Boates

Main script for running hockey analysis
"""
import MySQLdb as mdb
from classes.game import Game
from classes.team_season import TeamSeason
from classes.season import Season
from database import *
from utils import *

def main():
    
    # connect to MySQL db and get cursor
    con = mdb.connect(host='localhost', db='hockey', user='root')
    cur = con.cursor()
    
    # get all available season names
    seasonNames = getSeasonNames(cur)
    
    # initialize list to hold all games from all seasons
    gameList = []
    featureList = ['proj_diff_score', 'diff_streak']
    
    # loop over all seasons
    for seasonName in seasonNames:
        
        # get Season for seasonName
        S = getSeason(cur, seasonName)
        
        # compute projections for games in season, append to feature list
        S.getProjections(N=10, loc='all', result='all', scheme='constant')
        
        # compute streaks for all teams' games, append to feature list
        S.getStreaks(loc='all', result='all')
        
        # append all games from S to gameList
        gameList += S.allGames(featureList)
        
    # get all features from all games
    features, results = getFeatures(gameList, featureList)
    
    for j in range(len(features[0])):
        for i in range(len(features)):
            print features[i][j],
        print results[j]
       
    makePlots(features[0], results, nbins=100)
    
     
        
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()