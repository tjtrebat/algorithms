__author__ = 'Tom'

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "algorithms",
    version = "0.0.1",
    author = "Thomas J. Trebat",
    author_email = "tjtrebat@gmail.com",
    description = ("Implementation of various algorithms."),
    license = "GPLv2",
    keywords = "Algorithms, Heapsort, Quicksort, Breadth-first search, Depth-first search, Minimum-spanning tree, " \
               "Maximum Flow, Dynamic Programming",
    url = "https://github.com/tjtrebat/algorithms.git#egg=algorithms",
    packages=['algorithms'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPLv2 License",
        ],
    test_suite='tests'
)
