# Problem: 
problem='''
Regular expression for binary numbers divisible by 5

Define a regular expression which tests if a given string representing a binary number is divisible by 5.

Examples:
# 5 divisible by 5
PATTERN.match('101') == true

# 135 divisible by 5
PATTERN.match('10000111') == true

# 666 not divisible by 5
PATTERN.match('0000001010011010') == false
Note:
This can be solved by creating a Finite State Machine that evaluates if a string representing a number in binary base is divisible by given number.

The detailed explanation for dividing by 3 is here <http://math.stackexchange.com/questions/140283/why-does-this-fsm-accept-binary-numbers-divisible-by-three>

The FSM diagram for dividing by 5 is here <http://aswitalski.github.io/img/FSM-binary-divisible-by-five.png>

'''

# Notes: 
notes='''
See the notes about problem 1_kyu_Regular_Expression_for_Binary_Numbers_Divisible_by_n for more information
'''

# Solution: 

PATTERN = r'^(0|1(10|(0|11)(01*01)*01*00)*(0|11)(01*01)*1)+$'

# Sample Tests: 

Test.describe("Sample tests")

tests = [(False, "" ),
         (False, "abc"),
         (True,  "000"),
         (True,  "101"),
         (True,  "1010"),
         (True,  "10100"),
         (True,  "{:b}".format(65020)),
         (True,  "{:b}".format(6039865)),
         
         (False, "10110101"),
         (False, "1110001"),
         
         (False,  "{:b}".format(21)),
         (False,  "{:b}".format(15392)),
         (False,  "{:b}".format(23573)),
         (False,  "{:b}".format(19344)),
         
         (False,  "{:b}".format(43936)),
         (False,  "{:b}".format(32977)),
         (False,  "{:b}".format(328)),
         (False,  "{:b}".format(5729)),
        ]

for exp,s in tests:
    test.assert_equals(bool(re.match(PATTERN, s)), exp, "Should work with '{}'".format(s))
