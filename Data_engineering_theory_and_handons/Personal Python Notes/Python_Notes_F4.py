# =======================================================================================
# PYTHON PRACTICE PART 4 STUDY INDEX: TUPLE COMPOSITION & SET MATHEMATICS
# =======================================================================================
# * SINGLE-ENTRY TUPLES    : Declaring single items with mandatory trailing commas to prevent string fallback
# * SEQUENCE MODIFICATIONS : Bypassing immutable tuple rules by using temporary list() type conversions
# * COMPOUND CONCATENATIONS: Appending items to an existing tuple using inline combination operators (+=)
# * DATA UNPACKING PATTERNS: Unpacking sequences and using asterisk variables (*var) to capture excess entries
# * TUPLE DATA METHODS     : Querying matching items via .count() and identifying position indices via .index()
# * SET STRUCTURAL QUALITIES: Initializing unique, unordered, and unindexed collections using curly brackets {}
# * EVALUATION COLLISIONS  : Tracking how sets treat True/1 and False/0 values as identical duplicate pairs
# * SET MUTATIONS          : Inserting single elements via .add() and passing iterable objects into .update()
# * DELETION EXECUTIONS    : Evaluating hard errors via .remove() versus safe removals using the .discard() method
# * UNORDERED POPPING      : Extracting elements from a set using .pop() without fixed index destinations
# * SET MATHEMATICS UNIONS : Combining total elements into unique sets using .union() or the pipe operator (|)
# * INTERSECTION FILTERS   : Isolating shared duplicate matches using .intersection() or the ampersand (&)
# * IN-PLACE INTERSECTIONS : Mutating set items directly without creating copies via .intersection_update()
# * DIFFERENCE SUBTRACTIONS : Isolating distinct single-set items using .difference() or the minus sign (-)
# * SYMMETRIC EXCLUSIONS   : Capturing everything except shared values using .symmetric_difference() or (^)
# * LOCKED HASHABLE CONTAINERS: Locking down unique records into immutable, read-only forms using frozenset()
# =======================================================================================

# ==========================Python Tuples==========================
# Tuples are used to store multiple items in a single variable.
# Tuple is one of 4 built-in data types in Python used to store collections of data, the other 3 are List, Set, and Dictionary, all with different qualities and usage.
# A tuple is a collection which is ordered and unchangeable.
# Tuples are written with round brackets.
thistuple = ("apple", "banana", "cherry") #Tuple
print(thistuple)

# Tuple Items
# Tuple items are ordered, unchangeable, and allow duplicate values.
# Tuple items are indexed, the first item has index [0], the second item has index [1] etc.
# Ordered
# When we say that tuples are ordered, it means that the items have a defined order, and that order will not change.
# Unchangeable
# Tuples are unchangeable, meaning that we cannot change, add or remove items after the tuple has been created.
# Allow Duplicates
# Since tuples are indexed, they can have items with the same value:
thistuple = ("apple", "banana", "cherry", "apple", "cherry") #Duplicate items
print(thistuple)

# Print the number of items in the tuple i.e Length
print(len(thistuple))

# Create Tuple With One Item
# To create a tuple with only one item, you have to add a comma after the item, otherwise Python will not recognize it as a tuple.
thistuple = ("apple",)
print(type(thistuple))
#NOT a tuple
thistuple = ("apple")
print(type(thistuple))

# --------Access Tuple Items--------
# we can access tuple items by referring to the index number, inside square brackets:
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[1])
# Negative Indexing
# Negative indexing means start from the end.
# -1 refers to the last item, -2 refers to the second last item etc.
print(thistuple[-1])
# Range of Indexes
# we can specify a range of indexes by specifying where to start and where to end the range.
# When specifying a range, the return value will be a new tuple with the specified items.
print(thistuple[2:5])
# By leaving out the start value, the range will start at the first item:
print(thistuple[:4])
# By leaving out the end value, the range will go on to the end of the tuple:
print(thistuple[2:])
# Range of Negative Indexes
# Specify negative indexes if you want to start the search from the end of the tuple:
print(thistuple[-4:-1])
# Check if Item Exists
# To determine if a specified item is present in a tuple use the in keyword:
if "apple" in thistuple:
  print("Yes, 'apple' is in the fruits tuple")
# --------Access Tuple Items End--------

