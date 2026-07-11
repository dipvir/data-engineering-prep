# =======================================================================================
# PYTHON PRACTICE PART 1 STUDY INDEX: BASIC SYNTAX, VARIATION & STRING METHODS
# =======================================================================================
# * BASIC PRINTING         : Outputting text strings, numbers, math calculations, and managing quotes
# * CONFIGURING PRINTS     : Customizing row separation via sep="\n" and preserving lines via end=" "
# * SCOPE INDENTATIONS     : Using structural whitespace blocks to group code lines inside logic blocks
# * EXPLICIT CASTING       : Converting data formats explicitly using str(), int(), and float() factories
# * INTROSPECTION TOOLS    : Inspecting types via type() and listing valid object methods using dir()
# * VARIABLE NAMING LAWS   : Tracing case-sensitive assignments and casing styles (camelCase, snake_case)
# * OUTPUT CONCATENATIONS  : Mixing text and variables using automated comma spacing or explicit + signs
# * MULTI-ASSIGNMENTS      : Mapping multiple values inline or unpacking structural list elements to variables
# * SCOPE LIFECYCLES       : Modifying global scope behaviors from local scopes using global declarations
# * BUILT-IN CORE TYPES    : Auditing native standard categories (str, int, float, list, tuple, dict, set)
# * NUMERIC RANGES         : Initializing step-based immutable sequences using the range() function
# * RANDOM GENERATION      : Extracting a bounded inclusive/exclusive integer via random.randrange()
# * STRING SEQUENCES       : Traversing text characters, verifying counts with len(), and running 'in' tests
# * STRING SLICING BOUNDS  : Extracting explicit text substrings using positive and negative index slices
# * VALUE MODIFICATIONS    : Returning modified text strings via .upper(), .lower(), .strip(), and .replace()
# * STRING LAYOUT PADDING  : Centering and adjusting string layouts using .center(), .ljust(), and .rjust()
# * PATTERN MATCHING SPLITS: Cutting strings into structural list chunks via .split(), .rsplit(), and .partition()
# * CASEFOLD ALIGNMENTS    : Evaluating regional characters aggressively using case-insensitive .casefold()
# * EVALUATION CODES       : Running boolean inspection checks like .isidentifier(), .isdigit(), and .isprintable()
# * CHARACTER TRANSLATIONS : Building translation maps using str.maketrans() paired with the .translate() method
# * CHARACTER CODE MATCHES : Converting characters to unique integers and vice versa via ord() and chr()
# =======================================================================================

# just starting with printing didfferent objects
print("databricks personal account setup done")
print(2*5)
print(3)
print(358)
print(50000)
print(3 + 3)
print(2 * 5)

# if else block, its scope and indentataion syntax
if 5 > 2:
    print("Five is greater than two!") 
    if 5 > 2:
        print("Five is greater than two!") 

# defining varaible, using built in type and dir function
# sep paramater in print function
x = 5 
y = 5.32433
print(type(x),dir(x), x.is_integer(),sep= "\n")
print(type(y),dir(y), y.is_integer(),sep= "\n")
print(dir("sdsdsd"))
print(dir([]))

# Quotes in python, we can use either " double quotes or ' single quotes
print("This will work!")
print('This will also work!')

# By default, the print() function ends with a new line.
# If we want to print multiple words on the same line, we can use the 'end' parameter:
print("Hello World!", end=" ")
print("I will print on the same line.")

# casting a data type or object
x = str(3)    # x will be '3'
y = int("3")    # y will be 3
z = float(3)  # z will be 3.0
print(x,y,z)
print(type(x),type(y),type(z))

# Variable names are case-sensitive in python.
# This will create two variables:
a = 4
A = "Sally"

# Variable names with more than one word can be difficult to read.
# There are several techniques you can use to make them more readable:
# 1) Camel Case :- Each word, except the first, starts with a capital letter:
myVariableName = "John"
# 2) Pascal Case :- Each word starts with a capital letter:
MyVariableName = "John"
# 3) Snake Case :- Each word is separated by an underscore character:
my_variable_name = "John"

