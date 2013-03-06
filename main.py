#!/usr/bin/env python
"""
main.py
Author: Brian Boates

Main script for running hockey analysis
"""
import MySQLdb as mdb
from classes import Game
from classes import TeamSeason
from classes import Season
from database import *


def getFeatures(gameList, featureList):
    """
    return: dictionary of Game features
    params:
          gameList: list[Game]   | list of Games
       featureList: list[string] | list of feature names
    """
    # initialize 2d feature array
    features = [[] for f in featureList]
    
    # loop over features in Game
    for i, f in enumerate(featureList):
        
        # loop over all games in gameList
        for g in gameList:
            
            # append game feature to overall list
            print i, f
            print g
            print g.features
            features[i].append( g.features[f] )
            
    return features


def main():
    
    # connect to MySQL db and get cursor
    con = mdb.connect(host='localhost', db='hockey', user='root')
    cur = con.cursor()
    
    # get all available season names
    seasonNames = getSeasonNames(cur)
    
    # initialize list to hold all games from all seasons
    gameList = []
    featureList = []
    
    # loop over all seasons
#    for seasonName in seasonNames:
    for seasonName in seasonNames[-1:]:
        
        # get Season for seasonName
        S = getSeason(cur, seasonName)
        
        # compute projections for games in season, append to feature list
        S.getProjections(N=5, loc='all', result='all', scheme='constant')
        featureList.append('pdScore')
        
        # compute streaks for all teams' games, append to feature list
        S.getStreaks(loc='all', result='all')
        featureList.append('dStreak')
        
        # append all games from S to gameList
        gameList += S.allGames(featureList)
        
#    ts = S.getTeam('DET')    
#    for g in ts.getGames():
#        print g.features
    
    # get list of all games from all seasons       
#    for g in gameList:
#        if 'dStreak' not in g.features.keys():
#            print '------------'
#            print g
#            print g.features
    
    # get all features from all games
    features = getFeatures(gameList, featureList)
    
    for j in range(len(features[0])):
        for i in range(len(features)):
            print features[i][j],
        print
        
        
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()