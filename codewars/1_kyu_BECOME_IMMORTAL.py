# Problem: 
problem='''
BECOME IMMORTAL

In the nation of CodeWars, there lives an Elder who has lived for a long time. Some people call him the Grandpatriarch, but most people just refer to him as the Elder.

There is a secret to his longetivity: he has a lot of young worshippers, who regularly perform a ritual to ensure that the Elder stays immortal:

The worshippers lines up in a magic rectangle, of dimensions m and n.
They channel their will to wish for the Elder. In this magic rectangle, any worshipper can donate time equal to the xor of the column and the row (zero-indexed) he's on, in seconds, to the Elder.
However, not every ritual goes perfectly. The donation of time from the worshippers to the Elder will experience a transmission loss l (in seconds). Also, if a specific worshipper cannot channel more than l seconds, the Elder will not be able to receive this worshipper's donation.
The estimated age of the Elder is so old it's probably bigger than the total number of atoms in the universe. However, the lazy programmers (who made a big news by inventing the Y2K bug and other related things) apparently didn't think thoroughly enough about this, and so their simple date-time system can only record time from 0 to t-1 seconds. If the elder received the total amount of time (in seconds) more than the system can store, it will be wrapped around so that the time would be between the range 0 to t-1.

Given m, n, l and t, please find the number of seconds the Elder has received, represented in the poor programmer's date-time system.

(Note: t will never be bigger than 2^32 - 1, and in JS, 2^26 - 1.)

Example:

m=8, n=5, l=1, t=100

Let's draw out the whole magic rectangle:
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 0 1 6 7 4 5
3 2 1 0 7 6 5 4
4 5 6 7 0 1 2 3

Applying a transmission loss of 1:
0 0 1 2 3 4 5 6
0 0 2 1 4 3 6 5
1 2 0 0 5 6 3 4
2 1 0 0 6 5 4 3
3 4 5 6 0 0 1 2

Adding up all the time gives 105 seconds.

Because the system can only store time between 0 to 99 seconds, the first 100 seconds of time will be lost, giving the answer of 5.
This is no ordinary magic (the Elder's life is at stake), so you need to care about performance. All test cases (900 tests) can be passed within 1 second, but naive solutions will time out easily. Good luck, and do not displease the Elder.
'''

# Notes: 
notes='''
The bitwise XOR of a number K less than 2^N with the set of all numbers between 1 and 2^N is simply a permutation of those numbers, as each number swaps places with its XOR counterpart. 
In the case where the array of numbers specified in the problem form a (2^N)x(2^N) square, each row and column contains all the numbers from 1 to 2^n exactly once. If the shape is an Mx(2^N) rectangle with M < 2^N, then each full-length column (or row in the transposed case) contains all the numbers from 1 to 2^N exactly once. In those cases, the total can be determined through a formula for the sum of the numbers from 1 to 2^N, times the number of rows, minus the sum of the numbers from 1 to the high water mark L. The formula for the sum of the numbers from 1 to K is K(K+1)/2. 
In the case where the array of numbers is a less convenient shape, it can be cut into four pieces: a maximal square of side length 2^N, two rectangles of side length Mx(2^N) where M < 2^N, and a rectangle where both sides are of length less than 2^N. The values of the first three parts can be determined by formula, and the fourth can be determined by recursion, which will end in a number of steps similar to LOG_2(C) where C is the larger of the side lengths of the original array. 
All calculations must be done modulo the parameter T, so all calculations must also be done as integers with no lost of precision, even during division. 
'''

# Scratch code: 

def fun(rowCount,colCount,waterline,modulus):
	sum = 0
	for r in range(rowCount):
		#row = []
		for c in range(colCount):
			#row.append(r^c)
			sum += max(0,(r^c)-waterline)
		#print(row)
	print(sum%modulus)
def isPowerOfTwo(n):
	return n>0 and (n&(n-1))==0
def boundingBox(n):
	return (n^(n-1))/2+1
def roundDownToPowerOfTwo(n):
	bound = 1
	while bound<=n:
		bound *= 2
	return bound/2
