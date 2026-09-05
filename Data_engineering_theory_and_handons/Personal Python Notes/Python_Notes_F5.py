# =======================================================================================
# PYTHON PRACTICE PART 5 STUDY INDEX: DICTIONARY DICTS & CONDITIONAL FLOW PIPES
# =======================================================================================
# * DICTIONARY FOUNDATIONS : Initializing ordered key-value pairs that overwrite matching duplicate keys
# * VALUE EXTRACTION TOOLS : Retrieving entries via bracket lookups, fallback .get() methods, and 'in' checks
# * DYNAMIC VIEW OBJECTS   : Extracting tracking views of mappings via .keys(), .values(), and .items()
# * DATA MUTATIONS         : Inserting and updating mapping records using key variables or .update() methods
# * DICTIONARY PURGING     : Removing matching keys via .pop(), stripping last keys via .popitem(), or using clear()
# * MAP LOOP TRAVERSALS    : Iterating through compound items concurrently via for loops unpacking .items()
# * COPIES AND REFERENCES  : Creating distinct non-referenced dictionary backups using the .copy() function
# * MULTI-TIERED NESTING   : Accessing nested levels via chained brackets [key][subkey] and loops
# * LOGICAL SCOPE SHIFTS   : Managing code branches using structural if, elif, and catch-all else code blocks
# * TERNARY SHORTHANDS     : Evaluating value selections inline on a single line (x if True else y)
# * MULTI-CONDITION LINKS  : Combining logic pathways via inline connective operators (and, or, not)
# * LEVEL CONDITIONS       : Layering nested branch tests versus combining simple conditions with 'and'
# * SYNTACTIC PLACEHOLDERS : Using the pass statement as a structural empty code placeholder during development
# * STRUCTURAL MATCH CASES : Routing execution paths via match-case structures paired with the underscore (_) default
# * COUPLING PATTERN GUARDS: Matching multiple cases via values (|), variables, and conditional if loops
# =======================================================================================

# ====================Python Dictionaries=========================
# Dictionaries are used to store data values in key:value pairs.
# A dictionary is a collection which is ordered*, changeable and do not allow duplicates.
# As of Python version 3.7, dictionaries are ordered. In Python 3.6 and earlier, dictionaries are unordered.
# Dictionaries are written with curly brackets, and have keys and values:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict)

# Dictionary Items
# Dictionary items are ordered, changeable, and do not allow duplicates.
# Dictionary items are presented in key:value pairs, and can be referred to by using the key name.
print(thisdict["brand"])

# Ordered or Unordered?
# As of Python version 3.7, dictionaries are ordered. In Python 3.6 and earlier, dictionaries are unordered.
# When we say that dictionaries are ordered, it means that the items have a defined order, and that order will not change.
# Unordered means that the items do not have a defined order, you cannot refer to an item by using an index.

# Changeable
# Dictionaries are changeable, meaning that we can change, add or remove items after the dictionary has been created.

# Duplicates Not Allowed
# Dictionaries cannot have two items with the same key:
# Duplicate values will overwrite existing values:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "year": 2020
}
print(thisdict)

# Dictionary Length
# To determine how many items a dictionary has, use the len() function:
print(len(thisdict))

# Dictionary Items - Data Types
# The values in dictionary items can be of any data type:
# Example :- String, int, boolean, and list data types:
thisdict = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"]
}

# The dict() Constructor
# It is also possible to use the dict() constructor to make a dictionary.
thisdict = dict(name = "John", age = 36, country = "Norway")
print(thisdict)

# ---------------Access Dictionary Items------------------
# Accessing Items
# We can access the items of a dictionary by referring to its key name, inside square brackets:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(thisdict["model"])
# There is also a method called get() that will give you the same result:
print(thisdict.get("model"))

# Get Keys
# The keys() method will return a list of all the keys in the dictionary.
print(thisdict.keys())
# The list of the keys is a view of the dictionary, meaning that any changes done to the dictionary will be reflected in the keys list.
# Example
# Add a new item to the original dictionary, and see that the keys list gets updated as well:
car = {
"brand": "Ford",
"model": "Mustang",
"year": 1964
}
x = car.keys()
print(x) #before the change
car["color"] = "white"
print(x) #after the change

# Get Values
# The values() method will return a list of all the values in the dictionary.
print(thisdict.values())
# The list of the values is a view of the dictionary, meaning that any changes done to the dictionary will be reflected in the values list.
# Example
# Make a change in the original dictionary, and see that the values list gets updated as well:
x = car.values()
print(x) #before the change
car["year"] = 2020
print(x) #after the change
# Add a new item to the original dictionary, and see that the values list gets updated as well:
x = car.values()
print(x) #before the change
car["color"] = "red"
print(x) #after the change

