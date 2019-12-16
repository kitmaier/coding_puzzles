# Problem: 
problem='''
Regular Expression for Binary Numbers Divisible by n
Create a function that will return a regular expression string that is capable of evaluating binary strings (which consist of only 1s and 0s) and determining whether the given string represents a number divisible by n.

Tests
Inputs 1 <= n <= 18 will be tested

Each n will be tested against random invalid tests and random valid tests (which may or may not pass the regex test itself, accordingly).

Notes
Strings that are not binary numbers should be rejected.
Keep your solution under 5000 characters. This means you can't hard-code the answers.
Only these characters may be included in your returned string: 01?:*+^$()[]|
Python Notes
Whenever you use parentheses (...), instead use non-capturing ones (?:...). This is due to module re's restriction in the number of capturing (or named) groups, which is capped at 99.
Each regex will be tested with re.search, so be sure to include both starting and ending marks in your regex.
The second anti-cheat test checks if you used any of re, sys, or print in your code. You won't need to print anything since each test will show what numbers your code is being tested on.
'''

# Notes:
notes='''
Given a finite state machine, a set of states and transitions represented by characters from an alphabet, there is a generic algorithm that will compile it down to a regular expression accepting the same formal language. However, this algorithm is not particularly efficient, so it will help if the finite state machine is as small as possible. 
For any positive N, a finite state machine accepting the binary strings representing numbers divisible by N can be created that has only N states, with one of them being the accepting state. Starting from the most significant bit, iterate along the number, keeping track of what the initial segment of the number would be modulo N. That is, at each step, given the current state S and the next bit D, move to state (2*S+D)%N. For instance, for the string '10101011' with N=3, the sequence of states would be [1,2,2,1,0,0,1,0] and would end in the accepting state 0, showing that the number 171 is divisible by 3. 
There are some additional complications related to whether zero-padding is allowed or forbidden, and whether the empty string is accepted. 
In the case that N is even, the problem can be simplified to a smaller case where N is odd and the regex has some trailing zeros. 
In order to validate the functionality below, it was helpful to build tests that generate a large number of random values and check whether the regex gave the same answer as a modulo operation. 
'''


# DONE: manually create state machine for n=3

n = 3
cyclic_value_chain = [1,2]
    states = {    "0,1":{"accumulated_value":0,"cyclic_value":1,"next_state_if_digit_is_1":"1,2","next_state_if_digit_is_0":"0,2","is_end_state":True},
                "1,1":{"accumulated_value":1,"cyclic_value":1,"next_state_if_digit_is_1":"2,2","next_state_if_digit_is_0":"1,2","is_end_state":False},
                "2,1":{"accumulated_value":2,"cyclic_value":1,"next_state_if_digit_is_1":"0,2","next_state_if_digit_is_0":"2,2","is_end_state":False},
                "0,2":{"accumulated_value":0,"cyclic_value":2,"next_state_if_digit_is_1":"2,1","next_state_if_digit_is_0":"0,1","is_end_state":True},
                "1,2":{"accumulated_value":1,"cyclic_value":2,"next_state_if_digit_is_1":"0,1","next_state_if_digit_is_0":"1,1","is_end_state":False},
                "2,2":{"accumulated_value":2,"cyclic_value":2,"next_state_if_digit_is_1":"1,1","next_state_if_digit_is_0":"2,1","is_end_state":False}}

# DONE: automate testing the state machine

from random import randrange
n = 3
def testStateMachine(intval):
    binval = bin(intval)[2:]
    state = "0,1"
    for k in range(len(binval)-1,-1,-1):
        state = states[state]["next_state_if_digit_is_"+binval[k]]
        #print(k,binval[k],state)
    #print(state,states[state]["is_end_state"])
    return (intval,states[state]["is_end_state"])
def testStateMachineRandom():
    intval = randrange(10000000000000)*n
    intval2 = intval+randrange(n-1)+1
    return (testStateMachine(intval),testStateMachine(intval2))
for index in range(100):
    testStateMachineRandom()

# DONE: manually create regex-transition-based state machine for n=3

