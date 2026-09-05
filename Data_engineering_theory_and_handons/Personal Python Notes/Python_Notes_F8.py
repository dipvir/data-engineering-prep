# =======================================================================================
# PYTHON PRACTICE PART 8 STUDY INDEX: SYSTEM UTILITIES & EXCEPTION ARCHITECTURES
# =======================================================================================
# * CODE LIBRARIES        : Importing custom standalone .py code modules and invoking elements via dot notation
# * NAMESPACE ALIASING    : Mapping modular namespaces cleanly to simplified shortcuts using the 'as' keyword
# * SYSTEM INSPECTIONS    : Extracting active environment details and hardware platform indicators via platform
# * DIRECTORY DISCOVERY   : Using dir() to audit valid methods across text streams, integers, and dynamic modules
# * COMPONENT EXTRACTIONS : Pulling explicit dictionary targets directly into local scopes using from keywords
# * DATE OBJECT BUILDERS  : Constructing specific fixed date timestamps using three mandatory constructor arguments
# * TIMEZONE AWARENESS    : Resolving naive cloud anomalies by binding explicit IANA strings via ZoneInfo
# * THE STRFTIME PIPELINE : Converting operational datetime objects into custom formatted text display strings
# * THE STRPTIME ENGINE   : Parsing incoming raw text rows dynamically back into active datetime objects in memory
# * MATHEMATICAL ENGINES  : Running core built-in operations like min(), max(), abs(), and powered pow() equations
# * MATH ALGORITHM ROLES  : Invoking module equations to isolate square roots or rounding values via ceil()/floor()
# * JSON DATA DE-SERIAL   : Parsing structural raw text string payloads into local Python dictionaries via loads()
# * JSON DATA SERIALIZE   : Converting native compound maps into valid exported JSON text strings using dumps()
# * ENCODING EXTENSIONS   : Formatting serialization layouts cleanly using custom indent rules and sorted keys
# * REGEX MODULE RE       : [SKIPPED / LEFT INCOMPLETE FOR DATA ENGINEERING INTERVIEW STRATEGY INTERLUDE]
# * PIP MODULE UTILITIES  : Managing external library spaces, auditing versions, and running terminal lists
# * EXCEPTION HANDLING    : Wrapping fragile execution trees inside safe try-except error catching channels
# * ERROR SPECIFICITY     : Tracking explicit errors like NameError blocks while routing alternative fallbacks
# * FALLBACK ELSE CHAINS  : Triggering distinct post-evaluation code blocks strictly when zero exceptions occur
# * GUARANTEED FINALLY    : Enforcing mandatory resource cleanup tasks regardless of upstream execution errors
# * ATTRIBUTE STATUSES    : Querying the boolean .closed flag to verify successful system resource disconnections
# * ENFORCED EXCEPTIONS   : Terminating pipeline runs manually by throwing deliberate errors using raise actions
# * STRING FORMATTING     : [SKIPPED / LEFT INCOMPLETE FOR DATA ENGINEERING INTERVIEW STRATEGY INTERLUDE]
# * ABSENCE REPR NONE     : Tracking data absence or unreturned functional states natively using NoneType constants
# * INTERACTIVE INPUTS    : Pausing active execution lines to collect human keyboard string details via input()
# * STREAM VALIDATIONS    : Combining infinite while loops with try-except validation blocks to parse numerical inputs
# =======================================================================================

# =====================Python Modules======================
# What is a Module?
# Consider a module to be the same as a code library.
# A file containing a set of functions you want to include in your application.

# How to Create a Module
# To create a module just save the code you want in a file with the file extension .py:
"""Example :- Save this code in a file named my_first_module.py"""
"""
def greeting(name):
  print("Hello, " + name)
"""

# Using the Module
# Now we can use the module we just created, by using the import statement:
# Example :- Import the module named my_first_module, and call the greeting function:
import my_first_module
my_first_module.greeting("Dipesh")
"""Note: When using a function from a module, use the syntax: module_name.function_name."""