# Get Items
# The items() method will return each item in a dictionary, as tuples in a list.
# Get a list of the key:value pairs
print(thisdict.items())
# The returned list is a view of the items of the dictionary, meaning that any changes done to the dictionary will be reflected in the items list.
# Make a change in the original dictionary, and see that the items list gets updated as well:
x = car.items()
print(x) #before the change
car["year"] = 2020
print(x) #after the change
# Add a new item to the original dictionary, and see that the items list gets updated as well:
x = car.items()
print(x) #before the change
car["color"] = "red"
print(x) #after the change

# Check if Key Exists
# To determine if a specified key is present in a dictionary use the 'in' keyword:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
if "model" in thisdict:
  print("Yes, 'model' is one of the keys in the thisdict dictionary")
# ---------------Access Dictionary Items End------------------

# ---------------Change Dictionary Items------------------
# Change Values
# You can change the value of a specific item by referring to its key name:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["year"] = 2018
print(thisdict)

# Update Dictionary
# The update() method will update the dictionary with the items from the given argument.
# The argument must be a dictionary, or an iterable object with key:value pairs.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"year": 2020})
print(thisdict)
# ---------------Change Dictionary Items End------------------

# ---------------Add Dictionary Items------------------
# Adding Items
# Adding an item to the dictionary is done by using a new index key and assigning a value to it:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict["color"] = "red"
print(thisdict)

# Update Dictionary
# The update() method will update the dictionary with the items from a given argument. If the item does not exist, the item will be added.
# The argument must be a dictionary, or an iterable object with key:value pairs.
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.update({"color": "red"})
print(thisdict)
# ---------------Add Dictionary Items End------------------

# ---------------Remove Dictionary Items------------------
# Removing Items
# There are several methods to remove items from a dictionary, the pop() method removes the item with the specified key name:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.pop("model")
print(thisdict)

# The popitem() method removes the last inserted item (in versions before 3.7, a random item is removed instead):
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.popitem()
print(thisdict)

# The del keyword removes the item with the specified key name:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
del thisdict["model"]
print(thisdict)

# The del keyword can also delete the dictionary completely:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
del thisdict
print(thisdict) #this will cause an error because "thisdict" no longer exists.

# The clear() method empties the dictionary:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
thisdict.clear()
print(thisdict)
# ---------------Remove Dictionary Items End------------------

# ---------------Loop Dictionary------------------
# Loop Through a Dictionary
# we can loop through a dictionary by using a for loop.
# When looping through a dictionary, the return value are the keys of the dictionary, but there are methods to return the values as well.
# This prints all key names in the dictionary, one by one:
for x in thisdict:
  print(x)
# This print all values in the dictionary, one by one:
for x in thisdict:
  print(thisdict[x])
# We can also use the values() method to return values of a dictionary:
for x in thisdict.values():
  print(x)
# we can use the keys() method to return the keys of a dictionary:
for x in thisdict.keys():
  print(x)
# Looping through both keys and values, by using the items() method:
for x, y in thisdict.items():
  print(x, y)
# ---------------Loop Dictionary End------------------

# ---------------Copy Dictionaries------------------
# Copy a Dictionary
# You cannot copy a dictionary simply by typing dict2 = dict1, because: dict2 will only be a reference to dict1, and changes made in dict1 will automatically also be made in dict2.
"""Incorrect way to copy a dictionary
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict
mydict["color"] = "red"
print(thisdict, mydict, sep = "\n")
"""
# There are ways to make a copy, one way is to use the built-in Dictionary method copy().
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = thisdict.copy()
mydict["color"] = "red"
print(thisdict, mydict, sep = "\n")
# Another way to make a copy is to use the built-in function dict().
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
mydict = dict(thisdict)
mydict["color"] = "violet"
print(thisdict, mydict, sep = "\n")
# ---------------Copy Dictionaries End------------------

# ---------------Nested Dictionaries---------------
# A dictionary can contain dictionaries, this is called nested dictionaries.
myfamily = {
  "child1" : {
    "name" : "Emil",
    "year" : 2004
  },
  "child2" : {
    "name" : "Tobias",
    "year" : 2007
  },
  "child3" : {
    "name" : "Linus",
    "year" : 2011
  }
}
# Access Items in Nested Dictionaries
# To access items from a nested dictionary, you use the name of the dictionaries, starting with the outer dictionary:
print(myfamily["child2"]["name"])

