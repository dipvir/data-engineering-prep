# =======================================================================================
# PYTHON PRACTICE PART 2 STUDY INDEX: FORMATTING, BOOLEANS & OPERATOR EVALUATION
# =======================================================================================
# * F-STRING PLACEHOLDERS  : Injecting live variables inside text arrays and rounding decimals via :.2f
# * ESCAPE CHARACTERS      : Rendering restricted literals inside string tokens using backslashes (\", \n, \t)
# * BOOLEAN TRUTH VALUES   : Evaluating object contents where empty containers and zero resolve to False
# * CLASS VERIFICATIONS    : Validating exact variable structural types using the isinstance() function
# * MATHEMATICAL OPERATORS : Evaluating calculations, calculating remainders via %, and powers via **
# * INLINE DIVISIONS       : Running floating-point division (/) versus truncated whole floor division (//)
# * ASSIGNMENT EXPANSIONS  : Writing compound equations (+=, -=, %=) and tracking value updates
# * THE WALRUS OPERATOR    : Assigning values to local variables directly inside active expressions via :=
# * OPERATOR CHAINING      : Evaluating structural inline multi-comparison trees cleanly (1 < x < 10)
# * LOGICAL COMBINATIONS   : Linking evaluation pathways using priority-based logic words (and, or, not)
# * IDENTITY MEMORY CHECKS : Validating shared memory addresses (is) versus matching literal values (==)
# * COLLECTION MEMBERSHIP  : Checking item occurrences within arrays or text using 'in' and 'not in' words
# * BITWISE CALCULATIONS   : Mutating raw integer binary structures line-by-line using &, |, and ^ operators
# * BITWISE MANIPULATIONS  : Executing bit inversions with ~ and sliding positions via shift directions (<<, >>)
# * EVALUATION PRECEDENCE  : Resolving compound lines math first, comparisons second, and logic sequences last
# =======================================================================================

# ---------String Format---------
# In Python, we cannot combine strings and numbers like this:
age = 36
#This will produce an error:
# ------------txt = "My name is John, I am " + age
# print(txt)

# But we can combine strings and numbers by using f-strings or the format() method!
# Creating an f-string:
txt = f"My name is John, I am {age}"
print(txt)
# A placeholder (i.e {} curly brackets) can contain variables, operations, functions, and modifiers to format the value.
# A placeholder can include a modifier to format the value.
# A modifier is included by adding a colon : followed by a legal formatting type, like .2f which means fixed point number with 2 decimals:
price = 59.232323233
txt = f"The price is {price:.2f} dollars"
print(txt)
# ---------String Format END-------

# ---------Escape Character---------
# To insert characters that are illegal in a string, use an escape character.
# An escape character is a backslash \ followed by the character you want to insert.
# An example of an illegal character is a double quote inside a string that is surrounded by double quotes:
# Example
# You will get an error if you use double quotes inside a string that is surrounded by double quotes:
# ------------txt = "We are the so-called "Vikings" from the north."
# To fix this problem, use the escape character \":
# Example
# The escape character allows you to use double quotes when you normally would not be allowed:
txt = "We are the so-called \"Vikings\" from the north."
print(txt)

# Other escape characters used in Python:

# Code	Result	
# \'	Single Quote	
# \\	Backslash	
# \n	New Line	
# \r	Carriage Return	
# \t	Tab	
# \b	Backspace	
# \f	Form Feed	
# \ooo	Octal value	
# \xhh	Hex value	
print("ddasaasasa\\ndasa sas xd\\oooadad adad")
# ---------Escape Character END-------

# ---------Python Booleans---------
# Booleans represent one of two values: True or False.
# In programming you often need to know if an expression is True or False.
# You can evaluate any expression in Python, and get one of two answers, True or False.
# When you compare two values, the expression is evaluated and Python returns the Boolean answer:
print(10 > 9)
print(10 == 9)
print(10 < 9)
# When we run a condition in an if statement, Python returns True or False:
# Example
# Print a message based on whether the condition is True or False:
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
# Evaluate Values and Variables
# The bool() function allows you to evaluate any value, and give you True or False in return,
# Example
# Evaluate a string and a number:
print(bool("Hello"))
print(bool(""))
print(bool(0))
print(bool(15))
# Most Values are True
# Almost any value is evaluated to True if it has some sort of content.
# Any string is True, except empty strings.
# Any number is True, except 0.
# Any list, tuple, set, and dictionary are True, except empty ones.
# There are not many values that evaluate to False
# The following will return False:
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))
# Functions can Return a Boolean
def myFunction() :
  return True
print(myFunction())
# Python also has many built-in functions that return a boolean value, like the isinstance() function, which can be used to determine if an object is of a certain data type:
x = 200
print(isinstance(x, int))
# ---------Python Booleans END---------

