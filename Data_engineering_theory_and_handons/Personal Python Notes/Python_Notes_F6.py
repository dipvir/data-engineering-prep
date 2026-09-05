# =======================================================================================
# PYTHON PRACTICE PART 6 STUDY INDEX: STRUCTURAL LOOPS & FUNCTION DESIGNS
# =======================================================================================
# * CONDITION WHILE LOOPS  : Executing code loops using break exit lines, continue skips, and else blocks
# * ITERATIVE FOR LOOPS    : Traversing lists, strings, and ranges without predefined tracking index counters
# * NESTED MATRIX LOOPS    : Combining multi-level loops to process combinations of data items
# * STRUCTURE DEFINITIONS  : Declaring clean def blocks, case-sensitive names, and tracking output return paths
# * ARGUMENT RULES         : Mapping values to exact function parameter positions vs unordered keyword calls
# * INTERACTION FALLBACKS  : Configuring parameter default values to handle missing arguments during function calls
# * MIXED PARAMETER MAPS   : Sequencing regular parameters alongside default values in function signatures
# * INPUT RULES BOUNDARIES : Locking entry gates via positional-only (/) and keyword-only (*) separations
# * UNKNOWN ARGUMENT ARRAYS: Collecting extra positional parameters as tuples using the *args signature
# * UNKNOWN KEYWORD MAPS   : Packing unknown keyword arguments directly into variable dictionaries using **kwargs
# * VARIABLE EXPLOSIONS    : Unpacking existing lists (*) and dicts (**) directly inside active function calls
# * LEGB SCOPE PATHWAYS    : Resolving variable names following Local -> Enclosing -> Global -> Built-in lookups
# * INNER SCOPE WRITES     : Overriding external variable levels using local global and nonlocal variable definitions
# * DECORATOR ESSENTIALS   : Wrapping base functions with outer wrapper blocks using the @ shortcut notation
# * MULTI-ARGUMENT WRAPPERS: Scaling decorator inner functions to handle variables using (*args, **kwargs)
# * DECORATOR CONFIGURATORS: Adding variable levels to pass parameters directly into decorator blueprints
# * STACKED PIPELINES      : Tiering multiple decorator tags together to run execution wrappers in reverse order
# * METADATA PROTECTIONS   : Using functools.wraps to protect original function names and docstring descriptors
# =======================================================================================

# ====================While Loops======================
# Python has two primitive loop commands:
#  -> while loops
#  -> for loops

# The while Loop
# With the while loop we can execute a set of statements as long as a condition is true.
# Print i as long as i is less than 6:
i = 1
while i < 6:
  print(i)
  i += 1
"""Note :- remember to increment i, or else the loop will continue forever."""

# The break Statement
# With the break statement we can stop the loop even if the while condition is true:
# Example :- Exit the loop when i is 3:
i = 1
while i < 6:
  print(i)
  if i == 3:
    break
  i += 1

# The continue Statement
# With the continue statement we can stop the current iteration, and continue with the next:
# Example :- Continue to the next iteration if i is 3:
i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)

# The else Statement
# With the else statement we can run a block of code once when the condition no longer is true:
# Example :- Print a message once the condition is false:
i = 1
while i < 6:
  print(i)
  i += 1
else:
  print("i is no longer less than 6")
"""Note: The else block will NOT be executed if the loop is stopped by a break statement."""
# ====================While Loops End======================

# ====================For Loops======================
# A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).
# This is less like the for keyword in other programming languages, and works more like an iterator method as found in other object-orientated programming languages.
# With the for loop we can execute a set of statements, once for each item in a list, tuple, set etc.
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
"""The for loop does not require an indexing variable to set beforehand."""
# Looping Through a String :- Even strings are iterable objects, they contain a sequence of characters:
for x in "banana":
  print(x)

# The break Statement :- With the break statement we can stop the loop before it has looped through all the items:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

# Exit the loop when x is "banana", but this time the break comes before the print:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

# The continue Statement :- With the continue statement we can stop the current iteration of the loop, and continue with the next:
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    continue
  print(x)

# The range() Function
# To loop through a set of code a specified number of times, we can use the range() function,
# The range() function returns a sequence of numbers, starting from 0 by default, and increments by 1 (by default), and ends at a specified number.
for x in range(6): #Note that range(6) is not the values of 0 to 6, but the values 0 to 5.
    print(x)