# Variables in Module
# The module can contain functions, as already described, but also variables of all types (arrays, dictionaries, objects etc):
"""Example :- Save this code in the file my_first_module.py"""
"""
person1 = {
  "name": "John",
  "age": 36,
  "country": "Norway"
}
"""
"Example :- Import the module named my_first_module, and access the person1 dictionary:"
import my_first_module
print(my_first_module.person1)
print(my_first_module.person1["age"])

# Naming a Module
# We can name the module file whatever you like, but it must have the file extension .py
# Re-naming a Module
# We can create an alias when you import a module, by using the 'as' keyword:
"""Example :- Create an alias for my_first_module called mfm:"""
import my_first_module as mfm
a = mfm.person1["age"]
print(a)

# Built-in Modules
# There are several built-in modules in Python, which you can import whenever you like.
# Example :- Import and use the platform module:
import platform
x = platform.system()
print(x)

# Using the dir() Function
# There is a built-in function to list all the function names (or variable names) in a module. The dir() function:
# Example :- List all the defined names belonging to the platform module:
import platform
print(dir(platform),end = "\n\n")
# below part i added from my side on dir function usage
print(dir("dsdsdsd"),end = "\n\n")
print(dir(121),end = "\n\n")
print(dir(["dsdsdsd" , "sdsd" , 1 , [1,2,3]]))
"""Note: The dir() function can be used on all modules, also the ones you create yourself."""

# Import From Module
# We can choose to import only parts from a module, by using the 'from' keyword.
"""Example :- The module named my_first_module has one function and one dictionary:"""
"""
def greeting(name):
  print("Hello, " + name)

person1 = {
  "name": "John",
  "age": 36,
  "country": "Norway"
}
"""
"""Example :- Import only the person1 dictionary from the module:"""
from my_first_module import person1
print(person1["age"])
print(person1)
"""Note: When importing using the from keyword, do not use the module name when referring to elements in the module. Example: person1["age"], not mymodule.person1["age"]"""
# =====================Python Modules End======================

# =====================Python Datetime module ======================
# Python Dates
# A date in Python is not a data type of its own, but we can import a module named datetime to work with dates as date objects.
"""Example :- Import the datetime module and display the current date:"""
import datetime
x = datetime.datetime.now()
print(type(x))
print(x)
print(dir(datetime.datetime))
# Return the year and name of weekday:
print(x.year)
print(x.strftime("%A"))
"Note :- The above will not give timestamp related to our current location, it gives remote cloud server location timestamp"

# If We want the output to match our local timezone, we need to explicitly make our code "timezone-aware."
# In standard Python development, the cleanest and most modern way to handle this is by using the built-in 'zoneinfo' module paired with a timezone database identifier.
# 🕒 The Python Solution: Timezone-Aware Datetime
# Here is how we can update our code block to pull your specific local time, regardless of where your Databricks cluster is hosted in the world:
import datetime
from zoneinfo import ZoneInfo

# 1. Get the current time in UTC (Universal standard)
utc_time = datetime.datetime.now(ZoneInfo("UTC"))
print("Server UTC Time:  ", utc_time)
"""
Note: On a cloud server set to UTC, both commands print the same numbers. However, datetime.now() creates a naive object (no timezone label), while datetime.now(ZoneInfo("UTC")) creates an aware object (has a locked UTC label). Python treats them as completely different data forms in memory.
"""

# 2. Convert or fetch directly in your local timezone 
# (e.g., "Asia/Kolkata" for India Standard Time)
local_time = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
print("My Actual Local Time:", local_time)
print(type(local_time))