# {"current_state":{"next_state":"transition_regex",...}...}
forward_state_transitions = {    "0,1":{"1,2":"1","0,2":"0","Accept":"END"},
                                "1,1":{"2,2":"1","1,2":"0"},
                                "2,1":{"0,2":"1","2,2":"0"},
                                "0,2":{"2,1":"1","0,1":"0","Accept":"END"},
                                "1,2":{"0,1":"1","1,1":"0"},
                                "2,2":{"1,1":"1","2,1":"0"}}
backward_state_transitions = {    "Accept":{"0,1":"END","0,2":"END"},
                                "0,1":{"1,2":"1","0,2":"0"},
                                "1,1":{"2,2":"1","1,2":"0"},
                                "2,1":{"0,2":"1","2,2":"0"},
                                "0,2":{"2,1":"1","0,1":"0"},
                                "1,2":{"0,1":"1","1,1":"0"},
                                "2,2":{"1,1":"1","2,1":"0"}}

# DONE: automate testing regex-transition-based state machine (for case of regex in {"0","1"})

from random import randrange
n = 3
def testStateMachine(intval):
    binval = bin(intval)[2:]
    state = "0,1"
    for k in range(len(binval)-1,-1,-1):
        nextStateFound = False
        for nextState in forward_state_transitions[state]:
            if forward_state_transitions[state][nextState]==binval[k]:
                state = nextState
                nextStateFound = True
                break
        if not nextStateFound:
            return (intval,False)
    return (intval,("Accept" in forward_state_transitions[state]))
def testStateMachineRandom():
    intval = randrange(10000000000000)*n
    intval2 = intval+randrange(n-1)+1
    return (testStateMachine(intval),testStateMachine(intval2))
for index in range(100):
    testStateMachineRandom()

# DONE: automate testing regex-transition-based state machine (for general regex)

from random import randrange
import re
n = 3
matcher = None
def testStateMachine(intval):
    binval = bin(intval)[2:][::-1]+"END"
    #state = "0,1"
    state = 'x0'
    while len(binval)>0:
        matcher = None
        for nextState in forward_state_transitions[state]:
            matcher = re.match("^"+forward_state_transitions[state][nextState],binval)
            if(matcher):
                state = nextState
                binval = binval[matcher.span()[1]:]
                break
        if not matcher:
            return (intval,False)
    return (intval,True)
def testStateMachineRandom():
    intval = randrange(10000000000000)*n
    intval2 = intval+randrange(n-1)+1
    return (testStateMachine(intval),testStateMachine(intval2))
for index in range(100):
    testStateMachineRandom()

# DONE: automate compiling the regex-transition-based state machine into a regex

# for each state S that is not accepting
#     for each pair (state A transitioning to S by regex P, state B transitioning from S by regex R)
#         with S transitioning to itself by regex Q
#         add regex "P(Q)*R" as alternative transition from A to B (if P/Q/R is empty, drop it from the regex)
# for each accepting state that is not the starting state
#     do the same as the non-accepting states, but pay close attention to how the "Accept" state is handled, and its regex "END"
# final print-out from starting state (with reversal)
#     the same as non-accepting states, but A and P are empty, B = "Accept", and R = "END"

forward_state_transitions = {   "0,1":{"1,2":"1","0,2":"0","Accept":"END"},
                                "1,1":{"2,2":"1","1,2":"0"},
                                "2,1":{"0,2":"1","2,2":"0"},
                                "0,2":{"2,1":"1","0,1":"0","Accept":"END"},
                                "1,2":{"0,1":"1","1,1":"0"},
                                "2,2":{"1,1":"1","2,1":"0"}}
backward_state_transitions = {  "Accept":{"0,1":"END","0,2":"END"},
                                "0,1":{"1,2":"1","0,2":"0"},
                                "1,1":{"2,2":"1","1,2":"0"},
                                "2,1":{"0,2":"1","2,2":"0"},
                                "0,2":{"2,1":"1","0,1":"0"},
                                "1,2":{"0,1":"1","1,1":"0"},
                                "2,2":{"1,1":"1","2,1":"0"}}
