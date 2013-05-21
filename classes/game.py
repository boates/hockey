#!/usr/bin/env python
"""
game.py
Author: Brian Boates

Game object for hockey analysis and 
prediction package
"""

class Game():
    """
    Game object
    fields:
          date: string
          year: int
         month: int
           day: int
          away: string
          home: string
         agoal: int
         hgoal: int
        result: string
    methods:
        getDate()
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
            self.date   = str(rec[0])
            self.year   = int(self.date.split('-')[0])
            self.month  = int(self.date.split('-')[1])
            self.day    = int(self.date.split('-')[2])
            self.away   = str(rec[1])
            self.home   = str(rec[2])
            self.agoal  = int(rec[3])
            self.hgoal  = int(rec[4])
            self.result = str(rec[5])
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
        s  = self.date          + ' '
        s += self.away          + ' '
        s += self.home          + ' '
        s += str(self.agoal)    + ' '
        s += str(self.hgoal)    + ' '
        s += str(self.dScore()) + ' '
        s += self.result        + ' '
        
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
    
    
    def getDate(self):
        """
        return: string | date (i.e. 'YYYY-MM-DD')
        """
        return self.date
    
    
    def winner(self):
        """
        return: string | winning team name
        
        note: includes SO outcomes
        """
        if   self.agoal > self.hgoal: return self.away
        elif self.hgoal > self.agoal: return self.home
    
    
    def loser(self):
        """
        return: string | losing team name
        
        note: includes SO outcomes
        """
        if   self.agoal > self.hgoal: return self.home
        elif self.hgoal > self.agoal: return self.away
    
    
    def goalsFor(self, team, includeSO=False):
        """
        return: int | number of goals for given team
                      (may include SO goals)
        params:
               team: string | 3-character team name
          includeSO: bool   | whether SO goals count or not
        """
        # team must be one of two teams in Game
        assert team in [self.home, self.away], 'team='+str(team)
        
        # do not count SO goals if specified
        if self.result == 'SO' and not includeSO:
            return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team == self.home: return self.hgoal
            
        # if the given team was the away team
        elif team == self.away: return self.agoal
    
        
    def goalsAgainst(self, team, includeSO=False):
        """
        return: int | number of goals against given team
                      (may include SO goals)
        params:
               team: string | 3-character team name
          includeSO: bool   | whether SO goals count or not
        """
        # team must be one of two teams in Game
        assert team in [self.home, self.away], 'team='+str(team)
        
        # do not count SO goals if specified
        if self.result == 'SO' and not includeSO:
            return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team == self.home: return self.agoal
            
        # if the given team was the away team
        elif team == self.away: return self.hgoal
    
        
    def dScore(self, includeSO=False):
        """
        return: int | score differential for game
                    | computed as ghome - gaway so that pos/neg
                    | values correspond to home/away wins
                    | return 0 if game went to SO unless
                    | otherwise specified
        params:
            includeSO: bool | whether SO goals count or not
        """
        # return 0 in the case of a shootout unless otherwise specified
        if self.result == 'SO' and not includeSO:
            return 0
        
        # otherwise, return goal differential
        else:
            return self.hgoal - self.agoal
    
    
    def numericalResult(self):
        """
        return: int | a number version of the game result
                    |   0: home win / away loss (including OT)
                    |   0: away win / home loss (including OT)
                    |   1: SO
        """
        # reutnr 1 for SO
        if   self.result == 'SO': return 1
        
        #====================================================#
        # right now all regulation games are classified as 0 #
        
        # return 0 for non-SO home win
        elif self.home == self.winner(): return 0
        
        # return 0 for non-SO away win
        elif self.away == self.winner(): return 0
    
    
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
        
        # add projected goals for / against to features dict
        self.features['proj_home_GF'] = phGF
        self.features['proj_home_GA'] = phGA
        self.features['proj_away_GF'] = paGF
        self.features['proj_away_GA'] = paGA
        
        # add projected score differntial to features dict
        self.features['proj_diff_score'] = pdScore
    
    
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
        if   loc == 'home':
            self.hstreak = streak
            self.features['home_streak'] = streak
        elif loc == 'away':
            self.astreak = streak
            self.features['away_streak'] = streak
        
        # if both home and away streaks are available
        # put the difference into the features dict
        try:
            self.features['diff_streak'] = self.hstreak - self.astreak
        except AttributeError:
            pass
    
