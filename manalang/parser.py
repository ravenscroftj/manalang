"""
This module contains ManaLang parsing utilities

@author James Ravenscroft
"""

import re
import logging

from manalang import *
from manalang.dice import DiceRollExpression


#----------------------------------------------------------------------------

class ManaParseException(ManaLangException):
    pass

#----------------------------------------------------------------------------

class ManaLangExpression:

    def __init__(self, tokens):
        self.toks = tokens
        self.logger = logging.getLogger(__name__ + ":evaluator")

    def evaluate(self, context):
        """Evaluate a ManaLang expression and return the result
        
        ManaLang does BODMAS but we don't support 'order' operations
        and we do comparison operations last, so the rule
        is actually more like BDMASC where C=Comparisons
        
        """
        return self._reval(self.toks, context)[0]
        
    
    def _reval(self, toklist, context={}):
        """Recursively evaluate the ManaLang expression"""

        #if toklist is 1 long, it must just be a value
        if len(toklist) == 1:
            return toklist[0].value

        #detect any subexpressions (using brackets)
        toklist = self._subexpr(toklist)

        #evaluate subexpressions and dicerolls first
        for i, tok in enumerate(toklist):
            
            if isinstance(tok, ManaLangExpression):
                toklist[i] = tok.evaluate(context)

            if isinstance(tok, DiceRollExpression):
                
                self.logger.info("Evaluating dice roll %s", tok)
                rolls = tok.value()
                self.logger.info("Got %s from dice roll(s)", rolls)
                toklist[i] = ManaValue(sum(rolls))

        #get all operations
        opps = [ x for x in toklist if isinstance(x, ManaOperation) ]

        #sort all operations
        def oppsort(x):
            if x.opp == '/': return 0
            if x.opp == '*': return 1
            if x.opp == '+': return 2
            if x.opp == '-': return 3

        #apply all operations
        for opp in sorted(opps, key=oppsort):
            
            i = toklist.index(opp)

            tok = toklist[i]

            if i < 1:
                raise ManaLangException("Invalid syntax: cannot start expression with operator: %s" % tok)

            #now apply the operation
            val = tok.apply( toklist[i-1].value, toklist[i+1].value )

            toklist[i] = ManaValue(val)


            #strip away the old operating values
            toklist = [toklist[j] for j in range(0,len(toklist)) 
                        if j not in (i-1,i+1)]

        #return our result to the caller
        return toklist
                    
                

    def _subexpr(self, toklist):
        """This method is used to find subexpressions
        """

        pstack = []
        subs = []
        substart = -1

        #find all parentheses in the toklist
        for i,tok in enumerate(toklist):
            if isinstance(tok, ManaParenthesis):
                if tok.value == '(':
                    pstack.append(tok)

                    if substart < 0:
                        substart = i

                elif tok.value == ')':
                    pstack.pop()

                    if substart > -1 and len(pstack) == 0:
                        #collect the positions and start again 
                        subend = i
                        subs.append( (substart, i) )
                        substart = -1

        #if we got to this point and there is stuff on the stack, error
        if len(pstack) > 0:
            raise ManaLangException("Mismatched parentheses in expression")

        #cut the token list up and turn into subexpressions
        redundant = []
        for start,finish in subs:
            redundant += range( start+1, finish+1)
            toklist[start] = ManaLangExpression( toklist[start+1:finish] )

        #return the new toklist with subexpressions
        return [ toklist[i] for i in range(0,len(toklist)) 
                        if i not in redundant]
        


#----------------------------------------------------------------------------

class ManaLangParser:

    def __init__(self):
        self.logger = logging.getLogger(__name__ + ":parser")

    def parse(self, expr):

        parts = []
        
        for word in expr.split(" "):

            if re.match("[0-9]+d[0-9]+", word):
                parts.append( DiceRollExpression(word)  )
            
            elif re.match("^[A-Z]+$", word):
                parts.append( ManaVariable(word) )

            elif re.match("^[0-9]+(.[0-9])?$", word):
                parts.append( ManaValue(word) )

            elif re.match("^[\+-\/\*]+$",word):
                parts.append( ManaOperation(word) )

            elif word == '(' or word == ')':
                parts.append( ManaParenthesis(word) )
            
            else:
                raise ManaParseException("Invalid token %s" % word)

        return ManaLangExpression(parts)