Blist = list(forward_state_transitions.keys())
Blist.remove('0,1')
for B in Blist:
    Q = forward_state_transitions[B][B] if B in forward_state_transitions[B] else None
    # A -> B -> C
    # P    Q*   R
    # A-P->B(<>Q)-R->C
    for A in list(backward_state_transitions[B].keys()):
        print(A)
        if A == B:
            continue
        P = backward_state_transitions[B][A]
        for C in list(forward_state_transitions[B].keys()):
            if C == B:
                continue
            R = forward_state_transitions[B][C]
            regex = P + ("("+Q+")*" if Q is not None else "") + R
            #print(A,B,C,P,Q,R,regex)
            drop = forward_state_transitions[A].pop(B,None)
            forward_state_transitions[A][C] = regex if C not in forward_state_transitions[A] else "("+forward_state_transitions[A][C]+"|"+regex+")"
            drop = backward_state_transitions[C].pop(B,None)
            backward_state_transitions[C][A] = regex if A not in backward_state_transitions[C] else "("+backward_state_transitions[C][A]+"|"+regex+")"
    drop = forward_state_transitions.pop(B,None)
    drop = backward_state_transitions.pop(B,None)
#final_regex = "("+forward_state_transitions['0,1']['0,1']+")*"+forward_state_transitions['0,1']['Accept']
final_regex = "("+forward_state_transitions['x0']['x0']+")*"+forward_state_transitions['x0']['Accept']
final_regex = final_regex.replace("(","(?:").replace("END","")
final_regex = "^"+final_regex+"$"

# DONE: automate testing the regex

n = 3
def testRegex(intval):
    #binval = bin(intval)[2:]
    binval = bin(intval)[2:][::-1]
    matcher = re.match(final_regex,binval)
    return (intval,bool(matcher))
def testRegexRandom():
    intval = randrange(10000000000000)*n
    intval2 = intval+randrange(n-1)+1
    return (testRegex(intval),testRegex(intval2))
for index in range(100):
    testRegexRandom()

# DONE: automate creating regex-transition-based state machine for value n

# if n==1 then accept all inputs
# if n%2==0 then add a 0 to the end and use regex for n/2 (recursively)
# otherwise, n%2==1 (n is odd) and n>=3

n = 3
cyclic_value_chain = [1] # powers of 2 mod n
value = 2
while value != 1:
    cyclic_value_chain.append(value)
    value = (value*2)%n
cyclic_value_chain.append(1)
forward_state_transitions = {}
backward_state_transitions = {"Accept":{}}
for k in range(len(cyclic_value_chain)-1):
    value = cyclic_value_chain[k]
    next_value = cyclic_value_chain[k+1]
    for accumulated_value in range(n):
        current_state = str(accumulated_value)+","+str(value)
        state_after_0 = str(accumulated_value)+","+str(next_value)
        state_after_1 = str((accumulated_value+value)%n)+","+str(next_value)
        forward_state_transitions[current_state] = {}
        forward_state_transitions[current_state][state_after_0] = "0"
        forward_state_transitions[current_state][state_after_1] = "1"
        if accumulated_value==0:
            forward_state_transitions[current_state]["Accept"] = "END"
        if state_after_0 not in backward_state_transitions:
            backward_state_transitions[state_after_0] = {}
        if state_after_1 not in backward_state_transitions:
            backward_state_transitions[state_after_1] = {}
        backward_state_transitions[state_after_0][current_state] = "0"
        backward_state_transitions[state_after_1][current_state] = "1"
        if accumulated_value==0:
            backward_state_transitions["Accept"][current_state] = "END"

