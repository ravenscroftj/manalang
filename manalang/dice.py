"""
Simple library for dealing with Dice Roll expressions

You can define a dice roll expression and then get its value like this:
    
d = DiceRollExpression("3d8")

You'll get three random values between 1 and 8 presented in a list. 

E.g [3, 7, 2]

@author James Ravenscroft
"""
import random

from athena.manalang import ManaLangTok, ManaLangException

class DiceRollException(ManaLangException):
    pass

VALID_DICE_TYPES = ['4','6','8','10','12','20','100']

class DiceRollExpression(ManaLangTok):

    def __init__(self, expr=""):
        """Validate a dice roll expression and then store it"""
        try:
            self._parse(expr)
        except Exception as e:
            raise DiceRollException("Invalid dice expression %s" % expr)

    def _parse(self, expr):
        """Given a dice roll expression, parse validate and evaluate"""
        rolls, dtype = expr.split("d")

        assert dtype in VALID_DICE_TYPES

        self.rolls = int(rolls)
        self.dtype = int(dtype)

    def value(self):
        """Evaluate a dice roll expression"""

        return [random.randint(1,self.dtype) for 
            i in range(0,self.rolls)]

    def __str__(self):
        return "%dd%d" % (self.rolls, self.dtype)
        
    def __repr__(self):
        return "<DiceRollExpression '%dd%d'>" % (self.rolls, self.dtype)

