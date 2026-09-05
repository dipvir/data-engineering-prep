# ======================= Q13 -> Roman to Integer Problem ===============================
"""
PROBLEM DESCRIPTION:
Roman numerals are represented by seven different symbols:
Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
Roman numerals are typically written from largest to smallest, from left to right 
(e.g., XII = 10 + 2 = 12). However, the numeral for four is not IIII. Instead, 
it is written as IV. Because the 'I' (1) is before the 'V' (5), we subtract it, 
making four. The same principle applies to nine, written as IX.

There are exactly six instances where subtraction is used:
1. 'I' can be placed before 'V' (5) and 'X' (10) to make 4 and 9.
2. 'X' can be placed before 'L' (50) and 'C' (100) to make 40 and 90.
3. 'C' can be placed before 'D' (500) and 'M' (1000) to make 400 and 900.

Given a valid roman numeral string 's', convert it to its corresponding integer.
# ------------------------------------------------------------------------------
# TEST CASES
# ------------------------------------------------------------------------------
# TC1: "III"     -> Expected: 3     (Simple addition)
# TC2: "LVIII"   -> Expected: 58    (Mixed standard characters)
# TC3: "MCMXCIV" -> Expected: 1994  (Multiple subtractive pairs)
# TC4: "MMMCMXCIX" -> Expected: 3999 (Maximum value boundary constraint)
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (Token Strip & Replace (Brute Force))
# Core Concept: Identifies and tallies the 6 special pairs first, then strips them out using string mutations.
# Time Complexity: O(n) - Multiple scans due to sequential sub-string matching loops.
# Space Complexity: O(1) - Fixed dictionary lookups, though it re-allocates immutable strings midway.
# ---------------------------------------------------------------------------------------
def roman_to_int_brute_force(s):
    r_n_dict = {
        "I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000,
        "IV": 4, "IX": 9, "XL": 40, "XC": 90, "CD": 400, "CM": 900
    }
    total = 0
    subtractive_pairs = ("IV", "IX", "XL", "XC", "CD", "CM")
    
    for r_num in subtractive_pairs:
        if r_num in s:
            total += r_n_dict[r_num]
            s = s.replace(r_num, "")

    for r_num in s:
        total += r_n_dict[r_num]
    return total

print(roman_to_int_brute_force("III"))
print(roman_to_int_brute_force("LVIII"))
print(roman_to_int_brute_force("MCMXCIV"))
print(roman_to_int_brute_force("MMMCMXCIX"))


# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (Single-Pass Index Pointer)
# Core Concept: Inspects indices left-to-right in a single pass, tracking combinations with a skipping flag.
# Time Complexity: O(n) - Clean linear lookahead scan.
# Space Complexity: O(1) - Completely static variable tracking without string copying.
# ---------------------------------------------------------------------------------------
def roman_to_int_index_pointer(s):
    r_n_dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    flag = False
    for index in range(len(s) - 1):
        if flag: 
            flag = False
            continue
        if (s[index] == 'I' and s[index+1] == 'V') or \
           (s[index] == 'I' and s[index+1] == 'X') or \
           (s[index] == 'X' and s[index+1] == 'L') or \
           (s[index] == 'X' and s[index+1] == 'C') or \
           (s[index] == 'C' and s[index+1] == 'D') or \
           (s[index] == 'C' and s[index+1] == 'M'): 
            total += (r_n_dict[s[index+1]] - r_n_dict[s[index]])
            flag = True
        else:
            total += r_n_dict[s[index]]
    if not flag: total += r_n_dict[s[-1]]
    return total

print(roman_to_int_index_pointer("III"))
print(roman_to_int_index_pointer("LVIII"))
print(roman_to_int_index_pointer("MCMXCIV"))
print(roman_to_int_index_pointer("MMMCMXCIX"))


# ---------------------------------------------------------------------------------------
# OPTION 3: FASTER APPROACH WITH VALUE COMPARISON (Production-Grade Optimization)
# Core Concept: Leverages mathematics; subtracts the character value if it's smaller than the succeeding one.
# Time Complexity: O(n) - Continuous, non-interrupted single-pass loop processing.
# Space Complexity: O(1) - Absolute zero operational memory overhead.
# ---------------------------------------------------------------------------------------
def roman_to_int_math_comparison(s):
    r_n_dict = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for index in range(len(s) - 1):
        if r_n_dict[s[index]] < r_n_dict[s[index+1]]:
            total -= r_n_dict[s[index]]
        else:
            total += r_n_dict[s[index]]
    total += r_n_dict[s[-1]]
    return total

print(roman_to_int_math_comparison("III"))
print(roman_to_int_math_comparison("LVIII"))
print(roman_to_int_math_comparison("MCMXCIV"))
print(roman_to_int_math_comparison("MMMCMXCIX"))

# ======================= Q14 -> Longest Common Prefix ===============================
"""
Given an array of strings, find the longest common prefix string amongst them.
If there is no common prefix, return an empty string "".

