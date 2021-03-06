#!/usr/bin/env python
import setuptools
from setuptools import setup, find_packages 

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = [ 
    "pytest",
    "mypy",
    "numpy",
    "coverage",
    "pytest-cov",
    "pillow",
    "regex",
    "scikit-learn",
    "opencv-python",
    "importlib_resources"]

setuptools.setup(
     name='MarchMadness',  
     version='1.5.6',
     scripts=['MarchMadness/MarchMadnessRun.py', 'MarchMadness/Simulate.py', 'MarchMadness/AIWeighting.py', 'MarchMadness/bracket.py'] ,
     install_requires=REQUIRES,
     include_package_data=True,
     package_data={'MarchMadness/Previous': ['*'], 'MarchMadness/Simulations': ['*'], 'MarchMadness/Brackets': ['*']},
     author="Tycho Halpern, Rylee Benes, Luca Rivera",
     author_email="thalper@purdue.edu, rbenes@purdue.edu, river172@purdue.edu",
     description="March Madness bracket simulation 2022",
     license_files = ('LICENSE'),
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/thalper/March-Madness",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
     ],
 )
