#!/usr/bin/env python
"""
season.py
Author: Brian Boates

Season object for hockey analysis and 
prediction package
"""
from utils import getWeights
from game import Game

class Season():
    """
    Season object
    fields:
       season: string
          all: dict[string:TeamSeason]
    methods:
        insert(teamSeason)
        teams()
        get_team_season(team)
        get_projections(N, location, result, scheme)
        get_streaks(location, result)
        allGames()
    """
    def __init__(self, season='None'):
        """
        Initialize Season object
        """
        self.season = season
        self.all    = {}
    
    
    def insert(self, team_season):
        """
        Insert TeamSeason object into Season
        """
        self.all[team_season.team] = team_season
    
    
    def teams(self):
        """
        return: sorted list of teams present in Season
        """
        return sorted( self.all.keys() )
    
    
    def get_team_season(self, team):
        """
        return: TeamSeason | object for given team's season
        """
        return self.all[team]
    
    
    def get_projections(self, window, location='all', result='all', scheme='constant'):
        """
        Insert projections into each Game: 
            proj_home_GF, proj_away_GF, proj_home_GA, proj_away_GA, proj_diff_score
            proj_diff_score = (proj_home_GF+proj_away_GA)/2 - (proj_away_GF+proj_home_GA)/2
            ---> GF=goals for; GA=goals against
        params: 
            window: int    | window size (number of games) for weighting/projections
          location: string | location of games to include in projections
                             'all', 'home', or 'away' (default='all')
            result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
            scheme: string | weighting scheme: default='constant'
                             options are 'constant' or 'linear'
        """
        # location must be all, home, or away
        assert location in ['all', 'home', 'away'], 'location='+str(location)
        
        # result must be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
        # scheme must be 'constant' or 'linear'
        assert scheme in ['constant', 'linear'], 'scheme='+str(scheme)
        
        # get the projection weights
        weights = getWeights(window, scheme=scheme)
        
        # loop over teams in Season
        for team in self.teams():
            
            # get TeamSeason object
            team_season = self.get_team_season(team)
            
            # get selection of only all games (prone to double counting)
            games = team_season.get_games(location='all', result=result)
            
            # loop over team's games
            for g in games:
                
                # date of the game
                date = g.date
                
                # if current team is home team
                if team == g.home:
                    
                    # get opponent's TeamSeason
                    team_season_opponent = self.get_team_season(g.away)
                    
                    # get goals lists for home and away teams
                    home_GF_list, home_GA_list =          team_season.get_goals_lists(window, location=location, result=result, before=date)
                    away_GF_list, away_GA_list = team_season_opponent.get_goals_lists(window, location=location, result=result, before=date)
                
                # if current team is away team
                if team == g.away:
                    
                    # get opponent's TeamSeason
                    team_season_opponent = self.get_team_season(g.home)
                    
                    # get goals lists for home and away teams
                    away_GF_list, away_GA_list =          team_season.get_goals_lists(window, location=location, result=result, before=date)
                    home_GF_list, home_GA_list = team_season_opponent.get_goals_lists(window, location=location, result=result, before=date)                    
                
                # make sure N prior games were available for both teams
                if home_GF_list and home_GA_list and away_GF_list and away_GA_list:
                    
                    # initialize projection variables
                    proj_home_GF, proj_home_GA, proj_away_GF, proj_away_GA = 0.0, 0.0, 0.0, 0.0
                    
                    # loop over window size
                    for i in range(window):
                        
                        # compute the projections
                        proj_home_GF += home_GF_list[i] * weights[i]
                        proj_home_GA += home_GA_list[i] * weights[i]
                        proj_away_GF += away_GF_list[i] * weights[i]
                        proj_away_GA += away_GA_list[i] * weights[i]
                        
                    # compute the projected score differential
                    proj_diff_score = (proj_home_GF+proj_away_GA)/2.0 - (proj_away_GF+proj_home_GA)/2.0
                    
                    # add projected data to the Game object
                    g.insert_projections(proj_home_GF, proj_home_GA, proj_away_GF, proj_away_GA, proj_diff_score)
    
    
    def get_streaks(self, location='all', result='all'):
        """
        params:
          location: string | location of games to include in projections
                             'all', 'home', or 'away' (default='all')
            result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        """
        # location must be all, home, or away
        assert location in ['all', 'home', 'away'], 'location='+str(location)
        
        # result must be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
        # loop over all teams in season
        for team in self.teams():
            
            # get current TeamSeason
            team_season = self.get_team_season(team)
            
            # get all prior games for team
            games = team_season.get_games(location=location, result=result)
            
            # loop through team's games
            for i, g in enumerate(games):
                
                # initialize streak
                streak = 0
                
                # if first game, team has no streak
                if i == 0: streak = 0
                
                else:
                    # if team won its last game
                    if team == games[i-1].winner():
                        # loop over previous game outcomes until team didn't win
                        k = 1
                        while team == games[i-k].winner() and i-k > 0:
                            streak += 1
                            k += 1
                    
                    # if team lost its last game
                    elif team == games[i-1].loser():
                        # loop over previous game outcomes until team didn't lose
                        k = 1
                        while team == games[i-k].loser() and i-k > 0:
                            streak += -1
                            k += 1
                
                #### INSERT STREAK INTO Game OBJECTS ####
                
                if team == g.home:
                    # insert streak into Game
                    g.insert_streak(streak, location='home')                    
                    # also insert into the copy of the game 
                    # in the opponent's TeamSeason
                    opponent_game = self.get_team_season(g.away).game_on_date(g.date)
                    opponent_game.insert_streak(streak, location='home')
                    
                elif team == g.away:
                    # insert streak into Game
                    g.insert_streak(streak, location='away')
                    # also insert into the copy of the game 
                    # in the opponent's TeamSeason
                    opponent_game = self.get_team_season(g.home).game_on_date(g.date)
                    opponent_game.insert_streak(streak, location='away')
    
    
    def allGames(self, featureList=[]):
        """
        return: chronological list of all games
        params:
            featureList: list[string] | list of feature names
        """
        # initialize list to hold all games
        gameList = []
        
        # loop over all teams in season
        for team in self.teams():
            
            # get TeamSeason for team
            tS = self.get_team_season(team)
            
            # if specific features requested
            if featureList:
                # consider only home games to avoid duplicates
                gList = tS.get_games(location='home')
                # append only games with all features
                gameList += [g for g in gList if not [f for f in featureList if f not in g.features]]
            
            # if features not specified
            else:
                # only append team's home games (avoids duplicates)
                gameList += tS.get_games(location='home')
            
        # sort the gameList by date
        gameList = sorted(gameList, key=Game.get_date)
            
        return gameList
    






