# =======================================================================================
# PYTHON PRACTICE PART 3 STUDY INDEX: CORE MUTABILITY & LIST ARCHITECTURES
# =======================================================================================
# * MUTABILITY FOUNDATIONS : Modifying items in-place (Lists) versus creating entire memory updates (Strings)
# * NESTED CONTAINER TRAPS : Modifying mutable list elements stored inside immutable container tuples ()
# * HASHABLE KEY LAWS      : Enforcing immutable types for dictionary keys to preserve lookup locations
# * PASS-BY-REFERENCE RULES: Tracking how mutable items passed to def functions modify global variables
# * LIST CHARACTERISTICS   : Defining ordered, adjustable array collections that accept duplicate values
# * ELEMENT LOOKUPS        : Accessing explicit item positions using positive indices and negative end-offsets
# * RANGE SLICE SEGMENTS   : Extracting bounded sub-lists using optional step slice notations [start:stop:step]
# * INLINE ITEM REPLACEMENTS: Updating items or replacing dynamic index ranges by assigning new sequences
# * ARRAY INJECTIONS       : Adding elements via .append(), targeting locations via .insert(), and merging via .extend()
# * CONTAINER DELETIONS    : Removing entries via .remove(), extracting via .pop(), clearing via .clear(), or using del
# * ITERATION STRATEGIES   : Traversing data via explicit for lines, index positions, loops, or while structures
# * LIST COMPREHENSIONS    : Building inline array loops paired with conditional filtering expressions
# * ALPHANUMERIC SORTING   : Reordering items in-place using .sort() and reversing sequences via .reverse()
# * KEY FUNCTION SORTS     : Running case-insensitive sorts via key=str.lower or numeric sorts via key=abs
# * SHALLOW COPY TRAPS     : Avoiding reference pointing errors (list2 = list1) using .copy() or [:]
# * LISTS VS TUPLES        : Comparing dynamic list objects against rigid, lightweight tuple allocations
# =======================================================================================

# ==========================THE GOLDEN RULES OF OBJECT MUTABILITY==========================
# In Data Engineering, mutability dictates how objects behave in memory.
# - MUTABLE: Can be modified "in-place" without changing its memory ID.
# - IMMUTABLE: Cannot be modified. Any change spawns a new object with a new ID.
# =====================================================================

# 1. CORE TYPES BREAKDOWN
# ---------------------------------------------------------------------
"""
IMMUTABLE TYPES: int, float, bool, string, tuple, frozenset
MUTABLE TYPES  : list, dict, set
"""
# ---------------------------------------------------------------------

# 2. STRING IMMUTABILITY PROOF
# ---------------------------------------------------------------------
# Text methods like .upper() or .replace() NEVER change the original string.
# They return a completely new string. You must re-assign it to save it.
name = "peter"
print("Original ID:", id(name))

name.upper() # This does absolutely nothing to the 'name' variable!
print("After upper() without assignment:", name) 

name = name.upper() # Re-assignment forces it to point to the new creation
print("After re-assignment:", name)
print("New Memory ID:", id(name)) # Notice the ID completely changed!


# 3. LIST MUTABILITY PROOF (IN-PLACE MODIFICATIONS)
# ---------------------------------------------------------------------
# Methods like .append(), .extend(), or .sort() modify the list directly 
# in your computer's memory. No re-assignment is needed.
data_pipeline = ["source_blob", "bronze_table"]
print("\nOriginal List ID:", id(data_pipeline))

data_pipeline.append("silver_table") # Modifies in-place
print("Updated List:", data_pipeline)
print("Same Memory ID:", id(data_pipeline)) # The ID matches the original perfectly!


# 4. THE TUPLE MUTABLE TRAP
# ---------------------------------------------------------------------
# Tuples () are immutable arrays used to protect configuration settings.
# TRAP: If a tuple contains a mutable object (like a list), that 'nested list' can still be modified!
config = ("prod_env", [80, 443])
# config[0] = "dev_env" <-- Throws a TypeError (Tuple block is locked)
config[1].append(8080) # Works perfectly! (The nested list is mutable)
print("\nTrap Result:", config) 


