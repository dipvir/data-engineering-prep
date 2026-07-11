# =======================================================================================
# PYTHON PRACTICE PART 7 STUDY INDEX: ANONYMOUS FUNCTIONS, RECURSION & ITERATORS
# =======================================================================================
# * LAMBDA FUNCTIONS      : Writing small, single-expression anonymous functions that return values automatically
# * CUSTOM CORES (CLOSURES): Nesting lambda expressions inside regular functions to build dynamic multiplier shortcuts
# * BUILT-IN DATA TOOLS   : Using lambdas with map() to modify items, filter() to select items, and sorted() to order rows
# * RECURSION MECHANICS   : Breaking down repetitive loops into functions that call themselves using base and recursive cases
# * SYSTEM PROTECTION CAPS: Managing recursion error boundaries using explicit exception handling and sys.setrecursionlimit()
# * GENERATOR VALUE YIELDS: Creating memory-friendly functions that pause and freeze their variables using the yield keyword
# * GENERATOR NAVIGATION  : Stepping through frozen functions manually with next() and handling background StopIteration signals
# * GENERATOR SHORTHANDS  : Building quick loop sequences on-the-fly using round bracket comprehension expressions `()`
# * STREAM TIMING CODES   : Intercepting and altering active generator outputs dynamically via `.send()` and `.close()` methods
# * NUMERIC RANGE TYPES   : Creating sequence blocks by configuring single boundary limits or custom skip step intervals
# * RANGE STRUCTURES      : Verifying range sizes with len(), testing specific values with 'in', and slicing subsequences
# * LISTS VS TRUE ARRAYS  : Understanding why standard lists allow mixed data types while real arrays restrict inputs to one type
# * CONVERTING ITERABLES  : Pulling structural loop tools explicitly out of lists, tuples, or strings using the iter() function
# * CUSTOM LOOP OBJECTS   : Designing completely loopable classes from scratch by implementing the `__iter__` and `__next__` rules
# =======================================================================================

# --------------------Lambda Functions----------------------
# A lambda function is a small anonymous function.
# A lambda function can take any number of arguments, but can only have one expression.
"""
----Lambda Function Syntax-----
lambda arguments : expression
"""
# The expression is executed and the result is returned:
"""Example :- Add 10 to argument a, and return the result:"""
x = lambda a : a + 10
print(x(5))

# Lambda functions can take any number of arguments:
"""Example :- Multiply argument a with argument b and return the result:"""
x = lambda a, b : a * b
print(x(5, 6))

"""Example :- Summarize argument a, b, and c and return the result:"""
x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

# Why Use Lambda Functions?
# The power of lambda is better shown when you use them as an anonymous function inside another function.
# Say you have a function definition that takes one argument, and that argument will be multiplied with an unknown number:
def myfunc(n):
  return lambda a : a * n
# Use the above function definition to make a function that always doubles the number you send in:
# Example
mydoubler = myfunc(2)
print(mydoubler(11))
# Or, use the same function definition to make a function that always triples the number you send in:
# Example
mytripler = myfunc(3)
print(mytripler(11))

# Lambda with Built-in Functions
# Lambda functions are commonly used with built-in functions like map(), filter(), and sorted().
# Using Lambda with map(), The map() function applies a function to every item in an iterable:
"""Example :- Double all numbers in a list:"""
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

# Using Lambda with filter(), The filter() function creates a list of items for which a function returns True:
"""Example :- filter out odd numbers from a list:"""
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

# Using Lambda with sorted(), The sorted() function can use a lambda as a key for custom sorting:
"""Example :- Sort a list of tuples by the second element:"""
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

"""Example :- Sorting the list of strings by its length:"""
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)
# ----------------Lambda Functions End----------------

# ----------------Python Recursion----------------
# Recursion is when a function calls itself.
# Recursion is a common mathematical and programming concept. It means that a function calls itself. This has the benefit of meaning that you can loop through data to reach a result.
# The developer should be very careful with recursion as it can be quite easy to slip into writing a function which never terminates, or one that uses excess amounts of memory or processor power. However, when written correctly recursion can be a very efficient and mathematically-elegant approach to programming.