# -----------Update Tuples------------
# Tuples are unchangeable, so you cannot change, add, or remove items once the tuple is created.
# But there are some workarounds.
# Change Tuple Values
# Once a tuple is created, you cannot change its values. Tuples are unchangeable, or immutable as it also is called.
# But there is a workaround. You can convert the tuple into a list, change the list, and convert the list back into a tuple.
x = ("apple", "banana", "cherry")
y = list(x)
y[1] = "kiwi"
x = tuple(y)
print(x)

# Add Items
# Since tuples are immutable, they do not have a build-in append() method, but there are other ways to add items to a tuple.
# 1. Convert into a list: Just like the workaround for changing a tuple, you can convert it into a list, add your item(s), and convert it back into a tuple.
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.append("orange")
thistuple = tuple(y)
print(thistuple)
# 2. Add tuple to a tuple. You are allowed to add tuples to tuples, so if you want to add one item, (or many), create a new tuple with the item(s), and add it to the existing tuple:
thistuple = ("apple", "banana", "cherry")
y = ("orange",)
thistuple += y
print(thistuple)

# Remove Items
# Note: You cannot remove items in a tuple.
# Tuples are unchangeable, so you cannot remove items from it, but you can use the same workaround as we used for changing and adding tuple items:
thistuple = ("apple", "banana", "cherry")
y = list(thistuple)
y.remove("apple")
thistuple = tuple(y)
print(thistuple)
# Or you can delete the tuple completely:
thistuple = ("apple", "banana", "cherry")
del thistuple
print(thistuple) #this will raise an error because the tuple no longer exists
# -----------Update Tuples End------------

# -----------Unpack Tuples------------
# When we create a tuple, we normally assign values to it. This is called "packing" a tuple:
fruits = ("apple", "banana", "cherry")
# But, in Python, we are also allowed to extract the values back into variables. This is called "unpacking":
fruits = ("apple", "banana", "cherry")
(green, yellow, red) = fruits
print(green)
print(yellow)
print(red)

# Note: The number of variables must match the number of values in the tuple, if not, you must use an asterisk '*' to collect the remaining values as a list.
fruits = ("apple", "banana", "cherry", "strawberry", "raspberry")
(green, yellow, *red) = fruits
print(green)
print(yellow)
print(red)

# If the asterisk is added to another variable name than the last, Python will assign values to the variable until the number of values left matches the number of variables left.
fruits = ("apple", "mango", "papaya", "pineapple", "cherry")
(green, *tropic, red) = fruits
print(green)
print(tropic)
print(red)
# -----------Unpack Tuples End------------

# -----------Loop Tuples------------
# Loop Through a Tuple
# You can loop through the tuple items by using a for loop.
thistuple = ("apple", "banana", "cherry")
for x in thistuple:
  print(x)

# Loop Through the Index Numbers
# You can also loop through the tuple items by referring to their index number.
# Use the range() and len() functions to create a suitable iterable.
thistuple = ("apple", "banana", "cherry")
for i in range(len(thistuple)):
  print(thistuple[i])

# Using a While Loop
# You can loop through the list items by using a while loop.
# Use the len() function to determine the length of the tuple, then start at 0 and loop your way through the tuple items by refering to their indexes.
# Remember to increase the index by 1 after each iteration.
thistuple = ("apple", "banana", "cherry")
i = 0
while i < len(thistuple):
  print(thistuple[i])
  i = i + 1
# -----------Loop Tuples End------------

# -----------Join Tuples------------
# Join Two Tuples
# To join two or more tuples you can use the + operator:
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)
tuple3 = tuple1 + tuple2
print(tuple3)
# Multiply Tuples
# If you want to multiply the content of a tuple a given number of times, you can use the * operator:
fruits = ("apple", "banana", "cherry")
mytuple = fruits * 2
print(mytuple)
# -----------Join Tuples End------------

# -----------Tuple Methods------------
# Python has two built-in methods that you can use on tuples.
# count()	Returns the number of times a specified value occurs in a tuple
thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
x = thistuple.count(5)
print(x)

# index()	Searches the tuple for a specified value and returns the position of where it was found
"""
Note :-  The index() method raises an exception if the value is not found.
"""
thistuple = (1, 3, 7, 8, 7, 5, 4, 6, 8, 5)
x = thistuple.index(8)
print(x)
# ==========================Python Tuples End==========================

# ==========================Python Sets==========================
# Sets are used to store multiple items in a single variable.
# Set is one of 4 built-in data types in Python used to store collections of data, the other 3 are List, Tuple, and Dictionary, all with different qualities and usage.
# A set is a collection which is unordered, unchangeable*, and unindexed.
"""* Note: Set items are unchangeable, but you can remove items and add new items."""
# Creating a Set:
thisset = {"apple", "banana", "cherry"}
print(thisset)
"""Note: Sets are unordered, so you cannot be sure in which order the items will appear when printed or traversed."""