# 3. Format it beautifully for display
print("Formatted Local: ", local_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
print(type(local_time.strftime("%Y-%m-%d %H:%M:%S %Z")))

# Creating Date Objects
# To create a date, we can use the datetime() class (constructor) of the datetime module.
# The datetime() class requires three parameters to create a date: year, month, day.
"""Example :- Create a date object:"""
import datetime
x = datetime.datetime(2020, 5, 17)
print(x)
print(type(x))
"""The datetime() class also takes parameters for time and timezone (hour, minute, second, microsecond, tzone), but they are optional, and has a default value of 0, (None for timezone)."""

"""USE OF STRFTIME AND STRPTIME FROM GEMINI"""
# An easy way to never forget the difference between strftime and strptime is to focus entirely on the "f" and the "p" in their names:
  # strftime -> String From Datetime (Format)
  # strptime -> String Passed into Datetime (Parse)

"""1. strftime() — String From Datetime (Formatting)"""
# Use this when you already have a Python datetime object, and you want to convert it into a beautiful, human-readable string (like for a report or a filename).
import datetime
# 1. Start with a datetime object
now = datetime.datetime.now()
# 2. Convert it TO a string format
clean_string = now.strftime("%Y-%m-%d %H:%M:%S")
print(type(now))          # Output: <class 'datetime.datetime'>
print(clean_string)       # Output: "2026-05-24 10:41:25"
print(type(clean_string)) # Output: <class 'str'>

"""2. strptime() — String Passed into Datetime (Parsing)"""
# Use this when you are reading raw data (like a column from a CSV file or an API JSON payload) where the date is just text, and you need to convert it into an actual Python datetime object so you can do math or comparisons on it.
import datetime
# 1. Start with a raw text string
raw_log_date = "24/05/2026 14:30:00"
# 2. Tell Python exactly how to parse the pattern
datetime_object = datetime.datetime.strptime(raw_log_date, "%d/%m/%Y %H:%M:%S")
print(type(raw_log_date))    # Output: <class 'str'>
print(datetime_object)       # Output: 2026-05-24 14:30:00
print(type(datetime_object)) # Output: <class 'datetime.datetime'>

"""🎨 Quick Codebook Cheat Sheet for Your Notes"""
# Both methods use the exact same percentage (%) codes to map out where the numbers sit. Here are the main ones you will use 90% of the time:
"""
=====================================================================
CORE STRFTIME / STRPTIME TOKEN QUICK-REFERENCE
=====================================================================
 %Y -> 4-Digit Century Year             (e.g., 2026)
 %y -> 2-Digit Shortened Year           (e.g., 26)
 %m -> 2-Digit Numeric Month            (e.g., 05)
 %M -> 2-Digit Numeric Minute           (e.g., 30)
 %d -> 2-Digit Numeric Day of Month     (e.g., 24)
 %H -> 2-Digit 24-Hour Clock Hour       (e.g., 14)
 %S -> 2-Digit Numeric Second           (e.g., 00)
=====================================================================

1. CORE TOKEN CASE-SENSITIVITY LAWS
---------------------------------------------------------------------
Python time tokens are strictly case-sensitive. Changing a token's case 
shifts its programmatic instruction to a completely different layout rule.
Swapping letter cases will cause corrupted data readings or script crashes.

THE MONTH VS. MINUTE CLASH:
%m (Lowercase) -> Represents a 2-digit numeric Month (e.g., 05)
%M (Uppercase) -> Represents a 2-digit numeric Minute (e.g., 30)

THE CENTURY YEAR CLASH:
%y (Lowercase) -> Represents a 2-digit shortened Year (e.g., 26)
%Y (Uppercase) -> Represents a 4-digit full century Year (e.g., 2026)

THE CLOCK SYSTEM CLASH:
%H (Uppercase) -> Represents a 24-hour military clock hour (00 to 23)
%I (Uppercase) -> Represents a 12-hour standard clock hour (01 to 12)
"""
"""📌 Short Summary for Your Notes:"""
# strftime(): Takes a datetime object → Outputs a formatted String.
# strptime(): Takes a raw text String → Parses it into a Datetime object.

# The strftime() Method
# The datetime object has a method for formatting date objects into readable strings.
# The method is called strftime(), and takes one parameter, format, to specify the format of the returned string:
"""Example :- Display the name of the month:"""
import datetime
x = datetime.datetime(2018, 6, 1)
print(x.strftime("%B"))
"""Note :- I have put reference of all the legal format codes in file Python_Notes_File_Extra_Content.py"""
# =====================Python Datetime module End======================

# =====================Python Math Functions And Module======================
# Python has a set of built-in math functions, including an extensive math module, that allows you to perform mathematical tasks on numbers.

"""Built-in Math Functions"""
# The min() and max() functions can be used to find the lowest or highest value in an iterable:
x = min(5, 10, 25)
y = max(5, 10, 25)
print(x)
print(y)

# The abs() function returns the absolute (positive) value of the specified number:
x = abs(-7.25)
print(x)

# The pow(x, y) function returns the value of x to the power of y (xy).
"""Example :- Return the value of 4 to the power of 3 (same as 4 * 4 * 4):"""
x = pow(4, 3)
print(x)

"""The Math Module"""
# Python has also a built-in module called math, which extends the list of mathematical functions.
# To use it, we must import the math module:
import math
# When we have imported the math module, we can start using methods and constants of the module.
"""Example :- The math.sqrt() method for example, returns the square root of a number:"""
import math
x = math.sqrt(64)
print(x)

"""Example :- The math.ceil() method rounds a number upwards to its nearest integer, and the math.floor() method rounds a number downwards to its nearest integer, and returns the result:"""
import math
x = math.ceil(1.4)
y = math.floor(1.4)
print(x) # returns 2
print(y) # returns 1

"""Example :- The math.pi constant, returns the value of PI (3.14...)"""
import math
x = math.pi
print(x)
"""
Note :- Complete Math Module Reference
In W3school Math Module Reference you will find a complete reference of all methods and constants that belongs to the Math module.
"""
# =====================Python Math Functions And Module End======================

# =====================Python Json Package/Module======================
# JSON is a syntax for storing and exchanging data.
# JSON is text, written with JavaScript object notation.
# JSON in Python
# Python has a built-in package called json, which can be used to work with JSON data.
"""Example :- Import the json module:"""
import json
# Parse JSON - Convert from JSON to Python
# If you have a JSON string, you can parse it by using the json.loads() method.
# The result will be a Python dictionary.
"""Example :- Convert from JSON to Python:"""
import json
x = '{"name":"John", "age":30, "city":"New York"}' # some JSON:
print(type(x))
y = json.loads(x) # parse x:
print(y["age"]) # the result is a Python dictionary:

# Convert from Python to JSON
# If you have a Python object, you can convert it into a JSON string by using the json.dumps() method.
"""Example :- Convert from Python dictionary to JSON:"""
import json
# A Python object (dict):
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
y = json.dumps(x) # convert into JSON:
print(y) # the result is a JSON string:
print(type(y)) # <class 'str'>

"""
We can convert Python objects of the following types, into JSON strings:
dict
list
tuple
string
int
float
True
False
None
"""

"""Example :- Convert Python objects into JSON strings, and print the values:"""
import json
print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

"""When you convert from Python to JSON, Python objects are converted into the JSON (JavaScript) equivalent:"""
# Python      ->      JSON
# -------------------------------
# dict        ->      Object
# list        ->      Array
# tuple       ->      Array
# str         ->      String  
# int         ->      Number
# float       ->      Number
# True        ->      true
# False       ->      false
# None        ->      null

"""Example :- Convert a Python object containing all the legal data types:"""
import json
x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}
print(json.dumps(x) , type(json.dumps(x) ) , sep = "\n")

