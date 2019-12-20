# Problem: 
problem='''
Schrödinger's Boolean

Can a value be both True and False?

Define omnibool so that it returns True for the following:

omnibool == True and omnibool == False
If you enjoyed this kata, be sure to check out my other katas.
'''

# Notes: 
notes='''
Python allows classes to define their own behavior with respect to the build in comparison operators, so it is possible to construct a new type that is defined as equal to everything. 
'''

# Solution: 

class EqualsEverything():
    def __eq__(self,other):
        return True

omnibool = EqualsEverything()

# Example Tests: 

test.describe('Basic Tests')
test.expect(omnibool == True)
test.expect(omnibool == False)
print('<COMPLETEDIN::>')

