#!/usr/bin/env python
"""
features_test.py
Author: Brian Boates
"""
import numpy as np
from features import Features

def test_column_names(f, column_names):
    passed = 'passed: Features.column_names()'
    failed = 'failed: Features.column_names()'
    try:
        if all(f in column_names for f in f.column_names()) and len(f.column_names()) == len(column_names):
            print passed
        else: print failed
    except:
        print failed 


def test_feature_names(f, feature_names):
    passed = 'passed: Features.feature_names()'
    failed = 'failed: Features.feature_names()'
    try:
        if all(f in feature_names for f in f.feature_names()) and len(f.feature_names()) == len(feature_names):
            print passed
        else: print failed
    except:
        print failed


def test_class_names(f, class_names):
    passed = 'passed: Features.class_names()'
    failed = 'failed: Features.class_names()'
    try:
        if all(f in class_names for f in f.class_names()) and len(f.class_names()) == len(class_names):
            print passed
        else: print failed
    except:
        print failed


def test_num_columns(f, num_columns):
    passed = 'passed: Features.num_columns()'
    failed = 'failed: Features.num_columns()'
    try:
        if f.num_columns() == num_columns: print passed
        else: print failed
    except:
        print failed    


def test_num_features(f, num_features):
    passed = 'passed: Features.num_features()'
    failed = 'failed: Features.num_features()'
    try:
        if f.num_features() == num_features: print passed
        else: print failed
    except:
        print failed


def test_num_classes(f, num_classes):
    passed = 'passed: Features.num_classes()'
    failed = 'failed: Features.num_classes()'
    try:
        if f.num_classes() == num_classes: print passed
        else: print failed
    except:
        print failed


def test_num_examples(f, num_examples):
    passed = 'passed: Features.num_examples()'
    failed = 'failed: Features.num_examples()'
    try:
        if f.num_examples() == num_examples: print passed
        else: print failed
    except:
        print failed


def test_insert_column(f):
    pass

def test_insert_feature(f):
    pass


def main():
    
    # build a random feature object
    num_examples  = 11
    feature_names = ['a','b','c','d','e','f']
    class_names   = ['x','y','z']
    column_names     = feature_names + class_names
    num_features  = len(feature_names)
    num_classes   = len(class_names)
    num_columns   = len(column_names)    
    data  = np.transpose([np.random.rand(num_examples) for i in xrange(num_columns)])
    
    f = Features(feature_names=feature_names, class_names=class_names, data=data, columns=column_names)
    
    # perform all method tests
    test_column_names(f, column_names)
    test_feature_names(f, feature_names)
    test_class_names(f, class_names)
    test_num_columns(f, num_columns)
    test_num_features(f, num_features)
    test_num_classes(f, num_classes)
    test_num_examples(f, num_examples)
    

    


if __name__ == '__main__':
    main()