#!/usr/bin/env python
"""
features_test.py
Author: Brian Boates
"""
import numpy as np
from features import Features

def test_num_examples(f, num_examples):
    passed = 'passed: Features.num_exmaples()'
    failed = 'failed: Features.num_examples()'
    try:
        if f.num_examples() == num_examples: print passed
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


def main():
    
    # build a random feature object
    num_examples  = 11
    feature_names = ['a','b','c','d','e','f']
    class_names   = ['x','y','z']
    all_names     = feature_names + class_names
    num_features  = len(feature_names)
    num_classes   = len(class_names)
    num_all       = len(all_names)    
    data  = np.transpose([np.random.rand(num_examples) for i in xrange(num_features+num_classes)])
    
    f = Features(feature_names=feature_names, class_names=class_names, data=data, columns=all_names)
    
    # perform all method tests
    test_num_examples(f, num_examples)
    test_num_features(f, num_features)
    test_num_classes(f, num_classes)
    

    


if __name__ == '__main__':
    main()