# Set Items
# Set items are unordered, unchangeable, and do not allow duplicate values.
# Unordered
# Unordered means that the items in a set do not have a defined order.
# Set items can appear in a different order every time you use them, and cannot be referred to by index or key.
# Unchangeable
# Set items are unchangeable, meaning that we cannot change the items after the set has been created.
# Once a set is created, you cannot change its items, but you can remove items and add new items.

# Duplicates Not Allowed
# Sets cannot have two items with the same value, Duplicate values will be ignored:
thisset = {"apple", "banana", "cherry", "apple"}
print(thisset)

"""Note: The values True and 1 are considered the same value in sets, and are treated as duplicates:"""
thisset = {"apple", "banana", "cherry", True, 1, 2}
print(thisset)

"""Note: Again, the values False and 0 are considered the same value in sets, and are treated as duplicates:"""
thisset = {"apple", "banana", "cherry", False, True, 0}
print(thisset)
# Get the Length of a Set
print(len(thisset))

# ---------------Access Set Items------------------
# We cannot access items in a set by referring to an index or a key.
# But we can loop through the set items using a 'for' loop, or ask if a specified value is present in a set, by using the 'in' keyword.
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x)

# Check if "banana" is present in the set:
print("banana" in thisset)
# Check if "banana" is NOT present in the set:
print("banana" not in thisset)
# Change Items
# Once a set is created, you cannot change its items, but you can add new items.
# ---------------Access Set Items End------------------

# ---------------Add Set Items------------------
# To add one item to a set use the add() method.
thisset = {"apple", "banana", "cherry"}
thisset.add("orange")
print(thisset)

# To add items from another set into the current set, use the update() method.
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}
thisset.update(tropical)
print(thisset)

# Add Any Iterable
# The object in the update() method does not have to be a set, it can be any iterable object (tuples, lists, dictionaries etc.).
# Adding elements of a list to a set:
thisset = {"apple", "banana", "cherry"}
mylist = ["kiwi", "orange"]
thisset.update(mylist)
print(thisset)
mydict = {"a":1,"b":2,"c":3}
thisset.update(mydict)
thisset.update(mydict.values())
thisset.update(mydict.items())
print(thisset)
# ---------------Add Set Items End------------------

# ---------------Remove Set Items------------------
# To remove an item in a set, use the remove(), or the discard() method.
thisset = {"apple", "banana", "cherry"}
thisset.remove("banana")
print(thisset)
"""# Note: If the item to remove does not exist, remove() will raise an error."""

# To remove an item in a set, use the discard() method.
thisset.discard("banana")
print(thisset)
"""# Note: If the item to remove does not exist, discard() will NOT raise an error."""

# You can also use the pop(), method to remove an item, but this method will remove the last item. Remember that sets are unordered, so you will not know what item that gets removed.
# The return value of the pop() method is the removed item.
thisset = {"apple", "banana", "cherry"}
x = thisset.pop()
print(x)
print(thisset)
"""Note: Sets are unordered, so when using the pop() method, you do not know which item that gets removed."""
# The clear() method empties the set:
thisset = {"apple", "banana", "cherry"}
thisset.clear()
print(thisset)

# The del keyword will delete the set completely:
thisset = {"apple", "banana", "cherry"}
del thisset
print(thisset)
# ---------------Remove Set Items End------------------

# ---------------Loop Sets------------------  
thisset = {"apple", "banana", "cherry"}
for x in thisset:
  print(x)
# ---------------Loop Sets End------------------

# ---------------Join Sets------------------
# There are several ways to join two or more sets in Python.
# The union() and update() methods joins all items from both sets.
# The intersection() method keeps ONLY the duplicates.
# The difference() method keeps the items from the first set that are not in the other set(s).
# The symmetric_difference() method keeps all items EXCEPT the duplicates.

# Union
# The union() method returns a new set with all items from both sets.
set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set3 = set1.union(set2)
print(set3)
# we can use the | operator instead of the union() method, and you will get the same result.
set3 = set1 | set2
print(set3)

# Join Multiple Sets
# All the joining methods and operators can be used to join multiple sets.
# When using a method, just add more sets in the parentheses, separated by commas:
# join multiple sets with the union() method:: 
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}
set3 = {"John", "Elena"}
set4 = {"apple", "bananas", "cherry"}
myset = set1.union(set2, set3, set4)
print(myset)
# we can use the | operator instead of the union() method, and you will get the same result.
myset = set1 | set2 | set3 |set4
print(myset)

