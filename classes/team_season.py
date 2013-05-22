#!/usr/bin/env python
"""
team_season.py
Author: Brian Boates

TeamSeason object for hockey analysis and 
prediction package
"""

class TeamSeason():
    """
    TeamSeason object
    fields:
       season: string
       team:   string
       games:  list[Game]
    methods:
       insert()
       game_on_date(date)
       get_games(location, result, before, after)
       num_games(location, result, before, after)
       get_goals_lists(N, location, result, before)
    """
    def __init__(self, season='None', team='None'):
        """
        Initialize TeamSeason object
        """
        self.season = season
        self.team   = team
        self.games  = []
    
    
    def __repr__(self):
        """
        Print functionality
        """
        s  = 'team = '+str(self.team)+'; '
        s += str(self.num_games())+' games\n'
        for g in self.games:
            s += g.__repr__() + '\n'
        return s
    
    
    def insert(self, g):
        """
        insert game into season object
        """
        self.games.append(g)
    
    
    def game_on_date(self, date):
        """
        return: Game played on date (if exists)
        params:
            date: string | a date string e.g. '2010-10-31'
        """
        # select all games played on date (if available)
        g = [x for x in self.games if x.date == date]
        
        # if a game was found, return it
        if g:
            return g[0]
        
        # otherwise, raise error
        else:
            raise IndexError('no Game found on '+date)
    
    
    def get_games(self, location='all', result='all', before=None, after=None):
        """
        return: list[Game] | list of games for team in TeamSeason
        
        params:
          location: string | 'all', 'home', or 'away'
            result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
            before: string | cut-off date to consider games before
                             (e.g. '2010-10-31')
             after: string | cut-off date to consider games after
                             (e.g. '2010-10-31')
        """
        # location can only be 'all', 'home' or 'away'
        assert location in ['all', 'home', 'away'], 'location='+str(location)
        
        # result can only be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
        # consider both home and away games
        if location == 'all':
            
            # consider all games between two dates
            if before and after:
                selection = [g for g in self.games if before < g.date < after]
            
            # consider all games before given date
            elif before:
                selection = [g for g in self.games if g.date < before]
                
            # consider all games after given date
            elif after:
                selection = [g for g in self.games if g.date > after]
                
            # consider all games
            else:
                selection = self.games
        
        # consider only home games
        elif location == 'home':
            
            # select all home games
            home_games = [g for g in self.games if self.team == g.home]
            
            # consider home games between two dates
            if before and after:
                selection = [g for g in home_games if before < g.date < after]
             
            # consider only home games before given date
            elif before:
                selection = [g for g in home_games if g.date < before]
            
            # consider only home games after given date
            elif after:
                selection = [g for g in home_games if g.date > after]
                
            # consider all home games
            else:
                selection = home_games
                
        # consider only away games
        elif location == 'away':
            
            # select all away games
            away_games = [g for g in self.games if self.team == g.away]
            
            # consider away games between two dates
            if before and after:
                selection = [g for g in away_games if before < g.date < after]
            
            # consider only away games before given date
            if before:
                selection = [g for g in away_games if g.date < before]
            
            # consider only away games after given date
            if after:
                selection = [g for g in away_games if g.date > after]
                
            # consider all away games
            else: 
                selection = away_games
        
        #====================================#
        # now have "selection" of games      #
        # partitioned by dates and locations #
        #====================================#
        
        # return all results from selection
        if result == 'all':
            return selection
                        
        # consider only wins from selection
        elif result == 'wins':
            return [g for g in selection if self.team == g.winner()]
        
        # consider only losses from selection
        elif result == 'losses':
            return [g for g in selection if self.team == g.loser()]
        
        # consider only games that ended in regulation from selection
        elif result == 'R':
            return [g for g in selection if g.ended_in_regulation()]
        
        # consider only games that ended not in regulation from selection
        # i.e. all OT and SO games
        elif result == 'notR':
            return [g for g in selection if not g.ended_in_regulation()]
        
        # consider only games that ended in OT from selection
        elif result == 'OT':
            return [g for g in selection if g.ended_in_OT()]
            
        # consider only games that ended in SO from selection
        elif result == 'SO':
            return [g for g in selection if g.ended_in_SO()]
    
    
    def num_games(self, location='all', result='all', before=None, after=None):
        """
        return: int | number of games in season object
                      for location as all, home, or away
        params:
          location: string | 'all', 'home', or 'away'
            result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
            before: string | cut-off date to consider games before
                             (e.g. '2010-10-31')
             after: string | cut-off date to consider games before
                             (e.g. '2010-10-31')
        """
        # location can only be 'all', 'home' or 'away'
        assert location in ['all', 'home', 'away'], 'location='+str(location)
        
        # retrieve appropriate selection of games
        selection = self.get_games(location=location, result=result, before=before, after=after)
        
        return len( selection )
    
    
    def get_goals_lists(self, N, location='all', result='all', before=None):
        """
        Compute the total number of "goals for" for 
        the team, given location as all, home, or away
        
        return: goals_for_list, goals_against_list | list[int], list[int]
                ---> total goals for/against for date and result selection
        params:
                 N: int    | number of previous games to consider for total
                             if N > current games in season, return -1
          location: string | 'all', 'home', or 'away' (default='all')
            result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
            before: string | date string e.g. '2010-01-31'
        """
        # location can only be 'all', 'home' or 'away'
        assert location in ['all', 'home', 'away'], 'location='+str(location)
        
        # result can only be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
        # get all games with given location and result before given date
        games = self.get_games(location=location, result=result, before=before)
        
        # get goals for and goals against lists
        goals_for_list     = [g.goals_for(self.team)     for g in games]
        goals_against_list = [g.goals_against(self.team) for g in games]
        
        # check to see if enough data for N
        if len(goals_for_list) < N:
            # if not, return empty lists
            return [], []
        
        # otherwise there are enough games
        else:
            # return the previous N games
            return goals_for_list[-N:], goals_against_list[-N:]
    