# The range() function defaults to 0 as a starting value, however it is possible to specify the starting value by adding a parameter: range(2, 6), which means values from 2 to 6 (but not including 6):
for x in range(2, 6):
  print(x)

# The range() function defaults to increment the sequence by 1, however it is possible to specify the increment value by adding a third parameter: range(2, 30, 3):
for x in range(2, 30, 3): # Incrementing the sequence with 3 (default is 1):
  print(x)

# Else in For Loop
# The else keyword in a for loop specifies a block of code to be executed when the loop is finished:
for x in range(6):
  print(x)
else:
  print("Finally finished!")
"""Note: The else block will NOT be executed if the loop is stopped by a break statement."""
# Break the loop when x is 3, and see what happens with the else block:
for x in range(6):
  if x == 3: break
  print(x)
else:
  print("Finally finished!")

# Nested Loops
# A nested loop is a loop inside a loop.
# The "inner loop" will be executed one time for each iteration of the "outer loop": Print each adjective for every fruit
adj = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]
for x in adj:
  for y in fruits:
    print(x, y)

# The pass Statement
# for loops cannot be empty, but if you for some reason have a for loop with no content, put in the pass statement to avoid getting an error.
for x in [0, 1, 2]:
  pass
# ====================For Loops End======================

# ====================Python Functions======================
# A function is a block of code which only runs when it is called.
# A function can return data as a result.
# A function helps avoiding code repetition.
# Creating a Function :- In Python, a function is defined using the def keyword, followed by a function name and parentheses:
def my_function():
  print("Hello from a function")
# This creates a function named my_function that prints "Hello from a function" when called.
# The code inside the function must be indented. Python uses indentation to define code blocks.
# Calling a Function
my_function() #We can call the same function multiple times:

"""
Function Names
Function names follow the same rules as variable names in Python:
A function name must start with a letter or underscore
A function name can only contain letters, numbers, and underscores
Function names are case-sensitive (myFunction and myfunction are different)
Example
Valid function names:

calculate_sum()
_private_function()
myFunction2()
It's good practice to use descriptive names that explain what the function does.
"""

# Return Values
# Functions can send data back to the code that called them using the return statement.
# When a function reaches a return statement, it stops executing and sends the result back:
def get_greeting():
  return "Hello from a function"
message = get_greeting()
print(message)
"""Note :- If a function doesn't have a return statement, it returns None by default."""

# The pass Statement :- Function definitions cannot be empty. If you need to create a function placeholder without any code, use the pass statement:
def my_function():
  pass
# The pass statement is often used when developing, allowing you to define the structure first and implement details later.

# --------------------Function Arguments----------------------
# Information can be passed into functions as arguments. Arguments are specified after the function name, inside the parentheses. You can add as many arguments as you want, just separate them with a comma.
# The following example has a function with one argument (fname). When the function is called, we pass along a first name, which is used inside the function to print the full name:
def my_function(fname):
  print(fname + " Refsnes")
my_function("Emil")
my_function("Tobias")
my_function("Linus")


# Parameters vs Arguments
# The terms parameter and argument can be used for the same thing: information that are passed into a function.
# From a function's perspective:
# A parameter is the variable listed inside the parentheses in the function definition.
# An argument is the actual value that is sent to the function when it is called.
# Example
def my_function(name): # name is a parameter
  print("Hello", name)
my_function("Emil") # "Emil" is an argument

# Number of Arguments
# By default, a function must be called with the correct number of arguments.
# If your function expects 2 arguments, you must call it with exactly 2 arguments.
def my_function(fname, lname):
  print(fname + " " + lname)
my_function("Emil", "Refsnes") # function call
"""Note :- If you try to call the function with the wrong number of arguments, you will get an error:"""

# Default Parameter Values
# We can assign default values to parameters. If the function is called without an argument, it uses the default value:
def my_function(name = "friend"): #while defining the function, we can assign default values to parameters
  print("Hello", name)
# function calls
my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

# Keyword Arguments
# We can send arguments with the key = value syntax.
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function(animal = "dog", name = "Buddy") # function call 
# This way, with keyword arguments, the order of the arguments does not matter, check below.
my_function(name = "Buddy", animal = "dog") # function call 
"""Note :- The phrase Keyword Arguments is often shortened to kwargs in Python documentation."""

