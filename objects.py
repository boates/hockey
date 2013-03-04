#!/usr/bin/env python
"""
objects.py
Author: Brian Boates

objects for hockey analysis
and prediction package

classes:
    Game()
    TeamSeason()
    Season()
"""

class Game():
    """
    Game object
    fields:
          year: int
         month: int
           day: int
          away: string
          home: string
         agoal: int
         hgoal: int
        result: string
    methods:
        date()
        winner()
        loser()
    """
    def __init__(self, rec=None):
        """
        Initialize Game object (everything None
        if no record given at this time)
        """
        if rec:
            self.year   = int(rec[0])
            self.month  = int(rec[1])
            self.day    = int(rec[2])
            self.away   = str(rec[3])
            self.home   = str(rec[4])
            self.agoal  = int(rec[5])
            self.hgoal  = int(rec[6])
            self.result = str(rec[7])
        else:
            s = 'Must provide record when initializting game object'
            raise AttributeError(s)
    
        
    def __repr__(self):
        """
        Print functionality
        """
        # build the return string piece by piece
        s  = self.date()     + ' '
        s += self.away       + ' '
        s += self.home       + ' '
        s += str(self.agoal) + ' '
        s += str(self.hgoal) + ' '
        s += self.result
        
        return s
    
        
    def date(self):
        """
        return: string | formatted date string: 'YYYY-MM-DD'
        """
        # add year to date string
        d = str(self.year) + '-'
        
        # if month less than 10, add extra 0
        if self.month < 10:
            d += '0'
        d += str(self.month) + '-'
        
        # if day less than 10, add extra 0
        if self.day < 10:
            d += '0'
        d += str(self.day)
        
        return d
    
    
    def winner(self):
        """
        return: string | winning team name
        """
        if   self.agoal > self.hgoal: return self.away
        elif self.hgoal > self.agoal: return self.home
    
    
    def loser(self):
        """
        return: string | losing team name
        """
        if   self.agoal > self.hgoal: return self.home
        elif self.hgoal > self.agoal: return self.away
    

    
class TeamSeason():
    """
    TeamSeason object
    fields:
       season: string
       team:   string
       games:  list[Game]
    methods:
       insert()
       nGames()
       homeGames()
       awayGames()
       homeWins()
       awayWins()
       nhomeWins()
       nawayWins()
       OTGames(SO=True)
       nOTGames(SO=True)
    """
    def __init__(self, season='None', team='None'):
        """
        Initialize TeamSeason object
        """
        self.season = season
        self.team = team
        self.games = []
    
        
    def __repr__(self):
        """
        Print functionality
        """
        s  = 'team = '+str(self.team)+'; '
        s += str(self.nGames())+' games\n'
        for g in self.games:
            s += g.__repr__() + '\n'
        return s
    
    
    def insert(self, g):
        """
        insert game into season object
        """
        self.games.append(g)
    
        
    def nGames(self):
        """
        return: number of games in season object
        """
        return len(self.games)
    
    
    def homeGames(self):
        """
        return: list[Game] | list of home games
        """
        hGames = [g for g in self.games if self.home == g.home]
        return hGames
    
    
    def awayGames(self):
        """
        return: list[Game] | list of away games
        """
        aGames = [g for g in self.games if self.team == g.away]
        return aGames
    
    
    def homeWins(self):
        """
        return: list[Game] | list of home wins for team
        """
        hWins = [g for g in self.games if self.team == g.home == g.winner()]
        return hWins
    
    
    def awayWins(self):
        """
        return: list[Game] | list away wins for team
        """
        aWins = [g for g in self.games if self.team == g.away == g.winner()]
        return aWins
    
    
    def nhomeWins(self):
        """
        return: int | number of home wins for team
        """
        return len(self.homeWins)
    
    
    def nawayWins(self):
        """
        return: int | number of away wins for team
        """
        return len(self.awayWins)
    
    
    def OTGames(self, SO=True):
        """
        return: list[Game] | list of overtime games
        params:
            SO: bool | include SO games in list (default=True)
        """
        # retrieve all games that ended in OT (or possibly SO)
        if SO:
            return [g for g in self.games if g.result in ['OT','SO']]
        else:
            return [g for g in self.games if g.result == 'OT']
    
      
    def nOTGames(self, SO=True):
        """
        return: int | number of OT games ()
        params:
            SO: bool | include SO games in sum (default=True)
        """
        return len( self.OTGames(SO=SO) )
    


class Season():
    """
    Season object
    fields:
       season: string
          all: dict[string:TeamSeason]
    methods:
        insert()
        teams()
        getTeam(team)
    """
    def __init__(self, season='None'):
        """
        Initialize Season object
        """
        self.season = season
        self.all = {}
    
    
    def insert(self, teamSeason):
        """
        Insert TeamSeason object into Season
        """
        self.all[teamSeason.team] = teamSeason
    
    
    def teams(self):
        """
        return: list of teams present in Season
        """
        return sorted( self.all.keys() )
    
    
    def getTeam(self, team):
        """
        return: TeamSeason | object for given team's season
        """
        return self.all[team]
    
    