Short Test Cases:
# TC1: ["flower","flow","flight"] -> Expected: "fl" (Standard match)
# TC2: ["dog","racecar","car"]    -> Expected: ""   (No match at all)
# TC3: ["ab", "a"]                -> Expected: "a"  (Short string boundary match)
# TC4: [""]                       -> Expected: ""   (Empty string edge case)
"""

# ---------------------------------------------------------------------------------------
# OPTION 1: SLOWER APPROACH (Your Token Accumulation Brute Force Solution)
# Core Concept: Iterates through characters, appends them to a temporary string, and counts matches.
# Time Complexity: O(N * M) - Scans every element completely without early termination capabilities.
# Space Complexity: O(N) - Wastefully allocates and destroys temporary strings inside loops.
# ---------------------------------------------------------------------------------------
def longest_common_prefix_brute_force(strs):
    if not strs or "" in strs: return ""
    index = 0 
    result = ""
    smallest_str_len = min([len(s) for s in strs])
    
    while index < smallest_str_len:
        prefix = ""
        for s in strs:
            prefix += s[index]
        if len(strs) == prefix.count(prefix[0]): 
            result += prefix[0]
        else: 
            return result
        index += 1 
    return result

print(longest_common_prefix_brute_force(["flower","flow","flight"]))
print(longest_common_prefix_brute_force(["dog","racecar","car"]))
print(longest_common_prefix_brute_force(["ab", "a"]))
print(longest_common_prefix_brute_force([""]))
print(longest_common_prefix_brute_force(["baab", "bac", "b", "za"]))
print(longest_common_prefix_brute_force(["a", "ab", "abc", "abcd"]))
print(longest_common_prefix_brute_force(["databricks_pipeline_prod", "databricks_pipeline_prof", "databricks_pipeline_proc"]))

# ---------------------------------------------------------------------------------------
# OPTION 2: FASTER APPROACH (Vertical Scanning Pointer - Your Optimized Solution)
# Core Concept: Sets the first string as a baseline. Scans character-by-character across all rows, 
#               terminating instantly the exact millisecond a character mismatch is detected.
# Time Complexity: O(N * M) Worst Case | O(1) Best Case (Instant exit if first characters mismatch).
# Space Complexity: O(1) - Pure pointer tracking with absolute zero extra memory allocations.
# ---------------------------------------------------------------------------------------
def longest_common_prefix_vertical(strs):
    if not strs or "" in strs: return ""
    base_str = strs[0]
    list_len = len(strs)
    if list_len == 1: return base_str
    
    smallest_str_len = min([len(s) for s in strs])
    for i in range(smallest_str_len):
        for y in range(1, list_len):
            # Instant termination on mismatch
            if base_str[i] != strs[y][i]: 
                return base_str[:i]
    return base_str[:smallest_str_len]
    # return base_str[:i+1] # Alternative return statement

print(longest_common_prefix_vertical(["flower","flow","flight"]))
print(longest_common_prefix_vertical(["dog","racecar","car"]))
print(longest_common_prefix_vertical(["ab", "a"]))
print(longest_common_prefix_vertical([""]))
print(longest_common_prefix_vertical(["baab", "bac", "b", "za"]))
print(longest_common_prefix_vertical(["a", "ab", "abc", "abcd"]))
print(longest_common_prefix_vertical(["databricks_pipeline_prod", "databricks_pipeline_prof", "databricks_pipeline_proc"]))

# ---------------------------------------------------------------------------------------
# OPTION 3: FASTER APPROACH WITH ALPHABETICAL SORTING (The Data Engineer's Trick)
# Core Concept: Alphabetically sorts the array. Sorting guarantees that the first and last strings 
#               in the array become the most extreme opposites. Thus, any prefix shared across 
#               the whole array MUST be shared between the first and last element only.
# Time Complexity: O(N log N * M) - Driven by the initial string sorting operation lifecycle.
# Space Complexity: O(N * M) - Allocates memory for the newly sorted array representation.
# ---------------------------------------------------------------------------------------
def longest_common_prefix_sort(strs):
    if not strs or "" in strs: return ""
    if len(strs) == 1: return strs[0]
    
    # Sort strings lexicographically (alphabetically)
    strs.sort()
    print(strs)
    first, last = strs[0], strs[-1]
    result = []
    
    # Only compare the two extremes
    for i in range(min(len(first), len(last))):
        if first[i] != last[i]:
            break
        result.append(first[i])
    return "".join(result)

print(longest_common_prefix_sort(["flower","flow","flight"]))
print(longest_common_prefix_sort(["dog","racecar","car"]))
print(longest_common_prefix_sort(["ab", "a"]))
print(longest_common_prefix_sort([""]))
print(longest_common_prefix_sort(["baab", "bac", "b", "za"]))
print(longest_common_prefix_sort(["a", "ab", "abc", "abcd"]))
print(longest_common_prefix_sort(["databricks_pipeline_prod", "databricks_pipeline_prof", "databricks_pipeline_proc"]))

# ======================= Q15 -> Valid Parentheses =====================================
"""
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Short Test Cases:
# TC1: "()"       -> Expected: True  (Simple match)
# TC2: "()[]{}"   -> Expected: True  (Multiple sequential pairs)
# TC3: "(]"       -> Expected: False (Mismatch bracket types)
# TC4: "([])"     -> Expected: True  (Nested valid pairs)
# TC5: "([)]"     -> Expected: False (Correct brackets, but invalid closing order)
"""

# ---------------------------------------------------------------------------------------
# OPTIMAL APPROACH: Linear Scan with Stack Data Structure (Last-In, First-Out)
# Core Concept: Linear scan using a Stack. Opening brackets are pushed onto the stack. 
#               When a closing bracket appears, it must validate and eliminate the bracket 
#               sitting at the absolute top of the stack.
# Time Complexity: O(N) - Passes through the string length exactly once.
# Space Complexity: O(N) - Worst case memory footprint stores all open brackets (e.g., "((((( ")
# ---------------------------------------------------------------------------------------
def isValid(s: str) -> bool:
    # Quick Check: An odd number of characters can never have balanced pairs
    if len(s) % 2 != 0: return False
    # Map closing brackets to their corresponding opening partners
    brackets_dict = {
        ')': '(', 
        '}': '{', 
        ']': '['
    }
    # Initialize an empty list to act as our Stack (LIFO)
    stack = []
    # Iterate character by character through the string matrix
    for char in s:
        # Check if the current character is a closing bracket
        if char in brackets_dict:
            # The stack must have items, and the top item must match the opening partner
            if stack and stack[-1] == brackets_dict[char]:
                stack.pop() # Match found! Remove the validated opening bracket from top
            else:
                return False # Break instantly on mismatch or structural imbalance
        else:
            # It's an opening bracket, append it directly onto the top of the stack
            stack.append(char)
    # If the stack is completely empty, every single pair opened and closed flawlessly
    return len(stack) == 0
    # return not stack # Alternative return statement

print(isValid("()"))
print(isValid("()[]{}"))
print(isValid("(]"))
print(isValid("([])"))
print(isValid("([)]"))

# ======================= Q16 -> Remove Duplicates from Sorted Array =====================
"""
Given an integer array nums sorted in non-decreasing order, remove the duplicates 
in-place such that each unique element appears only once. The relative order of the 
elements should be kept the same. Then return the number of unique elements (k).