# Format the Result
# The example above prints a JSON string, but it is not very easy to read, with no indentations and line breaks.
# The json.dumps() method has parameters to make it easier to read the result:
"""Example :- Use the indent parameter to define the numbers of indents:"""
print(json.dumps(x, indent=4))

# We can also define the separators, default value is (", ", ": "), which means using a comma and a space to separate each object, and a colon and a space to separate keys from values:
"""Example :- Use the separators parameter to change the default separator:"""
print(json.dumps(x, indent=4, separators=(". ", " = ")))

# Order the Result
# The json.dumps() method has parameters to order the keys in the result:
"""Example :- Use the sort_keys parameter to specify if the result should be sorted or not:"""
print(json.dumps(x, indent=4, sort_keys=True))
# =====================Python Json Package/Module End======================

# =====================Python RegEx/re module======================
# A RegEx, or Regular Expression, is a sequence of characters that forms a search pattern.
# RegEx can be used to check if a string contains the specified search pattern.
# RegEx Module
# Python has a built-in package called re, which can be used to work with Regular Expressions.
# Importing the re module:
import re
"""Example :- Search the string to see if it starts with "The" and ends with "Spain":"""
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
print(x)

# =====================Python RegEx/re module Leaving Incomplete======================

# =====================Python PIP======================
"""What is PIP?"""
# PIP is a package manager for Python packages, or modules if you like.
"""Note: If you have Python version 3.4 or later, PIP is included by default."""
#  All the below are commands not code so we have to use it in cmd or powershell terminals.