# Join a Set and a Tuple
# The union() method allows you to join a set with other data types, like lists or tuples.
# The result will be a set.
x = {"a", "b", "c"}
y = (1, 2, 3)
z = x.union(y)
print(z)
"""Note: The  | operator only allows you to join sets with sets, and not with other data types like you can with the  union() method."""

# Update
# The update() method inserts all items from one set into another.
# The update() changes the original set, and does not return a new set.
# The update() method inserts the items in set2 into set1:
set1 = {"a", "b" , "c"}
set2 = {1, 2, 3}
set1.update(set2)
print(set1)
"""Note: Both union() and update() will exclude any duplicate items."""

# Intersection
# Keep ONLY the duplicates
# The intersection() method will return a new set, that only contains the items that are present in both sets.
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.intersection(set2)
print(set3)
# The intersection() method will return a new set, that only contains the items that are present in both sets.
set3 = set1 & set2
print(set3)
# The values True and 1 are considered the same value. The same goes for False and 0.
# Join sets that contains the values True, False, 1, and 0, and see what is considered as duplicates:
set1 = {"apple", 1,  "banana", 0, "cherry"}
set2 = {False, "google", 1, "apple", 2, True}
set3 = set1.intersection(set2)
print(set3)
"""Note: The & operator only allows you to join sets with sets, and not with other data types like you can with the intersection() method."""

# The intersection_update() method will keep only the items that are present in both sets.
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.intersection_update(set2)
print(set1)

# Difference
# The difference() method will return a new set that will contain only the items from the first set that are not present in the other set.
# Keep all items from set1 that are not in set2:
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.difference(set2)
print(set3)
# we can use the - operator instead of the difference() method, and you will get the same result.
set3 = set1 - set2
print(set3)
"""Note: The - operator only allows you to join sets with sets, and not with other data types like you can with the difference() method."""

# The difference_update() method will keep the items from the first set that are not in the other set, but it will change the original set instead of returning a new set.
# Use the difference_update() method to keep only the items from the first set that are not present in the other set:
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.difference_update(set2)
print(set1)

# Symmetric Differences
# The symmetric_difference() method will return a new set, that contains only the elements that are NOT present in both sets.
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set3 = set1.symmetric_difference(set2)
print(set3)

# we can use the ^ operator instead of the symmetric_difference() method, and you will get the same result.
set3 = set1 ^ set2
print(set3)
"""Note: The ^ operator only allows you to join sets with sets, and not with other data types like you can with the symmetric_difference() method."""

# The symmetric_difference_update() method will also keep all but the duplicates, but it will change the original set instead of returning a new set.
# Use the symmetric_difference_update() method to keep the items that are not present in both sets:
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}
set1.symmetric_difference_update(set2)
print(set1)
# ---------------Join Sets End------------------

# ---------------Python frozenset------------------
# frozenset is an immutable version of a set.
# Like sets, it contains unique, unordered, unchangeable elements.
# Unlike sets, elements cannot be added or removed from a frozenset.
# Creating a frozenset
# Use the frozenset() constructor to create a frozenset from any iterable.
x = frozenset({"apple", "banana", "cherry"})
print(x)
print(type(x))

# ---------------Set Methods------------------
# Python has a set of built-in methods that you can use on sets.
# Method                              Description                                                      Shortcut
# add()                               Adds an element to the set                                       N/A
# clear()                             Removes all the elements from the set                            N/A
# copy()                              Returns a copy of the set                                        N/A
# difference()                        Returns a set containing the difference between sets             -
# difference_update()                 Removes the items in this set that are also in another set       -=
# discard()                           Remove the specified item                                        N/A
# intersection()                      Returns a set with the intersection of sets                      &
# intersection_update()               Removes the items not present in other, specified set(s)         &=
# isdisjoint()                        Returns whether two sets have an intersection or not             N/A
# issubset()                          Returns whether another set contains this set or not             <=
# issuperset()                        Returns whether this set contains another set or not             >=
# pop()                               Removes an element from the set                                  N/A
# remove()                            Removes the specified element                                    N/A
# symmetric_difference()              Returns a set with the symmetric differences of two sets         ^
# symmetric_difference_update()       Inserts the symmetric differences from this set and another      ^=
# union()                             Return a set containing the union of sets                        |
# update()                            Update the set with the union of this set and others             |=
# ==========================Python Sets End==========================
