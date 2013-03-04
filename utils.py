#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

utility functions for hockey analysis
and prediction package

classes:
    game()
"""

class game():
    """
    Game object
    fields:
        year
        month
        day
        away
        home
        agoal
        hgoal
        result
    methods:
        date()
    """
    def __init__(self, rec=None):
        """
        Initialize game object (everything None
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
    
    

        
def main():
    pass



if __name__ == '__main__':
    main()
