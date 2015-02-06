__author__ = 'Marnee Dearman'
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5