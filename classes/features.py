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

class Features(object):
    """
    Features object

    fields:
        _df:             pd.DataFrame
        _feature_names:  list[string]
        _class_names:    list[string]

    methods:                                   RETURNS: |
        __init__(feature_names, class_names,            |
                                *args, **kwargs)        | N/A
        __repr__(*args, **kwargs)                       | string
        head(*args, **kwargs)                           | pd.DataFrame.head()
        tail(*args, **kwargs)                           | pd.DataFrame.tail()
        --
        column_names()                                  | list[string]
        feature_names()                                 | list[string]
        class_names()                                   | list[string]
        --
        num_columns()                                   | int
        num_features()                                  | int
        num_classes()                                   | int
        num_examples()                                  | int
        --
       _insert_column(column_array, column_name)        | N/A
        insert_feature(feature_array, feature_name)     | N/A
        insert_features(feature_arrays, feature_names)  | N/A
        insert_class(class_array, class_name)           | N/A
        insert_classes(class_arrays, class_names)       | N/A
        --
       _delete_column(column_name)                      | N/A
        delete_feature(feature_name)                    | N/A
        delete_features(feature_names)                  | N/A
        delete_class(class_name)                        | N/A
        delete_classes(class_names)                     | N/A
        --
        has_feature(feature_name)                       | bool
        has_features(feature_names)                     | bool
        has_class(class_name)                           | bool
        has_classes(class_names)                        | bool
        --
       _get(column_names, as_values)                    | pd.Series/DataFrame or np.array[dtype]
        get_all(as_values)                              | pd.Series/DataFrame or np.array[dtype]
        get_feature(feature_name, as_values)            | pd.Series or np.array[dtype]
        get_features(feature_names, as_values)          | pd.DataFrame or np.array[dtype]
        get_class(class_name, as_values)                | pd.Series or np.array[dtype]
        get_classes(class_names, as_values)             | pd.DataFrame or np.array[dtype]
        --
       _rename_column(current_name, new_name)           | N/A
        rename_feature(current_name, new_name)          | N/A
        rename_class(current_name, new_name)            | N/A
        --
        scale_feature(feature_name)                     | N/A
        scale_features(feature_names)                   | N/A
        --
        append(row)                                     | N/A
        split_data(train_perc, cv_perc, test_perc,      |
                               as_values, randomize)    | pd.DataFrame*3 or np.array[dtype]*3
    """
    def __init__(self, feature_names=[], class_names=[], *args, **kwargs):
        """
        Initialize Features object

        Note: If data/headers are given in initialization, they will
              all be assumed to be features and NOT classes

        params:
            *args, **kwargs: arguments for pd.DataFrame.__init__()
        """
