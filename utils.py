#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

Utility methods for hockey analysis
"""

def getWeights(N, scheme='constant'):
    """
    return: list[float] | list of weights, sum to 1
    params:
            N: int    | length of weight array
       scheme: string | weighting scheme: default='constant'
                        options are 'constant' or 'linear'
    """
    # make sure N is valid
    assert N > 1, 'N must be greater than 1'
    
    # make sure scale is valid
    assert scheme in ['constant', 'linear'], 'scale='+scale
    
    # constant weighting
    if scheme == 'constant':
        # compute normalized weights (sum to 1)
        weights = [1.0/N for i in range(N)]
        
    # linear weighting
    elif scheme == 'linear':
        # get a linear scale
        tmp    = range(1,N+1)
        # compute the sum for normaization
        tmpSum = float(sum(tmp))
        # compute normalized weights (sum to 1)
        weights = [x/tmpSum for x in tmp]
        
    return weights



if __name__ == '__main__':
    main()