# Positional Arguments
# When we call a function with arguments without using keywords, they are called positional arguments, Positional arguments must be in the correct order:
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)
my_function("dog", "Buddy") # function call
# The order matters with positional arguments, check below.
my_function("Buddy", "dog") # function call 

# Mixing Positional and Keyword Arguments
# We can mix positional and keyword arguments in a function call. However, positional arguments must come before keyword arguments:
def my_function(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)
my_function("dog", name = "Buddy", age = 5) # function call

# Passing Different Data Types
# We can send any data type as an argument to a function (string, number, list, dictionary, etc.). The data type will be preserved inside the function:
def my_function(fruits ,person):
  print("Name:", person["name"])
  print("Age:", person["age"])
  for fruit in fruits:
    print(fruit)
my_fruits = ["apple", "banana", "cherry"]
my_person = {"name": "Emil", "age": 25}
my_function(my_fruits, my_person) # function call

# Return Values :- Functions can return values using the return statement:
def my_function(x, y):
  return x + y
result = my_function(5, 3)
print(result)

# Returning Different Data Types :- Functions can return any data type, including lists, tuples, dictionaries, and more.
def my_function():
  return ["apple", (10, 20), {"name": "Emil", "age": 25}]
fruits = my_function() # function call
print(fruits[0])
print(fruits[1])
print(fruits[2])
x, y = fruits[1]
print("x:", x)
print("y:", y)
print("Name:", fruits[2]["name"])
print("Age:", fruits[2]["age"])

# Positional-Only Arguments
# WE can specify that a function can have ONLY positional arguments.
# To specify positional-only arguments, add , / after the arguments:
def my_function(name,age, gender, /):
  print(name , age , gender)
my_function("deep" , "25" , "male")
"""Note :- With ', /' you will get an error if you try to use keyword arguments:"""

# Keyword-Only Arguments
# To specify that a function can have only keyword arguments, add *, before the arguments:
def my_function(*, name,age, gender):
  print(name , age , gender)
my_function(age = 27, gender = "F" ,name = "niki") # function call
"""Note :- With '*,' you will get an error if you try to use positional arguments:"""

# Combining Positional-Only and Keyword-Only
# You can combine both argument types in the same function.
# Arguments before / are positional-only, and arguments after * are keyword-only:
def my_function(a, b, /, *, c, d):
  return a + b + c + d
result = my_function(5, 10, c = 15, d = 20) # function call
print(result)
# --------------------Function Arguments End----------------------

# --------------------Python *args and **kwargs----------------------
# By default, a function must be called with the correct number of arguments.
# However, sometimes you may not know how many arguments that will be passed into your function.
# *args and **kwargs allow functions to accept a unknown number of arguments.

# Arbitrary Arguments - *args
# If you do not know how many arguments will be passed into your function, add a * before the parameter name.
# This way, the function will receive a tuple of arguments and can access the items accordingly:
def my_function(*kids):
  for kid in kids: 
    print(kid)
my_function("Emil", "Tobias", "Linus") # function call
"""Note :- Arbitrary Arguments are often shortened to *args in Python documentation."""

# What is *args?
# The *args parameter allows a function to accept any number of positional arguments.
# Inside the function, args becomes a tuple containing all the passed arguments:
# Accessing individual arguments from *args:
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)
my_function("Emil", "Tobias", "Linus") # function call

# Using *args with Regular Arguments
# You can combine regular parameters with *args.
# Regular parameters must come before *args:
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)
my_function("Hello", "Emil", "Tobias", "Linus") # function call
"""In this example, "Hello" is assigned to greeting, and the rest are collected in names."""

# Practical Example with *args
# *args is useful when you want to create flexible functions:
# Example :- A function that calculates the sum of any number of values:
def my_function(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function(1, 2, 3))
print(my_function(10, 20, 30, 40))
print(my_function(5))

# Finding the maximum value:
def find_max_value(*numbers):
  if len(numbers) == 0:
    print("please provide some input its an empty tuple")
    return None
  max_value = numbers[0]
  for num in numbers:
    if max_value < num : max_value = num
  return max_value
# function calls
print(find_max_value(3, 7, 2, 9, 1))
print(find_max_value(100, 20, 3000, 40))
print(find_max_value())