def fun2(rowCount,colCount,waterline,modulus):
	if rowCount>colCount:
		return fun2(colCount,rowCount,waterline,modulus)
	if rowCount==1:
		return (max(0,colCount-waterline)*(max(0,colCount-waterline)-1)/2.0)%modulus
	if rowCount==0:
		return 0
	bound = roundDownToPowerOfTwo(colCount)
	if rowCount<=bound:
		upperLeftPart = (max(0,bound-waterline)*(max(0,bound-waterline)-1)/2.0)*rowCount
		upperRightPart = rowCount*(colCount-bound)*max(0,bound-waterline) + fun2(rowCount,colCount-bound,max(0,waterline-bound),modulus)
		return (upperLeftPart + upperRightPart)%modulus
	else:
		upperLeftPart = (max(0,bound-waterline)*(max(0,bound-waterline)-1)/2.0)*bound
		upperRightPart = bound*(colCount-bound)*max(0,bound-waterline) + fun2(bound,colCount-bound,max(0,waterline-bound),modulus)
		lowerLeftPart = bound*(rowCount-bound)*max(0,bound-waterline) + fun2(rowCount-bound,bound,max(0,waterline-bound),modulus)
		lowerRightPart = fun2(rowCount-bound,colCount-bound,waterline,modulus)
		return (upperLeftPart + upperRightPart + lowerLeftPart + lowerRightPart)%modulus

fun(16,16)
fun2(16,16)


# Solution: 

def roundDownToPowerOfTwo(n):
	bound = 1
	while bound<=n:
		bound *= 2
	return int(bound/2)
def triangleWithModulus(n,modulus):
	return (((n%(modulus*2))*(n%(modulus*2)-1))>>1)%modulus
def multiplyWithModulus(a,b,modulus):
	return ((a%modulus)*(b%modulus))%modulus
def multiplyWithModulus3(a,b,c,modulus):
	return multiplyWithModulus(multiplyWithModulus(a,b,modulus),c,modulus)
def elder_age(rowCount,colCount,waterline,modulus):
	if rowCount>colCount:
		return elder_age(colCount,rowCount,waterline,modulus)
	if rowCount==1:
		return triangleWithModulus(max(0,colCount-waterline),modulus)
	if rowCount==0:
		return 0
	bound = roundDownToPowerOfTwo(colCount)
	if rowCount<=bound:
		upperLeftPart = multiplyWithModulus(triangleWithModulus(max(0,bound-waterline),modulus),rowCount,modulus)
		upperRightPart = multiplyWithModulus3(rowCount,(colCount-bound),max(0,bound-waterline),modulus) + elder_age(rowCount,colCount-bound,max(0,waterline-bound),modulus)
		return (upperLeftPart + upperRightPart)%modulus
	else:
		upperLeftPart = multiplyWithModulus(triangleWithModulus(max(0,bound-waterline),modulus),bound,modulus)
		upperRightPart = multiplyWithModulus3(bound,(colCount-bound),max(0,bound-waterline),modulus) + elder_age(bound,colCount-bound,max(0,waterline-bound),modulus)
		lowerLeftPart = multiplyWithModulus3(bound,(rowCount-bound),max(0,bound-waterline),modulus) + elder_age(rowCount-bound,bound,max(0,waterline-bound),modulus)
		lowerRightPart = elder_age(rowCount-bound,colCount-bound,waterline,modulus)
		return (upperLeftPart + upperRightPart + lowerLeftPart + lowerRightPart)%modulus

# Example Tests: 

test.describe('Example tests')
test.assert_equals(elder_age(8,5,1,100), 5)
test.assert_equals(elder_age(8,8,0,100007), 224)
test.assert_equals(elder_age(25,31,0,100007), 11925)
test.assert_equals(elder_age(5,45,3,1000007), 4323)
test.assert_equals(elder_age(31,39,7,2345), 1586)
test.assert_equals(elder_age(545,435,342,1000007), 808451)
#You need to run this test very quickly before attempting the actual tests :)
test.assert_equals(elder_age(28827050410, 35165045587, 7109602, 13719506), 5456283);