The first k elements of nums must hold the unique numbers in their original sorted order.

Short Test Cases:
# TC1: [1, 1, 2]                 -> Expected: 2, nums = [1, 2, _]
# TC2: [0,0,1,1,1,2,2,3,3,4]     -> Expected: 5, nums = [0, 1, 2, 3, 4, _, _, _, _, _]
"""

# ---------------------------------------------------------------------------------------
# APPROACH 1: Element Popping & Resizing (Your Initial Implementation)
# Core Concept: Loops through with a while loop. When a duplicate is hit, it physically 
#               pops the index element out and appends an underscore to the end.
# Time Complexity: O(N^2) - .pop() forces an underlying memory shift of elements every single run.
# Space Complexity: O(1) - Modifies array layout in-place.
# Note: Functional, but causes boundary indexing traps and drops performance at scale.
# ---------------------------------------------------------------------------------------
def removeDuplicates_pop(nums):
    list_len = len(nums)
    if list_len < 2: 
        return list_len
    base_num = nums[0]
    index = 1
    unique_count = 1
    while index < list_len and isinstance(nums[index], int):
        if nums[index] == base_num:
            nums.pop(index)
            nums.append("_")
            index -= 1  # Adjust pointer because array shifted under us
        else:
            base_num = nums[index]
            unique_count += 1
        index += 1
    print(nums)
    return unique_count

print(removeDuplicates_pop([1,1,2,2,4]))
print(removeDuplicates_pop([0,0,1,1,1,2,2,3,3,4]))
print(removeDuplicates_pop([1,2,4]))
print(removeDuplicates_pop([1]))
print(removeDuplicates_pop([]))


# ---------------------------------------------------------------------------------------
# APPROACH 2: Two-Pointer Overwrite (Optimal Standard)
# Core Concept: Uses a slow 'write' pointer (i) and a fast 'read' pointer (j). The fast 
#               pointer scans for changes in value. When a new value is found, the slow 
#               pointer advances and overwrites the old duplicate. No physical resizing occurs.
# Time Complexity: O(N) - Single pass scan across the array layout.
# Space Complexity: O(1) - Modifies the memory space completely in-place.
# ---------------------------------------------------------------------------------------
def removeDuplicates(nums: list[int]) -> int:
    if not nums: 
        return 0
    i = 0  # Position of the last confirmed unique element
    for j in range(1, len(nums)):
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]  # Move unique value to its clean index position
    print(nums)
    return i + 1

print(removeDuplicates([1,1,2,2,4]))
print(removeDuplicates([0,0,1,1,1,2,2,3,3,4]))
print(removeDuplicates([1,2,4]))
print(removeDuplicates([1]))
print(removeDuplicates([]))

# ======================= Q17 -> Remove Element =========================================
"""
Given an integer array nums and an integer val, remove all occurrences of val in nums 
in-place. The order of the elements may be changed. Then return the number of elements 
in nums which are not equal to val (k).