# we can combine text and numbers in one output by separating them with a comma:
print("I am", 35, "years old.")
# In the print() function, we can output multiple variables, separated by a comma:
x = "Python"
y = "is"
z = "awesome"
print(x, y, z)
# we can also use the + operator to output multiple variables:
x = "Python "
y = "is "
z = "awesome"
print(x + y + z) #Notice the space character after "Python " and "is ", without them the result would be "Pythonisawesome".

# Assignment of many Values to Multiple Variables in oneline
x, y, z = "Orange", "Banana", "Cherry"
print(x)
print(y)
print(z)
# Aassignment of one Value to Multiple Variables in oneline
x = y = z = "Orange"
print(x)
print(y)
print(z)
# Unpack a Collection
# If we have a collection of values in a list, tuple etc. Python allows to extract the values into variables. This is called unpacking.
fruits = ["apple", "banana", "cherry"]
x, y, z = fruits
print(x)
print(y)
print(z)

# Global Variables in python
# Variables that are created outside of a function are known as global variables.
# Global variables can be used by everyone, both inside of functions and outside.
# Creating a variable outside of a function, and use it inside the function
x = "awesome"

def myfunc():
  print("Python is " + x)

myfunc()
# If you create a variable with the same name inside a function, this variable will be local, and can only be used inside the function. The global variable with the same name will remain as it was, global and with the original value.
# Creating a variable inside a function, with the same name as the global variable
x = "awesome"

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)
# Normally, when you create a variable inside a function, that variable is local, and can only be used inside that function.
# To create a global variable inside a function, you can use the global keyword.
# If you use the global keyword, the variable belongs to the global scope:
def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)
# To change the value of a global variable inside a function, refer to the variable by using the global keyword:
x = "awesome" # global variable

def myfunc():
  global x
  x = "fantastic"

myfunc()

print("Python is " + x)

# Built-in Data Types
# In programming, data type is an important concept.
# Variables can store data of different types, and different types can do different things.
# Python has the following data types built-in by default, in these categories:
"""Text Type:	str
Numeric Types:	int, float, complex
Sequence Types:	list, tuple, range
Mapping Type:	dict
Set Types:	set, frozenset
Boolean Type:	bool
Binary Types:	bytes, bytearray, memoryview
None Type:	NoneType"""

# Setting the Data Type
# In Python, the data type is set when you assign a value to a variable:
"""Example	          Data Type	
x = "Hello World"	str	
x = 20	int	
x = 20.5	float	
x = 1j	complex	
x = ["apple", "banana", "cherry"]	list	
x = ("apple", "banana", "cherry")	tuple	
x = range(6)	range	
x = {"name" : "John", "age" : 36}	dict	
x = {"apple", "banana", "cherry"}	set	
x = frozenset({"apple", "banana", "cherry"})	frozenset	
x = True	bool	
x = b"Hello"	bytes	
x = bytearray(5)	bytearray	
x = memoryview(bytes(5))	memoryview	
x = None	NoneType"""

# range data type related
print(range(5))
print(dir(range(5)))
print(type(range(5)))
print(list(range(5))) # be default start is 0 for range
print(list(range(3,15)))
print(list(range(3,15,2)))

# Random Number
# Python does not have a random() function to make a random number, but Python has a built-in module called random that can be used to make random numbers:
import random
print(random.randrange(1, 6)) # start inclusive and end exclusive

# Strings are Arrays
# Like many other popular programming languages, strings in Python are arrays of unicode characters.
# However, Python does not have a character data type, a single character is simply a string with a length of 1.
# Square brackets can be used to access elements of the string.
a = "Hello, World!"
print(a[1])
# Since strings are arrays, we can loop through the characters in a string, with a for loop.
for x in "banana":
  print(x)
print(len(a)) #The len() function returns the length of a string:
# To check if a certain phrase or character is present in a string, we can use the keyword 'in'.
txt = "The best things in life are free!"
print("free" in txt)
# Use it in an if statement:
if "free" in txt:
  print("Yes, 'free' is present.")
