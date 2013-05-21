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
        insertStreak(streak, loc)
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
            self.features = {}
                        
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
        s += str(self.dScore()) + ' '
        s += self.result     + ' '
        
        # include projections if available
        try:
            tmp = self.pdScore
            s += '| dp='
#            s += str(self.phGF) + ' '
#            s += str(self.phGA) + ' '
#            s += str(self.paGF) + ' '
#            s += str(self.paGA) + ' '
            s += str(self.pdScore) + ' '
        except AttributeError:
            pass
        
        # include streaks if available
        try:
            a, b = self.hstreak, self.astreak
            s += '| st='
            s += str(self.astreak) + ' '
            s += str(self.hstreak)
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
            return self.hgoal - self.agoal
    
    
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
        
        # add projected score differntial to features dict
        self.features['pdScore'] = pdScore
    
    
    def insertStreak(self, streak, loc):
        """
        Insert streaks for home or away team
        coming into Game
        
        params:
            streak: int    | streak (pos=winning, neg=losing)
               loc: string | 'home' or 'away'
        """
        # location must be either 'home' or 'away'
        assert loc in ['home', 'away'], 'loc='+str(loc)
        
        # insert the streak
        if   loc == 'home': self.hstreak = streak
        elif loc == 'away': self.astreak = streak
        
        # if both home and away streaks are available
        # put the difference into the features dict
        try:
            self.features['dStreak'] = self.hstreak - self.astreak
        except AttributeError:
            pass
    
    


class TeamSeason():
    """
    TeamSeason object
    fields:
       season: string
       team:   string
       games:  list[Game]
    methods:
       insert()
       gameOnDate(date)
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
    
    
    def gameOnDate(self, date):
        """
        return: Game played on date (if exists)
        params:
            date: string | a date string e.g. '2010-10-31'
        """
        # select all games played on date (if available)
        g = [x for x in self.games if x.date() == date]
        
        # if a game was found, return it
        if g:
            return g[0]
        
        # otherwise, raise error
        else:
            raise IndexError('no Game found on '+date)
    
    
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
        getStreaks(loc, result)
        allGames()
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
            tS = self.getTeam(team)
            
            # get selection of only all games (prone to double counting)
            games = tS.getGames(loc='all', result=result)
            
            # loop over team's games
            for g in games:
                
                # date of the game
                date = g.date()
                
                # if current team is home team
                if team == g.home:
                    
                    # get opponent's TeamSeason
                    tSopp = self.getTeam(g.away)
                    
                    # get goals lists for home and away teams
                    phGFlist, phGAlist =    tS.getGoalsLists(N, loc=loc, result=result, before=date)
                    paGFlist, paGAlist = tSopp.getGoalsLists(N, loc=loc, result=result, before=date)
                
                # if current team is away team
                if team == g.away:
                    
                    # get opponent's TeamSeason
                    tSopp = self.getTeam(g.home)
                    
                    # get goals lists for home and away teams
                    paGFlist, paGAlist =    tS.getGoalsLists(N, loc=loc, result=result, before=date)
                    phGFlist, phGAlist = tSopp.getGoalsLists(N, loc=loc, result=result, before=date)                    
                
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
            games = tS.getGames(loc=loc, result=result)
            
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
                    g.insertStreak(streak, loc='home')                    
                    # also insert into the copy of the game 
                    # in the opponent's TeamSeason
                    gOpp = self.getTeam(g.away).gameOnDate(g.date())
                    gOpp.insertStreak(streak, loc='home')
                    
                elif team == g.away:
                    # insert streak into Game
                    g.insertStreak(streak, loc='away')
                    # also insert into the copy of the game 
                    # in the opponent's TeamSeason
                    gOpp = self.getTeam(g.home).gameOnDate(g.date())
                    gOpp.insertStreak(streak, loc='away')
    
    
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
                gList = tS.getGames(loc='home')
                # append only games with all features
                gameList += [g for g in gList if sorted(g.features) == sorted(featureList)]
            
            # if features not specified
            else:
                # only append team's home games (avoids duplicates)
                gameList += tS.getGames(loc='home')
            
        # sort the gameList by date
        gameList = sorted(gameList, key=Game.date)
            
        return gameList
    





