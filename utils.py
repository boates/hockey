#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

utility functions for hockey analysis
and prediction package

classes:
    Game()
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


class Season():
    """
    Season object
    fields:
        team: string
       games: list[Game]
    methods:
       nGames()
       insert()
    """
    def __init__(self, team='None'):
        """
        Initialize Season object
        """
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
    
    
    def nGames(self):
        """
        return: number of games in season object
        """
        return len(self.games)
    
    
    def insert(self, g):
        """
        insert game into season object
        """
        self.games.append(g)
    
    
    def homeWins(self):
        """
        return: int | number of home wins for team
        """
        hWins = [g for g in self.games if g.winner == g.home == self.team]
        print hWins
        return len(hWins)
    
    def awayWins(self):
        """
        return: int | number of away wins for team
        """
        pass
    
    def nOT(self, SO=True):
        """
        return: int | number of OT games ()
        params:
            SO: bool | include SO games in sum (default=True)
        """
        # retrieve all games that ended in OT (or possibly SO)
        if SO:
            OT = [g for g in self.games if g.results in ['OT','SO']]
        else:
            OT = [g for g in self.games if g.results == 'OT']
            
        return len(OT)

        
def main():
    pass



if __name__ == '__main__':
    main()