# 5. THE DICTIONARY KEY LAW
# ---------------------------------------------------------------------
# Dictionary KEYS must always be immutable (Strings, Numbers, Tuples).
# This is because Python uses the key's fixed value to calculate where to
# store it in memory. Values, however, can be anything (lists, dicts, etc).
#
# bad_dict = { ["user1"]: "active" } <-- Throws a TypeError: unhashable type 'list'
good_dict = { "user1": ["active", "admin"] } # Strings as keys are perfect.


# 6. SET STRUCTURAL RULES & FROZENSET
# ---------------------------------------------------------------------
# A standard set {1, 2, 3} is mutable—you can add or remove items.
# However, every individual item inside a set MUST be immutable.
# To lock an entire set down so nothing can be altered, use frozenset().
active_users = {"alpha", "beta"}
active_users.add("gamma") # Works! Sets are mutable.
print(active_users)

locked_users = frozenset(["alpha", "beta"])
# locked_users.add("gamma") <-- Throws an AttributeError (frozenset is frozen)


# 7. THE PASS-BY-REFERENCE DANGER (DATA PIPELINE WARNING)
# ---------------------------------------------------------------------
# When you pass a mutable list into a function, Python passes the actual
# memory address. If the function alters the list, it alters your global data!
def clean_data(raw_list):
    raw_list.append("DIRTY_DATA_FOUND") # Alters the list globally

my_records = ["row1", "row2"]
clean_data(my_records)
print("\nGlobal Pollution Result:", my_records) # The global data was altered!
# ==========================THE GOLDEN RULES OF OBJECT MUTABILITY END==========================

# ==========================Python Lists==========================
mylist = ["apple", "banana", "cherry"]      
# Lists are used to store multiple items in a single variable.
# Lists are one of 4 built-in data types in Python used to store collections of data, the other 3 are Tuple, Set, and Dictionary, all with different qualities and usage.           
# Lists are created using square brackets:
print(mylist) # printing the List:
# List Items
# List items are ordered, changeable, and allow duplicate values.
# List items are indexed, the first item has index [0], the second item has index [1] etc.
# Ordered
# When we say that lists are ordered, it means that the items have a defined order, and that order will not change.
# If you add new items to a list, the new items will be placed at the end of the list.
"""Note: There are some list methods that will change the order, but in general: the order of the items will not change"""
# Changeable
# The list is changeable, meaning that we can change, add, and remove items in a list after it has been created.
# Allow Duplicates
# Since lists are indexed, lists can have items with the same value:
# Lists allow duplicate values:
thislist = ["apple", "banana", "cherry", "apple", "cherry"]
print(thislist)
# To determine how many items a list has, use the len() function:
print(len(thislist))
# List Items - Data Types
# List items can be of any data type:
# Example
# String, int and boolean data types:
list1 = ["apple", "banana", "cherry"]
list2 = [1, 5, 7, 9, 3]
list3 = [True, False, False]
# A list can contain different data types:
# Example
# A list with strings, integers and boolean values:
list1 = ["abc", 34, True, 40, "male"]

"""
Python Collections (Arrays)
There are four collection data types in the Python programming language:

--> List is a collection which is ordered and changeable. Allows duplicate members.
--> Tuple is a collection which is ordered and unchangeable. Allows duplicate members.
--> Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
--> Dictionary is a collection which is ordered** and changeable. No duplicate members.

*Set items are unchangeable, but you can remove and/or add items whenever you like.
**As of Python version 3.7, dictionaries are ordered. In Python 3.6 and earlier, dictionaries are unordered.
"""

# --------Access List Items--------
# List items are indexed and you can access them by referring to the index number:
thislist = ["apple", "banana", "cherry"]
print(thislist[1])
# Negative Indexing
# Negative indexing means start from the end
# -1 refers to the last item, -2 refers to the second last item etc.
thislist = ["apple", "banana", "cherry"]
print(thislist[-1])
# Range of Indexes
# we can specify a range of indexes by specifying where to start and where to end the range.
# When specifying a range, the return value will be a new list with the specified items
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])
print(thislist[:4])
print(thislist[2:])

