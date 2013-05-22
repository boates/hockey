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
        get_date()
        winner()
        loser()
        ended_in_regulation()
        ended_in_OT()
        ended_in_SO()
        has_team(team)
        goals_for(team)
        goals_against(team)
        diff_score()
        numerical_result()
        insert_projections(proj_home_GF, proj_home_GA, prj_away_GF, proj_away_GA, proj_diff_score)
        insert_streak(streak, location)
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
        s  = self.date              + ' '
        s += self.away              + ' '
        s += self.home              + ' '
        s += str(self.agoal)        + ' '
        s += str(self.hgoal)        + ' '
        s += str(self.diff_score()) + ' '
        s += self.result            + ' '
        
        # include projections if available
        try:
            tmp = self.pdScore
            s += '| dp='
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
    
    
    def get_date(self):
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
    
    
    def ended_in_regulation(self):
        """
        return: bool | whether the game ended in regulation or not
        """
        return self.result == 'R'
    
    
    def ended_in_OT(self):
        """
        return: bool | whether the game ended in OT or not
        """
        return self.result == 'OT'
    
    
    def ended_in_SO(self):
        """
        return: bool | whether the game ended in a SO or not
        """
        return self.result == 'SO'
    
    
    def has_team(self, team):
        """
        return: bool | whether the team is home or away
        """
        return team in [self.home, self.away]
    
    
    def goals_for(self, team, include_SO=False):
        """
        return: int | number of goals for given team
                      (may include SO goals)
        params:
                team: string | 3-character team name
          include_SO: bool   | whether SO goals count or not
        """
        # team must be one of two teams in Game
        assert self.has_team(team), 'team='+str(team)
        
        # do not count SO goals if specified
        if self.ended_in_SO() and not include_SO:
            return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team == self.home: return self.hgoal
            
        # if the given team was the away team
        elif team == self.away: return self.agoal
    
        
    def goals_against(self, team, include_SO=False):
        """
        return: int | number of goals against given team
                      (may include SO goals)
        params:
                team: string | 3-character team name
          include_SO: bool   | whether SO goals count or not
        """
        # team must be one of two teams in Game
        assert self.has_team(team), 'team='+str(team)
        
        # do not count SO goals if specified
        if self.ended_in_SO() and not include_SO:
            return min(self.hgoal, self.agoal)
        
        # if given team was the home team
        elif team == self.home: return self.agoal
            
        # if the given team was the away team
        elif team == self.away: return self.hgoal
    
        
    def diff_score(self, include_SO=False):
        """
        return: int | score differential for game
                    | computed as ghome - gaway so that pos/neg
                    | values correspond to home/away wins
                    | return 0 if game went to SO unless
                    | otherwise specified
        params:
            include_SO: bool | whether SO goals count or not
        """
        # return 0 in the case of a shootout unless otherwise specified
        if self.ended_in_SO() and not include_SO:
            return 0
        
        # otherwise, return goal differential
        else:
            return self.hgoal - self.agoal
    
    
    def numerical_result(self):
        """
        return: int | a number version of the game result
                    |   0: home win / away loss (including OT)
                    |   0: away win / home loss (including OT)
                    |   1: SO
        """
        # return 1 for SO
        if self.ended_in_SO(): return 1
        
        #====================================================#
        # right now all regulation games are classified as 0 #
        
        # return 0 for non-SO home win
        elif self.home == self.winner(): return 0
        
        # return 0 for non-SO away win
        elif self.away == self.winner(): return 0
    
    
    def insert_projections(self, proj_home_GF, proj_home_GA, proj_away_GF, proj_away_GA, proj_diff_score):
        """
        Insert projected scores into Game
        
        params:
             proj_home_GF: float | projected GF for home team
             proj_home_GA: float | projected GA for home team
             proj_away_GF: float | projected GF for away team
             proj_away_GA: float | projected GA for away team
          proj_diff_score: float | projected score differential
        """
        # set member variables
        self.proj_home_GF    = proj_home_GF
        self.proj_home_GA    = proj_home_GA
        self.proj_away_GF    = proj_away_GF
        self.proj_away_GA    = proj_away_GA
        self.proj_diff_score = proj_diff_score
        
        # add projected goals for / against to features dict
        self.features['proj_home_GF'] = proj_home_GF
        self.features['proj_home_GA'] = proj_home_GA
        self.features['proj_away_GF'] = proj_away_GF
        self.features['proj_away_GA'] = proj_away_GA
        
        # add projected score differntial to features dict
        self.features['proj_diff_score'] = proj_diff_score
    
    
    def insert_streak(self, streak, location):
        """
        Insert streaks for home or away team coming into Game
        
        params:
            streak: int    | streak (pos=winning, neg=losing)
          location: string | 'home' or 'away'
        """
        # location must be either 'home' or 'away'
        assert location in ['home', 'away'], 'location='+str(location)
        
        # insert the streak
        if location == 'home':
            self.home_streak = streak
            self.features['home_streak'] = streak
        elif location == 'away':
            self.away_streak = streak
            self.features['away_streak'] = streak
        
        # if both home and away streaks are available
        # put the difference into the features dict
        try:
            self.features['diff_streak'] = self.home_streak - self.away_streak
        except AttributeError:
            pass
    
