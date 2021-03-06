#!/usr/bin/env python
"""
utils.py
Author: Brian Boates

Utility methods for hockey analysis
"""
import pandas

def get_weights(N, scheme='constant'):
    """
    return: list[float] | list of weights, sum to 1
    params:
            N: int    | length of weight array
       scheme: string | weighting scheme: default='constant'
                        options are 'constant' or 'linear'
    """
    assert N >= 1, 'number of weights must be >= 1; given N='+str(N)
    assert scheme in ['constant', 'linear'], 'invalid scale='+str(scale)
    
    if scheme == 'constant':
        weights = [1.0/N for i in range(N)]
        
    elif scheme == 'linear':
        values = range(1,N+1)
        sum_values = float(sum(values))
        weights = [v/sum_values for v in values]
        
    return weights


def scale_feature(feature):
    """
    Feature scaling for individual features
    by subtracting mean and dividing by range
    
    return: list[float] | scaled feature
    params:
            list[float] | feature to be scaled
    """
    mean = sum(feature) / float(len(feature))
    
    distance = float(max(feature) - min(feature))
    
    scaled_feature = [(x-mean)/distance for x in feature]
    
    return scaled_feature


def scale_features(features, feature_names):
    """
    return: dataframe | scaled features dataframe
    
    params:
           features: dataframe    | original unscaled features
      feature_names: list[string] | list of features to scale
    """
    for f in feature_names:
        features[f] = scale_feature(features[f].values)
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
