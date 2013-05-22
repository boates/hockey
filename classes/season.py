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
        getTeam(team)
        getProjections(N, loc, result, scheme)
        getStreaks(loc, result)
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
    
    
    def getTeam(self, team):
        """
        return: TeamSeason | object for given team's season
        """
        return self.all[team]
    
    
    def getProjections(self, N, loc='all', result='all', scheme='constant'):
        """
        Insert projections into each Game: 
            hGF, aGF, hGA, aGA, pdScore
            h/a=home/away, GF/GA=goals for/against
            pdScore= (phGF+paGA)/2 - (paGF+phGA)/2
        params: 
               N: int    | window size for weighting/projections
             loc: string | location of games to include in projections
                           'all', 'home', or 'away' (default='all')
          result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
          scheme: string | weighting scheme: default='constant'
                           options are 'constant' or 'linear'
        """
        # location must be all, home, or away
        assert loc in ['all', 'home', 'away'], 'loc='+str(loc)
        
        # result must be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
        # scheme must be 'constant' or 'linear'
        assert scheme in ['constant', 'linear'], 'scheme='+str(scheme)
        
        # get the projection weights
        weights = getWeights(N, scheme=scheme)
        
        # loop over teams in Season
        for team in self.teams():
            
            # get TeamSeason object
            tS = self.getTeam(team)
            
            # get selection of only all games (prone to double counting)
            games = tS.get_games(location='all', result=result)
            
            # loop over team's games
            for g in games:
                
                # date of the game
                date = g.date
                
                # if current team is home team
                if team == g.home:
                    
                    # get opponent's TeamSeason
                    tSopp = self.getTeam(g.away)
                    
                    # get goals lists for home and away teams
                    phGFlist, phGAlist =    tS.get_goals_lists(N, location=loc, result=result, before=date)
                    paGFlist, paGAlist = tSopp.get_goals_lists(N, location=loc, result=result, before=date)
                
                # if current team is away team
                if team == g.away:
                    
                    # get opponent's TeamSeason
                    tSopp = self.getTeam(g.home)
                    
                    # get goals lists for home and away teams
                    paGFlist, paGAlist =    tS.get_goals_lists(N, location=loc, result=result, before=date)
                    phGFlist, phGAlist = tSopp.get_goals_lists(N, location=loc, result=result, before=date)                    
                
                # make sure N prior games were available for both teams
                if phGFlist and phGAlist and paGFlist and paGAlist:
                    
                    # initialize projection variables
                    phGF, phGA, paGF, paGA = 0.0, 0.0, 0.0, 0.0
                    
                    # loop over window size
                    for i in range(N):
                        
                        # compute the projections
                        phGF += phGFlist[i] * weights[i]
                        phGA += phGAlist[i] * weights[i]
                        paGF += paGFlist[i] * weights[i]
                        paGA += paGAlist[i] * weights[i]
                        
                    # compute the projected score differential
                    pdScore = (phGF+paGA)/2.0 - (paGF+phGA)/2.0
                    
                    # add projected data to the Game object
                    g.insert_projections(phGF, phGA, paGF, paGA, pdScore)
    
    
    def getStreaks(self, loc='all', result='all'):
        """
        params:
           loc: string | location of games to include in projections
                         'all', 'home', or 'away' (default='all')
        result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        """
        # loop over all teams in season
        for team in self.teams():
            
            # get current TeamSeason
            tS = self.getTeam(team)
            
            # get all prior games for team
            games = tS.get_games(location=loc, result=result)
            
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
                    gOpp = self.getTeam(g.away).game_on_date(g.date)
                    gOpp.insert_streak(streak, location='home')
                    
                elif team == g.away:
                    # insert streak into Game
                    g.insert_streak(streak, location='away')
                    # also insert into the copy of the game 
                    # in the opponent's TeamSeason
                    gOpp = self.getTeam(g.home).game_on_date(g.date)
                    gOpp.insert_streak(streak, location='away')
    
    
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
            tS = self.getTeam(team)
            
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
    