"""What is a Package?"""
# A package contains all the files you need for a module.
# Modules are Python code libraries you can include in your project.
# Check if PIP is Installed 
# Navigate your command line to the location of Python's script directory, and type the following:
#  -> pip --version

"""Download a Package"""
# Downloading a package is very easy.
# Open the command line interface and tell PIP to download the package you want.
# Navigate your command line to the location of Python's script directory, and type the following:
# """Example :- Download a package named "camelcase":"""
#  -> pip install camelcase

"""Using a Package"""
# Once the package is installed, it is ready to use.
# Import the "camelcase" package into your project.
"""Example :- Import and use "camelcase":"""
import camelcase
c = camelcase.CamelCase()
txt = "hello world"
print(c.hump(txt))

"""Remove a Package"""
# Use the uninstall command to remove a package:
"""Example :- Uninstall the package named "camelcase":"""
# -> pip uninstall camelcase
# The PIP Package Manager will ask you to confirm that you want to remove the camelcase package:
# Press y and the package will be removed.

"""List Packages"""
# Use the list command to list all the packages installed on your system:
"""Example :- List installed packages:"""
# -> pip list
# =====================Python PIP End======================

# =====================Python Try Except======================
# The try block lets you test a block of code for errors.
# The except block lets you handle the error.
# The else block lets you execute code when there is no error.
# The finally block lets you execute code, regardless of the result of the try- and except blocks.

"""Exception Handling"""
# When an error occurs, or exception as we call it, Python will normally stop and generate an error message.
# These exceptions can be handled using the try statement:
"""Example :- The try block will generate an exception, because x is not defined:"""
try:
  print(x)
except:
  print("An exception occurred")
# Since the try block raises an error, the except block will be executed.
# Without the try block, the program will crash and raise an error:
"""Example :- This statement will raise an error, because x is not defined:"""
print(x)

"""Many Exceptions"""
# You can define as many exception blocks as you want, e.g. if you want to execute a special block of code for a special kind of error:
"""Example :- Print one message if the try block raises a NameError and another for other errors:"""
try:
  print(x)
except NameError:
  print("Variable x is not defined")
except:
  print("Something else went wrong")
"""To check more Error types go to w3schools Python Built-in Exceptions Reference."""

"""Else Block"""
# We can use the else keyword to define a block of code to be executed if no errors were raised:
"""Example :- In this example, the try block does not generate any error:"""
try:
  print("Hello")
except:
  print("Something went wrong")
else:
  print("Nothing went wrong")

"""Finally Block"""
# The finally block, if specified, will be executed regardless if the try block raises an error or not.
try:
  print(x)
except:
  print("Something went wrong")
finally:
  print("The 'try except' is finished")

"""
This can be useful to close objects and clean up resources:
Example :- Try to open and write to a file that is not writable:
"""
try:
  f = open("demofile.txt") # Read-Only Mode (mode="r").
  print(f)
  try:
    f.write("Lorum Ipsum") # Throws error because file is opend in read-only mode
  except:
    print("Something went wrong when writing to the file")
  finally:
    f.close()
except:
  print("Something went wrong when opening the file")
# This attribute evaluates to True if the file has been successfully closed and released from memory, and False if the connection is still active.
print(f.closed)
"""As f.close() is used The program can continue, without leaving the file object open."""