# To check if a certain phrase or character is NOT present in a string, we can use the keyword 'not in'.
print("expensive" not in txt)
# Use it in an if statement:
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")

# Strings Slicing
# we can return a range of characters by using the slice syntax.
# Specify the start index and the end index, separated by a colon, to return a part of the string.
b = "Hello, World!"
print(b[2:5]) #Gets the characters from position 2 to position 4
# Note: The first character has index 0.
# To get the characters from the start to position 4
print(b[:5])
# To get the characters from position 2, and all the way to the end of the string
print(b[2:])
# Use negative indexes to start the slice from the end of the string
print(b[-5:-2]) #Gets the characters from position -5 to position -3

# -------------String Methods-------------
# Python has a set of built-in methods that you can use on strings.
# Strings in Python are immutable, so this methods return a new string instead of modifying the original string.
a = "  Hello, World!   "
b = "Hello, World!"
print(b.capitalize()) #The capitalize() method returns the string with its first character capitalized.
print(a.upper()) #The upper() method returns the string in upper case:
print(a.lower()) #The lower() method returns the string in lower case:
print(a.strip()) #The strip() method removes any whitespace from the beginning or the end:
print(b.center(20)) #The center() method will center align the string, using a specified character (space is default) as the fill character
print(b.center(20, "-")) #The center() method also takes the character paramter to fill the void with:
print(b.count("l")) #The count() method returns the number of times a specified value appears in the string:
# count takes two more optional parameters start and end, which are used to specify the range of the search.
print(b.count("o", 3, 11)) #here count searches between index 3 and 10
print(b.endswith("d!")) #The endswith() method returns True if the string ends with the specified character value, otherwise False:
print(a.replace("H", "J")) #The replace() method replaces a string with another string:
# The split() method splits a string into a list.
# we can specify the separator, default separator is any whitespace.
print(f"default space separator behavior, {a.split()}") #The split() method splits the string into substrings if it finds instances of the separator:
# by default it splits by space and removes all the spaces, while when we explicitlly pass a space as separator it does not remove the spaces
print(f"Explicitlly provided space separator behavior, {a.split(" ")}")
#other separator example
print(a.split(","))
# so there's one more optional paramter apart from 'sep' in split() i.e maxsplit which is the number of splits to do, default value is -1, which is "all occurrences"
txt = "hello, my name is Peter, I am 26 years old"
print(txt.split(", "))
print(txt.split(", ", 1)) # setting the maxsplit parameter to 1, will return a list with 2 elements!
# Casefold method explanation
# lower() vs. casefold()
# =====================================================================
# 1. .lower()   -> Standard lowercase conversion (A-Z to a-z). 
#                  Ignores complex regional/international characters.
#
# 2. .casefold() -> Aggressive lowercase conversion (Deletes ALL case distinctions).
#                  Converts complex regional characters into universal equivalents.
#
# USE CASE: Always use .casefold() for strict, case-insensitive string matching 
#           or data cleaning when dealing with international data.
# =====================================================================
text1 = "Straße"  # Lowercase German 'ß'
text2 = "STRASSE" # Uppercase German 'SS'
print(text1.lower() == text2.lower())       # False ('straße' != 'strasse')
print(text1.casefold() == text2.casefold()) # True  ('strasse' == 'strasse')

# =====================================================================
# REMAINING STRING METHODS QUICK REFERENCE
# =====================================================================
txt = "hello, my name is Peter, I am 26 years old"
print(txt.encode(encoding="utf-8")) # encode() returns an encoded version of the string
print("H\te\tl\tl\to".expandtabs(3)) # expandtabs() sets the tab size of the string
print(txt.find("Peter")) # find() searches for a value and returns its index. Returns -1 if not found.
print("Age is {0}".format(26)) # format() formats specified values in a string
print("Name: {name}".format_map({'name': 'Peter'})) # format_map() formats specified values from a dictionary