# Range of Negative Indexes
# Specify negative indexes if you want to start the search from the end of the list:
# Example
# This example returns the items from "orange" (-4) to, but NOT including "mango" (-1):
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[-4:-1])
# Check if Item Exists
# To determine if a specified item is present in a list use the in keyword:
# Example
# Check if "apple" is present in the list:
thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")
# --------Access List Items End--------

# --------Change List Items--------
# Change Item Value
# To change the value of a specific item, refer to the index number:
# Changing the second item:
thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist)
# Change a Range of Item Values
# To change the value of items within a specific range, define a list with the new values, and refer to the range of index numbers where you want to insert the new values:
# Change the values "banana" and "cherry" with the values "blackcurrant" and "watermelon":
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist)
thislist[2:] = ["green apple"]
print(thislist)
# If you insert more items than you replace, the new items will be inserted where you specified, and the remaining items will move accordingly:
# Change the second value by replacing it with two new values:
thislist = ["green apple", "banana", "cherry" ,"apple" , "orange", "kiwi", "mango"]
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist)
# If you insert more items than you replace, the new items will be inserted where you specified, and the remaining items will move accordingly:
thislist[3:5] = ["greps", "lemon" , "tamato" , "patato"]
print(thislist)
# If you insert less items than you replace, the new items will be inserted where you specified, and the remaining items will move accordingly:
thislist[1:3] = ["watermelon"]
print(thislist)

# Insert Items
# To insert a new list item, without replacing any of the existing values, we can use the insert() method.
# The insert() method inserts an item at the specified index:
# Inserting "watermelon" as the third item:
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)
# --------Change List Items End--------

# --------Add List Items--------
# Append Items
# To add an item to the end of the list, use the append() method:
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)
# Insert Items
# To insert a list item at a specified index, use the insert() method.
thislist.insert(1, "greps")
print(thislist)
# Extend List
# To append elements from another list to the current list, use the extend() method.
thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical) #The elements will be added to the end of the list.
print(thislist)
# Add Any Iterable
# The extend() method does not have to append lists, you can add any iterable object (tuples, sets, dictionaries etc.).
thislist = ["apple", "banana", "cherry"]
thistuple = ("kiwi", "orange")
thislist.extend(thistuple)
print(thislist)
# --------Add List Items End--------

# --------Remove List Items--------
# Remove Specified Item
# The remove() method removes the specified item.
thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)
# If there are more than one item with the specified value, the remove() method removes the first occurrence:
thislist = ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.remove("banana")
print(thislist)
# Remove Specified Index
# The pop() method removes the specified index.
thislist =  ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.pop(2)
print(thislist)
# If we do not specify the index, the pop() method removes the last item.
thislist.pop()
print(thislist)
# The del keyword also removes the specified index:
thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist)
# The del keyword can also delete the list completely by below syntax
del thislist
# Clear the List
# The clear() method empties the list, the list still remains, but it has no content.
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)
# --------Remove List Items End--------

# --------Loop Lists--------

# Loop Through a List
# we can loop through the list items by using a 'for' loop:
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

# Loop Through the Index Numbers
# We can also loop through the list items by referring to their index number.
# Use the range() and len() functions to create a suitable iterable.
thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
  print(thislist[i])
# The iterable created in the example above is [0, 1, 2].

# Using a While Loop
# You can loop through the list items by using a while loop.
# Use the len() function to determine the length of the list, then start at 0 and loop your way through the list items by referring to their indexes.
# Remember to increase the index by 1 after each iteration.
thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

# Looping Using List Comprehension
# List Comprehension offers the shortest syntax for looping through lists:
thislist = ["apple", "banana", "cherry"]
[print(x) for x in thislist]
# --------Loop Lists End--------

# --------List Comprehension--------
"""
-----General list comprehension syntax------
newlist = [expression for item in iterable if condition == True]
The return value is a new list, leaving the old list unchanged.
"""

# List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.
# Example:Based on a list of fruits, you want a new list, containing only the fruits with the letter "a" in the name.
# Without list comprehension you will have to write a for statement with a conditional test inside as shown below:
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = []
for x in fruits:
  if "a" in x:
    newlist.append(x)