"""Example :- A simple recursive function that counts down from 5:"""
def countdown(n):
  if n <= 0:
    print("Done!")
  else:
    print(n)
    countdown(n - 1)

countdown(5) # Function call

# Base Case and Recursive Case
# Every recursive function must have two parts:
"""
 -> A base case - A condition that stops the recursion
 -> A recursive case - The function calling itself with a modified argument
Without a base case, the function would call itself forever, causing a stack overflow error.
"""
"""Example :- Identifying base case and recursive case:"""
def factorial(n):
  # Base case
  if n == 0 or n == 1:
    return 1
  # Recursive case
  else:
    return n * factorial(n - 1)
print(factorial(5)) # Function call
"""Note :- The base case is crucial. Always make sure your recursive function has a condition that will eventually be met."""

"""Adding factorial function Example from Gemini with better explanation"""
# =====================================================================
# RECURSION CONCEPTS: THE FACTORIAL RESOLUTION RULE
# =====================================================================
def factorial(n):
    # 1. DEFENSIVE GUARD: Catch invalid negative numbers immediately
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
        
    # 2. THE BASE CASE: Stops recursion. Includes 0 because mathematically 0! = 1,
    # and it prevents 0 inputs from plunging into infinite negative recursion loops.
    if n == 0 or n == 1:
        return 1
        
    # 3. THE RECURSIVE CASE: Function calls itself with a modified argument (n - 1)
    else:
        return n * factorial(n - 1)

# Execution Traces:
print(factorial(5)) #stops cleanly at n == 1 -> Returns 120
print(factorial(0)) #stops cleanly at n == 0 -> Returns 1
print(factorial(-1)) #Throw error
# =====================================================================
# RECURSION CONCEPTS: THE FACTORIAL RESOLUTION RULE END
# =====================================================================

# Fibonacci Sequence
# The Fibonacci sequence is a classic example where each number is the sum of the two preceding ones. 
# The sequence starts with 0 and 1: 0, 1, 1, 2, 3, 5, 8, 13, ...
# The sequence continues indefinitely, with each number being the sum of the two preceding ones.
# We can use recursion to find a specific number in the sequence:
"""Example :- Find the 7th number in the Fibonacci sequence:"""
def fibonacci(n):
  if n <= 1:
    return n
  else:
    return fibonacci(n - 1) + fibonacci(n - 2)
print(fibonacci(7))

"""Below is the breakdown of how aboves recursive function works to find Nth number in the Fibonacci sequence:"""
# =====================================================================
# RECURSION CONCEPTS: THE FIBONACCI TREE RESOLUTION RULE
# =====================================================================
# How Python evaluates fibonacci(4):
#
#                    f(4)  -> Final Step: 2 + 1 = Returns 3
#                   /    \
#             f(3)=2      f(2)=1  (Evaluated much later!)
#            /      \
#       f(2)=1      f(1)=1
#      /      \
#  f(1)=1    f(0)=0
#
# =====================================================================
# For your print(fibonacci(7)) question, the tree splits exactly like 
# this but grows 7 layers deep, ultimately summing up to 13!
# =====================================================================
"""Adding fibonacci Soulttion from Gemini"""
def fibonacci(n):
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative steps.")
    
    # THE BASE CASE
    if n <= 1:
        return n
    
    # THE RECURSIVE CASE
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(4))  # Output: 3
print(fibonacci(7))  # Output: 13
# =====================================================================
# RECURSION CONCEPTS: THE FIBONACCI TREE RESOLUTION RULE END
# =====================================================================

# Recursion with Lists
# Recursion can be used to process lists by handling one element at a time:
"""Example :- Calculate the sum of all elements in a list:"""
def sum_list(numbers):
  if len(numbers) == 0:
    return 0
  else:
    return numbers[0] + sum_list(numbers[1:])

my_list = [1, 2, 3, 4, 5]
print(sum_list(my_list)) 