# ---------Python Operators---------
# Operators are used to perform operations on variables and values.
# In the example below, we use the + operator to add together two values:
print(10 + 5)
# Python divides the operators in the following groups:
# Arithmetic operators
# Assignment operators
# Comparison operators
# Logical operators
# Identity operators
# Membership operators
# Bitwise operators

# Arithmetic Operators
# Arithmetic operators are used with numeric values to perform common mathematical operations:
"""
Operator    Name                Example
+           Addition            x + y
-           Subtraction         x - y
*           Multiplication      x * y
/           Division            x / y
%           Modulus             x % y
**          Exponentiation      x ** y
//          Floor division      x // y
"""
# Here is an example using different arithmetic operators:
x = 10
y = 3

print(x + y)
print(x - y)
print(x * y)
print(x / y)
print(x % y) # Modulus operator (%) returns the remainder of a division.
print(x ** y)
print(x // y) # Floor division (//) returns the Quotient of a division.

# =====================================================================
#        CHILDHOOD LONG DIVISION LAYOUT (PARTS REF)
# =====================================================================
#
#                    QUOTIENT   (The result of your division // )
#                  ___________
#       DIVISOR   )  DIVIDEND   (The total amount you want to divide)
#      (What you    - ________
#     divide by)     REMAINDER  (What is left over at the end % )
#
# =====================================================================
#  QUICK WORKING EXAMPLE: 13 divided by 4
# =====================================================================
#
#                        3      <-- QUOTIENT  ( 13 // 4 )
#                  ___________
#              4  )     13      <-- DIVIDEND
#                     - 12
#                  ___________
#                        1      <-- REMAINDER ( 13 % 4 )
#
# =====================================================================
#  VERIFICATION FORMULA:
#  Dividend = (Divisor * Quotient) + Remainder
#  13       = (4 * 3) + 1
# =====================================================================

# Division in Python
# Python has two division operators:
"""
/ - Division (returns a float)
// - Floor division (returns an integer)
"""
x = 12
y = 5
print(x / y)
print(x // y)
# Arithmetic Operators End  

# Assignment Operators
# Assignment operators are used to assign values to variables:
"""
Operator    Example           Same As
=           x = 5             x = 5
+=          x += 3            x = x + 3
-=          x -= 3            x = x - 3
*=          x *= 3            x = x * 3
/=          x /= 3            x = x / 3
%=          x %= 3            x = x % 3
//=         x //= 3           x = x // 3
**=         x **= 3           x = x ** 3
&=          x &= 3            x = x & 3
|=          x |= 3            x = x | 3
^=          x ^= 3            x = x ^ 3
>>=         x >>= 3           x = x >> 3
<<=         x <<= 3           x = x << 3
:=          print(x := 3)     x = 3
                              print(x)
"""
# The Walrus Operator
# Python 3.8 introduced the := operator, known as the "walrus operator". It assigns values to variables as part of a larger expression:
# Example
# The count variable is assigned in the if statement, and given the value 5:
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")
# Assignment Operators End

# Comparison Operators
# Comparison operators are used to compare two values:
"""
Operator    Name                        Example
==          Equal                       x == y
!=          Not equal                   x != y
>           Greater than                x > y
<           Less than                   x < y
>=          Greater than or equal to    x >= y
<=          Less than or equal to       x <= y
"""
# Example
# Comparison operators return True or False based on the comparison:
x = 5
y = 3
print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

# Chaining Comparison Operators
# Python allows you to chain comparison operators:
# Example
x = 5
print(1 < x < 10) #chaining comparison operators is just like a shorthand for below line
print(1 < x and x < 10) # ganeral way
# Two more examples
print(1 != x <= 10)
print(1 != x == 10)
# Comparison Operators End

# Logical Operators
# Logical operators are used to combine conditional statements:
"""
Operator    Description                                                       Example
and         Returns True if both statements are true                          x < 5 and  x < 10
or          Returns True if one of the statements is true                     x < 5 or x < 4
not         Reverse the result, returns False if the result is true           not(x < 5 and x < 10)
"""
# Example
x = 5
print(x > 3 and x < 10)
print(x > 3 or x < 4)
print(not(x > 3 and x < 10))
# Logical Operators End

# Identity Operators
# Identity operators are used to compare the objects, not if they are equal, but if they are actually the same object, with the same memory location:
"""
Operator    Description                                                       Example
is          Returns True if both variables are the same object                x is y
is not      Returns True if both variables are not the same object            x is not y
"""
# Example
# The 'is' operator returns True if both variables point to the same object:
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x
print(x is z)
print(x is y)
print(x == y)

# Example
# The 'is' not operator returns True if both variables do not point to the same object:
x = ["apple", "banana"]
y = ["apple", "banana"]
print(x is not y)
# Difference Between is and ==
# is - Checks if both variables point to the same object in memory
# == - Checks if the values of both variables are equal
# Example
x = [1, 2, 3]
y = [1, 2, 3]

print(x == y)
print(x is y)
# Identity Operators End

# Membership Operators
# Membership operators are used to test if a sequence is presented in an object:
"""
Operator    Description                                                                         Example
in          Returns True if a sequence with the specified value is present in the object        x in
not in      Returns True if a sequence with the specified value is not present in the object    x not in
"""
# Example
x = ["apple", "banana"]
print("banana" in x)
print("pineapple" not in x)

# Membership in Strings
# You can also use membership operators to check if a string is present in another string:
x = "Hello, World!"
print("Hello" in x)
print("World" not in x)
# Membership Operators End

# Bitwise Operators
# Bitwise operators are used to compare (binary) numbers:
"""
Operator    Name                    Description                                                         Example
&           AND                     Sets each bit to 1 if both bits are 1                              x & y
|           OR                      Sets each bit to 1 if one of two bits is 1                         x | y
^           XOR                     Sets each bit to 1 if only one of two bits is 1                    x ^ y
~           NOT                     Inverts all the bits                                               ~x
<<          Zero fill left shift    Shift left by pushing zeros in from the right                      x << 2
                                    and let the leftmost bits fall off                      
>>          Signed right shift      Shift right by pushing copies of the leftmost                      x >> 2
                                    bit in from the left, and let the rightmost bits fall off
"""

# Example
# The & operator compares each bit and set it to 1 if both are 1, otherwise it is set to 0:
print(6 & 3)
# The binary representation of 6 is 0110
# The binary representation of 3 is 0011
# Then the & operator compares the bits and returns 0010, which is 2 in decimal.

# Example
# The | operator compares each bit and set it to 1 if one or both is 1, otherwise it is set to 0:
print(6 | 3)
# The binary representation of 6 is 0110
# The binary representation of 3 is 0011
# Then the | operator compares the bits and returns 0111, which is 7 in decimal.

# Example
# The ^ operator compares each bit and set it to 1 if only one of two bits is 1, otherwise it is set to 0:
print(6 ^ 3)
# The binary representation of 6 is 0110
# The binary representation of 3 is 0011
# Then the ^ operator compares the bits and returns 0101, which is 5 in decimal.

# Example
# The ~ operator inverts all the bits:
print(~6)
# The binary representation of 6 is 0110
# Then the ~ operator inverts all the bits and returns 1001, which is -7 in decimal.
# Note: The ~ operator is a unary operator, which means it only takes one operand.

# Example
# The << operator shifts the bits to the left by the specified number of bits:
print(6 << 2)
# The binary representation of 6 is 0110
# Then the << operator shifts the bits to the left by 2 bits and returns 011000, which is 24 in decimal.

# Example
# The >> operator shifts the bits to the right by the specified number of bits:
print(6 >> 2)
# The binary representation of 6 is 0110
# Then the >> operator shifts the bits to the right by 2 bits and returns 0001, which is 1 in decimal.
# Bitwise Operators End

# Operator Precedence
# Operator precedence describes the order in which operations are performed.
# Parentheses has the highest precedence, meaning that expressions inside parentheses must be evaluated first:
print((6 + 3) - (6 + 3))
# Multiplication * has higher precedence than addition +, and therefore multiplications are evaluated before additions:
print(100 + 5 * 3)
# The precedence order is described in the table below, starting with the highest precedence at the top:
"""
Operator                    Description
()                          Parentheses
**                          Exponentiation
+x  -x  ~x                  Unary plus, unary minus, and bitwise NOT
*  /  //  %                 Multiplication, division, floor division, and modulus
+  -                        Addition and subtraction
<<  >>                      Bitwise left and right shifts
&                           Bitwise AND
^                           Bitwise XOR
|                           Bitwise OR
==  !=  >                   Comparisons, identity, and membership operators
>=  <  <=    
is  is not
in  not in                  
not                         Logical NOT
and                         AND
or                          OR
"""
# Left-to-Right Evaluation
# If two operators have the same precedence, the expression is evaluated from left to right.

# Example
# Addition + and subtraction - has the same precedence, and therefore we evaluate the expression from left to right:
print(5 + 4 - 7 + 3)
# The Data Engineer Golden Rule: Arithmetic wraps up completely before comparisons look at the values, and comparisons wrap up completely before logical operators (and/or) tie the blocks together.
# =====================================================================
#  PYTHON OPERATOR PRECEDENCE REFERENCE
# =====================================================================
#  HIGH PRIOR:  ()  ->  **  ->  * , / , // , %  ->  + , -
#  MED PRIOR:   == , != , > , >= , < , <=
#  LOW PRIOR:   not  ->  and  ->  or
# =====================================================================
#  TRACING EXAMPLE:
#  val = 10 + 2 * 5 > 15 and not 5 == 4
#
#  Step 1 (Math):        10 + 10 > 15 and not 5 == 4
#  Step 2 (Math):             20 > 15 and not 5 == 4
#  Step 3 (Comparisons):    True      and not False
#  Step 4 (Logical Not):    True      and True
#  Step 5 (Logical And):    FINAL RESULT = True
# =====================================================================
# Operator Precedence End