print(newlist)  
# With list comprehension you can do all that with only one line of code:
newlist = [x for x in fruits if "a" in x] #The condition(if "a" in x) is like a filter that only accepts the items that evaluate to True.
print(newlist)
"""Note :- The return value is a new list, leaving the old list unchanged."""

# Iterable
# The iterable can be any iterable object, like a list, tuple, set etc.
# Example :- We can use the range() function to create an iterable:
newlist = [x for x in range(10)]
print(newlist)
# Same example, but with a condition:
newlist = [x for x in range(10) if x < 5]
print(newlist)

# Expression
# The expression is the current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list:
# Set the values in the new list to upper case:
fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
newlist = [x.upper() for x in fruits]
print(newlist)
# You can set the outcome to whatever you like:
newlist = ['hello' for x in fruits]
print(newlist)
# The expression can also contain conditions, not like a filter, but as a way to manipulate the outcome:
# Return "orange" instead of "banana":
newlist = [x if x != "banana" else "orange" for x in fruits]
print(newlist)
# --------List Comprehension End--------

# --------Sort Lists--------
# Sort List Alphanumerically (Ascending)
# List objects have a sort() method that will sort the list alphanumerically, ascending, by default:
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)

# Sort the list numerically:
thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)

# Sort Descending
# To sort descending, use the keyword argument reverse = True:
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist)

# Sort the list descending:
thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse = True)
print(thislist)

# Customize Sort Function
# You can also customize your own function by using the keyword argument key = function.
# The function will return a number that will be used to sort the list (the lowest number first):
# In lemen words, the function will return list sorted beased on how close the other number is to 50
def myfunc(n):
  return abs(n - 50)
thislist = [100, 50, 65, 82, 23]
thislist.sort(key = myfunc)
print(thislist)

# Case Insensitive Sort
# By default the sort() method is case sensitive, resulting in all capital letters being sorted before lower case letters:
# Case sensitive sorting can give an unexpected result , as shown below example:
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist)

# Luckily we can use built-in functions as key functions when sorting a list.
# So if you want a case-insensitive sort function, use str.lower as a key function:
# Example :- Perform a case-insensitive sort of the list:
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key = str.lower)
print(thislist)

# Reverse Order
# What if you want to reverse the order of a list, regardless of the alphabet?
# The reverse() method reverses the current sorting order of the elements.
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.reverse()
print(thislist)
# --------Sort Lists End--------

# --------Copy Lists--------
# You cannot copy a list simply by typing list2 = list1, because: list2 will only be a reference to list1, and changes made in list1 will automatically also be made in list2.
# There are ways to make a copy, one way is to use the built-in List method copy().
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)
# Another way to make a copy is to use the built-in method list().
thislist = ["apple", "banana", "cherry"]
mylist = list(thislist)
print(mylist)

# Use the slice Operator
# You can also make a copy of a list by using the : (slice) operator.
thislist = ["apple", "banana", "cherry"]
mylist = thislist[:]
print(mylist)
# --------Copy Lists End--------

# --------Join Lists--------
# Join Two Lists
# There are several ways to join, or concatenate, two or more lists in Python.
# One of the easiest ways are by using the + operator.
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
list3 = list1 + list2
print(list3)
# Another way to join two lists is by appending all the items from list2 into list1, one by one:
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]
for x in list2:
  list1.append(x)
print(list1)
# Or you can use the extend() method, which purpose is to add elements from one list to another list:
list1 = ["a", "b" , "c"]
list2 = [1, 2, 3]
list1.extend(list2)
print(list1)
# --------Join Lists End--------

# --------List Methods Reference--------
"""
| Method         | Description                                                                    |
|----------------|--------------------------------------------------------------------------------|
| append(x)      | Adds an item x to the end of the list                                          |
| extend(iter)   | Adds all items from an iterable (list, tuple, etc.) to the list                |
| insert(i, x)   | Inserts item x at position i                                                   |
| remove(x)      | Removes the first occurrence of item x                                         |
| pop([i])       | Removes and returns item at index i (removes last list item if i not specified)|
| clear()        | Removes all items from the list                                                |
| index(x)       | Returns the index of the first occurrence of item x                            |
| count(x)       | Returns the number of times x appears in the list                              |
| sort()         | Sorts the list in ascending order.for descending order pass argument reverse=True    |
| reverse()      | Reverses the elements of the list                                              |
| copy()         | Returns a shallow copy of the list                                             |
"""             
# ==========================Python Lists End==========================

