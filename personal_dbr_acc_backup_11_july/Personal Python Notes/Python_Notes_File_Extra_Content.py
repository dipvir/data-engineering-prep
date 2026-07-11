# =======================================================================================
# PYTHON PRACTICE NOTEBOOK: EXTRA REFERENCE CONTENT & EXHAUSTIVE DICTIONARIES
# =======================================================================================
# * PURPOSE        : This file serves as a secondary reference vault for detailed, lengthy,
#                    or low-frequency programming lookups.
# * STRATEGY       : Keeps the primary study files streamlined and readable while retaining
#                    deep technical reference data for edge-case development tasks.

"""SECTION 01 :- COMPLETE LOGICAL REFERENCE CODEBOOK FOR STRFTIME / STRPTIME"""
"""
=====================================================================
COMPLETE STRFTIME / STRPTIME LEGAL FORMAT REFERENCE CODEBOOK
=====================================================================
CATEGORIZED ALPHABETICALLY BY LOGICAL TIME UNIT FOR SCANNING CLARITY
---------------------------------------------------------------------

--- YEAR TOKENS ---
 %Y -> 4-Digit Full Century Year                    (e.g., 2026)
 %y -> 2-Digit Shortened Year (No Century)          (e.g., 26)
 %C -> Century Number (Year divided by 100)         (e.g., 20)
 %G -> ISO 8601 Standard Year                       (e.g., 2026)

--- MONTH TOKENS ---
 %m -> 2-Digit Numeric Month                        (e.g., 05)
 %B -> Full Text Month Name                         (e.g., May)
 %b -> Shortened 3-Letter Text Month Name           (e.g., May)

--- DAY & WEEKDAY TOKENS ---
 %d -> 2-Digit Numeric Day of Month                 (e.g., 24)
 %A -> Full Text Weekday Name                       (e.g., Sunday)
 %a -> Shortened 3-Letter Text Weekday Name         (e.g., Sun)
 %w -> Weekday as Integer (0=Sunday to 6=Saturday)  (e.g., 0)
 %u -> ISO 8601 Weekday Integer (1=Monday to 7=Sun) (e.g., 7)
 %j -> Day Number of Year (001 to 366 Calendar)     (e.g., 144)

--- WEEK CALCULATION TOKENS ---
 %U -> Week Number (00-53, Sunday as First Day)     (e.g., 21)
 %W -> Week Number (00-53, Monday as First Day)     (e.g., 20)
 %V -> ISO 8601 Standard Week Number (01-53)        (e.g., 21)

--- TIME, CLOCK, & FRACTION TOKENS ---
 %H -> 2-Digit 24-Hour Clock Hour (Military Time)   (e.g., 11)
 %I -> 2-Digit 12-Hour Clock Hour (Standard Time)   (e.g., 11)
 %p -> AM / PM Standard Period Indicator            (e.g., AM)
 %M -> 2-Digit Numeric Minute                       (e.g., 30)
 %S -> 2-Digit Numeric Second                       (e.g., 00)
 %f -> 6-Digit Microsecond Value padding            (e.g., 548513)

--- ZONE & REGIONAL SYSTEM INTERFACES ---
 %z -> UTC Memory Offset Value Alignment            (e.g., +0530)
 %Z -> Named Text Timezone Short Code Identifier    (e.g., IST)
 %c -> Combined Local Date and Time String Representation
 %x -> Separated Local Date Only String Format Representation
 %X -> Separated Local Time Only String Format Representation
 %% -> Literal Percent Character Escape             (e.g., %)
=====================================================================
"""

"""SECTION 02     : THE ARCHITECTURAL RULES OF MODULES, PACKAGES, AND FUNCTIONS"""
"""
# 1. CORE ARCHITECTURAL BREAKDOWN
# ---------------------------------------------------------------------
# Python organizes its system utilities using a distinct naming and folder 
# hierarchy. Confusing these terms leads to syntax mistakes (like calling 
# a module as if it were a function).

# --- FUNCTIONS ---
# * DEFINITION: A named block of executable code designed to perform a 
#   specific action when called with parentheses `()`.
# * ANALOGY   : A single, specific hand tool inside a toolbox.
# * EXAMPLES  : print(), len(), abs()

# --- MODULES ---
# * DEFINITION: A single `.py` file containing organized Python code, 
#   including variables, classes, and built-in functions.
# * ANALOGY   : A standalone storage toolbox containing multiple tools.
# * EXAMPLES  : math, random

# --- PACKAGES ---
# * DEFINITION: A physical system directory (folder) that bundles multiple 
#   related modules together under a shared namespace.
# * ANALOGY   : A complete tool shed hosting a collection of different toolboxes.
# * EXAMPLES  : os, sys


# 2. SPECIFIC FILE COMPONENT CASE STUDIES
# ---------------------------------------------------------------------

# CASE STUDY 01: THE DATETIME MODULE QUIRK
# - STATUS: Built-in Module
# - QUIRK : The 'datetime' module contains an internal class that is *also* explicitly named 'datetime'. 
# - CODE  : This structural overlay forces you to reference both layers:
import datetime
print(datetime.datetime.now()) # (module_name.class_name.method_name)


# CASE STUDY 02: THE MATH MODULE
# - STATUS: Built-in Module
# - TRAP  : 'math' is strictly a module, NOT a function. You cannot execute 
#           math(). It serves strictly as a container for math functions.
import math
# print(math())      # <-- Throws TypeError: 'module' object is not callable
print(math.sqrt(16)) # Correct usage: Calls the sqrt() function inside math module


# CASE STUDY 03: THE JSON UTILITY
# - STATUS: Built-in Module (Structured as a Package under the hood)
# - USE   : To a developer importing it, it behaves exactly like a module 
#           (import json). Under Python's hood, it is structured as a directory 
#           package of files, but it is treated as a module in regular scripts.
import json
data_dict = {"status": "active"}
print(json.dumps(data_dict)) # Calls the dumps() function inside json module
# =====================================================================
"""
# --------------------------------------------
import os

# Create a dummy file first so the script can find it
with open("demofile_1.txt", "w") as setup_file:
    setup_file.write("Initial setup text.")

try:
    # 1. Opened with NO mode parameter -> Defaults to Read-Only ("r")
    f = open("demofile_1.txt")
    print(f"1. Connection opened. Is file closed? -> {f.closed}") # Output: False
    
    try:
        # This will fail and jump straight to the 'except' block
        f.write("Lorum Ipsum")
    except Exception as error_message:
        print(f"2. Error Caught: The system blocked the write attempt.")
    finally:
        # 2. This block runs NO MATTER WHAT to free up system memory
        f.close()
        print(f"3. Finally block executed. Is file closed? -> {f.closed}") # Output: True

except Exception as outer_error:
    print("Could not locate or open the file.")

# Clean up the system file afterwards
if os.path.exists("demofile_1.txt"):
    os.remove("demofile_1.txt")

