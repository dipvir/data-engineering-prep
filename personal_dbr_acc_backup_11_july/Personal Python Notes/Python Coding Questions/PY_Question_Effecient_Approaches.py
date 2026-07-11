# Databricks notebook source
# MAGIC %md
# MAGIC ---
# MAGIC
# MAGIC ### 🍳 The 3-Step Recipe for Two-Pointer "In-Place" Problems
# MAGIC
# MAGIC Whenever a question says **"Sorted Array"** and **"In-Place / Remove / Modify"**, mentally visualize a **Writer** and a **Scanner**.
# MAGIC
# MAGIC Here is the exact formula you repeat in your head to write the code:
# MAGIC
# MAGIC #### **Step 1: The Anchor (Where does the Writer start?)**
# MAGIC
# MAGIC Ask yourself: *Is the very first element always safe?* Yes, the first number (`nums[0]`) can never be a duplicate of anything before it. So, your **Writer anchor** starts at index `0`.
# MAGIC
# MAGIC ```python
# MAGIC i = 0  # My Writer anchor
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC #### **Step 2: The Scanner (The Loop)**
# MAGIC
# MAGIC Your **Scanner** (`j`) needs to look at everything else. Since index `0` is already anchored, your loop naturally starts scanning from index `1`.
# MAGIC
# MAGIC ```python
# MAGIC for j in range(1, len(nums)):  # My Scanner
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC #### **Step 3: The "Aha!" Moment (The Trigger Condition)**
# MAGIC
# MAGIC Inside the loop, the Scanner is moving fast. What is it looking for? It's looking for a change! It compares where it is standing (`nums[j]`) to what the Writer last wrote (`nums[i]`).
# MAGIC
# MAGIC * If they are the **same**, the Scanner ignores it and keeps running.
# MAGIC * The moment they are **different** (the "Aha!" moment), you do two quick actions:
# MAGIC 1. Move your Writer forward to a fresh slot (`i += 1`).
# MAGIC 2. Overwrite that slot with the new value (`nums[i] = nums[j]`).
# MAGIC
# MAGIC
# MAGIC
# MAGIC ```python
# MAGIC if nums[j] != nums[i]:  # Found something new!
# MAGIC     i += 1              # Step 1: Advance the Writer
# MAGIC     nums[i] = nums[j]   # Step 2: Write the new value
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧠 How to Practice This Right Now (Mental Repetition)
# MAGIC
# MAGIC Look at how this exact same 3-step recipe applies to a slightly different question. What if the interviewer says: *"Remove all occurrences of the number `val = 3` in-place from an array?"* (LeetCode 27).
# MAGIC
# MAGIC 1. **The Anchor:** This time, index 0 might be a `3`, so it's not safe. Our Writer starts at `0`, but our Scanner *also* has to start at `0`.
# MAGIC 2. **The Scanner:** Loops through the whole array.
# MAGIC 3. **The Trigger:** The Scanner is looking for anything that is **NOT** a `3`. The moment `nums[j] != 3`, the Writer logs it: `nums[i] = nums[j]`, and the Writer moves forward `i += 1`.
# MAGIC
# MAGIC See how it's the exact same muscle memory?
# MAGIC
# MAGIC * **Writer Pointer (`i`):** Only moves when we find a "keeper."
# MAGIC * **Scanner Pointer (`j`):** Moves on every single beat of the clock.
# MAGIC
# MAGIC Does breaking it down into a **Writer vs. Scanner** workflow make the actual code structure feel easier to visualize from scratch? Give your brain a second to chew on that mental model!

# COMMAND ----------

# MAGIC %md
# MAGIC
