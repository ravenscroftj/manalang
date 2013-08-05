"""
This module contains base information on some of the ManaLang core language 
constructs: Tokens, Operations, Variables, Literals

It also defines the base class for ManaLang related exceptions

@author James Ravenscroft
"""


class ManaLangException(Exception):
    pass

#----------------------------------------------------------------------------

class ManaLangTok:
    pass

#----------------------------------------------------------------------------

class ManaParenthesis(ManaLangTok):
    """Class used to represent parenthesis '(' or ')' 
    """

    def __init__(self, val):
        self.value = val

#----------------------------------------------------------------------------

class ManaVariable(ManaLangTok):
    
    def __init__(self, name):
        self.name = name

#----------------------------------------------------------------------------

VALID_OPERATORS = ['+','-','/','*','=','==','+=','-=','*=','/=',
'>=','<=','!=', '>', '<']

class ManaOperation(ManaLangTok):
    
    def __init__(self, opstr):
        self.opp = opstr

        if opstr not in VALID_OPERATORS:
            raise ManaParseException("Invalid operator '%s'" % opstr)

        if opstr == '==' or opstr =='>=' or opstr == '<=' or opstr == '!=':
            self.type = "Comparison"
        else:
            self.type = "Arithmetic"

    def apply(self, op1, op2):
        if self.opp == '+':
            return op1 + op2
        elif self.opp == '-':
            return op1 - op2
        elif self.opp == '*':
            return op1 * op2
        elif self.opp == '/':
            return op1 / op2
        elif self.opp == '==':
            return op1 == op2
        elif self.opp == '>=':
            return op1 >= op2
        elif self.opp == '<=':
            return op1 <= op2
        elif self.opp == '!=':
            return op1 != op2

    def __repr__(self):
        return "<ManaOperation %s '%s'>" % (self.type, self.opp)

#----------------------------------------------------------------------------

class ManaValue(ManaLangTok):
    
    def __init__(self, opstr):
        self.value = float(opstr)

    def __repr__(self):
        return "<ManaValue '%f'>" % self.value 

#----------------------------------------------------------------------------