"""Raise an exception"""
# As a Python developer you can choose to throw an exception if a condition occurs.
# To throw (or raise) an exception, use the raise keyword.
"Example :- Raise an error and stop the program if x is lower than 0:"
x = -1
if x < 0:
  raise Exception("Sorry, no numbers below zero")

# The 'raise' keyword is used to raise an exception.
# You can define what kind of error to raise, and the text to print to the user.
"""Example :- Raise a TypeError if x is not an integer:"""
x = "hello"
if not type(x) is int:
  raise TypeError("Only integers are allowed")
# =====================Python Try Except End======================

# =====================Python String Formatting======================
# F-String was introduced in Python 3.6, and is now the preferred way of formatting strings.
# Before Python 3.6 we had to use the format() method.
# F-Strings
# F-string allows us to format selected parts of a string.
# To specify a string as an f-string, simply put an f in front of the string literal, like this:
"""Example :- Create an f-string:"""
txt = f"The price is {49} dollars"
print(txt)

"""Placeholders and Modifiers"""
# To format values in an f-string, add placeholders {}, a placeholder can contain variables, operations, functions, and modifiers to format the value.
"""Example :- Add a placeholder for the price variable:"""
price = 59
txt = f"The price is {price} dollars"
print(txt)
# =====================Python String Formatting Leaving Incomplete======================

# =====================Python None======================
# None is a special constant in Python that represents the absence of a value.
# Its data type is 'NoneType', and None is the only instance of a NoneType object.
"""NoneType"""
# Variables can be assigned None to indicate "no value" or "not set".
"""Example :- Assign and display a None value:"""
x = None
print(x , type(x) ,sep = "\n")

"""Comparing to None"""
# To compare a value to None, use the identity operator 'is' or 'is not'
"""Example :- Use the identity operator is for comparisons with None:"""
result = None
if result is None:
  print("No result yet")
else:
  print("Result is ready")

"""Example :- Similar example, but using is not instead:"""
result = None
if result is not None:
  print("Result is ready")
else:
  print("No result yet")

"""True or False, None evaluates to False in a boolean context."""
print(bool(None))

"""Functions returning None"""
# Functions that do not explicitly return a value return None by default.
"""Example :- A function without a return statement returns None:"""
def myfunc():
  x = 5
x = myfunc() #Function Call
print(x)
# =====================Python None End======================

# =====================Python User Input======================
# Python allows for user input.
# That means we are able to ask the user for input.
# The following example asks for your name, and when you enter a name, it gets printed on the screen:
print("Enter your name:")
name = input()
print(f"Hello {name}")
"""Python stops executing when it comes to the input() function, and continues when the user has given some input."""

"""Using prompt"""
# In the example above, the user had to input their name on a new line. The Python input() function has a prompt parameter, which acts as a message you can put in front of the user input, on the same line:
"""Example :- Add a message in front of the user input:"""
name = input("Enter your name:")
print(f"Hello {name}")

"""Multiple Inputs"""
# We can add as many inputs as you want, Python will stop executing at each of them, waiting for user input:
name = input("Enter your name:")
print(f"Hello {name}")
fav1 = input("What is your favorite animal:")
fav2 = input("What is your favorite color:")
fav3 = input("What is your favorite number:")
print(f"Do you want a {fav2} {fav1} with {fav3} legs?")

"""Input Number"""
# The input from the user is treated as a string. Even if, in the example above, you can input a number, the Python interpreter will still treat it as a string.
# You can convert the input into a number with the float() function:
"""Example :- To find the square root, the input has to be converted into a number:"""
import math
x = input("Enter a number:")
#find the square root of the number:
y = math.sqrt(float(x))
print(f"The square root of {x} is {y}")

"""Validate Input"""
# It is a good practice to validate any input from the user. In the example above, an error will occur if the user inputs something other than a number.
# To avoid getting an error, we can test the input, and if it is not a number, the user could get a message like "Wrong input, please try again", and allowed to make a new input:
"""Example :- Keep asking until you get a number:"""
y = True
while y == True:
  x = input("Enter a number:")
  try:
    x = float(x)
    y = False
  except:
    print("Wrong input, please try again.")
print("Thank you!")
# =====================Python User Input End======================