# Loop Through Nested Dictionaries
# We can loop through a dictionary by using the items() method like this:
for x, obj in myfamily.items():
  print(x)

  for y in obj:
    print(y + ':', obj[y])
# ---------------Nested Dictionaries End---------------

# ---------------Dictionary Methods---------------
# Python has a set of built-in methods that you can use on dictionaries.
# clear()      - Removes all elements from the dictionary
# copy()       - Returns a shallow copy of the dictionary
# fromkeys()   - Creates a dictionary from the given sequence of keys and values
# get()        - Returns the value for the specified key
# items()      - Returns a view object with key-value pairs
# keys()       - Returns a view object with all the keys
# pop()        - Removes the element with the specified key
# popitem()    - Removes the last inserted key-value pair
# setdefault() - Returns the value of a key, if the key does not exist: inserts the key with a specified value
# update()     - Updates the dictionary with the specified key-value pairs
# values()     - Returns a view object with all the values
# ---------------Dictionary Methods End---------------
# ====================Python Dictionaries End=========================

# ====================Python If Else====================== 
# ---------------Python If statements---------------
# Python Conditions and If statements
# Python supports the usual logical conditions from mathematics:
"""
Equals: a == b
Not Equals: a != b
Less than: a < b
Less than or equal to: a <= b
Greater than: a > b
Greater than or equal to: a >= b
"""
# These conditions can be used in several ways, most commonly in "if statements" and loops.
# An "if statement" is written by using the if keyword.
# Example
a = 33
b = 200
if b > a:
  print("b is greater than a")
else:
  print("a is greater than b")
"""
Note :- Python relies on indentation (whitespace at the beginning of a line) to define scope in the code. Other programming languages often use curly-brackets for this purpose.
We can use spaces or tabs for indentation, but we must use the same amount of indentation for all statements within the same code block.
"""

# Using Variables in Conditions :- Boolean variables can be used directly in if statements without comparison operators.
is_logged_in = True
if is_logged_in:
  print("Welcome back!")
# ---------------Python If statements End---------------

# ---------------Python Elif Statement---------------
# The Elif Keyword
# The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition".
# The elif keyword allows you to check multiple expressions for True and execute a block of code as soon as one of the conditions evaluates to True.
# Example
a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")

# Multiple Elif Statement, Testing multiple conditions:
score = 75
if score >= 90:
  print("Grade: A")
elif score >= 80:
  print("Grade: B")
elif score >= 70:
  print("Grade: C")
elif score >= 60:
  print("Grade: D")
"""Important: Only the first true condition will be executed. Even if multiple conditions are true, Python stops after executing the first matching block."""

# When to Use Elif
# Use elif when you have multiple mutually exclusive conditions to check. This is more efficient than using multiple separate if statements because Python stops checking once it finds a true condition.
day = 3
if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")
# ---------------Python Elif Statement End---------------

# ---------------Python Else Statement---------------
# The Else Keyword
# The else keyword catches anything which isn't caught by the preceding conditions.
# The else statement is executed when the if condition and all elif conditions if present evaluate to False.
# Example
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

# Else Without Elif :- We can also have an else without the elif:
# Example
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")
# This creates a simple two-way choice: if the condition is true, execute one block; otherwise, execute the else block.

# How Else Works
# The else statement provides a default action when none of the previous conditions are true. Think of it as a "catch-all" for any scenario not covered by your if and elif statements.
"""Note: The else statement must come last. You cannot have an elif after an else."""
# Example :- Checking even or odd numbers:
number = 7
if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")

# Complete If-Elif-Else Chain
# We can combine if, elif, and else to create a comprehensive decision-making structure.
temperature = 22
if temperature > 30:
  print("It's hot outside!")
elif temperature > 20:
  print("It's warm outside")
elif temperature > 10:
  print("It's cool outside")
else:
  print("It's cold outside!")
# ---------------Python Else Statement End---------------

# ---------------Python Shorthand If--------------
# If you have only one statement to execute, you can put it on the same line as the if statement.
a = 5
b = 2
if a > b: print("a is greater than b")
# Short Hand If ... Else
# If you have one statement for if and one for else, you can put them on the same line using a conditional expression:
a = 2
b = 330
print("A") if a > b else print("B")
"""Note :- This is called a conditional expression (sometimes known as a "ternary operator")."""

# Assign a Value With If ... Else
# You can also use a one-line if/else to choose a value and assign it to a variable:
a = 10
b = 20
bigger = a if a > b else b
print("Bigger is", bigger)
"""
The syntax follows this pattern:
variable = value_if_true if condition else value_if_false
"""