"""Example :- Find the maximum value in a list:"""
def find_max(numbers):
  if len(numbers) == 1:
    return numbers[0]
  else:
    max_of_rest = find_max(numbers[1:])
    return numbers[0] if numbers[0] > max_of_rest else max_of_rest

my_list = [3, 7, 2, 9, 1]
print(find_max(my_list))
"""Below is the breakdown of how aboves recursive function works to find max value in list"""
# =====================================================================
# RECURSION CONCEPTS: RECURSIVE LIST MAX POINTER
# =====================================================================
#  LIST STATE GOING DOWN             BATTLE STAGE COMING UP
#  f([3, 7, 2, 9, 1])                Is 3 > 9? No -> Returns 9 (🏆 FINAL)
#    └─ f([7, 2, 9, 1])              Is 7 > 9? No -> Returns 9
#         └─ f([2, 9, 1])            Is 2 > 9? No -> Returns 9
#              └─ f([9, 1])          Is 9 > 1? Yes -> Returns 9
#                   └─ f([1]) ------ Base Case: Returns 1
# =====================================================================

# Recursion Depth Limit
# Python has a limit on how deep recursion can go. The default limit is usually around 1000 recursive calls.
"""Example :- Check the recursion limit:"""
import sys
print(sys.getrecursionlimit())
# If we need deeper recursion, we can increase the limit, but we have to be careful as this can cause crashes:
import sys
sys.setrecursionlimit(2000)
print(sys.getrecursionlimit())
# ----------------Python Recursion End-------------

# ----------------Python Generators----------------
# Generators
# Generators are functions that can pause and resume their execution.
# When a generator function is called, it returns a generator object, which is an iterator.
# The code inside the function is not executed yet, it is only compiled. The function only executes when you iterate over the generator.
"""Example :- A simple generator function:"""
def my_generator():
  yield 1
  yield 2
  yield 3

for value in my_generator():
  print(value)

print(my_generator() , list(my_generator()) , type(my_generator()) , dir(my_generator()) , sep = "\n")
"""
Generators allow you to iterate over data without storing the entire dataset in memory.
Instead of using return, generators use the yield keyword.
"""

# The yield Keyword
# The yield keyword is what makes a function a generator.
# When yield is encountered, the function's state is saved, and the value is returned. The next time the generator is called, it continues from where it left off.
"""Example :- Generator that yields numbers:"""
def count_up_to(n):
  count = 1
  while count <= n:
    yield count
    count += 1
for num in count_up_to(5):
  print(num)
"""Unlike return, which terminates the function, yield pauses it and can be called multiple times."""

# Generators Saves Memory
# Generators are memory-efficient because they generate values on-the-fly instead of storing everything in memory.
# For large datasets, generators save memory:
# Example :- Generator for large sequences:
def large_sequence(n):
  for i in range(n):
    yield i
# This doesn't create a million numbers in memory
gen = large_sequence(1000000)
print(next(gen))
print(next(gen))
print(next(gen))

# Using next() with Generators, We can manually iterate through a generator using the next() function:
def simple_gen():
  yield "Emil"
  yield "Tobias"
  yield "Linus"
gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen))

# When there are no more values to yield, the generator raises a StopIteration exception
def simple_gen():
  yield 1
  yield 2
gen = simple_gen()
print(next(gen))
print(next(gen))
print(next(gen)) # This will raise StopIteration

# Generator Expressions
# Similar to list comprehensions, you can create generators using generator expressions with parentheses instead of square brackets:
"""Example :- List comprehension vs generator expression:"""
# List comprehension - creates a list
list_comp = [x * x for x in range(5)]
print(list_comp)
# Generator expression - creates a generator
gen_exp = (x * x for x in range(5))
print(gen_exp)
print(list(gen_exp))

"""Example :- Using a generator expression with sum:"""
# Calculate sum of squares without creating a list (i.e sum works with generator)
total = sum(x * x for x in range(10))
print(total)

# Fibonacci Sequence Generator
# Generators can be used to create the Fibonacci sequence.
# It can continue generating values indefinitely, without running out of memory:
"""Example :- Generate 100 Fibonacci numbers:"""
def fibonacci():
  a, b = 0, 1
  while True:
    yield a
    a, b = b, a + b

