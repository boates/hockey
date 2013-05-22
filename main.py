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
    game_list = []
    feature_names = ['proj_diff_score', 'diff_streak']
    
    # loop over all seasons
    for seasonName in seasonNames:
        
        # get Season for seasonName
        S = getSeason(cur, seasonName)
        
        # compute projections for games in season, append to feature list
        S.get_projections(window=10, location='all', result='all', scheme='constant')
        
        # compute streaks for all teams' games, append to feature list
        S.get_streaks(location='all', result='all')
        
        # append all games from S to game_ist
        game_list += S.all_games(feature_names)
        
    # get features dataframe for all games
    features = getFeatures(game_list, feature_names, scale=True)
    
    print features.tail(100)
    
    
#    for j in range(len(features[0])):
#        for i in range(len(features)):
#            print features[i][j],
#        print results[j]
       
#    makePlots(features[0], results, nbins=100)
    
     
        
    # close cursor and connection to MySQL db
    if cur: cur.close()
    if con: con.close()    
    
    
    
    
if __name__ == '__main__':
    main()