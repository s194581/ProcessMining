# coding=utf-8
"""
This module is used to test all functional requirements regarding their fulfillment
"""
import os
import sys
import unittest

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../conformancechecker'))
sys.path.insert(0, path)

if __name__ == '__main__':
    tests = unittest.TestLoader().discover('.', 'test_frq*evaluation.py')
    unittest.TextTestRunner(verbosity=1).run(tests)