# Get first 100 Fibonacci numbers
gen = fibonacci()
for i in range(100):
  print(next(gen))

# Generator Methods
# Generators have special methods for advanced control
"""send() Method :- The send() method allows you to send a value to the generator:"""
def echo_generator():
  while True:
    received = yield
    print("Received:", received)

gen = echo_generator()
next(gen) # Prime the generator
gen.send("Hello")
gen.send("World")

"""close() Method :- The close() method stops the generator:"""
def my_gen():
  try:
    yield 1
    yield 2
    yield 3
  finally:
    print("Generator closed")

gen = my_gen()
print(next(gen))
gen.close()
# ====================Python Functions End======================

# ===================Python range======================
# The built-in range() function returns an immutable sequence of numbers, commonly used for looping a specific number of times.
# This set of numbers has its own data type called range.
"""Note: Immutable means that it cannot be modified after it is created."""

"""Creating ranges :- The range() function can be called with 1, 2, or 3 arguments, using below syntax:
 -> range(start, stop, step)
"""

# Call range() With One Argument
# If the range function is called with only one argument, the argument represents the stop value.
# The start argument is optional, and if not provided, it defaults to 0.
# range(10) returns a sequence of each number from 0 to 9. (The start argument, 0 is inclusive, and the stop argument, 10 is exclusive).
"""Example :- Create a range of numbers from 0 to 9:"""
print(range(10))
print(list(range(10)))

# Call range() With Two Arguments
# If the range function is called with two arguments, the first argument represents the start value, and the second argument represents the stop value. range(3, 10) returns a sequence of each number from 3 to 9:
"""Example :- Create a range of numbers from 3 to 9:"""
print(range(3, 10))
print(list(range(3, 10)))

# Call range() With Three Arguments
# If the range function is called with three arguments, the third argument represents the step value.
# The step value means the difference between each number in the sequence. It is optional, and if not provided, it defaults to 1.
# range(3, 10, 2) returns a sequence of each number from 3 to 9, with a step of 2:
"""Example :- Create a range of numbers from 3 to 9:"""
print(range(3, 10, 2))
print(list(range(3, 10, 2)))

# Using ranges
# Ranges are often used in for loops to iterate over a sequence of numbers.
"""Example :- Iterate over each value in a range:"""
for i in range(10):
  print(i)

# Using List to Display Ranges
# The range object is a data type that represents an immutable sequence of numbers, and it is not directly displayable.
# Therefore, ranges are often converted to lists for display.
"""Example :- Convert different ranges to lists:"""
print(list(range(5)))
print(list(range(1, 6)))
print(list(range(5, 20, 3)))

# Slicing Ranges
# Like other sequences, ranges can be sliced to extract a subsequence.
"""Example :- Extract a subsequence from a range:"""
r = range(12 , 24)
print(list(r))
print(r[5])
print(r[:3])
print(list(r[:3]))
"""Note: The first print statement returns the value at index 2, and the second print statement returns a new range object, from index 0 to 3."""

# Membership Testing
# Ranges support membership testing with the 'in' operator.
"""Example :- Test if the numbers 6 and 7 are present in a range:"""
r = range(0, 10, 2)
print(list(r))
print(6 in r)
print(7 in r)
"""The return value is True when the number is present in the range, and False when it is not."""

# Length
# Ranges support the len() function to get the number of elements in the range.
"""Example :- Get the length of a range:"""
r = range(0, 10, 2)
print(list(r))
print(len(r))
# ===================Python range End======================

# ===================Python Arrays======================
"""Note: Python does not have built-in support for Arrays, but Python Lists can be used instead.
Arrays
Note: This page shows you how to use LISTS as ARRAYS, however, to work with arrays in Python you will have to import a library, like the NumPy library.
"""
# Arrays are used to store multiple values in one single variable:
"""Example :- Create an array containing car names:"""
cars = ["Ford", "Volvo", "BMW"]
print(type(cars))