# n = 5
forward_state_transitions = {'0,1': {'0,2': '0', '1,2': '1', 'Accept': 'END'}, '1,1': {'1,2': '0', '2,2': '1'}, '2,1': {'2,2': '0', '3,2': '1'}, '3,1': {'3,2': '0', '4,2': '1'}, '4,1': {'4,2': '0', '0,2': '1'}, '0,2': {'0,4': '0', '2,4': '1', 'Accept': 'END'}, '1,2': {'1,4': '0', '3,4': '1'}, '2,2': {'2,4': '0', '4,4': '1'}, '3,2': {'3,4': '0', '0,4': '1'}, '4,2': {'4,4': '0', '1,4': '1'}, '0,4': {'0,3': '0', '4,3': '1', 'Accept': 'END'}, '1,4': {'1,3': '0', '0,3': '1'}, '2,4': {'2,3': '0', '1,3': '1'}, '3,4': {'3,3': '0', '2,3': '1'}, '4,4': {'4,3': '0', '3,3': '1'}, '0,3': {'0,1': '0', '3,1': '1', 'Accept': 'END'}, '1,3': {'1,1': '0', '4,1': '1'}, '2,3': {'2,1': '0', '0,1': '1'}, '3,3': {'3,1': '0', '1,1': '1'}, '4,3': {'4,1': '0', '2,1': '1'}}
backward_state_transitions = {'Accept': {'0,1': 'END', '0,2': 'END', '0,4': 'END', '0,3': 'END'}, '0,2': {'0,1': '0', '4,1': '1'}, '1,2': {'0,1': '1', '1,1': '0'}, '2,2': {'1,1': '1', '2,1': '0'}, '3,2': {'2,1': '1', '3,1': '0'}, '4,2': {'3,1': '1', '4,1': '0'}, '0,4': {'0,2': '0', '3,2': '1'}, '2,4': {'0,2': '1', '2,2': '0'}, '1,4': {'1,2': '0', '4,2': '1'}, '3,4': {'1,2': '1', '3,2': '0'}, '4,4': {'2,2': '1', '4,2': '0'}, '0,3': {'0,4': '0', '1,4': '1'}, '4,3': {'0,4': '1', '4,4': '0'}, '1,3': {'1,4': '0', '2,4': '1'}, '2,3': {'2,4': '0', '3,4': '1'}, '3,3': {'3,4': '0', '4,4': '1'}, '0,1': {'0,3': '0', '2,3': '1'}, '3,1': {'0,3': '1', '3,3': '0'}, '1,1': {'1,3': '0', '3,3': '1'}, '4,1': {'1,3': '1', '4,3': '0'}, '2,1': {'2,3': '0', '4,3': '1'}}



# DONE: automate creating minimized regex-transition-based state machine for value n

# if n==1 then accept all inputs
# if n%2==0 then add a 0 to the end and use regex for n/2 (recursively)
# otherwise, n%2==1 (n is odd) and n>=3

n = 3
half = 0
for k in range(n):
    if (k*2)%n==1:
        half = k
forward_state_transitions = {}
backward_state_transitions = {"Accept":{}}
for k in range(n):
    current_state = "x"+str(k)
    state_after_0 = "x"+str((half*k)%n)
    state_after_1 = "x"+str((half*(k+1))%n)
    forward_state_transitions[current_state] = {}
    forward_state_transitions[current_state][state_after_0] = "0"
    forward_state_transitions[current_state][state_after_1] = "1"
    if k==0:
        forward_state_transitions[current_state]["Accept"] = "END"
    if state_after_0 not in backward_state_transitions:
        backward_state_transitions[state_after_0] = {}
    if state_after_1 not in backward_state_transitions:
        backward_state_transitions[state_after_1] = {}
    backward_state_transitions[state_after_0][current_state] = "0"
    backward_state_transitions[state_after_1][current_state] = "1"
    if k==0:
        backward_state_transitions["Accept"][current_state] = "END"

# n = 3
forward_state_transitions = {'x0': {'x0': '0', 'x2': '1', 'Accept': 'END'}, 'x1': {'x2': '0', 'x1': '1'}, 'x2': {'x1': '0', 'x0': '1'}}
# n = 13
forward_state_transitions = {'x0': {'x0': '0', 'x7': '1', 'Accept': 'END'}, 'x1': {'x7': '0', 'x1': '1'}, 'x2': {'x1': '0', 'x8': '1'}, 'x3': {'x8': '0', 'x2': '1'}, 'x4': {'x2': '0', 'x9': '1'}, 'x5': {'x9': '0', 'x3': '1'}, 'x6': {'x3': '0', 'x10': '1'}, 'x7': {'x10': '0', 'x4': '1'}, 'x8': {'x4': '0', 'x11': '1'}, 'x9': {'x11': '0', 'x5': '1'}, 'x10': {'x5': '0', 'x12': '1'}, 'x11': {'x12': '0', 'x6': '1'}, 'x12': {'x6': '0', 'x0': '1'}}
backward_state_transitions = {'Accept': {'x0': 'END'}, 'x0': {'x0': '0', 'x12': '1'}, 'x7': {'x0': '1', 'x1': '0'}, 'x1': {'x1': '1', 'x2': '0'}, 'x8': {'x2': '1', 'x3': '0'}, 'x2': {'x3': '1', 'x4': '0'}, 'x9': {'x4': '1', 'x5': '0'}, 'x3': {'x5': '1', 'x6': '0'}, 'x10': {'x6': '1', 'x7': '0'}, 'x4': {'x7': '1', 'x8': '0'}, 'x11': {'x8': '1', 'x9': '0'}, 'x5': {'x9': '1', 'x10': '0'}, 'x12': {'x10': '1', 'x11': '0'}, 'x6': {'x11': '1', 'x12': '0'}}