# Arbitrary Keyword Arguments - **kwargs
# If you do not know how many keyword arguments will be passed into your function, add two asterisks ** before the parameter name.
# This way, the function will receive a dictionary of arguments and can access the items accordingly:
# Example
# Using **kwargs to accept any number of keyword arguments:
def my_function(**kid):
  print("His last name is " + kid["lname"] , type(kid))
my_function(fname = "Tobias", lname = "Refsnes") # function call
"""Note :- Arbitrary Keyword Arguments are often shortened to **kwargs in Python documentation."""

# What is **kwargs?
# The **kwargs parameter allows a function to accept any number of keyword arguments.
# Inside the function, kwargs becomes a dictionary containing all the keyword arguments:
# Example :- Accessing values from **kwargs:
def my_function(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)
my_function(name = "deep", age = 25, city = "nagpur") # function call

# Using **kwargs with Regular Arguments
# We can combine regular parameters with **kwargs.
# Regular parameters must come before **kwargs:
def my_function(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)
my_function("deep", age = 25, city = "nagpur", hobby = "coding") # function call

"""
Combining *args and **kwargs
You can use both *args and **kwargs in the same function.
The order must be:
-> regular parameters
-> *args
-> **kwargs
"""
# Example
def my_function(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)
my_function("User Info", "Deep", "Male", age = 25, city = "nagpyr") # function call

# Unpacking Arguments
# The * and ** operators can also be used when calling functions to unpack (expand) a list or dictionary into separate arguments.
# Unpacking Lists with *, If you have values stored in a list, you can use * to unpack them into individual arguments:
def my_function(a, b, c):
  return a + b + c
numbers = [1, 2, 3]
result = my_function(*numbers) # Same as: my_function(1, 2, 3)
print(result)

# Unpacking Dictionaries with **
# If you have keyword arguments stored in a dictionary, you can use ** to unpack them:
# Example :- Using ** to unpack a dictionary into keyword arguments:
def my_function(fname, lname):
  print("Hello", fname, lname)
person = {"fname": "Deep", "lname": "Veer"}
my_function(**person) # Same as: my_function(fname="Emil", lname="Refsnes")
"""Remember: Use * and ** in function definitions to collect arguments, and use them in function calls to unpack arguments."""
# --------------------Python *args and **kwargs End----------------------

# --------------------Python Scope----------------------
# Scope :- A variable is only available from inside the region it is created. This is called scope.
# Local Scope :- A variable created inside a function belongs to the local scope of that function, and can only be used inside that function.
# Example :- A variable created inside a function is available inside that function:
def myfunc():
  x = 300
  print(x)
myfunc() # function call
"""print(x) # This will through 'NameError: name 'x' is not defined'"""

# Function Inside Function
# As explained in the example above, the variable x is not available outside the function, but it is available for any function inside the function:
def myfunc():
  x = 300
  def myinnerfunc():
    print(x)
  myinnerfunc() # function call
myfunc() # function call

# Global Scope
# A variable created in the main body of the Python code is a global variable and belongs to the global scope.
# Global variables are available from within any scope, global and local.
# Example :- A variable created outside of a function is global and can be used by anyone:
x = 300
def myfunc():
  print(x)
myfunc() # function call
print(x)

# Naming Variables
# If you operate with the same variable name inside and outside of a function, Python will treat them as two separate variables, one available in the global scope (outside the function) and one available in the local scope (inside the function):
# Example :- The function will print the local x, and then the code will print the global x:
x = 300
def myfunc():
  x = 200
  print(x)
myfunc() # function call
print(x)

# Global Keyword
# If you need to create a global variable, but are stuck in the local scope, you can use the global keyword.
# The global keyword makes the variable global.
# Example :- If you use the global keyword, the variable belongs to the global scope:
def myfunc():
  global x
  x = 300
myfunc() # function call
print(x)
# Also, use the global keyword if you want to make a change to a global variable inside a function.
# Example :- To change the value of a global variable inside a function, refer to the variable by using the global keyword:
x = 300
def myfunc():
  global x
  x = 200
myfunc() # function call
print(x)

