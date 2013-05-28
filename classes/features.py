#!/usr/bin/env python
"""
features.py
Author: Brian Boates

Features object for hockey prediction
and analysis package
"""
import numpy as np
import pandas as pd
from random import shuffle

class Features():
    """
    Features object
    
    IMPORTANT:  like a pandas.DataFrame, the index array
                must be given on initialization since the
                DataFrame is size-mutable
                
                i.e. my_features = Features(index=[...])
    
    fields:
        _feature_names: list[string]
        _class_names:   list[string]
    
    methods:                                   RETURNS: |
        __init__(index)                                 | N/A
        __repr__()                                      | string
        --
        num_examples()                                  | int
        --
        num_features()                                  | int
        feature_names()                                 | list[string]
        get_feature(feature_name, as_values=False)      | Series or np.array[dtype]
        get_features(feature_names, as_values=False)    | DataFrame or np.array[dtype]
        insert_feature(feature_array, feature_name)     | N/A
        insert_features(feature_arrays, feature_names)  | N/A
        delete_feature(feature_name)                    | N/A
        delete_features(feature_names)                  | N/A
        has_feature(feature_name)                       | bool
        has_features(feature_names)                     | bool
        rename_feature(current_name, new_name)          | N/A
        scale_feature(feature_name)                     | N/A
        scale_features(feature_names)                   | N/A
        --
        num_classes()                                   | int
        class_names()                                   | list[string]
        get_class(class_name, as_values=False)          | Series or np.array[dtype]
        get_classes(class_names, as_values=False)       | DataFrame or np.array[dtype]
        insert_class(class_array, class_name)           | N/A
        insert_classes(class_arrays, class_names)       | N/A
        delete_class(class_name)                        | N/A
        delete_classes(class_names)                     | N/A
        has_class(class_name)                           | bool
        has_classes(class_names)                        | bool
        rename_class(current_name, new_name)            | N/A
        --
        append(row)                                     | N/A
        split_data(train_perc, cv_perc, test_perc, as_values=False, shuffle=True)   | array, array, array
    """
    def __init__(self, index):
        """
        Initialize Features object with index array for DataFrame
        
        params:
            index: list[int] | index array for DataFrame initialization
        """