# Multiple Conditions on One Line
# You can chain conditional expressions, but keep it short so it stays readable:
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")

# Practical Examples
# Ternary operators are particularly useful for simple assignments and return statements.
# Example 1:- Finding the maximum of two numbers:
x = 15
y = 20
max_value = x if x > y else y
print("Maximum value:", max_value)

# Example 2:- Setting a default value:
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)
# ---------------Python Shorthand If End--------------

# ---------------Logical Operators--------------
"""
Python Logical Operators
Logical operators are used to combine conditional statements. Python has three logical operators:
and - Returns True if both statements are true
or - Returns True if one of the statements is true
not - Reverses the result, returns False if the result is true
"""
# The and Operator
# The and keyword is a logical operator, and is used to combine conditional statements. Both conditions must be true for the entire expression to be true.
a = 200
b = 33
c = 500
if a > b and c > a:
  print("Both conditions are True")

# The or Operator
# The or keyword is a logical operator, and is used to combine conditional statements. At least one condition must be true for the entire expression to be true.
a = 200
b = 33
c = 500
if a > b or a > c:
  print("At least one of the conditions is True")

# The not Operator
# The not keyword is a logical operator, and is used to reverse the result of the conditional statement.
a = 33
b = 200
if not a > b:
  print("a is NOT greater than b")

# Combining Multiple Operators
# You can combine multiple logical operators in a single expression. Python evaluates not first, then and, then or.
age = 25
is_student = False
has_discount_code = True
if (age < 18 or age > 65) and not is_student or has_discount_code:
  print("Discount applies!")
# ---------------Logical Operators End--------------

# ---------------Nested If--------------
# Nested If Statements
# We can have if statements inside if statements. This is called nested if statements.
x = 41
if x > 10:
  print("Above ten,")
  if x > 20:
    print("and also above 20!")
  else:
    print("but not above 20.")
"""In this example, the inner if statement only runs if the outer condition (x > 10) is true."""

# How Nested If Works
# Each level of nesting creates a deeper level of decision-making. The code evaluates from the outermost condition inward.
age = 25
has_license = True
if age >= 18:
  if has_license:
    print("You can drive")
  else:
    print("You need a license")
else:
  print("You are too young to drive")

# Multiple Levels of Nesting
# We can nest as many levels deep as needed, but keep in mind that too many levels can make code harder to read.
score = 85
attendance = 90
submitted = True
if score >= 60:
  if attendance >= 80:
    if submitted:
      print("Pass with good standing")
    else:
      print("Pass but missing assignment")
  else:
    print("Pass but low attendance")
else:
  print("Fail")

# Nested If vs Logical Operators
# Sometimes nested if statements can be simplified using logical operators like and. The choice depends on your logic.
# For Example :- This nested if code:
temperature = 25
is_sunny = True
if temperature > 20:
  if is_sunny:
    print("Perfect beach weather!")
# Could also be written with and:
temperature = 25
is_sunny = True
if temperature > 20 and is_sunny:
  print("Perfect beach weather!")
"""Note :- Both approaches produce the same result. Use nested if statements when the inner logic is complex or depends on the outer condition. Use and when both conditions are simple and equally important.
"""
# ---------------Nested If End--------------

# ---------------Python Pass Statement--------------
# if statements cannot be empty, but if you for some reason have an if statement with no content, put in the pass statement to avoid getting an error.
a = 33
b = 200
if b > a:
  pass
"""The pass statement is a null operation - nothing happens when it executes. It serves as a placeholder."""

"""
Why Use pass?
The pass statement is useful in several situations:
  -> When you're creating code structure but haven't implemented the logic yet
  -> When a statement is required syntactically but no action is needed
  -> As a placeholder for future code during development
  -> In empty functions or classes that you plan to implement later
"""

# pass in Development
# During development, you might want to sketch out your program structure before implementing the details. The pass statement allows you to do this without syntax errors.
age = 16
if age < 18:
  pass # TODO: Add underage logic later
else:
  print("Access granted")

# pass vs Comments
# A comment is ignored by Python, but pass is an actual statement that gets executed (though it does nothing). You need pass where Python expects a statement, not just a comment.
"""
score = 85
if score > 90:
  # This is excellent
# This will raise an IndentationError
"""
# This works correctly with pass:
score = 95
if score > 90:
  pass # This is excellent
print("Score processed")

# pass with Multiple Conditions
# We can use pass in any branch of an if-elif-else statement.
value = 50
if value < 0:
  print("Negative value")