# Nonlocal Keyword
# The nonlocal keyword is used to work with variables inside nested functions.
# The nonlocal keyword makes the variable belong to the outer function.
# Example :- If you use the nonlocal keyword, the variable will belong to the outer function:
def myfunc1():
  x = "Jane"
  def myfunc2():
    nonlocal x
    x = "hello"
  myfunc2() # function call
  return x
print(myfunc1()) # function call

"""
The LEGB Rule
Python follows the LEGB rule when looking up variable names, and searches for them in this order:
  -> Local - Inside the current function
  -> Enclosing - Inside enclosing functions (from inner to outer)
  -> Global - At the top level of the module
  -> Built-in - In Python's built-in namespace
""" 
# Example :- Understanding the LEGB rule:
x = "global"
def outer():
  x = "enclosing"
  def inner():
    x = "local"
    print("Inner:", x)
  inner()
  print("Outer:", x)
outer()
print("Global:", x)
# --------------------Python Scope End----------------------

# --------------------Python Decorators----------------------
# Decorators let you add extra behavior to a function, without changing the function's code.
# A decorator is a function that takes another function as input and returns a new function.
# Basic Decorator
# Define the decorator first, then apply it with @decorator_name above the main/primary function.
# Example :- A basic decorator that uppercases the return value of the decorated function.
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Hello Sally"
  
print(myfunction())
"""
By placing @changecase directly above the function definition, the function myfunction is being "decorated" with the changecase function.
The function changecase is the decorator.
The function myfunction is the function that gets decorated
"""

# Multiple Decorator Calls
# A decorator can be called multiple times. Just place the decorator above the function you want to decorate.
# Example :- Using the @changecase decorator on two functions:
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Hello Sally"

@changecase
def otherfunction():
  return "I am speed!"
print(myfunction())
print(otherfunction())

# Arguments in the Decorated Function
# Functions that require arguments can also be decorated, just make sure you pass the arguments to the wrapper function:
# Example :- Functions with arguments can also be decorated:
def changecase(func):
  def myinner(x):
    return func(x).upper()
  return myinner

@changecase
def myfunction(nam):
  return "Hello " + nam

print(myfunction("John"))  # function call

# *args and **kwargs
# Sometimes the decorator function has no control over the arguments passed from decorated function, to solve this problem, add (*args, **kwargs) to the wrapper function, this way the wrapper function can accept any number, and any type of arguments, and pass them to the decorated function.
# Example :- Secure the function with *args and **kwargs arguments:
def changecase(func):
  def myinner(*args, **kwargs):
    return func(*args, **kwargs).upper()
  return myinner

@changecase
def myfunction(nam):
  return "Hello " + nam

print(myfunction("John"))  # function call

# Decorator With Arguments
# Decorators can accept their own arguments by adding another wrapper level.
# Example :- A decorator factory that takes an argument and transforms the casing based on the argument value.
def changecase(n):
  def changecase(func):
    def myinner():
      if n == 1:
        a = func().lower()
      else:
        a = func().upper()
      return a
    return myinner
  return changecase

@changecase(2)
def myfunction():
  return "Hello Linus"

print(myfunction())  # function call

# Multiple Decorators
# We can use multiple decorators on one function.
# This is done by placing the decorator calls on top of each other.
# Decorators are called in the reverse order, starting with the one closest to the function.
# Example :- One decorator for upper case, and one for adding a greeting:
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

def addgreeting(func):
  def myinner():
    return "Hello " + func() + " Have a good day!"
  return myinner

@changecase
@addgreeting
def myfunction():
  return "Deep"

print(myfunction())  # function call

# Preserving Function Metadata
# Functions in Python has metadata that can be accessed using the __name__ and __doc__ attributes.
# Example :- Normally, a function's name can be returned with the __name__ attribute:
def myfunction():
  return "Have a great day!"
print(myfunction.__name__) 
# But, when a function is decorated, the metadata of the original function is lost.
# Example :- Try returning the name from a decorated function and you will not get the same result:
def changecase(func):
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Have a great day!"
print(myfunction.__name__)

# To fix this, Python has a built-in function called functools.wraps that can be used to preserve the original function's name and docstring.
# Example :- Import functools.wraps to preserve the original function name and docstring.

import functools
def changecase(func):
  @functools.wraps(func)
  def myinner():
    return func().upper()
  return myinner

@changecase
def myfunction():
  return "Have a great day!"
print(myfunction.__name__)
# --------------------Python Decorators End----------------------