#        super(Features, self).__init__(index=index)
        self._df = pd.DataFrame(index=index)
        self._feature_names = []
        self._class_names   = []
    
    
    def __repr__(self):
        """
        Invokes pd.DataFrame.__repr__()
        """
        return self._df.__repr__()
    
    
    def num_examples(self):
        """
        return: int | number of examples in Features object
        """
        return len(self._df)
    
    
    def num_features(self):
        """
        return: int | number of features in Feature object
        """
        return len(self.feature_names())
    
    
    def feature_names(self):
        """
        return: list[string] | list of feature names
        """
        return self._feature_names
    
    
    def get_feature(self, feature_name, as_values=False):
        """
        return: pandas Series | feature data with name
                -- OR (depending on as_values flag) --
                np.array      | 1D array of feature data
        
        params:
           feature_name: string | feature to get
              as_values: bool   | return as np.array or not
        """
        if as_values:
            return self._df.get(feature_name).values
        else:
            return self._df.get(feature_name)
    
    
    def get_features(self, feature_names=['all'], as_values=False):
        """
        return: pandas DataFrame | features data with names
                -- OR (depending on as_values flag) --
                np.array         | 2D array of features data
        
        params:
           feature_names: list[string] | list of features to get
                                       | (default=['all'])
               as_values: bool         | return as np.array or not
        """
        if feature_names == ['all'] and 'all' not in self.feature_names():
            feature_names = self.feature_names()
        
        if as_values:
            return self._df.get(feature_names).values
        else:
            return self._df.get(feature_names) 
    
    
    def insert_feature(self, feature_array, feature_name):
        """
        Insert a feature into Features object
        
        params:
            feature_array: list[float] | feature data
             feature_name: string      | feature name
        """
        self._df[feature_name] = feature_array
        self._feature_names.append(feature_name)
    
    
    def insert_features(self, feature_arrays, feature_names):
        """
        Insert multiple features into the Features object
        
        params:
            feature_arrays: list[list[float]] | 2D array of feature data
             feature_names: list[string]      | list of feature names
        """
        for i, feature_name in enumerate(feature_names):
            self.insert_feature(feature_name, feature_arrays[i])
    
    
    def delete_feature(self, feature_name):
        """
        Remove feature column from Features object
        
        params:
            feature_name: string | feature to delete
        """
        deleted_feature = self._df.pop(feature_name)
        self._feature_names.pop(feature_name)
    
    
    def delete_features(self, feature_names):
        """
        Remove set of given features from Features object
        
        params:
            feature_names: list[string] | features to delete
        """
        for feature_name in feature_names:
            self.delete_feature(feature_name)
    
    
    def has_feature(self, feature_name):
        """
        return: bool | has feature or not
        
        params:
            feature_name: string | feature to check for
        """
        return feature_name in self.feature_names()
    
    
    def has_features(self, feature_names):
        """
        return: bool | has all features or not
        
        params:
            feature_names: list[string] | features to check for
        """
        return all(f in self.feature_names() for f in feature_names)
    
    
    def rename_feature(self, current_name, new_name):
        """
        Rename feature; current_name ---> new_name
        
        params:
           current_name: string | name of feature to be renamed
               new_name: string | name to be given to feature
        """
        self._df.rename(columns={current_name:new_name}, inplace=True)
        
        self._feature_names.remove(current_name)
        self._feature_names.append(new_name)
    
    
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
        
        self._df[feature_name] = (feature - mean) / span
    
    
    def scale_features(self, feature_names=['all']):
        """
        Scale given list of features
        
        params:
            feature_names: list[string] | list of feature names
                                        | default=['all'] (i.e. 
                                        | scale all features)
        """
        if feature_names == ['all'] and 'all' not in self.feature_names(): 
            feature_names = self.feature_names()
        
        for feature_name in feature_names:
            self.scale_feature(feature_name)
    
    
    def num_classes(self):
        """
        return: int | number of classes in Feature object
        """
        return len(self._class_names)
    
    
    def class_names(self):
        """
        return: list[string] or string (if only one class)
        """
        return self._class_names
    
    
    def get_class(self, class_name, as_values=False):
        """
        Uses get_feature() method to retrieve class data
        
        return: pandas Series | class data with name
                -- OR (depending on as_values flag) --
                np.array      | 1D array of class data
        
        params:
            class_name: string | class to get
             as_values: bool   | return as np.array or not
        """
        return self.get_feature(class_name, as_values=as_values)
    
    
    def get_classes(self, class_names, as_values=False):
        """
        Uses get_features() method to retrieve class data
        
        return: pandas DataFrame | class data with names
                -- OR (depending on as_values flag) --
                np.array         | 2D array of classes data
        
        params:
            class_names: list[string] | list of classes to get
              as_values: bool         | return as np.array or not
        """
        return self.get_features(class_names, as_values=as_values)
    
    
    def insert_class(self, class_array, class_name):
        """
        Insert a class into Features object
        
        params:
            class_array: list[float] | class data
             class_name: string      | class name
        """
        self._df[class_name] = class_array
        self._class_names.append(class_name)
    
    
    def insert_classes(self, class_arrays, class_name):
        """
        Insert multiple classes into the Features object
        
        params:
            class_arrays: list[list[float]] | 2D array of class data
             class_names: list[string]      | list of class names
        """
        for i, class_name in enumerate(class_names):
            self.insert_class(class_name, class_arrays[i])
    
    
    def delete_class(self, class_name):
        """
        Remove class column from Features object
        
        params:
            class_name: string | class to delete
        """
        deleted_class = self._df.pop(class_name)
        self._class_names.pop(class_name)
    
    
    def delete_classes(self, class_names):
        """
        Remove set of given classes from Features object
        
        params:
            class_names: list[string] | class to delete
        """
        for class_name in class_names:
            self.delete_class(class_name)
    
    
    def has_class(self, class_name):
        """
        return: bool | has class or not
        
        params:
            class_name: string | class to check for
        """
        return class_name in self.class_names()
    
    
    def has_classes(self, class_names):
        """
        return: bool | has all classes or not
        
        params:
            class_names: list[string] | classes to check for
        """
        return all(c in self.class_names() for c in class_names) 
    
    
    def rename_class(self, current_name, new_name):
        """
        Rename class; current_name ---> new_name
        
        params:
           current_name: string | name of class to be renamed
               new_name: string | name to be given to class
        """
        self._df.rename(columns={current_name:new_name}, inplace=True)
        
        self._class_names.remove(current_name)
        self._class_names.append(new_name)
    
    
    def append(self, row):
        """
        Append a new row to the Features object
        
        NOTE: row data must contain values for all current feature/class 
        
        params:
            row: dict[string:dtype] | dictionary of feature names and data
        """
        assert sorted(row.keys()) == sorted(self.feature_names()+self.class_names()), 'Missing key(s) for append'
        
        single_row = pd.DataFrame(index=range(1))
        for key, value in row.items():
            single_row[key] = [value]
        
        self._df = self._df.append(single_row, ignore_index=True)
    
    
    def split_data(self, train_perc=0.7, cv_perc=0.0, test_perc=0.3, as_values=False, random=True):
        """
        return: train_data, cv_data, test_data | as pandas DataFrames and Series
                -- OR (depending on the as_values flag) --
                train_data, cv_data, test_data | as np.arrays (2D and/or 1D)
        params:
           train_perc: float | percentage of data for training set (default=0.7)
              cv_perc: float | percentage of data for cross validation set (default=0.0)
            test_perc: float | percentage of data for test set (default=0.3)
                               ---> (trainPerc + cvPerc + testPerc must equal 1.0)
            as_values: bool  | return as np.array or not
               random: bool  | random shuffling for train/test/cv data or not
        """
        assert train_perc + cv_perc + test_perc == 1.0, 'train_perc + cv_perc + test_perc != 1.0'
        
        N = self.num_examples()
        
        indices = range(N)
        if random:
            shuffle(indices)
        
        train_length = int(N*train_perc)
        cv_length    = int(N*cv_perc)
        test_length  = int(N*test_perc)
        
        train_data = self._df.ix[ indices[:train_length] ]
        cv_data    = self._df.ix[ indices[train_length:train_length+cv_length] ]
        test_data  = self._df.ix[ indices[-test_length:] ]
        
        if as_values:
            return train_data.values, cv_data.values, test_data.values
            
        return train_data, cv_data, test_data    
    


def main():
    
    f = Features(index=range(10))
    f.insert_feature(range(10,20), 'the')
    f.insert_feature(range(17,27), 'abc')
    print f
    
    f.append({'the':99,'abc':101})
    print f
    
    


if __name__ == '__main__':
    main()
    
    
    
    #pct_change(periods=X) for increases in GF / GA etc. over time as a feature
    
    #.truncate() for date range selection
    
    # from_records() for MySQL read-in
    
    
    
    
    