#        super(Features, self).__init__(*args, **kwargs)
        #### NEED CHECK FOR feature_names + class_names and columns consistency ####
        self._feature_names = feature_names
        self._class_names   = class_names
        self._df = pd.DataFrame(*args, **kwargs)

    def __repr__(self):
        """
        Use the pd.DataFrame.__repr__()
        """
        return self._df.__repr__()

    def head(self, *args, **kwargs):
        """
        Wrapper for pd.DataFrame.head()
        """
        return self._df.head(*args, **kwargs)

    def tail(self, *args, **kwargs):
        """
        Wrapper for pd.DataFrame.tail()
        """
        return self._df.tail(*args, **kwargs)

    def column_names(self):
        """
        return: list[string] | list of all feature and class names
        """
        return self._feature_names + self._class_names

    def feature_names(self):
        """
        return: list[string] | list of feature names
        """
        return self._feature_names

    def class_names(self):
        """
        return: list[string] or string (if only one class)
        """
        return self._class_names

    def num_columns(self):
        """
        return int | number of features and classes in total
        """
        return len(self.column_names())

    def num_features(self):
        """
        return: int | number of features
        """
        return len(self.feature_names())

    def num_classes(self):
        """
        return: int | number of classes
        """
        return len(self.class_names())

    def num_examples(self):
        """
        return: int | number of examples
        """
        return len(self._df)

    def _insert_column(self, column_array, column_name):
        """
        Insert a column

        params:
            column_array: list[float] | data to insert
             column_name: string      | name of column to insert
        """
        assert_msg = column_name+' already exists - cannot insert'
        assert column_name not in self.column_names(), assert_msg

        self._df[column_name] = column_array

    def insert_feature(self, feature_array, feature_name):
        """
        Insert a feature

        params:
            feature_array: list[float] | feature data
             feature_name: string      | feature name
        """
        self._insert_column(feature_array, feature_name)
        self._feature_names.append(feature_name)

    def insert_features(self, feature_arrays, feature_names):
        """
        Insert multiple features at once

        params:
            feature_arrays: list[list[float]] | 2D array of feature data
             feature_names: list[string]      | list of feature names
        """
        for i, feature_name in enumerate(feature_names):
            self.insert_feature(feature_arrays[i], feature_name)

    def insert_class(self, class_array, class_name):
        """
        Insert a class

        params:
            class_array: list[float] | class data
             class_name: string      | class name
        """
        self._insert_column(class_array, class_name)
        self._class_names.append(class_name)

    def insert_classes(self, class_arrays, class_names):
        """
        Insert multiple classes at once

        params:
            class_arrays: list[list[float]] | 2D array of class data
             class_names: list[string]      | list of class names
        """
        for i, class_name in enumerate(class_names):
            self.insert_class(class_arrays[i], class_name)

    def _delete_column(self, column_name):
        """
        Remove column

        params:
            column_name: string | name of column to delete
        """
        assert_msg = column_name+' not present - cannot delete'
        assert column_name in self.column_names(), assert_msg

        self._df.pop(column_name)

    def delete_feature(self, feature_name):
        """
        Remove feature column from Features object

        params:
            feature_name: string | feature to delete
        """
        self._delete_column(feature_name)
        self._feature_names.pop(feature_name)

    def delete_features(self, feature_names):
        """
        Remove set of given features

        params:
            feature_names: list[string] | features to delete
        """
        for feature_name in feature_names:
            self.delete_feature(feature_name)

    def delete_class(self, class_name):
        """
        Remove class column

        params:
            class_name: string | class to delete
        """
        self._delete_column(class_name)
        self._class_names.pop(class_name)

    def delete_classes(self, class_names):
        """
        Remove set of given classes

        params:
            class_names: list[string] | class to delete
        """
        for class_name in class_names:
            self.delete_class(class_name)

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

    def _get(self, column_names, as_values=False):
        """
        return: pandas Series | column data with name
                -- OR (depending on as_values flag) --
                np.array      | 1D array of column data

        params:
           column_names: string       | column to get
                         -- OR --
                         list[string] | columns to get
              as_values: bool         | return as np.array or not
        """
        if as_values:
            return self._df.get(column_names).values
        else:
            return self._df.get(column_names)

    def get_all(self, as_values=False):
        """
        return: pd.DataFrame | contains all features and classes
                -- OR (depending on as_values flag) --
                np.array     | contains all features and classes data

        params:
            as_values: bool | whether to return as np.array or not
        """
        return self._get(self.column_names(), as_values)

    def get_feature(self, feature_name, as_values=False):
        """
        Uses _get() method to retrieve feature data

        return: pandas Series | feature data with name
                -- OR (depending on as_values flag) --
                np.array      | 1D array of feature data

        params:
           feature_name: string | feature to get
              as_values: bool   | return as np.array or not
        """
        assert_msg = feature_name+' not in self.feature_names() - cannot get'
        assert self.has_feature(feature_name), assert_msg

        return self._get(feature_name, as_values)

    def get_features(self, feature_names=['all'], as_values=False):
        """
        Uses _get() method to retrieve features data

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

        assert_msg = 'one or more features not in self.feature_names() - cannot get'
        assert self.has_features(feature_names), assert_msg

        return self._get(feature_names, as_values)

    def get_class(self, class_name, as_values=False):
        """
        Uses _get() method to retrieve class data

        return: pandas Series | class data with name
                -- OR (depending on as_values flag) --
                np.array      | 1D array of class data

        params:
            class_name: string | class to get
             as_values: bool   | return as np.array or not
        """
        assert_msg = class_name+' not in self.class_names() - cannot get'
        assert self.has_class(class_name), assert_msg

        return self._get(class_name, as_values)

    def get_classes(self, class_names=['all'], as_values=False):
        """
        Uses _get() method to retrieve classes data

        return: pandas DataFrame | class data with names
                -- OR (depending on as_values flag) --
                np.array         | 2D array of classes data

        params:
            class_names: list[string] | list of classes to get
              as_values: bool         | return as np.array or not
        """
        if class_names == ['all'] and 'all' not in self.class_names():
            class_names = self.class_names()

        assert_msg = 'one or more classes not in self.class_names() - cannot get'
        assert self.has_classes(class_names), assert_msg

        return self._get(class_names, as_values)

    def _rename_column(self, current_name, new_name):
        """
        Rename column; current name ---> new_name
        """
        self._df.rename(columns={current_name:new_name}, inplace=True)

    def rename_feature(self, current_name, new_name):
        """
        Rename feature; current_name ---> new_name

        params:
           current_name: string | name of feature to be renamed
               new_name: string | name to be given to feature
        """
        assert_msg = current_name+' not in self.feature_names() - cannot rename'
        assert self.has_feature(current_name), assert_msg

        self._rename_column(current_name, new_name)

        self._feature_names.remove(current_name)
        self._feature_names.append(new_name)

    def rename_class(self, current_name, new_name):
        """
        Rename class; current_name ---> new_name

        params:
           current_name: string | name of class to be renamed
               new_name: string | name to be given to class
        """
        assert_msg = current_name+' not in self.class_names() - cannot rename'
        assert self.has_class(current_name), assert_msg

        self._rename_column(current_name, new_name)

        self._class_names.remove(current_name)
        self._class_names.append(new_name)

    def scale_feature(self, feature_name):
        """
        Scale the feature given by feature_name
        Note: this changes the feature in self explicitly

        params:
            feature_name: string | name of feature to be scaled
        """
        assert_msg = feature_name+' not in self.feature_names() - cannot scale'
        assert self.has_feature(feature_name), assert_msg

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

        assert_msg = 'one or more features not in self.feature_names() - cannot scale'
        assert self.has_features(feature_names), assert_msg

        for feature_name in feature_names:
            self.scale_feature(feature_name)

    def append(self, row):
        """
        Append a new row to the self._df DataFrame
          ---> NaN's inserted for absent feature/class names

        params:
            row: dict[string:dtype] | dictionary of feature/class names and data
        """
        self._df = self._df.append(row, ignore_index=True)

    def get_rows(self, idx, as_values=False):
        """
        return: pd.DataFrame | 1-row DataFrame for idx
                -- OR --
                np.array | 1D array of row data
        params:
                idx: int       | row index
                     -- OR --
                     list[int] | list of row indices
          as_values: bool | return as np.array or not
        """
        if as_values:
            return self._df.iloc[idx].values
        else:
            return self._df.iloc[idx]

    def get_row(self, idx, as_values=False):
        """
        Calls get_rows()
        """
        return get_rows(idx=idx, as_values=as_values)

    def get_slice(self, begin=None, end=None, stride=None, as_values=False):
        """
        return: pd.DataFrame | rows sliced from _df

        params:
              begin: int  | begin index for slice
                end: int  | end index for slice
             stride: int  | stride for slice
          as_values: bool | return as np.array or not
        """
        if begin:
            if end:
                if stride:
                    result = self._df.iloc[begin:end:stride]
                else:
                    result = self._df.iloc[begin:end]
            else:
                if stride:
                    result = self._df.iloc[begin::stride]
                else:
                    result = self._df.iloc[begin:]

        elif end:
            if stride:
                result = self._df.iloc[:end:stride]
            else:
                result = self._df.iloc[:end]

        if as_values:
            return result.values
        else:
            return result





        if begin and end and stride:
            result = self._df.iloc[begin:end:stride]
        elif begin and end and not stride:
            result = self._df.iloc[begin:end]
        elif begin and not end and stride:


        else:
            if end:
                result = self._df.iloc[:end:stride]
            else:
                result = self._df.iloc[::stride]

        if as_values:
            return self._df.iloc[begin:end:stride].values
        else:
            return self._df.iloc[begin:end:stride]

    def split_data(self, frac=0.70, as_values=False, randomize=True):
        """
        return: pd.DataFrame, pd.DataFrame
                -- OR (depending on the as_values flag) --
                np.array, np.array
        params:
           frac: float | fraction of data for first segment (between 0-1),
                       | second segment will thus be (1-frac)
            as_values: bool  | return as np.array or not
            randomize: bool  | random shuffling for train/test/cv data or not
        """
        N = self.num_examples()

        indices = range(N)
        if randomize:
            shuffle(indices)

        first_data  = self.get_rows(indices[:int(N*frac)])
        second_data = self.get_rows(indices[int(N*frac):])

        if as_values:
            return first_data.values, second_data.values

        return first_data, second_data



def main():

    import time
    t0 = time.time()
    N = int( 1e4 )
#    f = Features(index=range(N))
#    print "init:", time.time() - t0
#    f.insert_feature(range(N), 'a')
#    print "insert 1 feature:", time.time() - t0
#    f.insert_feature(range(N), 'b')
#    f.insert_feature(range(N), 'c')
#    f.insert_feature(range(N), 'd')
#    f.insert_feature(range(N), 'e')
#    f.insert_feature(range(N), 'f')
#    print "insert 5 more features:", time.time() - t0

    f = Features()
    headers = ['a','b','c','d','e','f']
    f.insert_features([[]]*len(headers), headers)
    for i in xrange(N):
        f = f.append_row({'a':1,'b':1,'c':1,'d':1,'e':1,'f':1})
    print "append row:", time.time() - t0

    print '========================================='

    t0 = time.time()
    df = pd.DataFrame(columns=headers)
    for i in xrange(N):
        df = df.append({'a':1,'b':1,'c':1,'d':1,'e':1,'f':1}, ignore_index=True)
    print "append:", time.time() - t0






if __name__ == '__main__':
    main()



    #pct_change(periods=X) for increases in GF / GA etc. over time as a feature

    #.truncate() for date range selection

    # from_records() for MySQL read-in ---> pd.io.sql