elif value == 0:
  pass # Zero case - no action needed
else:
  print("Positive value")

# pass in Other Contexts
# While we focus on pass with if statements here, it's also commonly used with loops, functions, and classes.
def calculate_discount(price):
  pass # TODO: Implement discount logic
calculate_discount(3)
# Function exists but doesn't do anything yet
# ====================Python If Else End====================== 

# ====================Python Match======================
# The match statement is used to perform different actions based on different conditions.
# Instead of writing many if..else statements, you can use the match statement.
# The match statement selects one of many code blocks to be executed.
# Syntax
"""
match expression:
  case x:
    code block
  case y:
    code block
  case z:
    code block
"""

# This is how it works:
# The match expression is evaluated once.
# The value of the expression is compared with the values of each case.
# If there is a match, the associated block of code is executed.

# The example below uses the weekday number to print the weekday name:
day = 4
match day:
  case 1:
    print("Monday")
  case 2:
    print("Tuesday")
  case 3:
    print("Wednesday")
  case 4:
    print("Thursday")
  case 5:
    print("Friday")
  case 6:
    print("Saturday")
  case 7:
    print("Sunday")

# Default Value
# Use the underscore character _ as the last case value if you want a code block to execute when there are not other matches:
day = 4
match day:
  case 6:
    print("Today is Saturday")
  case 7:
    print("Today is Sunday")
  case _:
    print("Looking forward to the Weekend")
  
# Combine Values
# Use the pipe character | as an or operator in the case evaluation to check for more than one value match in one case:
day = 4
match day:
  case 1 | 2 | 3 | 4 | 5:
    print("Today is a weekday")
  case 6 | 7:
    print("I love weekends!")

# If Statements as Guards
# We can add if statements in the case evaluation as an extra condition-check:
month = 5
day = 4
match day:
  case 1 | 2 | 3 | 4 | 5 if month == 4:
    print("A weekday in April")
  case 1 | 2 | 3 | 4 | 5 if month == 5:
    print("A weekday in May")
  case _:
    print("No match")

# one complex example form google gemini.
# =====================================================================
# GENERAL EXAMPLE: TEXT-BASED GAME ACTION PARSER (match-case)
# =====================================================================
# This function takes a player's command (split into a list of words) 
# and uses pattern matching to figure out what they want to do.
def parse_action(command_list):
    match command_list:
        # 1. EXACT LITERAL MATCH WITH 'OR'
        # Matches a list with exactly ONE item that is either "quit" or "exit"
        case ["quit"] | ["exit"]:
            return "Quitting the game. Thanks for playing!"
            
        case ["look"]:
            return "You see a dark forest and a glowing cave."
            
        # 2. VARIABLE EXTRACTION (BINDING)
        # Matches any 2-item list starting with "go". 
        # It automatically saves the second word into the 'direction' variable.
        case ["go", direction]:
            return f"You walk bravely towards the {direction}."
            
        # 3. EXTRACTION WITH 'OR' LOGIC ON A SINGLE SPOT
        # Matches any 2-item list where the first word is take, grab, or pick.
        case ["take" | "grab" | "pick", item]:
            return f"You put the {item} in your inventory."
            
        # 4. CONDITIONAL GUARDS (IF STATEMENTS)
        # Matches exactly 3 items. It captures the amount and item, but ONLY 
        # runs if the amount consists of numbers (using .isdigit()).
        case ["drop", amount, item] if amount.isdigit():
            return f"You dropped {amount} {item}(s) on the ground."
            
        # Matches the same 3-item structure, but acts as a fallback if the 
        # guard above failed (meaning they didn't type a number).
        case ["drop", amount, item]:
            return f"Error: You can't drop '{amount}'. You must specify a number!"
            
        # 5. THE WILDCARD (_)
        # The catch-all. If the command doesn't match any shape above, it lands here.
        case _:
            return "I don't understand that command."
# =====================================================================
# LET'S TEST THE PARSER
# =====================================================================

print(parse_action(["look"]))                   
# Output: You see a dark forest and a glowing cave.

print(parse_action(["go", "north"]))            
# Output: You walk bravely towards the north.

print(parse_action(["grab", "sword"]))          
# Output: You put the sword in your inventory.

print(parse_action(["drop", "3", "potions"]))   
# Output: You dropped 3 potions(s) on the ground.

print(parse_action(["drop", "all", "potions"])) 
# Output: Error: You can't drop 'all'. You must specify a number!

print(parse_action(["dance", "wildly"]))        
# Output: I don't understand that command.
# ====================Python Match End======================