The first k elements of nums must hold the valid elements. Remaining elements are ignored.

Short Test Cases:
# TC1: nums = [3, 2, 2, 3], val = 3     -> Expected: 2, nums = [2, 2, _, _]
# TC2: nums = [0,1,2,2,3,0,4,2], val = 2 -> Expected: 5, nums = [0, 1, 4, 0, 3, _, _, _]
"""

# ---------------------------------------------------------------------------------------
# APPROACH 1: Two-Pointer Overwrite (Optimal Standard)
# Core Concept: The Scanner (j) travels sequentially through the array layout. 
#               The Writer (i) only steps forward when the Scanner finds an element 
#               that is NOT equal to 'val' and writes it down.
# Time Complexity: O(N) - Linear single-pass scan.
# Space Complexity: O(1) - Constant memory allocated completely in-place.
# ---------------------------------------------------------------------------------------
def removeElement(nums: list[int], val: int) -> int:
    i = 0  # Initialize the Writer anchor at the starting gate
    # The Scanner (j) sweeps sequentially across the entire matrix length
    for j in range(len(nums)):
        # Trigger Condition: The moment we find a value we want to keep
        if nums[j] != val:
            nums[i] = nums[j]  # Write the keeper element over the old value/duplicate
            i += 1             # Shift the Writer forward to the next available slot
    # Because 'i' increments immediately after writing, it naturally stores 
    # the exact count of elements that are not equal to val.
    print(nums)
    return i

print(removeElement([3, 2, 2, 3], 3))
print(removeElement([0,1,2,2,3,0,4,2], 2))
print(removeElement([3,3], 2))
print(removeElement([2,2], 2))
print(removeElement([1], 2))
print(removeElement([0,1,2], 2))
print(removeElement([], 2))

# ==============Q18 -> FIND FIRST OCCURRENCE INDEX IN A STRING====================
"""
Problem Statement:
Given two strings needle and haystack, return the index of the first occurrence 
of needle in haystack, or -1 if needle is not part of haystack.
"""
# ==============================================================================

# ------------------------------------------------------------------------------
# APPROACH 1: THE PRODUCTION-GRADE BUILT-IN METHOD
# ------------------------------------------------------------------------------
# This approach leverages Python's optimized, built-in string libraries. 
# It is clean, readable, and perfectly suited for fast production data pipelines.
#
# Time Complexity: Time: O(1) Best / O(H) Average / O(H*N) Worst (C-optimized, fastest).
# Space Complexity: O(1) auxiliary space as it handles the search in place.
# ------------------------------------------------------------------------------

def strStr_builtin(haystack: str, needle: str) -> int:
    # Since constraints guarantee lowercase, we drop .lower() to save memory
    first_index = haystack.find(needle)
    
    if first_index != -1: 
        return first_index
    else: 
        return -1

print(strStr_builtin("sadbutsad", "sad"))      # Expected output: 0
print(strStr_builtin("leetcode", "leeto"))     # Expected output: -1
print(strStr_builtin("mississippi", "issip"))  # Expected output: 4
print(strStr_builtin("hello", "ll"))           # Expected output: 2

# ------------------------------------------------------------------------------
# APPROACH 2: THE LOGICAL SLIDING WINDOW
# ------------------------------------------------------------------------------
# Used if an interviewer asks to implement the search manually without relying 
# on internal methods like .find() or the 'in' keyword. We look at a slice of 
# the data matching the needle's length and slide it forward step-by-step.
#
# Time Complexity:  O(N) Best / O(H*N) Average / O((H-N)*N) Worst (Manual loop).
# Space Complexity: O(1) auxiliary space because it only calculates indices.
# ------------------------------------------------------------------------------

def strStr_sliding_window(haystack: str, needle: str) -> int:
    h_len = len(haystack)
    n_len = len(needle)
    
    # Edge Case: If the needle is longer than the haystack, a match is impossible
    if n_len > h_len:
        return -1
        
    # Slide the window across the haystack string.
    # Stop at (h_len - n_len + 1) because remaining characters wouldn't fit the needle.
    for i in range(h_len - n_len + 1):
        
        # Check if the current slice of haystack matches the needle
        if haystack[i : i + n_len] == needle:
            return i  # Return the starting index of the first match immediately
            
    return -1

print(strStr_sliding_window("sadbutsad", "sad"))      # Expected output: 0
print(strStr_sliding_window("leetcode", "leeto"))     # Expected output: -1
print(strStr_sliding_window("mississippi", "issip"))  # Expected output: 4
print(strStr_sliding_window("hello", "ll"))           # Expected output: 2

# ==============Q19 -> SEARCH INSERT POSITION IN A SORTED ARRAY================
"""
Problem Statement:
Given a sorted array of distinct integers and a target value, return the index 
if the target is found. If not, return the index where it would be if it were 
inserted in order.