"""
What is an Array?
An array is a special variable, which can hold more than one value at a time.
If you have a list of items (a list of car names, for example), storing the cars in single variables could look like this:
car1 = "Ford"
car2 = "Volvo"
car3 = "BMW"
However, what if you want to loop through the cars and find a specific one? And what if you had not 3 cars, but 300?
The solution is an array!
An array can hold many values under a single name, and you can access the values by referring to an index number.
"""

# Access the Elements of an Array
# You refer to an array element by referring to the index number.
"""Example :- Get the value of the first array item:"""
x = cars[0]
print(x)
"""Example :- Modify the value of the first array item:"""
cars[0] = "Toyota"
print(cars)
      
# The Length of an Array
# Use the len() method to return the length of an array (the number of elements in an array).
"""Example :- Return the number of elements in the cars array:"""
print(len(cars)) #Note: The length of an array is always one more than the highest array index.

# Looping Array Elements
# We can use the 'for in' loop to loop through all the elements of an array.
"""Example :- Print each item in the cars array:"""
for x in cars:
  print(x)

# Adding Array Elements
# You can use the append() method to add an element to an array.
"""Example :- Add one more element to the cars array:"""
cars.append("Honda")

# Removing Array Elements
# We can use the pop() method to remove an element from the array.
"""Example :- Delete the second element of the cars array:"""
cars.pop(1)

# We can also use the remove() method to remove an element from the array.
"""Example :- Delete the element that has the value "Volvo":"""
cars.remove("Volvo")
"""Note: The list's remove() method only removes the first occurrence of the specified value."""
# =====================================================================
# DEVELOPER ARCHITECTURAL NOTE: PYTHON LISTS VS. TRUE ARRAYS
# =====================================================================
# Pure Python does NOT have built-in array support; standard collections 
# like fruits = ["apple", "banana"] are strictly Lists. 
# Python lists are flexible and hold mixed data types (heterogeneous).
# True arrays require importing external libraries (like NumPy) to enforce 
# a single data type (homogeneous) for high-performance data engineering pipelines.
# =====================================================================
# ===================Python Arrays End======================

# ===================Python Iterators======================
# An iterator is an object that contains a countable number of values.
# An iterator is an object that can be iterated upon, meaning that you can traverse through all the values.
# Technically, in Python, an iterator is an object which implements the iterator protocol, which consist of the methods __iter__() and __next__().

# Iterator vs Iterable
# Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers which you can get an iterator from.
# All these objects have a iter() method which is used to get an iterator:
"""Example :- Return an iterator from a tuple, and print each value:"""

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)
print(type(myit))
print(next(myit))
print(next(myit))
print(next(myit))
#Even strings are iterable objects, and can return an iterator
"""Example :- Strings are also iterable objects, containing a sequence of characters:"""
mystr = "banana"
myit = iter(mystr)
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

# Looping Through an Iterator
# We can also use a for loop to iterate through an iterable object:
"""Example :- Iterate the values of a tuple:"""
mytuple = ("apple", "banana", "cherry")
for x in mytuple:
  print(x)
"""Example :- Iterate the characters of a string:"""
mystr = "banana"
for x in mystr:
  print(x)
"""Note :- The for loop actually creates an iterator object and executes the next() method for each loop."""

# Creating an Iterator
# To create an object/class as an iterator you have to implement the methods __iter__() and __next__() to your object.
# As we will learn in the Python Classes/Objects chapter, all classes have a function called __init__(), which allows you to do some initializing when the object is being created.

# The __iter__() method acts similar, you can do operations (initializing etc.), but must always return the iterator object itself.

# The __next__() method also allows you to do operations, and must return the next item in the sequence.
"""Example :- Create an iterator that returns numbers, starting with 1, and each sequence will increase by one (returning 1,2,3,4,5 etc.):
"""
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))


# StopIteration
# The example above would continue forever if you had enough next() statements, or if it was used in a for loop.
# To prevent the iteration from going on forever, we can use the StopIteration statement.
# In the __next__() method, we can add a terminating condition to raise an error if the iteration is done a specified number of times:
"""Example :- Stop after 20 iterations:"""
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)
# ===================Python Iterators End======================


