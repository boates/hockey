#!/usr/bin/env python
"""
features.py
Author: Brian Boates

Features object for hockey prediction
and analysis package
"""
from pandas import DataFrame
import numpy as np

class Features(DataFrame):
    """
    Features object inherits from pandas.DataFrame
    
    IMPORTANT:  like a pandas.DataFrame, the index array
                must be given on initialization since the
                DataFrame is size-mutable
                
                i.e. my_features = Features(index=[...])
    
    methods:
        feature_names()
        num_features()
        get_feature(feature_name, as_values=False)
        get_features(feature_names, as_values=False)
        add_feature(feature_name, feature_array)
        add_features(feature_names, feature_arrays)
        scale_feature(feature_name)
        scale_features(feature_names)
    """
    def feature_names(self):
        """
        return: list[string] | list of feature names
        """
        return self.columns
    
    
    def num_features(self):
        """
        return: int | number of features in Feature object
        """
        return len(self.columns)
    
    
    def get_feature(self, feature_name, as_values=False):
        """
        return: pandas Series | feature data with name
                -- OR (depending on as_values flag) --
                np.array      | 1D array of feature data
        
        params:
           feature_name: string | feature to get
              as_values: bool         | return as np.array or not
        """
        if as_values:
            return self.get(feature_name).values
        else:
            return self.get(feature_name)
    
    
    def get_features(self, feature_names, as_values=False):
        """
        return: pandas DataFrame | features data with names
                -- OR (depending on as_values flag) --
                np.array         | 2D array of features data
        
        params:
           feature_names: list[string] | list of features to get
               as_values: bool         | return as np.array or not
        """
        if as_values:
            return self.get(feature_names).values
        else:
            return self.get(feature_names) 
    
    
    def add_feature(self, feature_name, feature_array):
        """
        Insert a feature into Features object
        
        params:
             feature_name: string      | feature name
            feature_array: list[float] | feature data
        """
#        self.insert(loc=self.num_features(), column=feature_name, value=feature_array)
        self[feature_name] = feature_array
    
    
    def add_features(self, feature_names, feature_arrays):
        """
        Insert multiple features into the Features object
        
        params:
             feature_names: list[string]      | list of feature names
            feature_arrays: list[list[float]] | 2D array of feature data
        """
        for i, feature_name in enumerate(feature_names):
            self.add_feature(feature_name, features_array[i])
    
    
    def delete_feature(self, feature_name):
        """
        Remove feature column from Features object
        
        params:
            feature_name: string | feature to delete
        """
        deleted_feature = self.pop(feature_name)
    
    
    def delete_features(self, feature_names):
        """
        Remove set of given features from Features object
        
        params:
            feature_names: list[string] | features to delete
        """
        for feature_name in feature_names:
            self.delete_feature(feature_name)
    
    
    def scale_feature(self, feature_name):
        """
        Scale the feature given by feature_name
        Note: this changes the feature in self explicitly
        
        params:
            feature_name: string | name of feature to be scaled
        """
        feature = self.get_feature(feature_name)
        
        mean = feature.mean()
        span = (feature.max() - feature.min())/2.0
        
        self[feature_name] = (feature - mean) / span
    
    
    def scale_features(self, feature_names=['all']):
        """
        Scale given list of features
        
        params:
            feature_names: list[string] | list of feature names
                                        | default=['all'] (i.e. 
                                        | scale all features)
        """
        if feature_names == ['all']: 
            feature_names = self.feature_names()
        
        for feature_name in feature_names:
            self.scale_feature(feature_name)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    