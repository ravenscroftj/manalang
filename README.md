# MANALANG MetaLanguage

MANALANG is a language for parsing tabletop game and MUD dice roll
expressions. The language can also evaluate basic maths operations and uses
the BDMAS (no order/power operations supported currently) evaluation order.

You can use MANALANG in the following way

    from manalang.parser import ManaLangParser

    p = ManaLangParser()
    expr = p.evaluate("2d8 + 6")
    print expr.evaluate({}) #should give you a random value between 6 and 24

MANALANG is a work-in-progress and I'm about to implement some new stuff so
watch this space.

MANALANG is distributed under the MIT license.
