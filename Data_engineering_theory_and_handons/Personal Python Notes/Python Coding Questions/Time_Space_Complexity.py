# =======================================================================================
#                  COMPUTER SCIENCE & ENGINEERING: COMPLETE BIG-O MASTER GUIDE
# =======================================================================================
# DESCRIPTION: A core Computer Science curriculum breakdown of the 7 primary asymptotic 
#              scalability curves across Time and Space dimensions.
# =======================================================================================

# ---------------------------------------------------------------------------------------
# CORE PREREQUISITE: THE TWO HARDWARE ASSETS
# ---------------------------------------------------------------------------------------
# Every algorithm you write bargains directly with your system's underlying hardware resources:
#   1. CPU Clock Cycles -> Tracked by TIME COMPLEXITY (Total primitive operation count).
#   2. RAM Memory Slots -> Tracked by SPACE COMPLEXITY (Auxiliary data structure overhead).
#
# Big-O Notation: A mathematical asymptotic notation describing the limiting behavior of a 
# function, tracking upper bounds in the WORST-CASE SCENARIO as input size (N) approaches infinity.
# ---------------------------------------------------------------------------------------

# =======================================================================================
# PART 1: THE COMPLETE TIME COMPLEXITY SPECTRUM (BEST TO WORST)
# =======================================================================================

# ---------------------------------------------------------------------------------------
# RATIO 1: CONSTANT TIME -> O(1) [EXCELLENT]
# Core Rule: Algorithm execution step count is completely independent of the input size N.
# Academic Analogy: Evaluating if the top element of a Stack of size N meets a condition.
# ---------------------------------------------------------------------------------------
def constant_time_example(lst):
    # Direct offset memory addressing requires a single primitive CPU step.
    return lst[0]


# ---------------------------------------------------------------------------------------
# RATIO 2: LOGARITHMIC TIME -> O(log N) [GREAT]
# Core Rule: Highly efficient. Every processing step halves the remaining dataset size.
# Academic Analogy: Binary Search across a sorted array (e.g., looking up a word in a 
# physical dictionary by repeatedly splitting the pages exactly in the middle).
# ---------------------------------------------------------------------------------------
def logarithmic_time_example(sorted_lst, target):
    low = 0
    high = len(sorted_lst) - 1\
    while low <= high:
        mid = (low + high) // 2  # Find midpoint axis
        if sorted_lst[mid] == target:
            return mid
        elif sorted_lst[mid] < target:
            low = mid + 1        # Discard lower half
        else:
            high = mid - 1       # Discard upper half
    return -1


# ---------------------------------------------------------------------------------------
# RATIO 3: LINEAR TIME -> O(N) [GOOD / FAIR]
# Core Rule: The total number of primitive operations grows in direct 1:1 proportion with N.
# Academic Analogy: Performing a sequential Linear Search across an unsorted array.
# ---------------------------------------------------------------------------------------
def linear_time_example(lst, target):
    # Worst-case: Target is at the very end or entirely absent.
    for item in lst:
        if item == target:
            return True
    return False


# ---------------------------------------------------------------------------------------
# RATIO 4: LINEARITHMIC TIME -> O(N log N) [STANDARD SORTING]
# Core Rule: Achieved when an O(N) linear pass is combined with an O(log N) divide-and-conquer strategy.
# Academic Analogy: Optimal sorting algorithms like Merge Sort, Quick Sort, or Python's built-in Timsort.
# ---------------------------------------------------------------------------------------
def linearithmic_time_example(lst):
    # Python's native sorting engine runs on Timsort, which scales at O(N log N) performance.
    lst.sort()
    return lst


# ---------------------------------------------------------------------------------------
# RATIO 5: QUADRATIC TIME -> O(N^2) [POOR / SLOW]
# Core Rule: Processing cycles scale as a square function of input size (N * N).
# Danger: Scaling the input dataset by a factor of 10 results in a 100x increase in CPU operations!
# Academic Analogy: Brute-force nested loops comparing every element to all other elements.
# ---------------------------------------------------------------------------------------
def quadratic_time_example(lst):
    # Nested loops, where the inner loop range scales with the outer loop range.
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False


# ---------------------------------------------------------------------------------------
# RATIO 6: CUBIC TIME -> O(N^3) [VERY SLOW]
# Core Rule: Three nested loops running on the same dataset dimension.
# Academic Analogy: Brute-force 3D matrix multiplication or finding triplet groups in a list.
# ---------------------------------------------------------------------------------------
def cubic_time_example(matrix_3d):
    n = len(matrix_3d)
    count = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if matrix_3d[i][j][k] == 0:
                    count += 1
    return count


# ---------------------------------------------------------------------------------------
# RATIO 7: EXPONENTIAL TIME -> O(2^N) [CATASTROPHIC]
# Core Rule: Execution overhead doubles with every single addition to the dataset size N.
# Academic Analogy: Finding all possible subsets of a set (Power Set) or brute-force 
# recursive calculations without optimization.
# ---------------------------------------------------------------------------------------
def exponential_time_example(n):
    # Unoptimized, naive recursive Fibonacci sequence execution.
    if n <= 1:
        return n
    # Generates a massive binary tree of repetitive function stack allocations.
    return exponential_time_example(n - 1) + exponential_time_example(n - 2)


# =======================================================================================
# PART 2: SPACE COMPLEXITY ANALYSIS (AUXILIARY RAM STACK & HEAP AUDITS)
# =======================================================================================

# ---------------------------------------------------------------------------------------
# RATIO 1: CONSTANT SPACE -> O(1)
# Core Rule: The algorithm performs destructive in-place mutations without allocating 
# extra context-dependent structures. Memory footprint is flat.
# ---------------------------------------------------------------------------------------
def constant_space_reversal(lst):
    # Allocates exactly ONE auxiliary scalar pointer reference (p1) in a single stack frame.
    for i in range(len(lst) // 2):
        p1 = lst[i]
        lst[i] = lst[len(lst) - 1 - i]
        lst[len(lst) - 1 - i] = p1
    return lst

# ---------------------------------------------------------------------------------------
# RATIO 2: LINEAR SPACE -> O(N)
# Core Rule: The algorithm allocates secondary memory objects (on stack or heap) that 
# scale up linearly in size to support data processing.
# ---------------------------------------------------------------------------------------
def linear_space_tracking(lst):
    # Allocates a dynamic hash-set container in heap memory.
    # Worst-Case: Input elements are unique; hash-set scales to hold all N items simultaneously.
    seen = set()
    for num in lst:
        if num in seen:
            return True
        seen.add(num)
    return False


# =======================================================================================
# PART 3: THE COMPREHENSIVE MATH ANALYSIS LAWS
# =======================================================================================
"""
LAW 1: Asymptotic Dominance (Law of Dominant Terms)
       When combining sequential operations, lower-order terms and constants are dropped.
       O(1) + O(N) + O(N^2) simplifies to the highest-order dominant term: O(N^2).

LAW 2: Structural Compounding (Nested Loops)
       If an O(N) loop encapsulates an internal O(N) execution loop, their time values 
       multiply, generating an O(N * N) = O(N^2) computational expression.

LAW 3: Shorthand Tracing Rules for Quick Code Audits:
       - Direct Primitive Arithmetic / Array Index Index Lookup  -->  O(1) Time
       - Array Halving / Binary Search Splits                      -->  O(log N) Time
       - Single Traversal Loop (0 to N)                            -->  O(N) Time
       - Symmetrically Bounded Double-Nested Loops                 -->  O(N^2) Time
"""

# ========================================End============================================