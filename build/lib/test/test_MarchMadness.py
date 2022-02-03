import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import MarchMadness

def test_addition():
  assert MarchMadness.addition(2, 3) == 5
