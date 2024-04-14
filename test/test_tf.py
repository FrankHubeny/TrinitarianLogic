# Test pf altrea.tf 

from sympy.abc import A, B
from altrea.tf import Proof
goal = A & B
p = Proof(goal)

def test_proofname():
    assert p.name == ''

def test_proofgoal():
    assert p.goal == goal