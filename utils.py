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
    assert N >= 1, 'N must be >= 1; N='+str(N)
    
    # make sure scale is valid
    assert scheme in ['constant', 'linear'], 'scale='+str(scale)
    
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


def scaleFeature(f):
    """
    Feature scaling for individual features
    by subtracting mean and dividing by range
    
    return: list[float] | scaled feature
    params:
            list[float] | feature to be scaled
    """
    # compute the mean
    m = sum(f) / float(len(f))
    
    # get the max-min distance
    d = float(max(f) - min(f))
    
    # scale the feature
    scaledFeature = [(x-m)/d for x in f]
    
    return scaledFeature