# TODO: automate creating the state machine for value n
# TODO: consider edge cases such as the empty string or a string with leading zeros (maybe just have regex require a 1 digit come first)
# TODO: nail down the reversal issue with a non-symmetric number (13 vs 11) test case





# Solution: 

def generateStateMachine(n):
    if n%2==0 or n<3:
        return (None, None)
    forward_state_transitions = {}
    backward_state_transitions = {"Accept":{}}
    for k in range(n):
        current_state = str(k)
        state_after_0 = str((2*k)%n)
        state_after_1 = str((2*k+1)%n)
        forward_state_transitions[current_state] = {}
        forward_state_transitions[current_state][state_after_0] = "0"
        forward_state_transitions[current_state][state_after_1] = "1"
        if k==0:
            forward_state_transitions[current_state]["Accept"] = "END"
        if state_after_0 not in backward_state_transitions:
            backward_state_transitions[state_after_0] = {}
        if state_after_1 not in backward_state_transitions:
            backward_state_transitions[state_after_1] = {}
        backward_state_transitions[state_after_0][current_state] = "0"
        backward_state_transitions[state_after_1][current_state] = "1"
        if k==0:
            backward_state_transitions["Accept"][current_state] = "END"
    return (forward_state_transitions,backward_state_transitions)
def condenseStateMachine(n):
    if n%2==0 or n<3:
        return (None, None)
    (forward_state_transitions,backward_state_transitions) = generateStateMachine(n)
    Blist = list(forward_state_transitions.keys())
    Blist.remove('0')
    for B in Blist:
        Q = forward_state_transitions[B][B] if B in forward_state_transitions[B] else None
        # A -> B -> C
        # P    Q*   R
        # A-P->B(<>Q)-R->C
        for A in list(backward_state_transitions[B].keys()):
            if A == B:
                continue
            P = backward_state_transitions[B][A]
            for C in list(forward_state_transitions[B].keys()):
                if C == B:
                    continue
                R = forward_state_transitions[B][C]
                regex = P + ("("+Q+")*" if Q is not None else "") + R
                drop = forward_state_transitions[A].pop(B,None)
                forward_state_transitions[A][C] = regex if C not in forward_state_transitions[A] else "("+forward_state_transitions[A][C]+"|"+regex+")"
                drop = backward_state_transitions[C].pop(B,None)
                backward_state_transitions[C][A] = regex if A not in backward_state_transitions[C] else "("+backward_state_transitions[C][A]+"|"+regex+")"
        drop = forward_state_transitions.pop(B,None)
        drop = backward_state_transitions.pop(B,None)
    return (forward_state_transitions,backward_state_transitions)
def compileRegex(n):
    if n==1:
        return '^(?:[01]*)$'
    if n==2:
        return '^(?:0*|[01]*0)$'
    if n==4:
        return '^(?:0*|[01]*00)$'
    if n==8:
        return '^(?:0*|[01]*000)$'
    if n==16:
        return '^(?:0*|[01]*0000)$'
    zeros = ""
    if n==6:
        n = 3
        zeros = "0"
    if n==10:
        n = 5
        zeros = "0"
    if n==12:
        n = 3
        zeros = "00"
    if n==14:
        n = 7
        zeros = "0"
    if n==18:
        n = 9
        zeros = "0"
    (forward_state_transitions,backward_state_transitions) = condenseStateMachine(n)
    final_regex = "("+forward_state_transitions['0']['0']+")*"+forward_state_transitions['0']['Accept']
    final_regex = final_regex.replace("END","")
    if zeros!="":
        final_regex = "0*|("+final_regex+")"+zeros
    final_regex = final_regex.replace("(","(?:")
    final_regex = "^(?:"+final_regex+")$"
    return final_regex
def regex_divisible_by(n):
    return compileRegex(n)