print(txt.index("Peter")) # index() searches for a value and returns its index. Throws an error if not found.
print(txt.isalnum()) # isalnum() returns True if all characters are alphanumeric (letters or numbers)
print(txt.isalpha()) # isalpha() returns True if all characters are in the alphabet
print(txt.isascii()) # isascii() returns True if all characters are ASCII characters
print(txt.isdecimal()) # isdecimal() returns True if all characters are decimals
print(txt.isdigit()) # isdigit() returns True if all characters are digits
print(txt.isidentifier()) # isidentifier() returns True if the string is a valid Python identifier

print(txt.islower()) # islower() returns True if all characters are lower case
print(txt.isnumeric()) # isnumeric() returns True if all characters are numeric
print(txt.isprintable()) # isprintable() returns True if all characters are printable (Non-printable characters examples :- \n (Newline / Line break), \t (Tab space), \r (Carriage return))
print(txt.isspace()) # isspace() returns True if all characters are whitespaces
print(txt.istitle()) # istitle() returns True if the string follows the rules of Title Case
print(txt.isupper()) # isupper() returns True if all characters are upper case

print(", ".join(["Python", "SQL"])) # join() converts elements of an iterable (like a list) into a string using a separator
print(txt.ljust(50, "-")) # ljust() returns a left-justified version of the string
print(txt.lstrip()) # lstrip() returns a left trim version (removes leading spaces only)
print(txt.partition("is")) # partition() splits string at first occurrence of separator and returns a 3-item tuple

print(txt.rfind("e")) # rfind() searches for a value and returns the LAST position index
print(txt.rindex("e")) # rindex() searches for a value and returns the LAST position index (errors out if not found)
print(txt.rjust(50, "-")) # rjust() returns a right-justified version of the string
print(txt.rpartition("is")) # rpartition() splits string at last occurrence of separator and returns a 3-item tuple
print(txt.rsplit(", ", 1)) # rsplit() splits the string at the specified separator starting from the right
print(txt.rstrip()) # rstrip() returns a right trim version (removes trailing spaces only)

print(txt.splitlines()) # splitlines() splits the string at line breaks (\n) and returns a list
print(txt.startswith("hello")) # startswith() returns True if the string starts with the specified value
print(txt.swapcase()) # swapcase() swaps cases, lower case becomes upper case and vice versa
print(txt.title()) # title() converts the first character of each word to upper case
# maketrans() returns a translation table to be used in translate()
print(txt.translate(str.maketrans("hy", "Ju"))) # translate() returns a translated string using a map from maketrans()
print("45".zfill(5)) # zfill() fills the string with a specified number of 0 values at the beginning -> '00045'
# ------------String Methods End-------------------

# String Concatenation and ord, chr functions use in python
# To concatenate, or combine, two strings we can use the + operator.
a = "Hello"
b = "World"
c = a + b
print(c)
# To add a space between them, add a " ":
c = a + " " + b
print(c)

# ord, chr functions use in python
print(ord("A")) #ord function convert char to int
print(chr(97)) #chr funtion convert int to char
for i in range(65,65+26):
  print(chr(i),end=" ")

print()

for i in range(97,97+26):
  print(chr(i),end=" ")
# -----------------End-----------------------

# ------------------Python File Handling----------------------  
# File handling is an important part of any web application.
# Python has several functions for creating, reading, updating, and deleting files.

"""File Handling"""
# The key function for working with files in Python is the open() function.
# The open() function takes two parameters; filename, and mode.

# There are four different methods (modes) for opening a file:
#  -> "r" - Read - Default value. Opens a file for reading, error if the file does not exist
#  -> "a" - Append - Opens a file for appending, creates the file if it does not exist
#  -> "w" - Write - Opens a file for writing, creates the file if it does not exist
#  -> "x" - Create - Creates the specified file, returns an error if the file exists
"""In addition you can specify if the file should be handled as binary or text mode"""
# -> "t" - Text - Default value. Text mode
# -> "b" - Binary - Binary mode (e.g. images)

"""Syntax to open a file for reading it is enough to specify the name of the file:"""
f = open("demofile.txt")
print(f , dir(f) ,sep = "\n")
# The code above is the same as:
f = open("demofile.txt", "rt")
# Because "r" for read, and "t" for text are the default values, you do not need to specify them.
"""Note: Make sure the file exists, or else you will get an error."""