# =============abs() FUNCTION (ABSOLUTE VALUE)====================
# The abs() function removes the negative sign from any numeric value.
# It always returns a positive number (or zero).
# =====================================================================

# 1. WORKING WITH INTEGERS
# ---------------------------------------------------------------------
# If the number is negative, it becomes positive. 
# If it is already positive or zero, it stays exactly the same.
print(abs(-5))  # Output: 5
print(abs(5))   # Output: 5
print(abs(0))   # Output: 0

# 2. WORKING WITH FLOATS (DECIMALS)
# ---------------------------------------------------------------------
# It preserves the exact decimal precision while removing the negative sign.
temperature_drop = -12.75
print(abs(temperature_drop))  # Output: 12.75

# 3. WHY DATA ENGINEERS USE THIS (PRACTICAL EXAMPLE)
# ---------------------------------------------------------------------
# In data pipelines, you often need to calculate the variance or difference 
# between two values (like actual data vs forecasted target data). 
# You only care about *how big* the error is, not whether it is over or under.
actual_count = 150
forecast_count = 185
# Without abs(), this subtraction gives -35
raw_difference = actual_count - forecast_count 
# With abs(), you get the true variance magnitude
variance = abs(raw_difference)
print(f"The pipeline variance is {variance} rows.") # Output: 35 rows
# =============abs() FUNCTION (ABSOLUTE VALUE)= END===================

# =====================================================================
#          LIST vs TUPLE: THE CORE DIFFERENCES
# =====================================================================
#  FEATURE          LIST []                        TUPLE ()
# ---------------------------------------------------------------------
#  Mutability:      MUTABLE (Can change)           IMMUTABLE (Locked)
#  Performance:     Slower (Allocates extra room)  Faster (Exact memory fit)
#  Methods:         Many (.append, .pop, .sort)    Only two (.count, .index)
#  Use Case:        Tracking changing data streams Static lookups/configs
# =====================================================================

# 1. SYNTAX DIFFERENCE
# ---------------------------------------------------------------------
my_list = ["bronze", "silver", "gold"]   # Uses square brackets []
my_tuple = ("bronze", "silver", "gold")  # Uses parentheses ()

# 2. MUTABILITY PROOF (THE MODIFICATION TEST)
# ---------------------------------------------------------------------
# Lists let you swap items out or add new ones on the fly:
my_list[0] = "raw_source"
my_list.append("platinum")
print("Modified List:", my_list)

# Tuples will completely crash your script if you try to modify them:
# my_tuple[0] = "raw_source"  # <-- Throws TypeError: 'tuple' object does not support item assignment
# my_tuple.append("platinum") # <-- Throws AttributeError: 'tuple' object has no attribute 'append'

# 3. PERFORMANCE & MEMORY (WHY DATA ENGINEERS CARE)
# ---------------------------------------------------------------------
# Because lists are designed to grow, Python over-allocates memory for them 
# just in case you append later. Tuples are locked, so Python allocates the 
# exact byte-size required.
import sys
large_list = [1, 2, 3, 4, 5]
large_tuple = (1, 2, 3, 4, 5)
print(f"List Memory Size: {sys.getsizeof(large_list)} bytes")   # Higher memory usage
print(f"Tuple Memory Size: {sys.getsizeof(large_tuple)} bytes") # Lower memory usage

# 4. DESIGN INTENT (WHEN TO USE WHICH)
# ---------------------------------------------------------------------
# Use a LIST when your data is a collection of the same type of items 
# that will change as your pipeline runs (e.g., streaming records):
active_pipeline_jobs = ["job_101", "job_102"]
active_pipeline_jobs.append("job_103") # Perfect use case for a list

# Use a TUPLE when the data represents a single structural "record" or 
# fixed configuration metadata that must never be accidentally altered:
db_connection_setting = ("10.0.0.1", 5432, "admin_user") # (IP, Port, User)

# ===============LIST vs TUPLE: THE CORE DIFFERENCE END================