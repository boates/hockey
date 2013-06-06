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
from classes.features import Features
from database import *
from utils import *

def get_features(game_list, feature_names, scale=True):
    """
    return: features dataframe
    
    params:
          game_list: list[Game]   | list of Games
      feature_names: list[string] | list of feature names
              scale: bool         | whether to feature scale or not
    """
    # initialize features array
    all_features = []
    
    # loop over all Games
    for g in game_list:
        
        # create empty feature vector for current Game
        game_features = []
        
        # loop over requested features
        for f in feature_names:
            
            # append to game features
            game_features.append( g.features[f] )
        
        # set the target metric
        result = int( g.numerical_result() )
        
        # append the result as the final Game feature
        game_features.append(result)
        
        # append the Game feature list to features array
        all_features.append(game_features)
    
    # create features dataframe
    features = pandas.DataFrame(all_features, columns=feature_names+['class'])
    
    # feature scaling if requested
    if scale:
        features = scale_features(features, feature_names)
    
    return features


def main():
    
    # connect to MySQL db and get cursor
    con = mdb.connect(host='localhost', db='hockey', user='root')
    cur = con.cursor()
    
    # get all available season names
    season_names = getSeasonNames(cur)
    
    # initialize list to hold all games from all seasons
    game_list = []
    feature_names = ['proj_diff_score', 'diff_streak']
    
    # loop over all seasons
    for season_name in season_names:
        
        # get Season for season_name
        season = getSeason(cur, season_name)
        
        # compute projections for games in season, append to feature list
        season.get_projections(window=10, location='all', result='all', scheme='constant')
        
        # compute streaks for all teams' games, append to feature list
        season.get_streaks(location='all', result='all')
        
        # append all games from season to game_ist
        game_list += season.all_games(feature_names)
        
    # get features dataframe for all games
    features = get_features(game_list, feature_names, scale=True)
    
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