You must write an algorithm with O(log n) runtime complexity.
"""
# ==============================================================================
# ------------------------------------------------------------------------------
# APPROACH 1: LINEAR SCAN (BRUTE FORCE INTUITION)
# ------------------------------------------------------------------------------
# This approach iterates through the array sequentially using a loop to check 
# where the target fits. It is simple but inefficient for large datasets.
#
# Time Complexity: O(1) Best / O(N) Average / O(N) Worst (Sequential scan).
# Space Complexity: O(1) - Constant Space. Flat memory usage.
# ------------------------------------------------------------------------------
def searchInsert_brute_force(nums: list, target: int) -> int:
    for index, num in enumerate(nums):
        # The moment we find a number >= target, that's our index or insertion point
        if target <= num:
            return index
    # If the target is greater than all elements, it belongs at the very end
    return len(nums)

print(searchInsert_brute_force([1, 3, 5, 6], 5))  # Expected output: 2
print(searchInsert_brute_force([1, 3, 5, 6], 2))  # Expected output: 1
print(searchInsert_brute_force([1, 3, 5, 6], 7))  # Expected output: 4
print(searchInsert_brute_force([1, 3, 5, 6], 0))  # Expected output: 0

# ------------------------------------------------------------------------------
# APPROACH 2: BINARY SEARCH (OPTIMIZED & COMPLIANT)
# ------------------------------------------------------------------------------
# Since the array is sorted, we use a two-pointer binary search. We look at 
# the midpoint and eliminate half of the remaining data with every step.
#
# Time Complexity: O(1) Best / O(log N) Average / O(log N) Worst (Divide and conquer).
# Space Complexity: O(1) - Constant Space. Pointers are modified in place.
# ------------------------------------------------------------------------------
def searchInsert(nums: list, target: int) -> int:
    low = 0
    high = len(nums) - 1
    while low <= high:
        # Calculate the middle index using integer floor division
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid        # Scenario A: Target found natively.
        elif nums[mid] < target:
            low = mid + 1     # Scenario B: Target is in the right half.
        else:
            high = mid - 1    # Scenario C: Target is in the left half.
    # CRITICAL INSIGHT: If the target is not in the array, the 'low' pointer 
    # naturally settles at the exact boundary where the element should be inserted.
    return low

print(searchInsert([1, 3, 5, 6], 5))  # Expected output: 2
print(searchInsert([1, 3, 5, 6], 2))  # Expected output: 1
print(searchInsert([1, 3, 5, 6], 7))  # Expected output: 4
print(searchInsert([1, 3, 5, 6], 0))  # Expected output: 0