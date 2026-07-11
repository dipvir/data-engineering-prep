# =======================================================================================
#                          PYTHON PRACTICE QUESTIONS FILE 1
# =======================================================================================

# ======================= Q1 -> Two Sum Problem =========================================
"""
Given an array of numbers and a target sum, find two numbers that add up to the target 
and return their indices.
Example: In [3, -1, 4, 2, -5, 4, 11] with target -1, the answer is indices [2, 4] 
because 4 + (-5) = -1.
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (True Brute Force)
# Core Concept: Checks every possible pair using nested loops.
# Time Complexity: O(n²) - Becomes exceptionally slow with large input arrays.
# Space Complexity: O(1) - Constant memory allocation.
# ---------------------------------------------------------------------------------------
def twoSum_brute_force(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

print("Q1 Brute Force Test:", twoSum_brute_force([3, -1, 4, 2, -5, 4, 11], -1))


# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (The Hash-Table Lookup)
# Core Concept: Uses a dictionary to store processed numbers and their indices. 
# For each value, it computes the target delta and triggers an instant lookup.
# Time Complexity: O(n) - Single-pass linear time traversal.
# Space Complexity: O(n) - Scales directly with dictionary memory growth.
# ---------------------------------------------------------------------------------------
def twoSum_optimized(nums, target):
    # This dictionary acts as our fast lookup memory bank
    # Key: The number value, Value: The index position of that number
    seen_numbers = {}
    
    # We loop through the array exactly ONCE
    for current_index, current_num in enumerate(nums):
        # Calculate the exact missing piece we need to hit the target
        missing_piece = target - current_num
        
        # INSTANT O(1) LOOKUP: Have we seen this missing piece before?
        if missing_piece in seen_numbers:
            # If yes, return the index of the missing piece and the current index
            return [seen_numbers[missing_piece], current_index]
        
        # If no, remember the current number and its index for future steps
        seen_numbers[current_num] = current_index

print("Q1 Optimized Test  :", twoSum_optimized([3, -1, 4, 2, -5, 4, 11], -1))


# ======================= Q2 -> Contains Duplicate Problem ===============================
"""
Given an array, determine if any value appears at least twice. Return True if any 
duplicates exist, otherwise False.
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (True Brute Force)
# Core Concept: Nested loop comparison checking every possible unique pair.
# Time Complexity: O(n²) - Inefficient; execution cycles balloon on larger tables.
# Space Complexity: O(1) - Requires no extra cluster memory allocations.
# ---------------------------------------------------------------------------------------
def check_contains_duplicate_brute_force(lst):
    for i in range(len(lst)):
        for j in range(i+1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False

print("\nQ2 Brute Force:", check_contains_duplicate_brute_force([1, 2, 3, 4, 5]))
print("Q2 Brute Force:", check_contains_duplicate_brute_force([1, 2, 3, 4, 5, 3]))


# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (The Pythonic Hash-Set One-Liner)
# Core Concept: Automatically eliminates duplicates by casting the list to a set and comparing lengths.
# Time Complexity: O(n) - Fast linear table scan runtime.
# Space Complexity: O(n) - Allocates memory for the unique set instantiation.
# ---------------------------------------------------------------------------------------
def check_contains_duplicate_set(lst):
    return len(lst) != len(set(lst))

print("Q2 Hash-Set :", check_contains_duplicate_set([1, 2, 3, 4, 5]))
print("Q2 Hash-Set :", check_contains_duplicate_set([1, 2, 3, 4, 5, 3]))


# ---------------------------------------------------------------------------------------
# OPTION 3: FASTER APPROACH WITH EARLY TERMINATION (Production-Grade Optimization)
# Core Concept: Iterates through elements sequentially, terminating the script loop the exact millisecond a duplicate hit is confirmed.
# Time Complexity: O(n) Worst Case | O(1) Best Case (If duplicates sit at index 0 and 1).
# Space Complexity: O(n) - Worst case memory threshold for tracking seen entries.
# ---------------------------------------------------------------------------------------
def check_contains_duplicate_early_exit(lst):
    # Create an empty set to look up elements we have already processed
    seen = set()   
    for num in lst:
        # If the number is already in our memory vault, we drop out instantly!
        if num in seen:
            return True
        # Otherwise, add it to our tracking vault
        seen.add(num)      
    return False

print("Q2 Early Exit :", check_contains_duplicate_early_exit([1, 2, 3, 4, 5]))
print("Q2 Early Exit :", check_contains_duplicate_early_exit([1, 2, 3, 4, 5, 3]))

# ======================= Q3 -> Array Reversal Challenge ================================
"""
Given an array (or list) of elements, modify the sequence so that the elements appear 
in the exact reverse order. The modification must happen in-place (directly in memory) 
without allocating a second helper list.
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (Out-of-Place Duplication / Slicing Shortcut)
# Core Concept: Creates a completely new list reversed or uses slicing copies (nums[::-1]).
# Time Complexity: O(N) - Linear time execution to copy elements.
# Space Complexity: O(N) - Faulty for big data; duplicates memory allocations in RAM.
# ---------------------------------------------------------------------------------------
def reverse_array_out_of_place(lst):
    return lst[::-1]

print("\nQ3 Out-of-Place Test:", reverse_array_out_of_place([10, 20, 30, 40, 50, 60]))
print("\nQ3 Out-of-Place Test:", reverse_array_out_of_place([10, 20, 30, 40, 50]))

# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (Midpoint Iteration with Temporary Variable) - [YOUR SOLUTION]
# Core Concept: Iterates exactly halfway through the sequence, leveraging a single scalar 
# memory slot (p1) to swap elements symmetrically across the center axis.
# Time Complexity: O(N) Linear Time - Scales predictably, executing exactly N/2 iterations.
# Space Complexity: O(1) Constant Space - Highly efficient; updates data directly in-place.
# ---------------------------------------------------------------------------------------
def reverse_array_temp_variable(lst):
    for i in range(len(lst) // 2):
        p1 = lst[i]
        lst[i] = lst[len(lst) - 1 - i]
        lst[len(lst) - 1 - i] = p1
    return lst

print("Q3 Temp Variable Test:", reverse_array_temp_variable([10, 20, 30, 40, 50, 60]))
print("Q3 Temp Variable Test:", reverse_array_temp_variable([10, 20, 30, 40, 50]))

# ---------------------------------------------------------------------------------------
# OPTION 3: FASTER APPROACH (Simultaneous Assignment Pythonic One-Liner)
# Core Concept: Runs up to the exact midpoint, using Python's native tuple unpacking 
# core rules to swap elements instantly without declaring any temporary identifiers.
# 
# Simplicity Example (The Underlying Mechanic):
#   a, b = 10, 11
#   a, b = b, a  --> Evaluates right side first to create a hidden tuple: (11, 10)
#   print(a, b)  --> Output: 11, 10 (Swapped safely!)
#
# Time Complexity: O(N) Linear Time - Linear execution trend tracking exactly N/2 passes.
# Space Complexity: O(1) Constant Space - Modifies underlying data blocks directly in memory.
# ---------------------------------------------------------------------------------------
def reverse_array_pythonic(lst):
    for i in range(len(lst) // 2):
        # Python applies the exact same variable-swap mechanism to the array indices.
        # It evaluates the entire right-hand side first, packing a hidden tuple 
        # before unpacking it cleanly to the left targets.
        lst[i], lst[len(lst)-1-i] = lst[len(lst)-1-i], lst[i]
    return lst

print("Q3 Pythonic Swap Test:", reverse_array_pythonic([1, 2, 3, 4, 5]))
print("Q3 Pythonic Swap Test:", reverse_array_pythonic([1, 2, 3, 4, 5 ,6]))

# ======================= Q4 -> Palindrome Number Problem ===============================
"""
Given an integer x, return True if x is a palindrome, and False otherwise.
An integer is a palindrome when it reads the same backward as forward.
Example: 121 reads as 121 from left to right and right to left, making it a palindrome. 
-121 reads as 121- from right to left, so it is NOT a palindrome.
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (String Casting Conversion)
# Core Concept: Casts the integer directly to a string string type and uses Python's native 
# slicing engine to check if the string matches its exact reversed copy.
# Time Complexity: O(N) - Where N is the number of digits in the integer.
# Space Complexity: O(N) - Allocates extra memory in RAM to store the string copy.
# ---------------------------------------------------------------------------------------
def is_palindrome_string(x):
    # A negative number can never be a palindrome because of the leading '-' sign
    if x < 0:
        return False
    
    str_x = str(x)
    return str_x == str_x[::-1]

print(is_palindrome_string(23432))
print(is_palindrome_string(121))
print(is_palindrome_string(120))
print(is_palindrome_string(1))
print(is_palindrome_string(-1))
print(is_palindrome_string(1212121))


# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (Mathematical Digits Extraction)
# Core Concept: Reconstructs the integer mathematically without casting it to text. 
# It isolates individual digits using modulo (%) and trims the original number down using 
# floor division (//) until the full reverse number is built.
# Time Complexity: O(log10(N)) - Extremely fast; the loop drops processing cycles by 
# a factor of 10 during every iteration step.
# Space Complexity: O(1) Constant Space - Highly optimal; uses a few scalar placeholders.
# ---------------------------------------------------------------------------------------
def is_palindrome_math(x):
    # Base Case Edge Guards: Negative numbers and numbers ending in 0 (except 0 itself) can never be palindromes in base-10 mathematics. and single digit numbers are palindromes
    if 0 <= x < 10 : return True       
    elif (x < 0) or (x % 10 == 0): return False   

    original_num = x
    reversed_num = 0    
    while x > 0:
        # Step A: Extract the last digit using Modulo (%)
        last_digit = x % 10        
        # Step B: Shift existing reversed digits left by 10 and add the new digit
        reversed_num = (reversed_num * 10) + last_digit        
        # Step C: Shave off the processed last digit using Floor Division (//)
        x = x // 10        
    return original_num == reversed_num

print(is_palindrome_math(23432))
print(is_palindrome_math(121))
print(is_palindrome_math(120))
print(is_palindrome_math(1))
print(is_palindrome_math(-1))
print(is_palindrome_math(1212121))

# ======================= Q5 -> Clean the list of strings ================================
"""
Given a raw list of strings containing inconsistent casing and leading/trailing 
whitespace anomalies, return a clean dataset where all elements are stripped 
and transformed strictly to lowercase.
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: TRADITIONAL APPROACH (Explicit Iteration with Manual Append)
# Core Concept: Instantiates an empty collector array and sequentially updates elements 
# using explicit loop boundaries and method chaining.
# Time Complexity: O(N) Linear Time - Travels through all N strings sequentially.
# Space Complexity: O(N) Linear Space - Allocates a secondary clean collection container.
# ---------------------------------------------------------------------------------------
def clean_list_loop(users_lst):
    cleaned_list = []
    for user in users_lst:
        cleaned_list.append(user.strip().lower())
    return cleaned_list

print("\nQ5 Loop Output:", clean_list_loop(["  Dipesh ", "gOPAL", "  niTesh   ", " Amit", "vIkaS  "]))


# ---------------------------------------------------------------------------------------
# OPTION 2: PYTHONIC APPROACH (List Comprehension One-Liner) - [YOUR SOLUTION]
# Core Concept: Leverages native Python sequence comprehension syntax to execute both 
# loop logistics and string transformations natively within the list initialization frame.
# Optimization: Faster execution trend due to processing loop lookups at the C-engine layer.
# Time Complexity: O(N) Linear Time - Single linear traversal pass across N elements.
# Space Complexity: O(N) Linear Space - Instantiates a single new target list container.
# ---------------------------------------------------------------------------------------
def clean_list_comprehension(users_lst):
    return [user.strip().lower() for user in users_lst]

print("Q5 Comprehension:", clean_list_comprehension(["  Dipesh ", "gOPAL", "  niTesh   ", " Amit", "vIkaS  "]))

# ======================= Q6 -> Clean and Filter a List of Strings ======================
"""
Given a raw list of record ID strings containing mixed casing and irrelevant system errors, 
return a filtered dataset containing only valid user IDs (IDs starting with 'U' or 'u') 
and normalize the final output tokens to uppercase.
"""

# ---------------------------------------------------------------------------------------
# COMPREHENSION OPTION A: LOWERCASE INTERNALS [YOUR APPROACH VARIANT]
# Core Concept: Applies formatting functions across both the evaluation guard and the 
# output assignment engine to capture mixed-case characters.
# Time Complexity: O(N) Linear Time - Single pass through N records.
# Space Complexity: O(N) Linear Space - Allocates a secondary filtered results container.
# ---------------------------------------------------------------------------------------
def clean_and_filter_ids_variant(record_ids):
    return [id.upper() for id in record_ids if id.upper().startswith("U")]

print("\nQ6 Comprehension Output A:", clean_and_filter_ids_variant(["u101", "error_404", "u102", "system_failure", "U103"]))


# ---------------------------------------------------------------------------------------
# COMPREHENSION OPTION B: TUPLE PATTERN MATCHING [OPTIMIZED APPROACH]
# Core Concept: Evaluates the raw unmutated prefix against a tuple threshold ('u', 'U') 
# to save CPU cycles, executing the `.upper()` allocation step only for confirmed targets.
# Time Complexity: O(N) Linear Time - One pass through N rows.
# Space Complexity: O(N) Linear Space - Scales with the volume of valid extraction matches.
# ---------------------------------------------------------------------------------------
def clean_and_filter_ids_optimized(record_ids):
    return [id.upper() for id in record_ids if id.startswith(('u', 'U'))]

print("Q6 Comprehension Output B:", clean_and_filter_ids_optimized(["u101", "error_404", "u102", "system_failure", "U103"]))

# ======================= Q7 -> Clean and Map a Dictionary of Strings ==================
"""
Given a raw list of tuple pairs containing employee names and ID numbers, 
return a clean key-value lookup dictionary. Filter out any records with invalid 
IDs (IDs <= 0) and normalize the name values to lowercase without whitespace.
"""

# ---------------------------------------------------------------------------------------
# COMPREHENSION APPROACH: DICTIONARY COMPREHENSION [YOUR SOLUTION]
# Core Concept: Leverages curly braces and a key:value mapping expression to build a 
# highly optimized dictionary lookup bank in a single pass.
# Time Complexity: O(N) Linear Time - Processes the collection of N tuples sequentially.
# Space Complexity: O(N) Linear Space - Allocates a dictionary container holding valid entries.
# ---------------------------------------------------------------------------------------
def build_employee_lookup(employee_data):
    return {ID : name.strip().lower() for name, ID in employee_data if ID > 0}

print("\nQ7 Dictionary Comprehension Output:")
print(build_employee_lookup([("  Dipesh ", 101), ("gOPAL", 0), ("  niTesh   ", 102), (" Amit", -5), ("vIkaS  ", 103)]))

# ======================= Q8 -> Prime Numbers Range Finder ===============================
"""
Given a numerical range defined by a start and end integer, find and extract all prime 
numbers within that range (inclusive).
Example:    Test Case 1:
            Input: start = 1, end = 10
            Expected Output: [2, 3, 5, 7]

            Test Case 2:
            Input: start = 10, end = 30
            Expected Output: [11, 13, 17, 19, 23, 29]
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (Brute Force with Even-Number Skipping)
# Core Concept: Iterates through the range, skipping even values. Checks odd numbers for 
# factors by looping all the way from 2 up to half of the current number's value (V // 2).
# Time Complexity: O(N * End) - Grows quadratically toward O(N²) in the worst case.
# Space Complexity: O(N) - Linear memory allocation to store output results in prime_list.
# ---------------------------------------------------------------------------------------
def get_prime_numbers_brute_force(start: int, end: int) -> list:
    prime_list = []
    for num in range(start, end + 1):
        if num == 2: 
            prime_list.append(num)
            continue
        elif num % 2 == 0 or num < 2: 
            continue 
            
        if num > 2:
            is_prime = True
            # Loop up to half the value. (+1 ensures the floor-division bound is inclusive)
            for i in range(2, (num // 2) + 1): 
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime: 
                prime_list.append(num)
    return prime_list

print("\nQ3 Brute Force Test:", get_prime_numbers_brute_force(-10, 100))

# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (Square Root Boundary & Odd Factor Stepping)
# Core Concept: Optimizes calculations using two rules:
# 1. Factors always repeat after the square root of a number (limit = math.isqrt(num)).
# 2. Since even values are skipped, odd numbers can only be divided by odd factors (step=2).
# Time Complexity: O(N * √End) - High-performance optimization; drops loops significantly.
# Space Complexity: O(N) - Linear memory required for the final output array.
# ---------------------------------------------------------------------------------------
import math
def get_prime_numbers_optimized(start: int, end: int) -> list:
    prime_list = []
    # Automatically bound the start range to ignore elements less than 2
    actual_start = max(2, start)
    for num in range(actual_start, end + 1):
        if num == 2:
            prime_list.append(num)
            continue
        if num % 2 == 0: 
            continue 
        is_prime = True
        # Calculate integer square root to define the mathematical factor wall
        limit = math.isqrt(num) # this gives the floor value of the square root of num (i in isqrt stands for integer)
        
        # Start at 3, end at sqrt, step by 2 to ignore useless even factor iterations
        for i in range(3, limit+1 , 2): 
            if num % i == 0:
                is_prime = False
                break
        if is_prime: 
            prime_list.append(num)
    return prime_list

print("Q3 Optimized Test  :", get_prime_numbers_optimized(-10, 100))

# ======================= Q9 -> Reverse All Numbers =====================================
"""
Given an array of integers, reverse the digits of each number while keeping its sign 
(positive/negative) and its relative position in the list intact.
Example: 
1) Input = [123, -456, 120, 0] , output =  [321, -654, 21, 0].
2) Input = [120, 5, -90, 0] , output = [21, 5, -9, 0]
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: STRING CONVERSION & SLICING (The Pythonic Approach)
# Core Concept: Converts the absolute value of the number into a string, reverses it 
# instantly using Python's built-in slicing shortcut ([::-1]), casts it back to an 
# integer, and reapplies the sign.
# Time Complexity: O(N) - Where N is the number of elements. String conversion and 
#                  slicing take linear time relative to the number of digits.
# Space Complexity: O(K) - Temporary memory allocation to store the string characters 
#                    for the largest number of digits (K) during conversion.
# ---------------------------------------------------------------------------------------
def reverse_all_numbers_string(nums: list) -> list:
    for index, num in enumerate(nums):
        # 1. Convert absolute value to string, reverse it via slicing, cast back to int
        reversed_num = int(str(abs(num))[::-1])
        # 2. Reapply the negative sign if the original number was negative
        nums[index] = -reversed_num if num < 0 else reversed_num
    return nums

print("\nQ4 Mathematical Test:", reverse_all_numbers_string([123, -456, 120, 0]))
print("\nQ4 Mathematical Test:", reverse_all_numbers_string([120, 5, -90, 0]))

# ---------------------------------------------------------------------------------------
# OPTION 2 (More efficient): MATHEMATICAL DIGIT EXTRACTION (Production-Grade In-Place Solution)
# Core Concept: Extracts digits sequentially from right to left using modulo (% 10) 
# and floor division (// 10). 
# Preserves the sign with a boolean flag and mutates the  
# array in-place to avoid extra memory allocation.
# Time Complexity: O(N) - Where N is the number of elements. The inner loop runs based 
#                  on the number of digits per integer, which is a constant upper bound.
# Space Complexity: O(1) - Constant memory; updates the input list directly.
# ---------------------------------------------------------------------------------------
def reverse_all_numbers_math(nums: list) -> list:
    for index, num in enumerate(nums):
        reversed_num = 0
        is_negative = False
        # Capture sign and convert to absolute value for extraction
        if num < 0: 
            is_negative = True
            num = abs(num)
        # Extract digits mathematically
        while num > 0:
            reversed_num = reversed_num * 10 + (num % 10)
            num //= 10
        # Reapply sign using Python's inline ternary expression
        nums[index] = -reversed_num if is_negative else reversed_num
    return nums

print("\nQ4 Mathematical Test:", reverse_all_numbers_math([123, -456, 120, 0]))
print("\nQ4 Mathematical Test:", reverse_all_numbers_math([120, 5, -90, 0]))

# ======================= Q10 -> Mean and Median Finder ===================================
"""
Given an unsorted list of numbers, calculate both the arithmetic mean and the median 
without utilizing the built-in 'statistics' module.

Example test cases:
Input = [-5, 10, -2, 4, 8]        -> Returns (3.0, 4.0)
Input = [15, 5, 20, 10, 10, 12]   -> Returns (12.0, 11.0)
Input = [15]                      -> Returns (15.0, 15.0)
Input = [3, 6, 2, 12]             -> Returns (5.75, 4.5)
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: INLINE TERNARY EXTRACTION (Your Approach - Concise & Direct)
# Core Concept: Sorts the list in-place and leverages a single-line Python ternary 
# expression to split evaluation for even and odd lengths, minimizing code blocks.
# Time Complexity: O(N log N) - Dominated by the in-place .sort() Timsort engine.
# Space Complexity: O(1) - Modifies the array in-place with constant extra memory.
# ---------------------------------------------------------------------------------------
def calculate_mean_and_median_ternary(lst: list) -> tuple:
    lst.sort()
    lst_len = len(lst)
    return (sum(lst)/lst_len , (lst[(int(lst_len/2))-1]+lst[int(lst_len/2)])/2 ) if len(lst)%2 == 0 else (sum(lst)/lst_len , lst[lst_len//2])

print(calculate_mean_and_median_ternary([-5, 10, -2, 4, 8]))
print(calculate_mean_and_median_ternary([15, 5, 20, 10, 10, 12]))
print(calculate_mean_and_median_ternary([15]))
print(calculate_mean_and_median_ternary([3, 6, 2, 12] ))

# ---------------------------------------------------------------------------------------
# OPTION 2: EXPLICIT STRUCTURAL SEPARATION (Alternative Approach - Highly Readable)
# Core Concept: Separates the floor-division index tracking explicitly before evaluating 
# parity. This avoids repeating the index calculation inside the return statement and 
# provides an easy-to-read layout for standard production debugging.
# Time Complexity: O(N log N) - Identical performance; driven by sorting.
# Space Complexity: O(1) - Modifies the array in-place with zero additional collections.
# ---------------------------------------------------------------------------------------
def calculate_mean_and_median(lst: list) -> tuple:
    if not lst:
        return (0.0, 0.0)
        
    lst.sort()
    lst_len = len(lst)
    mean_val = sum(lst) / lst_len
    # Extract median using ternary split based on length parity
    median_val = (lst[(lst_len // 2) - 1] + lst[lst_len // 2]) / 2 if lst_len % 2 == 0 else lst[lst_len // 2]
    return (float(mean_val), float(median_val))

print(calculate_mean_and_median([-5, 10, -2, 4, 8]))
print(calculate_mean_and_median([15, 5, 20, 10, 10, 12]))
print(calculate_mean_and_median([15]))
print(calculate_mean_and_median([3, 6, 2, 12] ))

# ---------------------------------------------------------------------------------------
# OPTION 3: OPTIMIZED LINEAR SELECTION (Advanced Approach - Scalable Production)
# Core Concept: Bypasses full dataset sorting. Uses an Introselect/Quickselect algorithm 
# via NumPy to locate only the exact middle-index element(s). Highly efficient for large-scale 
# data engineering pipelines where full sorting overhead is too expensive.
# Time Complexity: O(N) average / O(N\logN) worst-case - Linear time tracking for both mean and median discovery.
# Space Complexity: O(N) - Allocates memory internally for array partitioning.
# ---------------------------------------------------------------------------------------
import numpy as np
def calculate_mean_and_median_linear(lst: list) -> tuple:
    if not lst:
        return (0.0, 0.0)
        
    # sum() is O(N) linear time
    mean_val = sum(lst) / len(lst)
    # np.median utilizes partition-based Introselect algorithm.
    median_val = np.median(lst)
    return (float(mean_val), float(median_val))

print(calculate_mean_and_median_linear([-5, 10, -2, 4, 8]))
print(calculate_mean_and_median_linear([15, 5, 20, 10, 10, 12]))
print(calculate_mean_and_median_linear([15]))
print(calculate_mean_and_median_linear([3, 6, 2, 12] ))

# ======================= Q11 -> Digit Count of Comma-Separated Numbers ===================
"""
Process a string containing whole numbers separated by commas and determine the total 
number of digits present in each individual number, completely ignoring spaces and negative signs.

Example test cases:
Input = "123,45,6789,2"                 -> Returns "3,2,4,1"
Input = "  56, -789, 0,   123456  "     -> Returns "2,3,1,6"
Input = "999"                           -> Returns "3"
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: GLOBAL CHAINED REPLACEMENT (Your Approach - Elegant & Concise)
# Core Concept: Pre-cleans the entire string globally by stripping out all whitespaces 
# and negative symbols sequentially. Splinters the cleaned text via commas and measures 
# O(1) string lengths directly within a list comprehension wrapper.
# Time Complexity: O(N) - Linear scans run sequentially; no nested loop multipliers exist.
# Space Complexity: O(N) - Allocates memory for intermediate replaced strings and token lists.
# ---------------------------------------------------------------------------------------
def numbers_digits_count_global(nums_str: str) -> str:
    # Pre-clean formatting characters globally across the raw string
    nums_lst = nums_str.replace(" ", "").replace("-", "").split(",")
    return ",".join([str(len(num)) for num in nums_lst])

print(numbers_digits_count_global("  56, -789, 0,   123456  "))
print(numbers_digits_count_global("123,45,6789,2"))
print(numbers_digits_count_global("999"))

# ---------------------------------------------------------------------------------------
# OPTION 2: TOKENIZED STRIPPING (Alternative - Memory Defensive)
# Core Concept: Splits the string first, then cleans individual components. Useful 
# if the input string is a multi-gigabyte stream where global pre-allocations of heavy 
# replaced strings might spike memory thresholds unnecessarily.
# Time Complexity: O(N) - Linear iteration over split segments.
# Space Complexity: O(N) - Stores list tokens natively.
# ---------------------------------------------------------------------------------------
def numbers_digits_count_tokenized(nums_str: str) -> str:
    # Split first, clean individual tokens during iteration
    tokens = nums_str.split(",")
    counts = []
    for token in tokens:
        # Strip outer spaces, eliminate negative signs locally
        clean_token = token.strip().replace("-", "")
        counts.append(str(len(clean_token)))
    return ",".join(counts)

print(numbers_digits_count_tokenized("  56, -789, 0,   123456  "))
print(numbers_digits_count_tokenized("123,45,6789,2"))
print(numbers_digits_count_tokenized("999"))

# ======================= Q12 -> Find Second Highest Number ===============================
"""
Identify the second largest unique value inside an unsorted list of numbers without 
utilizing built-in sorting mechanisms.

Example test cases:
Input = [12, 35, 1, 10, 34, 1]    -> Returns 34
Input = [10, 10, 10]              -> Returns None
Input = [7.5, 2.3, 9.8, 9.8, 4.6] -> Returns 7.5
Input = [5]                       -> Returns None
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SET-BASED MULTI-PASS (Your Approach - Clean & Fast)
# Core Concept: Utilizes a Python set to handle duplicate elimination instantly. Checks 
# lengths for edge cases, drops the absolute maximum value in O(1) time from the set, 
# and returns the remaining maximum.
# Time Complexity: O(N) - Sequential linear scans across the dataset.
# Space Complexity: O(N) - Allocates memory for the unique element set storage.
# ---------------------------------------------------------------------------------------
import sys
def find_second_highest_set(nums_lst: list):
    # Unique transformation wipes out duplicate traps
    unique_set = set(nums_lst)
    if len(unique_set) <= 1:
        return None
    # Manual scan to find the max value
    max_num = -sys.maxsize
    for num in unique_set:
        if max_num < num:
            max_num = num
    # Droping the max value
    unique_set.remove(max_num)
    return max(unique_set)

print(find_second_highest_set([]))
print(find_second_highest_set([12, 35, 1, 10, 34, 1]))
print(find_second_highest_set([7.5, 2.3, 9.8, 9.8, 4.6]))
print(find_second_highest_set([5]))
print(find_second_highest_set([5,5,5]))

# ---------------------------------------------------------------------------------------
# OPTION 2: SINGLE-PASS STREAMING (Optimized - Pure Constant Space)
# Core Concept: Tracks the 'highest' and 'second_highest' placeholders simultaneously. 
# Processes elements in a single stream, shifting positions when a new leader emerges 
# while explicitly bypassing duplicate values.
# Time Complexity: O(N) - Single continuous evaluation loop.
# Space Complexity: O(1) - Modifies no structures and maintains constant tracking variables.
# ---------------------------------------------------------------------------------------
def find_second_highest_single_pass(nums_lst: list):
    if len(nums_lst) < 2:
        return None
    highest = float('-inf') # float('-inf') will always be the lowest possible value
    second_highest = float('-inf')
    for num in nums_lst:
        # Case A: New absolute leader found
        if num > highest:
            second_highest = highest
            highest = num
        # Case B: Number fits right between the leader and runner-up
        elif num > second_highest and num != highest:
            second_highest = num
            
    return None if second_highest == float('-inf') else second_highest

print(find_second_highest_single_pass([12, 35, 1, 10, 34, 1]))
print(find_second_highest_single_pass([]))
print(find_second_highest_single_pass([7.5, 2.3, 9.8, 9.8, 4.6]))
print(find_second_highest_single_pass([5]))
print(find_second_highest_single_pass([5,5,5]))

# ==================Further More Questions are continued in Python_Questions_F2.py==========================