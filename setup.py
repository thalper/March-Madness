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
    "opencv-python"]

setuptools.setup(
     name='MarchMadness',  
     version='1.0',
     scripts=['MarchMadness/MarchMadness.py', 'MarchMadness/Simulate.py', 'MarchMadness/AIWeighting.py', 'MarchMadness/bracket.py'] ,
     install_requires=REQUIRES,
     include_package_data=True,
     package_data={'MarchMadness/Previous': ['*'], 'MarchMadness/Simulations': ['*'], 'MarchMadness/Brackets': ['*']},
     author="Tycho Halpern, Rylee Benes, Luca Rivera",
     author_email="thalper@purdue.edu, rbenes@purdue.edu, river172@purdue.edu",
     description="March Madness bracket simulation 2022",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/thalper/March-Madness",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
     ],
 )
