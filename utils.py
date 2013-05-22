#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

Utility methods for hockey analysis
"""
import pandas

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


def scaleFeatures(features, featureList):
    """
    return: dataframe | scaled features dataframe
    
    params:
         features: dataframe    | original unscaled features
      featureList: list[string] | list of features to scale
    """
    # scale each feature
    for f in featureList:
        features[f] = scaleFeature(features[f].values)
    return features


def getFeatures(gameList, featureList, scale=True):
    """
    return: features dataframe
    
    params:
          gameList: list[Game]   | list of Games
       featureList: list[string] | list of feature names
             scale: bool         | whether to feature scale or not
    """
    # initialize features array
    all_features = []
    
    # loop over all Games
    for g in gameList:
        
        # create empty feature vector for current Game
        game_features = []
        
        # loop over requested features
        for f in featureList:
            
            # append to game features
            game_features.append( g.features[f] )
        
        # set the target metric (1 for SO, 0 for anything else)
        result = int( g.numerical_result() )
        
        # append the result as the final Game feature
        game_features.append(result)
        
        # append the Game feature list to features array
        all_features.append(game_features)
    
    # create features dataframe
    features = pandas.DataFrame(all_features, columns=featureList+['class'])
    
    # feature scaling if requested
    if scale:
        features = scaleFeatures(features, featureList)
    
    return features


def makePlots(feature, results, nbins=100):
    """
    """
    import numpy
    
    allpdS, home, away, tie = [], [], [], []
    
    for i, f in enumerate(feature):
        if   results[i] == 0: tie.append(f)
        elif results[i]  > 0: home.append(f)
        elif results[i]  < 0: away.append(f)
        allpdS.append(f)
        
    # Create histograms for all, favor, upset, and tie
    aHist = numpy.histogram(numpy.array(allpdS), bins=nbins,normed=False,range=(min(allpdS),max(allpdS)))
    hHist = numpy.histogram(numpy.array(home), bins=nbins,normed=False,range=(min(allpdS),max(allpdS)))
    vHist = numpy.histogram(numpy.array(away), bins=nbins,normed=False,range=(min(allpdS),max(allpdS)))
    tHist = numpy.histogram(numpy.array(tie),  bins=nbins,normed=False,range=(min(allpdS),max(allpdS)))
    
    ax, vx, hx, tx = aHist[1], vHist[1], hHist[1], tHist[1]
    ay, vy, hy, ty = aHist[0], vHist[0], hHist[0], tHist[0]
    
    # Scale the histograms by event occurence
    a, v, h, t = list(ay), list(vy), list(hy), list(ty)
    for i in range(len(ay)):
        
        if ay[i] != 0:
            v_scale = float(vy[i]) / float(ay[i])
            h_scale = float(hy[i]) / float(ay[i])
            t_scale = float(ty[i]) / float(ay[i])
            
            v[i] = v_scale
            h[i] = h_scale
            t[i] = t_scale
            
    # Write histogram for visitors (away)
    out = open('away.hist','w')
    for i in range(len(v)):
        if ay[i] > 0:  # don't write if this value of dP has never occured
            out.write(str(vx[i])+' '+str(v[i])+'\n')
    out.close()
    
    # Write histogram for home
    out = open('home.hist','w')
    for i in range(len(h)):
        if ay[i] > 0:  # don't write if this value of dP has never occured
            out.write(str(hx[i])+' '+str(h[i])+'\n')
    out.close()
    
    # Write histogram for ties
    out = open('tie.hist','w')
    for i in range(len(t)):
        if ay[i] > 0:  # don't write if this value of dP has never occured
            out.write(str(tx[i])+' '+str(t[i])+'\n')
    out.close()
