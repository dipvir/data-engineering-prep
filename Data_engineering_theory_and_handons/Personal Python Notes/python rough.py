# 1. Using the bin() function
# Note: It returns '0b11000'. The '0b' prefix just means "this is a binary number"
print(bin(24))  

# 2. Using format strings (f-strings) to get clean text without the '0b' prefix
print(f"{24:b}")  # Output: 11000


# =====================================================================
# THE ANATOMY OF A PYTHON DECORATOR
# =====================================================================
# A decorator is a function that takes another function as an input,
# wraps it with extra code, and returns the modified "wrapped" function.
# =====================================================================

# SCENARIO 1: THE BASIC MECHANICS (UNDER THE HOOD)
# ---------------------------------------------------------------------
# Let's build a decorator manually without the '@' symbol first so you 
# can see the exact computer science layout.

def my_decorator(original_function):
    # This inner function is the actual "wrapping paper"
    def wrapper():
        print("1. [Setup] Code running BEFORE the original function.")
        original_function()  # Executing your actual function
        print("3. [Cleanup] Code running AFTER the original function.")
    
    return wrapper  # Returning the wrapped package unexecuted

def simple_greet():
    print("2. Hello World!")

# The manual way to apply a decorator:
wrapped_greet = my_decorator(simple_greet)
wrapped_greet()


# SCENARIO 2: USING THE SYNTACTIC SUGAR (@)
# ---------------------------------------------------------------------
# Writing 'variable = decorator(function)' gets messy. Python uses the 
# '@' symbol as a clean shorthand to do the exact same thing automatically.

@my_decorator
def simple_bye():
    print("2. Goodbye World!")

# When you call this, Python automatically triggers the wrapper layout instead!
simple_bye()


# SCENARIO 3: HANDLING ARGUMENTS WITH (*args, **kwargs)
# ---------------------------------------------------------------------
# CRITICAL TRAP: What if the function you want to wrap takes parameters? 
# If 'simple_greet' needed a name, the basic 'wrapper()' above would crash.
# To fix this, always pass (*args, **kwargs) through the wrapper layer.

def security_shield(original_function):
    def wrapper(*args, **kwargs):
        print("\n[Security Check] Verifying user permissions...")
        
        # Pass the arguments smoothly into the original function
        result = original_function(*args, **kwargs)
        
        print("[Security Check] Audit log recorded successfully.")
        return result  # Return the output if the function returns something
    return wrapper

@security_shield
def delete_user(user_id, force=False):
    print(f"Executing: Erasing User ID {user_id} (Force={force}) from database.")
    return "Success"

# Test with dynamic arguments
status = delete_user(9402, force=True)
print(f"Function output: {status}")


# SCENARIO 4: COMPLEX REAL-WORLD USE CASE (PERFORMANCE TIMER)
# ---------------------------------------------------------------------
# In real development, decorators are incredibly powerful for structural 
# tracking tasks like timing code execution, logging, or error handling.

import time

def execution_timer(original_function):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start the clock
        
        result = original_function(*args, **kwargs)  # Run the code
        
        end_time = time.time()    # Stop the clock
        duration = end_time - start_time
        
        print(f"\n[Performance Log] '{original_function.__name__}' took {duration:.4f} seconds to complete.")
        return result
    return wrapper

@execution_timer
def complex_math_loop():
    total = 0
    for i in range(10_000_000): # Simulating a heavy computation
        total += i
    return total

# Run the decorated function
complex_math_loop()


# ----------------------------------

# =====================================================================
# GENERATOR CONCEPTS: THE UNDER-THE-HOOD NEXT ENGINE
# =====================================================================

def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

# 1. Create the generator object (It stays frozen at the start)
generator_object = count_up_to(2)

# 2. Advance the bookmark manually
print(next(generator_object))  # Output: 1 (Function pauses at yield)
print(next(generator_object))  # Output: 2 (Function pauses at yield)

# 3. Try to advance it one more time
# Because count becomes 3, the while loop breaks and the function ends.
print(next(generator_object))

# --------------------------------


# =====================================================================
# ITERATOR PROTOCOL MECHANICS: EXPLICIT MANUAL EXECUTION
# =====================================================================

my_list = ["A", "B"]

# Step 1: Python calls the __iter__() method to get the tracking engine.
# Shorthand for: my_list.__iter__()
engine = iter(my_list) 
print(type(engine))  # Output: <list_iterator object>

# Step 2: Python repeatedly calls __next__() to pull data points out.
# Shorthand for: engine.__next__()
print(next(engine))  # Output: "A"
print(next(engine))  # Output: "B"

# Step 3: The sequence is empty. The next call throws the protocol stop signal.
print(next(engine))  # Raises: StopIteration


# ---------------------------------------

import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

# ------------------------------------
# r_n * 10 + last_digit
r_n = 0
print(123//10 , 123%10)
print(12//10 , 12%10)
print(1//10 , 1%10)

r_n = r_n * 10 + 123%10
print(r_n)
r_n = r_n * 10 + 12%10
print(r_n)
r_n = r_n * 10 + 1%10
print(r_n)

# -----------------------------

lst = [3,5,1,22,44,55,11,6,7,9,0]
# lst.reverse()
# print(lst) vb
print(lst[::-1])





