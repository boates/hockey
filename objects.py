#!/usr/bin/env python
"""
objects.py
Author: Brian Boates

objects for hockey analysis and 
prediction package

classes:
    Game()
    TeamSeason()
    Season()
"""
from utils import getWeights

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
        goalsFor(team)
        goalsAgainst(team)
        dScore()
        numericalResult()
        insertProjections(hGF, hGA, aGF, aGA, pdScore)
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
            
            #======= projections
            # self.phGF, self.phGA, self.paGF, self.paGA, self.pdScore
            #======= to be created later
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
        
        # include projections if available
        try:
            tmp = self.phGF
            s += '; p= '
            s += str(self.phGF) + ' '
            s += str(self.phGA) + ' '
            s += str(self.paGF) + ' '
            s += str(self.paGA) + ' '
            s += str(self.pdScore)
        except AttributeError:
            pass
        
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
        assert team in [self.home, self.away], 'team='+str(team)
        
        # SO edge case, SO goals do not count
        if self.result == 'SO': return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team == self.home: return self.hgoal
            
        # if the given team was the away team
        elif team == self.away: return self.agoal
    
        
    def goalsAgainst(self, team):
        """
        return: int | number of goals against given team
                      does NOT include SO goals
        params:
            team: string | 3-character team name
        """
        # team must be one of two teams in Game
        assert team in [self.home, self.away], 'team='+str(team)
        
        # SO edge case, SO goals do not count
        if self.result == 'SO': return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team == self.home: return self.agoal
            
        # if the given team was the away team
        elif team == self.away: return self.hgoal
    
        
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
    
    
    def numericalResult(self):
        """
        return: int | a number version of the game result
                    |   0: home win / away loss (including OT)
                    |   1: away win / home loss (including OT)
                    |   2: SO
        """
        # reutnr 2 for SO
        if   self.result == 'SO': return 2
        
        # return 0 for non-SO home win
        elif self.home == self.winner(): return 0
        
        # return 1 for non-SO away win
        elif self.away == self.winner(): return 1
    
    
    def insertProjections(self, phGF, phGA, paGF, paGA, pdScore):
        """
        Insert projected scores into Game
        
        params:
             phGF: float | projected GF for home team
             phGA: float | projected GA for home team
             paGF: float | projected GF for away team
             paGA: float | projected GA for away team
          pdScore: float | projected score differential
        """
        # set member variables
        self.phGF    = phGF
        self.phGA    = phGA
        self.paGF    = paGF
        self.paGA    = paGA
        self.pdScore = pdScore
    


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
       getGoalsLists(N, loc, result, before)
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
        assert loc in ['all', 'home', 'away'], 'loc='+str(loc)
        
        # result can only be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
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
                selection = [g for g in homeGames if g.date() < before]
            
            # consider only home games after given date
            elif after:
                selection = [g for g in homeGames if g.date() > after]
                
            # consider all home games
            else:
                selection = homeGames
                
        # consider only away games
        elif loc == 'away':
            
            # select all away games
            awayGames = [g for g in self.games if self.team == g.away]
            
            # consider away games between two dates
            if before and after:
                selection = [g for g in awayGames if before < g.date() < after]
            
            # consider only away games before given date
            if before:
                selection = [g for g in awayGames if g.date() < before]
            
            # consider only away games after given date
            if after:
                selection = [g for g in awayGames if g.date() > after]
                
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
    
    
    def nGames(self, loc='all', result='all', before=None, after=None):
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
        assert loc in ['all', 'home', 'away'], 'loc='+str(loc)
        
        # retrieve appropriate selection of games
        selection = self.getGames(loc=loc, result=result, before=before, after=after)
        
        return len( selection )
    
    
    def getGoalsLists(self, N, loc='all', result='all', before=None):
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
        assert loc in ['all', 'home', 'away'], 'loc='+str(loc)
        
        # result can only be 'all', 'wins', 'losses', 'R', 'notR', 'OT', or 'SO'
        assert result in ['all', 'wins', 'losses', 'R', 'notR', 'OT', 'SO'], 'result='+str(result)
        
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
        insert(teamSeason)
        teams()
        getTeam(team)
        getProjections(N, loc, result, scheme)
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
            tS = self.all[team]
            
            # get selection of only all games (prone to double counting)
            games = tS.getGames(loc='all', result=result)
            
            # loop over team's games
            for g in games:
                
                # date of the game
                date = g.date()
                
                # get TeamSeason for opponent
                tSopp = self.all[g.away]
                
                # get goals lists for home and away teams
                phGFlist, phGAlist =    tS.getGoalsLists(N, loc=loc, result=result, before=date)
                paGFlist, paGAlist = tSopp.getGoalsLists(N, loc=loc, result=result, before=date)
                
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
                    g.insertProjections(phGF, phGA, paGF, paGA, pdScore)
    
    
