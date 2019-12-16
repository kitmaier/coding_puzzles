# Problem: 
problem='''
Regular Expression - Check if divisible by 0b111 (7)

Create a regular expression capable of evaluating binary strings (which consist of only 1's and 0's) and determining whether the given string represents a number divisible by 7.

Note:

Empty strings should be rejected.
Your solution should reject strings with any character other than 0 and 1.
No leading 0's will be tested unless the string exactly denotes 0.
'''

# Notes: 
notes='''
See the notes about problem 1_kyu_Regular_Expression_for_Binary_Numbers_Divisible_by_n for more information
'''

# Solution: 

A = "01*0(11(01)*1)*0"
B = "01*0(11(01)*1)*(10|11(01)*00)(0(01)*00|0(01)*1(11(01)*1)*(10|11(01)*00))*(1|0(01)*1(11(01)*1)*0)"
C = "1(0(01)*00|0(01)*1(11(01)*1)*(10|11(01)*00))*(1|0(01)*1(11(01)*1)*0)"

solution = "^(0|"+C+"("+A+"|"+B+")*1)(0|"+C+"("+A+"|"+B+")*1)*$"

# Sample Tests

test.assert_equals(isinstance(solution,str),True,'your solution is not a string')

import re
from random import random
rgx = re.compile(solution)

test.describe('gentle fixed tests')
test.it('from 0 to 100')
for num in range(0,101):
    print('Testing for: '+str(num))
    test.assert_equals(bool(rgx.match(bin(num)[2:])),num%7 == 0)