"""Open a File on the Server"""
# Assume we have the following file, located in the same folder as Python:
#  -> demofile.txt
"""
Hello! Welcome to demofile.txt
This file is for testing purposes.
Good Luck!
"""
# To open the file, use the built-in open() function.
# The open() function returns a file object, which has a read() method for reading the content of the file:
f = open("demofile.txt")
print(f.read() , type(f.read()) , sep = "\n")

# If the file is located in a different location, you will have to specify the file path, like this:
"""Example :- Open a file on a different location:"""
f = open("/Workspace/Users/dipvirmani28@gmail.com/Drafts/dummytextfile.txt")
print(f.read())

"""Using the with statement"""
# We can also use the with statement when opening a file:
with open("demofile.txt") as f:
  print(f.read())
"""Then you do not have to worry about closing your files, the with statement takes care of that."""

"""Close Files"""
# It is a good practice to always close the file when you are done with it.
# If you are not using the with statement, you must write a close statement in order to close the file:
"""Example :- Close the file when you are finished with it:"""
f = open("demofile.txt")
print(f.read())
f.close()
"""Note: You should always close your files. In some cases, due to buffering, changes made to a file may not show until you close the file."""

"""Read Only Parts of the File"""
# By default the read() method returns the whole text, but you can also specify how many characters you want to return:
"""Example :- Return the 5 first characters of the file:"""
with open("demofile.txt") as f:
  print(f.read(5))

"""Read Lines"""
# We can return one line by using the readline() method:
with open("demofile.txt") as f:
  print(f.readline())

# By calling readline() two times, you can read the two first lines:
"""Example :- Read two lines of the file:"""
with open("demofile.txt") as f:
  print(f.readline())
  print(f.readline())

# By looping through the lines of the file, you can read the whole file, line by line:
"""Example :- Loop through the file line by line:"""
with open("demofile.txt") as f:
  for x in f:
    print(x)

"""Python Write/Create Files"""
# Write to an Existing File
# To write to an existing file, you must add a parameter to the open() function:
#  -> "a" - Append - will append to the end of the file
#  -> "w" - Write - will overwrite any existing content
"""Example :- Open the file "demofile.txt" and append content to the file:"""
with open("demofile.txt", "a") as f:
  f.write("Now the file has more content!")

#open and read the file after the appending:
with open("demofile.txt") as f:
  print(f.read())

"""Overwrite Existing Content"""
# To overwrite the existing content to the file, use the w parameter:
"""Example :- Open the file "demofile.txt" and overwrite the content:"""
with open("demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

#open and read the file after the overwriting:
with open("demofile.txt") as f:
  print(f.read())
"""Note: the "w" method will overwrite the entire file."""

"""Create a New File"""
# To create a new file in Python, use the open() method, with one of the following parameters:
#  -> "x" - Create - will create a file, returns an error if the file exists
#  -> "a" - Append - will create a file if the specified file does not exists
#  -> "w" - Write - will create a file if the specified file does not exists
"""Example :- Create a new file called "myfile.txt":"""
f = open("myfile.txt", "x")
# Result: a new empty file is created.
"""Note: If the file already exists, an error will be raised."""

"""Python Delete File"""
# To delete a file, you must import the OS module, and run its os.remove() function:
"""Example :- Remove the file "demofile.txt":"""
import os
os.remove("demofile.txt")

"""Check if File exist:"""
# To avoid getting an error, you might want to check if the file exists before you try to delete it:
"""Example :- Check if file exists, then delete it:"""
import os
if os.path.exists("myfile.txt"):
  os.remove("myfile.txt")
else:
  print("The file does not exist")

"""Delete Folder"""
# To delete an entire folder, use the os.rmdir() method:
"""Example :- Remove the folder 'dummyfolder'"""
import os
os.rmdir("dummyfolder")
"""Note: You can only remove empty folders."""
# ------------------Python File Handling End----------------------  


