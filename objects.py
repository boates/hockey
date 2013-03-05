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
        dScore()
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
    
    
    def goalsFor(self, team):
        """
        return: int | number of goals for given team
                      does NOT include SO goals
        params:
            team: string | 3-character team name
        """
        # team must be one of two teams in Game
        assert team in [self.home, self.away], 'team='+team
        
        # SO edge case, SO goals do not count
        if self.result == 'SO': return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team = self.home: return self.hgoal
            
        # if the given team was the away team
        elif team = self.away: return self.agoal
    
        
    def goalsAgainst(self, team):
        """
        return: int | number of goals against given team
                      does NOT include SO goals
        params:
            team: string | 3-character team name
        """
        # team must be one of two teams in Game
        assert team in [self.home, self.away], 'team='+team
        
        # SO edge case, SO goals do not count
        if self.result == 'SO': return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team = self.home: return self.agoal
            
        # if the given team was the away team
        elif team = self.away: return self.hgoal
    
        
    def dScore(self):
        """
        return: int | score differential for game
                    | computed as ghome - gaway so that pos/neg
                    | values correspond to home/away wins
                    | return 0 if game went to SO
        """
        # return 0 in the case of a shootout
        if self.result == 'SO':
            return 0
        
        # otherwise, return goal differential
        else:
            return self.ghome - self.gaway
    
    


class TeamSeason():
    """
    TeamSeason object
    fields:
       season: string
       team:   string
       games:  list[Game]
    methods:
       insert()
       getGames(loc, result, before, after)
       nGames(loc, result, before, after)
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
    
        
    def getGames(self, loc='all', result='all', before=None, after=None):
        """
        return: list[Game] | list of games for team
                             in TeamSeason
        params:
              loc: string | 'all', 'home', or 'away'
           result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
           before: string | cut-off date to consider games before
                            (e.g. '2010-10-31')
            after: string | cut-off date to consider games after
                            (e.g. '2010-10-31')
        """
        # loc can only be 'all', 'home' or 'away'
        assert loc in ['all', 'home', 'away'], 'loc='+loc
        
        # result can only be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+result
        
        # consider both home and away games
        if loc == 'all':
            
            # consider all games between two dates
            if before and after:
                selection = [g for g in self.games if before < g.date() < after]
            
            # consider all games before given date
            elif before:
                selection = [g for g in self.games if g.date() < before]
                
            # consider all games after given date
            elif after:
                selection = [g for g in self.games if g.date() > after]
                
            # consider all games
            else:
                selection = self.games
        
        # consider only home games
        elif loc == 'home':
            
            # select all home games
            homeGames = [g for g in self.games if self.team == g.home]
            
            # consider home games between two dates
            if before and after:
                selection = [g for g in homeGames if before < g.date() < after]
             
            # consider only home games before given date
            elif before:
                selection = [g for g in homeGames if g.date() < date]
            
            # consider only home games after given date
            elif after:
                selection = [g for g in homeGames if g.date() > date]
                
            # consider all home games
            else:
                selection = homeGames
                
        # consider only away games
        elif loc == 'away':
            
            # select all away games
            awayGames = [g for g in self.games if self.team = g.away]
            
            # consider away games between two dates
            if before and after:
                selection = [g for g in awayGames if before < g.date() < after]
            
            # consider only away games before given date
            if before:
                selection = [g for g in awayGames if g.date() < date]
            
            # consider only away games after given date
            if after:
                selection = [g for g in awayGames if g.date() > date]
                
            # consider all away games
            else: 
                selection = awayGames
        
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
            return [g for g in selection if g.result == 'R']
        
        # consider only games that ended not in regulation from selection
        # i.e. all OT and SO games
        elif result == 'notR':
            return [g for g in selection if g.result != 'R']
        
        # consider only games that ended in OT from selection
        elif result == 'OT':
            return [g for g in selection if g.result == 'OT']
            
        # consider only games that ended in SO from selection
        elif result == 'SO':
            return [g for g in selection if g.result == 'SO']
    
    
    def nGames(self, loc='all', result='all' before=None, after=None):
        """
        return: int | number of games in season object
                      for location as all, home, or away
        params:
              loc: string | 'all', 'home', or 'away'
           result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
           before: string | cut-off date to consider games before
                            (e.g. '2010-10-31')
            after: string | cut-off date to consider games before
                            (e.g. '2010-10-31')
        """
        # loc can only be 'all', 'home' or 'away'
        assert loc in ['all', 'home', 'away'], 'loc='+loc
        
        # retrieve appropriate selection of games
        selection = self.getGames(loc=loc, result=result, before=before, after=after) )
        
        return len( selection )


    

    def getGoalsList(self, N, loc='all', result='all', before=None):
        """
        Compute the total number of "goals for" for 
        the team, given location as all, home, or away
        
        return: goalsForList, goalsAgainstList | list[int], list[int]
                ---> total goals for/against for date and result selection
        params:
                N: int    | number of previous games to consider for total
                            if N > current games in season, return -1
              loc: string | 'all', 'home', or 'away' (default='all')
           result: string | 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
           before: string | date string e.g. '2010-01-31'
        """
        # loc can only be 'all', 'home' or 'away'
        assert loc in ['all', 'home', 'away'], 'loc='+loc
        
        # result can only be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+result

        # get all games with given location and result before given date
        games = self.getGames(loc=loc, result=result, before=before)
        
        # get goals for and goals against lists
        goalsForList     = [g.goalsFor(self.team)     for g in games]
        goalsAgainstList = [g.goalsAgainst(self.team) for g in games]
        
        # check to see if enough data for N
        if len(goalsForList) < N:
            # if not, return empty lists
            return [], []
        
        # otherwise there are engouh games
        else:
            # return the previous N games
            return goalsForList[-N:], goalsAgainstList[-N:]
    



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
    
    

