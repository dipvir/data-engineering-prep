# Databricks notebook source
# DBTITLE 1,Imports
from pyspark.sql.types import *
import pyspark.sql.functions as F

# COMMAND ----------

# DBTITLE 1,Spark Query Plan - Detailed Overview
# MAGIC %md
# MAGIC ### Spark Query Plan — A Deep Dive
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### What is a Spark Query Plan?
# MAGIC
# MAGIC When you submit a Spark SQL query or a DataFrame transformation, Spark **does not execute it immediately**. Instead, it builds a **Query Plan** — a structured, multi-stage blueprint that describes how the computation will be performed. This plan goes through several transformations before actual execution.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Stages of a Spark Query Plan
# MAGIC
# MAGIC ```
# MAGIC SQL / DataFrame API
# MAGIC        | <- validate if syntax is correct
# MAGIC        v
# MAGIC ┌─────────────────────────┐
# MAGIC │ Unresolved Logical Plan │  ← Raw parsed tree (names not validated)
# MAGIC └─────────────────────────┘
# MAGIC        |
# MAGIC    [Analyzer]  — Resolves column names, table refs via Catalog
# MAGIC        |
# MAGIC        v
# MAGIC ┌─────────────────────────┐
# MAGIC │  Resolved Logical Plan  │  ← All references validated
# MAGIC └─────────────────────────┘
# MAGIC        |
# MAGIC    [Optimizer]  — Applies Catalyst rule-based & cost-based optimizations
# MAGIC        |
# MAGIC        v
# MAGIC ┌─────────────────────────┐
# MAGIC │  Optimized Logical Plan │  ← Filters pushed down, columns pruned, etc.
# MAGIC └─────────────────────────┘
# MAGIC        |
# MAGIC    [Planner]  — Converts logical plan to one or more physical strategies
# MAGIC        |
# MAGIC        v
# MAGIC ┌─────────────────────────┐
# MAGIC │     Physical Plan(s)    │  ← Multiple candidate execution strategies
# MAGIC └─────────────────────────┘
# MAGIC        |
# MAGIC    [Cost Model]  — Selects the best physical plan
# MAGIC        |
# MAGIC        v
# MAGIC ┌─────────────────────────┐
# MAGIC │  Selected Physical Plan │  ← Final execution plan with operators
# MAGIC └─────────────────────────┘
# MAGIC        |
# MAGIC    [Code Generation]  — Whole-stage codegen (Tungsten)
# MAGIC        |
# MAGIC        v
# MAGIC       RDD Execution
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 1. Unresolved Logical Plan
# MAGIC
# MAGIC - Produced by the **Parser** from SQL strings or DataFrame transformations.
# MAGIC - Column names and table references are **not yet validated** — they are treated as unresolved attributes.
# MAGIC - Think of it as an **Abstract Syntax Tree (AST)**.
# MAGIC
# MAGIC ```python
# MAGIC df = spark.sql("SELECT name, age FROM employees WHERE age > 30")
# MAGIC # At this stage: 'name', 'age', 'employees' are just strings — not validated yet
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 2. Resolved (Analyzed) Logical Plan
# MAGIC
# MAGIC - The **Analyzer** uses the **Catalog** (metadata store) to resolve:
# MAGIC   - Table names → actual data sources
# MAGIC   - Column names → validated fields with data types
# MAGIC   - Functions → registered UDFs or built-ins
# MAGIC - Raises `AnalysisException` if any reference cannot be resolved.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 3. Optimized Logical Plan
# MAGIC
# MAGIC The **Catalyst Optimizer** applies a rich set of rules:
# MAGIC
# MAGIC | Optimization | Description |
# MAGIC |---|---|
# MAGIC | **Predicate Pushdown** | Moves filters as close to the data source as possible |
# MAGIC | **Column Pruning** | Removes unused columns early to reduce I/O |
# MAGIC | **Constant Folding** | Evaluates constant expressions at compile time (e.g., `1 + 2` → `3`) |
# MAGIC | **Boolean Simplification** | Simplifies logical conditions |
# MAGIC | **Join Reordering** | Reorders joins using table statistics (Cost-Based Optimizer) |
# MAGIC | **Subquery Elimination** | Flattens correlated subqueries where possible |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 4. Physical Plan
# MAGIC
# MAGIC - Translates the logical plan into **executable operators** using Spark's execution engine.
# MAGIC - Key physical operators:
# MAGIC
# MAGIC | Operator | Description |
# MAGIC |---|---|
# MAGIC | `FileScan` | Reads data from disk (Parquet, Delta, CSV, etc.) |
# MAGIC | `Filter` | Applies row-level predicates |
# MAGIC | `Project` | Selects specific columns |
# MAGIC | `BroadcastHashJoin` | Joins a small table via broadcast |
# MAGIC | `SortMergeJoin` | Joins two large tables after sorting |
# MAGIC | `HashAggregate` | Performs aggregation using hash maps |
# MAGIC | `Exchange` | Shuffles data across partitions (network I/O) |
# MAGIC | `Sort` | Sorts data within partitions |
# MAGIC | `WholeStageCodegen` | Combines multiple operators into a single JVM function |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 5. Whole-Stage Code Generation (Tungsten)
# MAGIC
# MAGIC - Spark fuses multiple operators into **a single optimized JVM bytecode function**.
# MAGIC - Eliminates virtual function dispatch overhead between operators.
# MAGIC - Dramatically improves CPU efficiency for tight loops.
# MAGIC - Indicated by `*(n)` prefix in the physical plan output.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### How to Inspect the Query Plan
# MAGIC
# MAGIC ```python
# MAGIC df = spark.sql("SELECT dept, COUNT(*) as cnt FROM employees GROUP BY dept")
# MAGIC
# MAGIC # 1. Parsed (Unresolved) Logical Plan
# MAGIC df.explain("parsed")
# MAGIC
# MAGIC # 2. Analyzed (Resolved) Logical Plan
# MAGIC df.explain("analyzed")
# MAGIC
# MAGIC # 3. Optimized Logical Plan
# MAGIC df.explain("optimized")
# MAGIC
# MAGIC # 4. Physical Plan only (default)
# MAGIC df.explain()
# MAGIC
# MAGIC # 5. Full plan — all 4 stages at once
# MAGIC df.explain("extended")   # or df.explain(True)
# MAGIC
# MAGIC # 6. Formatted (most readable, recommended)
# MAGIC df.explain("formatted")
# MAGIC
# MAGIC # 7. Cost-Based plan with statistics
# MAGIC df.explain("cost")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Understanding Exchange (Shuffle)
# MAGIC
# MAGIC The **Exchange** operator represents a **shuffle** — one of the most expensive operations:
# MAGIC
# MAGIC - Data is **redistributed across partitions** over the network.
# MAGIC - Triggered by: `groupBy`, `join` (SortMergeJoin), `orderBy`, `distinct`, `repartition`.
# MAGIC - Controlled by `spark.sql.shuffle.partitions` (default: **200**).
# MAGIC
# MAGIC ```python
# MAGIC # Tune shuffle partitions for your data size
# MAGIC spark.conf.set("spark.sql.shuffle.partitions", "50")
# MAGIC
# MAGIC # Or use Adaptive Query Execution (AQE) to auto-tune
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Adaptive Query Execution (AQE)
# MAGIC
# MAGIC Introduced in Spark 3.0 — **re-optimizes the plan at runtime** using actual data statistics:
# MAGIC
# MAGIC | Feature | Benefit |
# MAGIC |---|---|
# MAGIC | **Dynamic Partition Coalescing** | Merges small shuffle partitions automatically |
# MAGIC | **Dynamic Join Strategy Switching** | Converts SortMergeJoin → BroadcastHashJoin if one side is small |
# MAGIC | **Skew Join Optimization** | Splits and replicates skewed partitions |
# MAGIC
# MAGIC ```python
# MAGIC # Enable AQE (default: true in Spark 3.2+)
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Join Strategies in the Physical Plan
# MAGIC
# MAGIC | Join Type | When Used | Cost |
# MAGIC |---|---|---|
# MAGIC | **BroadcastHashJoin** | One table fits in memory (`<= 10 MB` default) | Fast — no shuffle |
# MAGIC | **SortMergeJoin** | Both tables are large | Expensive — requires sort + shuffle |
# MAGIC | **ShuffledHashJoin** | Medium-sized tables | Hash-based, requires shuffle |
# MAGIC | **BroadcastNestedLoopJoin** | Non-equi joins, no join key | Very slow — O(n×m) |
# MAGIC | **CartesianProduct** | Cross join | Extremely slow |
# MAGIC
# MAGIC ```python
# MAGIC # Control broadcast threshold
# MAGIC spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)  # 50 MB
# MAGIC
# MAGIC # Force broadcast with hint
# MAGIC from pyspark.sql.functions import broadcast
# MAGIC df_result = large_df.join(broadcast(small_df), "id")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Key Metrics to Watch in the Spark UI
# MAGIC
# MAGIC | Metric | What to Look For |
# MAGIC |---|---|
# MAGIC | **Shuffle Read/Write** | High values → expensive shuffle, consider partitioning |
# MAGIC | **Spill (Memory/Disk)** | Data spilling to disk → increase executor memory |
# MAGIC | **Task Duration Skew** | One task much longer → data skew issue |
# MAGIC | **GC Time** | High % → JVM garbage collection pressure |
# MAGIC | **Records Read** | Compare to output — large reduction = good filter pushdown |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Quick Reference: Plan Reading Tips
# MAGIC
# MAGIC > **Read the physical plan bottom-up** — data flows from the leaf nodes (data sources) upward through transformations to the final result.
# MAGIC
# MAGIC - `*(n)` → Inside WholeStageCodegen stage `n`  
# MAGIC - `+- ` → Child operator  
# MAGIC - `Exchange` → Shuffle boundary (expensive!)  
# MAGIC - `==` separators → Divide logical vs physical sections in `explain("extended")`  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Summary
# MAGIC
# MAGIC ```
# MAGIC Parsed → Analyzed → Optimized → Physical → CodeGen → Execution
# MAGIC    ↑          ↑           ↑           ↑
# MAGIC Parser    Analyzer    Catalyst    Planner
# MAGIC                      Optimizer
# MAGIC ```
# MAGIC
# MAGIC | Stage | Component | Key Action |
# MAGIC |---|---|---|
# MAGIC | Parsed | Parser | Build AST |
# MAGIC | Analyzed | Analyzer + Catalog | Resolve names & types |
# MAGIC | Optimized | Catalyst Optimizer | Apply rule/cost-based optimizations |
# MAGIC | Physical | Planner | Choose execution strategy |
# MAGIC | Execution | Tungsten + AQE | Run with codegen & runtime re-optimization |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Loading Source Files As Dataframe

# COMMAND ----------

# DBTITLE 1,Display Sample Files in Data Lake Path
# MAGIC %fs ls abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/

# COMMAND ----------

# DBTITLE 1,Load and Preview Sample Transactions Data
transactions_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/transactions.parquet/")
display(transactions_df.limit(5))

# COMMAND ----------

# DBTITLE 1,Getting Active And Total Spark Partitions Of Dataframe
# Returns the number of unique Spark partition IDs present in the DataFrame (may be less than total partitions if some are empty)
num_active_partitions = transactions_df.select(F.spark_partition_id().alias("partition_id")).distinct().count()

# Returns the total number of partitions allocated to the DataFrame's underlying RDD (including empty partitions)
num_total_partitions = transactions_df.rdd.getNumPartitions()

print(num_active_partitions)
print(num_total_partitions)

# COMMAND ----------

# DBTITLE 1,Load and Preview Sample Customers Data
customers_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/customers.parquet/")
display(customers_df.limit(5))

# COMMAND ----------

# DBTITLE 1,Getting Active And Total Spark Partitions Of Dataframe
# Returns the number of unique Spark partition IDs present in the DataFrame (may be less than total partitions if some are empty)
num_active_partitions = customers_df.select(F.spark_partition_id().alias("partition_id")).distinct().count()

# Returns the total number of partitions allocated to the DataFrame's underlying RDD (including empty partitions)
num_total_partitions = customers_df.rdd.getNumPartitions()

print(num_active_partitions)
print(num_total_partitions)

# COMMAND ----------

# MAGIC %md
# MAGIC **Note :- Please Read This**
# MAGIC
# MAGIC - In Spark, a query plan goes through several stages: Parsed, Analyzed, Optimized, and finally **Physical Plan**. Only the last stage (**== Physical Plan ==**) is actually executed on the cluster to perform the transformations and actions.
# MAGIC - The examples shown below use `.explain()` to display the query plan. This is for inspection and learning purposes—**calling `.explain()` does not trigger a Spark job or execute the transformations**. It simply prints the plan to the console.
# MAGIC - You can use `.explain()` with different modes to view various levels of detail:
# MAGIC     - `df.explain()` — shows only the physical plan (default).
# MAGIC     - `df.explain(True)` or `df.explain("extended")` — shows all stages: parsed, analyzed, optimized, and physical plans.
# MAGIC     - `df.explain("formatted")` — shows a readable, structured breakdown of the physical plan.
# MAGIC     - `df.explain("cost")` — shows logical plan with statistics if available.
# MAGIC - **Why inspect the plan?** Understanding the query plan helps you:
# MAGIC     - Identify expensive operations (like shuffles, joins, scans).
# MAGIC     - Optimize your code by minimizing wide transformations.
# MAGIC     - Debug issues related to performance or correctness.
# MAGIC - **Key takeaway:** Only the physical plan is executed, but reviewing all stages helps you understand how Spark interprets and optimizes your code before execution.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Narrow Transformations in Spark
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### What Are Narrow Transformations?
# MAGIC
# MAGIC **Narrow transformations** are operations in Spark where each input partition contributes to only one output partition. Data does **not need to be shuffled** across the network; it stays within the same partition. This makes narrow transformations **fast and efficient**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Key Characteristics
# MAGIC
# MAGIC - **No shuffle:** Data remains in the same partition.
# MAGIC - **Low network I/O:** No data movement between executors.
# MAGIC - **Examples:** `map`, `filter`, `union`, `sample`, `withColumn`, `select`.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Why Are They Important?
# MAGIC
# MAGIC - **Performance:** Narrow transformations are much faster than wide transformations because they avoid expensive shuffles.
# MAGIC - **Execution:** Spark can pipeline multiple narrow transformations together in a single stage.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Examples
# MAGIC
# MAGIC python
# MAGIC ```
# MAGIC # Filter: Only rows where city == 'boston'
# MAGIC df = customers_df.filter(F.col("city") == "boston")
# MAGIC
# MAGIC # Map: Add 5 years to age
# MAGIC df = df.withColumn("age", F.col("age") + 5)
# MAGIC
# MAGIC # Select: Choose specific columns
# MAGIC df = df.select("cust_id", "name", "age")
# MAGIC ```
# MAGIC
# MAGIC All these are **narrow transformations** — each row is processed independently, and no shuffle occurs.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Visual Representation
# MAGIC
# MAGIC ```
# MAGIC Partition 1 ──► Partition 1
# MAGIC Partition 2 ──► Partition 2
# MAGIC Partition 3 ──► Partition 3
# MAGIC ```
# MAGIC Each input partition maps directly to an output partition.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Summary Table
# MAGIC
# MAGIC | Transformation | Narrow/Wide | Shuffle? |
# MAGIC |---|---|---|
# MAGIC | `map`, `filter`, `select`, `withColumn` | Narrow | No |
# MAGIC | `groupBy`, `join`, `distinct`, `repartition` | Wide | Yes |
# MAGIC
# MAGIC **Narrow transformations** are the backbone of efficient Spark pipelines. Use them wherever possible to minimize shuffles and maximize performance.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC **The phrase meaning: `Each input partition contributes to only one output partition`**
# MAGIC
# MAGIC Think of your data as being split into separate "buckets" (partitions) spread across multiple machines in a cluster.
# MAGIC
# MAGIC
# MAGIC
# MAGIC When Spark applies a narrow transformation, whatever data lives in **Partition 1 stays in Partition 1** to produce the output. It never needs to look at or combine with data from Partition 2 or Partition 3.
# MAGIC
# MAGIC **A concrete example with narrow transformations** like `filter`:
# MAGIC
# MAGIC ```
# MAGIC Input                                                   Output
# MAGIC ─────────────────────────────────────────────────────────────────────────────────────
# MAGIC Partition 1: [row1, row2, row3]  →  Partition 1: [row1, row3]   (row2 filtered out)
# MAGIC Partition 2: [row4, row5, row6]  →  Partition 2: [row4, row6]   (row5 filtered out)
# MAGIC Partition 3: [row7, row8, row9]  →  Partition 3: [row8, row9]   (row7 filtered out)
# MAGIC ```
# MAGIC
# MAGIC Each executor processes its own partition **independently and in isolation**. No executor needs to talk to another executor.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Contrast this with a wide transformation** like `groupBy`:
# MAGIC
# MAGIC **Where `Each input partition may contribute data to multiple output partitions`**
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC Input                                                   Output
# MAGIC ───────────────────────────────────────────────────────────────────────────
# MAGIC Partition 1: [city=boston, city=nyc]  ──►  Partition A: [all boston rows]
# MAGIC Partition 2: [city=boston, city=la ]  ──►  Partition B: [all nyc rows]
# MAGIC Partition 3: [city=nyc,    city=la ]  ──►  Partition C: [all la rows]
# MAGIC ```
# MAGIC
# MAGIC Here, rows with `city=boston` are **scattered across multiple partitions**. To group them together, Spark must **shuffle** — move data across the network — so all boston rows land in the same partition. This is expensive.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **The key insight:** "one input partition → one output partition" simply means the transformation is **self-contained per partition** — no cross-partition communication needed, hence no shuffle, hence fast.

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For Narrow Transformations
df_narrow_transform = (
    customers_df.filter(F.col("city") == "boston")
    .withColumn("first_name", F.split("name", " ").getItem(0))
    .withColumn("last_name", F.split("name", " ").getItem(1))
    .withColumn("age", F.col("age") + F.lit(5))
    .select("cust_id", "first_name", "last_name", "age", "gender", "birthday")
)

df_narrow_transform.show(5, False)
df_narrow_transform.explain(True)

# COMMAND ----------

# DBTITLE 1,Check Number Of Partitions In Spark RDD
df_narrow_transform.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ```
# MAGIC *(1) Project [cust_id#53, split(name#54,  , 2)[0] AS first_name#125, split(name#54,  , 3)[1] AS last_name#127, (cast(age#55 as bigint) + 5) AS age#129L, gender#56, birthday#57]
# MAGIC +- *(1) Filter (isnotnull(city#59) AND (city#59 = boston))
# MAGIC    +- *(1) ColumnarToRow
# MAGIC       +- FileScan parquet [cust_id#53,name#54,age#55,gender#56,birthday#57,city#59] Batched: true, DataFilters: [isnotnull(city#59), (city#59 = boston)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [IsNotNull(city), EqualTo(city,boston)], ReadSchema: struct<cust_id:string,name:string,age:string,gender:string,birthday:string,city:string>
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads data from the Parquet file. Only columns needed for downstream operations are loaded.  
# MAGIC   - **DataFilters**: Filters applied at scan time, including `isnotnull(city)` and `(city = boston)`, help reduce the amount of data read (i.e **predicate pushdown**).
# MAGIC   - **PushedFilters**: These are filters Spark pushes down to the Parquet reader for efficiency.
# MAGIC   - **ReadSchema**: Only the columns required by downstream operations are read, minimizing I/O.
# MAGIC - `ColumnarToRow`: Converts columnar batches (optimized for scan and vectorized processing) to row format, which is needed for subsequent row-based operations like `filter` and `project`.
# MAGIC - `Filter (isnotnull(city#59) AND (city#59 = boston))`: Filters rows where `city` is not null and equals "boston". The `isnotnull(city)` filter ensures null values are excluded, which is important for correctness and can improve performance.
# MAGIC - `Project [...]`: Creates new columns (`first_name`, `last_name`, `age + 5`) and selects the required fields for output.
# MAGIC
# MAGIC > **All steps are narrow transformations. No `Exchange` operator means no shuffle; each partition is processed independently and efficiently.**

# COMMAND ----------

# DBTITLE 1,rough
print("Hello")

# COMMAND ----------

# DBTITLE 1,Wide Transformations in Spark
# MAGIC %md
# MAGIC ### Wide Transformations in Spark
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### What Are Wide Transformations?
# MAGIC
# MAGIC **Wide transformations** are operations in Spark where each input partition may contribute data to **multiple output partitions**. This requires data to be **shuffled across the network** between executors — making them significantly more expensive than narrow transformations.
# MAGIC
# MAGIC > Wide transformations are also called **shuffle transformations** because they always trigger a shuffle.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### What is a Shuffle?
# MAGIC
# MAGIC A **shuffle** is the process of redistributing data across partitions — data physically moves over the network from one executor to another.
# MAGIC
# MAGIC ```
# MAGIC Before Shuffle (data spread randomly):          After Shuffle (data regrouped by key):
# MAGIC
# MAGIC Executor 1 Partition: [boston, nyc, la]          Executor 1: [ALL boston rows]
# MAGIC Executor 2 Partition: [boston, nyc, la]   ──►    Executor 2: [ALL nyc rows]
# MAGIC Executor 3 Partition: [boston, nyc, la]          Executor 3: [ALL la rows]
# MAGIC ```
# MAGIC
# MAGIC Spark writes intermediate shuffle data to **disk**, then reads it back — this is why shuffles are costly.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Key Characteristics
# MAGIC
# MAGIC | Property | Detail |
# MAGIC |---|---|
# MAGIC | **Shuffle** | Always triggers a shuffle (network I/O) |
# MAGIC | **Disk I/O** | Shuffle data is written to & read from disk |
# MAGIC | **Stage Boundary** | Creates a new Spark stage |
# MAGIC | **Partition Count** | Output partition count controlled by `spark.sql.shuffle.partitions` (default: **200**) |
# MAGIC | **Fault Tolerance** | Shuffle files are retained so lost partitions can be recomputed |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Common Wide Transformations
# MAGIC
# MAGIC | Operation | Why It's Wide |
# MAGIC |---|---|
# MAGIC | `groupBy()` | Rows with the same key must be co-located |
# MAGIC | `join()` (SortMergeJoin) | Matching keys from two DFs must land on the same partition |
# MAGIC | `distinct()` | All copies of duplicate rows must meet to be deduplicated |
# MAGIC | `orderBy()` / `sort()` | Global sort requires all data to be ordered across partitions |
# MAGIC | `repartition(n)` | Explicitly redistributes data into `n` partitions |
# MAGIC | `cube()` / `rollup()` | Aggregations over multiple grouping sets |
# MAGIC | `window()` | Partitions data by window spec keys |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Stages and Shuffle Boundaries
# MAGIC
# MAGIC Every wide transformation creates a **stage boundary** in Spark's execution DAG.
# MAGIC
# MAGIC ```
# MAGIC Stage 1 (no shuffle)                   Stage 2 (after shuffle)
# MAGIC ────────────────────                   ─────────────────────────
# MAGIC FileScan                               HashAggregate (final)
# MAGIC   └─ Filter                              └─ Exchange (Shuffle Read)
# MAGIC        └─ Project                               ↑
# MAGIC             └─ HashAggregate (partial)    ← Shuffle Write
# MAGIC                  └─ Exchange  ────────────────────────────►
# MAGIC                       (Shuffle Boundary)
# MAGIC ```
# MAGIC
# MAGIC - **Stage 1** ends at the `Exchange` (shuffle write).
# MAGIC - **Stage 2** starts after the `Exchange` (shuffle read).
# MAGIC - Each stage runs independently; Stage 2 cannot start until all tasks in Stage 1 complete.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Wide Transformation Example
# MAGIC
# MAGIC ```python
# MAGIC # Wide Transformation: groupBy triggers a shuffle
# MAGIC df_wide = transactions_df \
# MAGIC     .groupBy("city") \
# MAGIC     .agg(
# MAGIC         F.count("transaction_id").alias("total_transactions"),
# MAGIC         F.sum("amount").alias("total_amount")
# MAGIC     )
# MAGIC
# MAGIC df_wide.explain("formatted")
# MAGIC # Look for: Exchange hashpartitioning — this is the shuffle!
# MAGIC ```
# MAGIC
# MAGIC In the physical plan you will see:
# MAGIC
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC *(2) HashAggregate(keys=[city], functions=[count, sum])
# MAGIC +- Exchange hashpartitioning(city, 200)        ← SHUFFLE HERE
# MAGIC    +- *(1) HashAggregate(keys=[city], functions=[partial_count, partial_sum])
# MAGIC       +- *(1) FileScan parquet [city, transaction_id, amount]
# MAGIC ```
# MAGIC
# MAGIC > `*(1)` and `*(2)` are two separate **WholeStageCodegen** stages separated by the `Exchange`.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Two-Phase Aggregation (Partial → Final)
# MAGIC
# MAGIC For `groupBy` + aggregation, Spark performs a **two-phase aggregation** to minimize shuffle data:
# MAGIC
# MAGIC ```
# MAGIC Phase 1 — Partial Aggregation (before shuffle):   Each executor pre-aggregates its local data
# MAGIC
# MAGIC   Partition 1: [boston×3, nyc×2]   ──┐
# MAGIC   Partition 2: [boston×5, nyc×1]   ──┼──► Exchange (shuffle by city key)
# MAGIC   Partition 3: [boston×2, nyc×4]   ──┘
# MAGIC
# MAGIC Phase 2 — Final Aggregation (after shuffle):      Combine partial results
# MAGIC
# MAGIC   boston total: 3 + 5 + 2 = 10
# MAGIC   nyc total:    2 + 1 + 4 = 7
# MAGIC ```
# MAGIC
# MAGIC **`Partial Aggregation (before shuffle)` significantly reduces the amount of data transferred over the network.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Controlling Shuffle Behavior
# MAGIC
# MAGIC ```python
# MAGIC # Default: 200 shuffle partitions (often too many for small data)
# MAGIC spark.conf.set("spark.sql.shuffle.partitions", "50")
# MAGIC
# MAGIC # Enable Adaptive Query Execution (AQE) — auto-tunes partition count at runtime
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC
# MAGIC # Force broadcast join to avoid shuffle when one table is small
# MAGIC from pyspark.sql.functions import broadcast
# MAGIC df_result = large_df.join(broadcast(small_df), "cust_id")
# MAGIC
# MAGIC # Increase broadcast threshold (default: 10 MB)
# MAGIC spark.conf.set("spark.sql.autoBroadcastJoinThreshold", str(50 * 1024 * 1024))  # 50 MB
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Join Types — Wide vs Narrow
# MAGIC
# MAGIC | Join Strategy | Shuffle? | When Used |
# MAGIC |---|---|---|
# MAGIC | `BroadcastHashJoin` | **No** (narrow) | Small table broadcast |
# MAGIC | `SortMergeJoin` | **Yes** (wide) | Both tables large |
# MAGIC | `ShuffledHashJoin` | **Yes** (wide) | Medium-sized tables |
# MAGIC | `BroadcastNestedLoopJoin` | **No shuffle but slow** | Non-equi joins |
# MAGIC | `CartesianProduct` | **No shuffle but O(n×m)** | Cross join |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Narrow vs Wide — Side-by-Side Comparison
# MAGIC
# MAGIC | Property | Narrow | Wide |
# MAGIC |---|---|---|
# MAGIC | **Data movement** | None | Across network (shuffle) |
# MAGIC | **Stage boundary** | No | Yes — always |
# MAGIC | **Disk I/O** | No | Yes (shuffle write/read) |
# MAGIC | **Speed** | Fast | Slower |
# MAGIC | **Examples** | `filter`, `map`, `select` | `groupBy`, `join`, `distinct` |
# MAGIC | **Physical Plan marker** | No `Exchange` | `Exchange` present |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Summary
# MAGIC
# MAGIC > **Wide transformations are unavoidable** in real pipelines — but you can reduce their cost by:
# MAGIC > - Using **AQE** to auto-tune shuffle partition counts
# MAGIC > - Using **broadcast joins** to eliminate shuffles for small tables
# MAGIC > - **Minimizing shuffles** by applying narrow transformations (filter, select) early to reduce data volume before a shuffle
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC #### 1. Repartition(n)
# MAGIC
# MAGIC `repartition(n)` is a **wide transformation** in Spark that redistributes data across `n` partitions, triggering a shuffle. It is used to **increase or decrease the number of partitions** for a DataFrame or RDD, ensuring data is spread evenly. This operation moves data across the network, making it more expensive than narrow transformations.

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For Repartition(n)
transactions_df.repartition(24).explain(True)

# COMMAND ----------

# DBTITLE 1,Retrieve Number of Partitions from Transactions Dataframe
transactions_df.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC AdaptiveSparkPlan isFinalPlan=false
# MAGIC +- == Initial Plan ==
# MAGIC    Exchange RoundRobinPartitioning(24), REPARTITION_BY_NUM, [plan_id=316]
# MAGIC    +- FileScan parquet [cust_id#6,start_date#7,end_date#8,txn_id#9,date#10,year#11,month#12,day#13,expense_type#14,amt#15,city#16] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<cust_id:string,start_date:string,end_date:string,txn_id:string,date:string,year:string,mon...
# MAGIC ```
# MAGIC ---
# MAGIC
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads the source data from the Parquet file.
# MAGIC - `Exchange RoundRobinPartitioning(24), REPARTITION_BY_NUM`: This is the key operator for `repartition(24)`. It triggers a **shuffle** to redistribute all rows evenly across 24 output partitions using a round-robin strategy. In round-robin partitioning, Spark assigns rows to partitions in a cyclic manner (row 1 to partition 1, row 2 to partition 2, ..., row 25 to partition 1 again), ensuring balanced distribution without regard to row content. This is a **wide transformation**—data moves across the network and disk.
# MAGIC - `AdaptiveSparkPlan`: Indicates Spark may further optimize the plan at runtime (if AQE is enabled).
# MAGIC
# MAGIC > **The presence of the `Exchange` operator confirms that `repartition(n)` causes a shuffle, making it more expensive than narrow transformations. Use it when you need to control partition count for downstream operations.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Visual: How `repartition(24)` works**
# MAGIC
# MAGIC Before repartition (random, uneven partitions):
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC Partition 1: [row1, row2, row3, ...]
# MAGIC Partition 2: [row4, row5, ...]
# MAGIC Partition 3: [row6, row7, ...]
# MAGIC ...
# MAGIC Partition N: [rowX, rowY, ...]
# MAGIC ```
# MAGIC ---
# MAGIC After repartition(24) (even/balanced rows distributed through round-robin):
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC Partition 1: [row1, row25, row49, ...]
# MAGIC Partition 2: [row2, row26, row50, ...]
# MAGIC Partition 3: [row3, row27, row51, ...]
# MAGIC ...
# MAGIC Partition 24: [row24, row48, row72, ...]
# MAGIC ```
# MAGIC ---
# MAGIC - All rows are shuffled and assigned to partitions in a cyclic (round-robin) manner.
# MAGIC - Ensures **balanced partition sizes** for downstream processing.
# MAGIC - **Shuffle boundary**: Data moves across the cluster, incurring network and disk I/O.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Coalesce(n)
# MAGIC %md
# MAGIC #### 2. Coalesce(n)
# MAGIC
# MAGIC `coalesce(n)` is a transformation in Spark that **reduces the number of partitions** in a DataFrame or RDD **without triggering a full shuffle** by default. It simply merges existing partitions together, moving data only if necessary, and avoids expensive network and disk I/O.
# MAGIC
# MAGIC - **How is it better than `repartition(n)`?**
# MAGIC   - `coalesce(n)` is **much faster** and more efficient because it does **not shuffle** all data across the cluster (unless explicitly requested).
# MAGIC   - It is ideal for **decreasing** partition count (e.g., from 200 to 20) after a wide transformation, before writing output.
# MAGIC   - Use `coalesce(n)` when you want to minimize shuffle and only reduce partitions.
# MAGIC
# MAGIC - **Does `coalesce(n)` ever shuffle?**
# MAGIC   - `coalesce(n)` never writes **shuffle files**, creates no `Exchange` operator in the plan, and creates **no stage boundary**. In the strict Spark sense — it does not shuffle.
# MAGIC   - **However, it can still involve real network I/O** depending on where the data lives:
# MAGIC
# MAGIC | Scenario | What happens | Network movement? |
# MAGIC |---|---|---|
# MAGIC | Storage-backed DF (Parquet/Delta on ADLS, S3) | Coalesced task reads more files directly from storage | None between executors |
# MAGIC | In-memory DF (e.g. after a groupBy, join, repartition) | Coalesced task must fetch data from other executors' memory | Yes — severe for extreme reductions like 200→1 |
# MAGIC
# MAGIC   - For **extreme reduction** (e.g. `coalesce(1)` on a 200-partition in-memory DF), that single task fetches data from potentially all 200 source partitions across executors — significant network I/O even though Spark does not write shuffle files for it.
# MAGIC   - The distinction from a real shuffle: a shuffle writes intermediate files to disk with a separate map/reduce phase and creates a **stage boundary**. `coalesce` moves data inline during task execution — no shuffle files, no stage boundary — but the network cost is still real for in-memory data with aggressive reduction.
# MAGIC   - With explicit `shuffle=True` (RDD API only), it behaves exactly like `repartition(n)` with a full shuffle.
# MAGIC
# MAGIC - **When to use `repartition(n)` instead?**
# MAGIC   - `repartition(n)` triggers a **full shuffle** to evenly distribute data across partitions, necessary when you need balanced partitions or are **increasing** partition count.
# MAGIC
# MAGIC **Summary Table:**
# MAGIC
# MAGIC | Operation | Shuffle files? | Stage boundary? | Network I/O? | Balanced output? |
# MAGIC |---|---|---|---|---|
# MAGIC | `coalesce(n)` on storage-backed DF | No | No | No | No (skewed possible) |
# MAGIC | `coalesce(n)` on in-memory DF (extreme reduction) | No | No | Yes (inline fetch) | No (skewed possible) |
# MAGIC | `coalesce(n, shuffle=True)` (RDD only) | Yes | Yes | Yes | Yes |
# MAGIC | `repartition(n)` | Yes | Yes | Yes | Yes |
# MAGIC
# MAGIC > **Precise rule: `coalesce(n)` avoids shuffle files and stage boundaries always. But for in-memory DataFrames with extreme partition reduction, tasks still fetch data across the network — it just happens inline, not via shuffle files. For storage-backed DataFrames (like Parquet on ADLS) it is always cheap. Use `repartition(n)` when you need balanced output or are increasing partitions.**
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Explain Physical Plan for Coalesced Transactions Datafr ...
transactions_df.coalesce(1).explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC Coalesce 1
# MAGIC +- *(1) ColumnarToRow
# MAGIC    +- FileScan parquet [cust_id#6,start_date#7,end_date#8,txn_id#9,date#10,year#11,month#12,day#13,expense_type#14,amt#15,city#16] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<cust_id:string,start_date:string,end_date:string,txn_id:string,date:string,year:string,mon...
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads the source data from the Parquet file. Only the required columns are loaded.
# MAGIC - `ColumnarToRow`: Converts columnar batches to row format for downstream processing.
# MAGIC - `Coalesce 1`: Merges all existing partitions into a single output partition **without triggering a shuffle**. This is efficient for reducing partition count, especially after wide transformations, and avoids expensive network and disk I/O.
# MAGIC - No `Exchange` operator is present, confirming that `coalesce(1)` does not shuffle data by default.
# MAGIC
# MAGIC > **Use `coalesce(n)` to efficiently reduce partition count when writing output or after shuffles, **but note that it may result in uneven partition sizes**.**
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Joins as Wide Transformations
# MAGIC %md
# MAGIC #### 3. Joins
# MAGIC
# MAGIC `join()` is one of the most common **wide transformations** in Spark. When two DataFrames are joined on a key, Spark must ensure that all rows with the **same key value** from both DataFrames land on the **same partition** — which almost always requires a shuffle.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Why Joins Are Wide
# MAGIC
# MAGIC Consider joining `transactions_df` and `customers_df` on `cust_id`. Before the join, rows with `cust_id = C001` may exist in different partitions on different executors across both DataFrames. Spark must shuffle data so matching keys are co-located:
# MAGIC
# MAGIC ```
# MAGIC Before Join (keys scattered):               After Shuffle (keys co-located):
# MAGIC
# MAGIC transactions:                                   Partition A: [C001 txns + C001 customer]
# MAGIC executor 1    [C001, C002, C003, ...]  ──►      Partition B: [C002 txns + C002 customer]
# MAGIC executor 2    [C004, C005, C006, ...]           Partition C: [C003 txns + C003 customer]
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Join Strategies in Spark
# MAGIC
# MAGIC Spark chooses a join strategy automatically based on table sizes and configurations:
# MAGIC
# MAGIC | Join Strategy | Shuffle? | When Used | Physical Plan Marker |
# MAGIC |---|---|---|---|
# MAGIC | `SortMergeJoin` (SMJ) | **Yes** — both sides | Both tables large | `SortMergeJoin`, `Exchange` |
# MAGIC | `ShuffledHashJoin` (SHJ) | **Yes** — both sides | Medium tables, one fits in memory as hash map | `ShuffledHashJoin`, `Exchange` |
# MAGIC | `BroadcastHashJoin` (BHJ) | **No** | One table small enough to broadcast | `BroadcastHashJoin`, `BroadcastExchange` |
# MAGIC | `BroadcastNestedLoopJoin` | **No shuffle, but O(n×m)** | Non-equi joins with a small table | `BroadcastNestedLoopJoin` |
# MAGIC | `CartesianProduct` | **No shuffle, but O(n×m)** | Cross joins | `CartesianProduct` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### SortMergeJoin — The Default Wide Join
# MAGIC
# MAGIC For large tables, Spark defaults to **SortMergeJoin**. It has two phases:
# MAGIC
# MAGIC ```
# MAGIC Phase 1 — Shuffle:   Both DFs are shuffled by the join key so matching keys land on the same partition
# MAGIC Phase 2 — Sort+Merge: Each partition is sorted by key, then merged like a zipper
# MAGIC ```
# MAGIC
# MAGIC Physical plan signature:
# MAGIC ```
# MAGIC *(5) SortMergeJoin [cust_id], [cust_id], Inner
# MAGIC :- *(2) Sort [cust_id ASC]                         ← sort left side
# MAGIC :  +- Exchange hashpartitioning(cust_id, 200)      ← shuffle left side
# MAGIC :     +- *(1) FileScan parquet (transactions)
# MAGIC +- *(4) Sort [cust_id ASC]                         ← sort right side
# MAGIC    +- Exchange hashpartitioning(cust_id, 200)      ← shuffle right side
# MAGIC       +- *(3) FileScan parquet (customers)
# MAGIC ```
# MAGIC
# MAGIC > Two `Exchange` operators — one per side — confirm this is a wide transformation creating a stage boundary.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### BroadcastHashJoin — The Narrow Exception
# MAGIC
# MAGIC If one DataFrame is small enough (default threshold: **10 MB**), Spark broadcasts it to every executor — eliminating the shuffle entirely:
# MAGIC
# MAGIC ```
# MAGIC Small DF (customers) ──► broadcast to ALL executors
# MAGIC
# MAGIC Each executor:  local_transactions JOIN broadcasted_customers  (no network shuffle!)
# MAGIC ```
# MAGIC
# MAGIC Physical plan signature:
# MAGIC ```
# MAGIC *(2) BroadcastHashJoin [cust_id], [cust_id], Inner, BuildRight
# MAGIC :- *(2) FileScan parquet (transactions)            ← large side, no shuffle
# MAGIC +- BroadcastExchange HashedRelationBroadcastMode   ← broadcast the small side
# MAGIC    +- *(1) FileScan parquet (customers)
# MAGIC ```
# MAGIC
# MAGIC > `BroadcastExchange` is NOT a shuffle — it replicates data to all nodes instead of redistributing by key.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Controlling Join Behavior
# MAGIC
# MAGIC ```python
# MAGIC from pyspark.sql.functions import broadcast
# MAGIC
# MAGIC # Force a broadcast join
# MAGIC df_result = transactions_df.join(broadcast(customers_df), "cust_id")
# MAGIC
# MAGIC # Increase broadcast threshold (default: 10 MB)
# MAGIC spark.conf.set("spark.sql.autoBroadcastJoinThreshold", str(50 * 1024 * 1024))  # 50 MB
# MAGIC
# MAGIC # Disable broadcast entirely (force SortMergeJoin)
# MAGIC spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")
# MAGIC
# MAGIC # Let AQE switch join strategy at runtime based on actual data sizes
# MAGIC spark.conf.set("spark.sql.adaptive.enabled", "true")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Summary
# MAGIC
# MAGIC - **SortMergeJoin** and **ShuffledHashJoin** are wide — both sides shuffle, two stage boundaries, expensive.
# MAGIC - **BroadcastHashJoin** is narrow — small side is replicated, no shuffle, very fast.
# MAGIC - AQE can dynamically switch from SortMergeJoin → BroadcastHashJoin at runtime if it detects one side is small after filtering.
# MAGIC - Always filter (`where`/`filter`) and select only needed columns **before** a join to reduce the data volume that gets shuffled.
# MAGIC
# MAGIC ---

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For Join (SortMergeJoin)
# --- SortMergeJoin (default for large tables) ---
# Disabling broadcast to force SortMergeJoin regardless of table size
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "-1")

df_smj = transactions_df.join(customers_df, "cust_id", "inner")
print("=== SortMergeJoin (broadcast disabled) ===")
df_smj.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC **SortMergeJoin Plan (broadcast disabled):**
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC AdaptiveSparkPlan isFinalPlan=false
# MAGIC +- == Initial Plan ==
# MAGIC    Project [cust_id#6, start_date#7, end_date#8, txn_id#9, date#10, year#11, month#12, day#13, expense_type#14, amt#15, city#16, name#55, age#56, gender#57, birthday#58, zip#59, city#60]
# MAGIC    +- SortMergeJoin [cust_id#6], [cust_id#54], Inner
# MAGIC       :- Sort [cust_id#6 ASC NULLS FIRST], false, 0
# MAGIC       :  +- Exchange hashpartitioning(cust_id#6, 200), ENSURE_REQUIREMENTS, [plan_id=365]
# MAGIC       :     +- Filter isnotnull(cust_id#6)
# MAGIC       :        +- FileScan parquet [cust_id#6,start_date#7,end_date#8,txn_id#9,date#10,year#11,month#12,day#13,expense_type#14,amt#15,city#16] Batched: true, DataFilters: [isnotnull(cust_id#6)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [IsNotNull(cust_id)], ReadSchema: struct<cust_id:string,start_date:string,end_date:string,txn_id:string,date:string,year:string,mon...
# MAGIC       +- Sort [cust_id#54 ASC NULLS FIRST], false, 0
# MAGIC          +- Exchange hashpartitioning(cust_id#54, 200), ENSURE_REQUIREMENTS, [plan_id=366]
# MAGIC             +- Filter isnotnull(cust_id#54)
# MAGIC                +- FileScan parquet [cust_id#54,name#55,age#56,gender#57,birthday#58,zip#59,city#60] Batched: true, DataFilters: [isnotnull(cust_id#54)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [IsNotNull(cust_id)], ReadSchema: struct<cust_id:string,name:string,age:string,gender:string,birthday:string,zip:string,city:string>
# MAGIC ```
# MAGIC ---
# MAGIC
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads the source data from the Parquet files for both DataFrames, loading only required columns.
# MAGIC - `Filter isnotnull(cust_id)`: Filters out rows with null `cust_id` values to ensure join correctness.
# MAGIC - `Exchange hashpartitioning(cust_id, 200)`: Both sides are shuffled by the join key (`cust_id`) into 200 partitions, so matching keys are co-located. This is the shuffle step and marks a stage boundary.
# MAGIC     - **About hashpartitioning:** Spark uses a hash function on the join key (`cust_id`) to assign each row to a partition. All rows with the same key value are guaranteed to land in the same partition, enabling correct join results. This ensures that matching keys from both DataFrames are co-located after the shuffle.
# MAGIC - `Sort [cust_id ASC NULLS FIRST]`: Each partition is sorted by `cust_id` to prepare for efficient merging.
# MAGIC - `SortMergeJoin [cust_id], [cust_id], Inner`: Performs the actual join by merging sorted partitions from both sides.
# MAGIC - `Project [...]`: Selects and outputs the required columns from the joined result.
# MAGIC - `AdaptiveSparkPlan`: Indicates Spark may optimize the plan further at runtime (if AQE is enabled).
# MAGIC
# MAGIC > **The presence of two `Exchange hashpartitioning` operators confirms this is a wide transformation (shuffle join). Both DataFrames are shuffled and sorted before the join, making it expensive but necessary for large tables.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Example (Visual):**
# MAGIC
# MAGIC Suppose you join transactions and customers on `cust_id`:
# MAGIC
# MAGIC **Before Shuffle:**
# MAGIC
# MAGIC | Partition | transactions(c_id) | customers(c_id) |
# MAGIC |-----------|--------------|----------|
# MAGIC | 1         | C001, C002   | C002     |
# MAGIC | 2         | C003, C001   | C001     |
# MAGIC | 3         | C004         | C003     |
# MAGIC
# MAGIC **After Shuffle (by cust_id):**
# MAGIC
# MAGIC | Partition | transactions(c_id) | customers(c_id) |
# MAGIC |-----------|--------------|----------|
# MAGIC | A         | C001         | C001     |
# MAGIC | B         | C002         | C002     |
# MAGIC | C         | C003         | C003     |
# MAGIC | D         | C004         |          |
# MAGIC
# MAGIC - All rows with the same `cust_id` are moved to the same partition.
# MAGIC - Now, each partition contains all transaction and customer rows for a given `cust_id`, so the join can happen correctly and efficiently.

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For Join (BroadcastHashJoin)
# --- BroadcastHashJoin (small table broadcast) ---
# Re-enabling broadcast and forcing it explicitly
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", str(50 * 1024 * 1024))

from pyspark.sql.functions import broadcast
df_bhj = transactions_df.join(broadcast(customers_df), "cust_id", "inner")
print("\n=== BroadcastHashJoin (broadcast forced) ===")
df_bhj.explain(True)

# COMMAND ----------

# DBTITLE 1,BroadcastHashJoin Physical Plan Explanation
# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC **BroadcastHashJoin Plan (broadcast enabled)**
# MAGIC
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC AdaptiveSparkPlan isFinalPlan=false
# MAGIC +- == Initial Plan ==
# MAGIC    Project [cust_id#6, start_date#7, end_date#8, txn_id#9, date#10, year#11, month#12, day#13, expense_type#14, amt#15, city#16, name#55, age#56, gender#57, birthday#58, zip#59, city#60]
# MAGIC    +- BroadcastHashJoin [cust_id#6], [cust_id#54], Inner, BuildRight, false, true
# MAGIC       :- Filter isnotnull(cust_id#6)
# MAGIC       :  +- FileScan parquet [cust_id#6,start_date#7,end_date#8,txn_id#9,date#10,year#11,month#12,day#13,expense_type#14,amt#15,city#16] Batched: true, DataFilters: [isnotnull(cust_id#6)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [IsNotNull(cust_id)], ReadSchema: struct<cust_id:string,start_date:string,end_date:string,txn_id:string,date:string,year:string,mon...
# MAGIC       +- Exchange SinglePartition, EXECUTOR_BROADCAST, [plan_id=467]
# MAGIC          +- Filter isnotnull(cust_id#54)
# MAGIC             +- FileScan parquet [cust_id#54,name#55,age#56,gender#57,birthday#58,zip#59,city#60] Batched: true, DataFilters: [isnotnull(cust_id#54)], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [IsNotNull(cust_id)], ReadSchema: struct<cust_id:string,name:string,age:string,gender:string,birthday:string,zip:string,city:string>
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads the source data from the Parquet files for both DataFrames, loading only required columns.
# MAGIC - `Filter isnotnull(cust_id)`: Filters out rows with null `cust_id` values to ensure join correctness.
# MAGIC - `Exchange SinglePartition, EXECUTOR_BROADCAST`: The smaller DataFrame (`customers_df`) is collected and broadcasted to all executors. This avoids a shuffle and allows each executor to join its local data with the broadcasted table.
# MAGIC - `BroadcastHashJoin [cust_id], [cust_id], Inner, BuildRight`: Spark performs a hash join, using the broadcasted table as the build side. No shuffle occurs; the join is fast and efficient.
# MAGIC - `Project [...]`: Selects and outputs the required columns from the joined result.
# MAGIC - `AdaptiveSparkPlan`: Indicates Spark may optimize the plan further at runtime (if AQE is enabled).
# MAGIC
# MAGIC > **The presence of `BroadcastHashJoin` and `Exchange SinglePartition, EXECUTOR_BROADCAST` confirms this is a broadcast join. This strategy is used when one table is small enough to be broadcasted, eliminating the need for expensive shuffles and making the join much faster.**

# COMMAND ----------

# MAGIC %md
# MAGIC #### 4. GroupBy
# MAGIC
# MAGIC A `groupBy` in Spark is a **wide transformation**. When you group rows by a column (e.g., `city`), Spark must ensure that all rows with the same group key are placed in the same partition. This requires a **shuffle**: data is moved across the cluster so matching keys are co-located, enabling correct aggregation.
# MAGIC
# MAGIC - **Physical plan marker:** Look for `Exchange hashpartitioning(key, n)` in the plan, which indicates a shuffle by the group key.
# MAGIC - **Why wide?** Rows with the same key may be scattered across partitions; Spark shuffles them so all matching keys are together for aggregation.
# MAGIC
# MAGIC > `groupBy` is wide because it triggers a shuffle to group data by key, making it more expensive than narrow transformations.

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For GroupBy With Count
df_city_counts = (
    transactions_df
    .groupBy("city")
    .count()
)

df_city_counts.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC AdaptiveSparkPlan isFinalPlan=false
# MAGIC +- == Initial Plan ==
# MAGIC    HashAggregate(keys=[city#16], functions=[finalmerge_count(merge count#131L) AS count(1)#129L], output=[city#16, count#117L])
# MAGIC    +- Exchange hashpartitioning(city#16, 200), ENSURE_REQUIREMENTS, [plan_id=535]
# MAGIC       +- HashAggregate(keys=[city#16], functions=[partial_count(1) AS count#131L], output=[city#16, count#131L])
# MAGIC          +- FileScan parquet [city#16] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<city:string>
# MAGIC ```
# MAGIC ---
# MAGIC
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads the source data from the Parquet file, loading only the `city` column needed for grouping.
# MAGIC - `HashAggregate(keys=[city], functions=[partial_count(1)])`: Performs partial aggregation (count) locally within each partition. **This minimizes the amount of data shuffled**.
# MAGIC - `Exchange hashpartitioning(city, 200)`: Shuffles data across the cluster so all rows with the same `city` value are co-located in the same partition. This is the wide transformation and marks a stage boundary.
# MAGIC - `HashAggregate(keys=[city], functions=[finalmerge_count])`: After the shuffle, Spark merges partial counts to produce the final count per city.
# MAGIC - `AdaptiveSparkPlan`: Indicates Spark may optimize the plan further at runtime (if AQE is enabled).
# MAGIC
# MAGIC > The presence of the `Exchange` operator confirms that `groupBy` triggers a shuffle, making it a wide transformation. Spark uses a two-phase aggregation (partial → shuffle → final) to reduce shuffle data and improve performance.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Example (Visual):**
# MAGIC
# MAGIC Suppose your data is:
# MAGIC
# MAGIC | Partition | Data(city)   |
# MAGIC |-----------|--------------|
# MAGIC | 1         | boston       |
# MAGIC | 1         | boston       |
# MAGIC | 1         | nyc          |
# MAGIC | 2         | nyc          |
# MAGIC | 2         | la           |
# MAGIC | 2         | boston       |
# MAGIC | 3         | la           |
# MAGIC | 3         | la           |
# MAGIC | 3         | boston       |
# MAGIC
# MAGIC **Step 1: Partial Count (before shuffle)**
# MAGIC
# MAGIC - Partition 1: boston=2, nyc=1
# MAGIC - Partition 2: nyc=1, la=1, boston=1
# MAGIC - Partition 3: la=2, boston=1
# MAGIC
# MAGIC **Step 2: Shuffle (Exchange)**
# MAGIC
# MAGIC All rows with the same city are moved to the same partition:
# MAGIC
# MAGIC - Partition A: boston: 2, 1, 1
# MAGIC - Partition B: nyc: 1, 1
# MAGIC - Partition C: la: 1, 2
# MAGIC
# MAGIC **Step 3: Final Count (after shuffle)**
# MAGIC
# MAGIC - boston: 2+1+1 = 4
# MAGIC - nyc: 1+1 = 2
# MAGIC - la: 1+2 = 3
# MAGIC
# MAGIC > This is how `groupBy("city").count()` works: partial counts, shuffle, then final aggregation.

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For GroupBy With Sum
df_txn_amt_city = (
    transactions_df
    .groupBy("city")
    .agg(F.sum("amt").alias("txn_amt"))
)

df_txn_amt_city.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC AdaptiveSparkPlan isFinalPlan=false
# MAGIC +- == Initial Plan ==
# MAGIC    HashAggregate(keys=[city#16], functions=[finalmerge_sum(merge sum#112) AS sum(amt)#110], output=[city#16, txn_amt#98])
# MAGIC    +- Exchange hashpartitioning(city#16, 200), ENSURE_REQUIREMENTS, [plan_id=247]
# MAGIC       +- HashAggregate(keys=[city#16], functions=[partial_sum(cast(amt#15 as double)) AS sum#112], output=[city#16, sum#112])
# MAGIC          +- FileScan parquet [amt#15,city#16] Batched: true, DataFilters: [], Format: Parquet, Location: InMemoryFileIndex(1 paths)[abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core...., PartitionFilters: [], PushedFilters: [], ReadSchema: struct<amt:string,city:string>
# MAGIC ```
# MAGIC ---
# MAGIC
# MAGIC **Explanation:**
# MAGIC
# MAGIC - `FileScan parquet [...]`: Reads the source data from the Parquet file, loading only the `amt` and `city` columns needed for grouping and aggregation.
# MAGIC - `HashAggregate(keys=[city], functions=[partial_sum])`: Performs partial aggregation (sum) locally within each partition. **This minimizes the amount of data shuffled**.
# MAGIC - `Exchange hashpartitioning(city, 200)`: Shuffles data across the cluster so all rows with the same `city` value are co-located in the same partition. This is the wide transformation and marks a stage boundary.
# MAGIC - `HashAggregate(keys=[city], functions=[finalmerge_sum])`: After the shuffle, Spark merges partial sums to produce the final sum per city.
# MAGIC - `AdaptiveSparkPlan`: Indicates Spark may optimize the plan further at runtime (if AQE is enabled).
# MAGIC
# MAGIC > The presence of the `Exchange` operator confirms that `groupBy` triggers a shuffle, making it a wide transformation. Spark uses a two-phase aggregation (partial → shuffle → final) to reduce shuffle data and improve performance.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Example (Visual):**
# MAGIC
# MAGIC Suppose your data is:
# MAGIC
# MAGIC | Partition | Data(city, amt)   |
# MAGIC |-----------|-------------------|
# MAGIC | 1         | boston, 10        |
# MAGIC | 1         | boston, 5         |
# MAGIC | 1         | la, 10            |
# MAGIC | 2         | nyc, 20           |
# MAGIC | 2         | la, 25            |
# MAGIC | 2         | boston, 20        |
# MAGIC | 3         | la, 15            |
# MAGIC | 3         | nyc, 30           |
# MAGIC | 3         | nyc, 15           |
# MAGIC
# MAGIC **Step 1: Partial Sum (before shuffle)**
# MAGIC
# MAGIC - Partition 1: boston=10+5=15, la=10
# MAGIC - Partition 2: nyc=20, la=25, boston=20
# MAGIC - Partition 3: la=15, nyc=30+15=45
# MAGIC
# MAGIC **Step 2: Shuffle (Exchange)**
# MAGIC
# MAGIC All rows with the same city are moved to the same partition:
# MAGIC
# MAGIC - Partition A: boston: 15, 20
# MAGIC - Partition B: nyc: 20, 45
# MAGIC - Partition C: la: 10, 25, 15
# MAGIC
# MAGIC **Step 3: Final Sum (after shuffle)**
# MAGIC
# MAGIC - boston: 15+20 = 35
# MAGIC - nyc: 20+45 = 65
# MAGIC - la: 10+25+15 = 50
# MAGIC
# MAGIC > This is how `groupBy("city").agg(sum("amt"))` works: partial sums, shuffle, then final aggregation.

# COMMAND ----------

# DBTITLE 1,GroupBy Count Distinct
# MAGIC %md
# MAGIC #### 5. GroupBy Count Distinct
# MAGIC
# MAGIC `groupBy().agg(countDistinct())` is a **wide transformation** — and it is significantly **more expensive than a regular groupBy count** because it requires **two separate shuffles** instead of one.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Why Count Distinct Needs Two Shuffles
# MAGIC
# MAGIC For a regular `count()`, Spark only needs to ensure rows with the same group key are co-located once. For `countDistinct()`, Spark must additionally **deduplicate** the distinct column globally before counting — and deduplication itself requires a separate shuffle.
# MAGIC
# MAGIC ```
# MAGIC groupBy("city").count()           → 1 shuffle  (by city)
# MAGIC groupBy("city").countDistinct()   → 2 shuffles (by city+cust_id, then by city)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### The Two-Shuffle Execution Plan
# MAGIC
# MAGIC ```
# MAGIC FileScan parquet [cust_id, city]
# MAGIC     ↓
# MAGIC HashAggregate(keys=[city, cust_id])     ← Step 1: LOCAL pre-dedup per partition
# MAGIC     ↓
# MAGIC Exchange hashpartitioning(city, cust_id, 200)   ← SHUFFLE 1: redistribute by (city + cust_id)
# MAGIC     ↓                                              to globally deduplicate
# MAGIC HashAggregate(keys=[city, cust_id])     ← Step 2: GLOBAL dedup — remove duplicate cust_ids
# MAGIC     ↓
# MAGIC Exchange hashpartitioning(city, 200)    ← SHUFFLE 2: redistribute by city alone
# MAGIC     ↓                                     to aggregate the final count
# MAGIC HashAggregate(keys=[city], count)       ← Step 3: FINAL count per city
# MAGIC ```
# MAGIC
# MAGIC **Shuffle 1** hashes on **(city, cust_id)** — all rows with the same `(city, cust_id)` pair land on the same partition so duplicates can be eliminated globally.
# MAGIC
# MAGIC **Shuffle 2** hashes on **(city)** alone — once duplicates are removed, rows are re-grouped by city to compute the final count.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Why This Is Expensive
# MAGIC
# MAGIC | | Regular `count()` | `countDistinct()` |
# MAGIC |---|---|---|
# MAGIC | Shuffles | 1 | **2** |
# MAGIC | Stage boundaries | 1 | **2** |
# MAGIC | Shuffle key | `(city)` | `(city, cust_id)` then `(city)` |
# MAGIC | Data volume shuffled | Low (partial counts) | High (full rows for dedup) |
# MAGIC
# MAGIC The first shuffle moves **full rows** keyed by `(city, cust_id)` — the cardinality is much higher than just `(city)`, so the shuffle is wider and heavier.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Optimization — Use `approx_count_distinct` When Exact Count Is Not Required
# MAGIC
# MAGIC ```python
# MAGIC import pyspark.sql.functions as F
# MAGIC
# MAGIC # Exact — 2 shuffles, expensive
# MAGIC df.groupBy("city").agg(F.countDistinct("cust_id"))
# MAGIC
# MAGIC # Approximate — 1 shuffle, uses HyperLogLog (default ~5% error)
# MAGIC df.groupBy("city").agg(F.approx_count_distinct("cust_id", rsd=0.05))
# MAGIC ```
# MAGIC
# MAGIC `approx_count_distinct` avoids the dedup shuffle entirely by using a **HyperLogLog sketch** that accumulates distinct value counts locally and merges them in one pass.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC > **Key takeaway:** `countDistinct` always triggers **two stage boundaries**. Prefer `approx_count_distinct` when approximate results are acceptable — it is significantly faster on large datasets.

# COMMAND ----------

# DBTITLE 1,Understand Query Plan For GroupBy Count Distinct
df_city_distinct_customers = (
    transactions_df
    .groupBy("city")
    .agg(F.countDistinct("cust_id").alias("unique_customers"))
)

df_city_distinct_customers.explain(True)

# COMMAND ----------

# DBTITLE 1,GroupBy Count Distinct Physical Plan Explanation
# MAGIC %md
# MAGIC    
# MAGIC **== Physical Plan == (This is the final plan which gets executed on the cluster)**
# MAGIC
# MAGIC ---
# MAGIC ```
# MAGIC == Physical Plan ==
# MAGIC AdaptiveSparkPlan isFinalPlan=false
# MAGIC +- == Initial Plan ==
# MAGIC    HashAggregate(keys=[city#16], functions=[finalmerge_count(distinct merge count#145L) AS count(distinct cust_id#6)#143L], output=[city#16, unique_customers#130L])
# MAGIC    +- Exchange hashpartitioning(city#16, 200), ENSURE_REQUIREMENTS, [plan_id=612]       ← SHUFFLE 2
# MAGIC       +- HashAggregate(keys=[city#16], functions=[partial_count(distinct city#16, cust_id#6) AS count#145L], output=[city#16, count#145L])
# MAGIC          +- HashAggregate(keys=[city#16, cust_id#6], functions=[], output=[city#16, cust_id#6])
# MAGIC             +- Exchange hashpartitioning(city#16, cust_id#6, 200), ENSURE_REQUIREMENTS, [plan_id=611]      ← SHUFFLE 1
# MAGIC                +- HashAggregate(keys=[city#16, cust_id#6], functions=[], output=[city#16, cust_id#6])
# MAGIC                   +- FileScan parquet [cust_id#6,city#16] Batched: true, DataFilters: [], Format: Parquet, ...
# MAGIC ```
# MAGIC ---
# MAGIC
# MAGIC **Explanation (bottom to top — how Spark executes):**
# MAGIC
# MAGIC - `FileScan parquet [cust_id, city]`: Reads only the two required columns from Parquet. Column pruning keeps I/O minimal.
# MAGIC - `HashAggregate(keys=[city, cust_id])` *(first one)*: **Local pre-dedup** — removes duplicate `(city, cust_id)` pairs within each partition before any data moves. Reduces shuffle volume significantly.
# MAGIC - `Exchange hashpartitioning(city, cust_id, 200)` — **SHUFFLE 1**: Redistributes rows by the composite key `(city, cust_id)`. All rows with the same `(city, cust_id)` pair land on the same partition so global duplicates can be eliminated. This is the expensive shuffle — the key has much higher cardinality than `city` alone.
# MAGIC - `HashAggregate(keys=[city, cust_id])` *(second one)*: **Global dedup** — after the shuffle, each `(city, cust_id)` pair is now fully unique within its partition. This step makes them distinct.
# MAGIC - `HashAggregate(keys=[city], partial_count)`: Collapses deduplicated rows into a partial count per city within each partition.
# MAGIC - `Exchange hashpartitioning(city, 200)` — **SHUFFLE 2**: Re-shuffles by `city` alone to co-locate all partial counts for the same city.
# MAGIC - `HashAggregate(keys=[city], finalmerge_count)`: Merges partial counts to produce the final `unique_customers` value per city.
# MAGIC - `AdaptiveSparkPlan`: AQE may rewrite the plan at runtime (e.g. coalesce shuffle partitions, change join strategy).
# MAGIC
# MAGIC > Two `Exchange` operators = two stage boundaries = two shuffles. Compare to `groupBy("city").count()` which has only one `Exchange`.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Example (Visual):**
# MAGIC
# MAGIC Suppose your data is:
# MAGIC
# MAGIC | Partition | city, cust_id |
# MAGIC |-----------|---------------|
# MAGIC | 1         | boston, C001  |
# MAGIC | 1         | boston, C001  |
# MAGIC | 1         | boston, C002  |
# MAGIC | 2         | nyc, C001     |
# MAGIC | 2         | boston, C002  |
# MAGIC | 3         | nyc, C003     |
# MAGIC | 3         | boston, C001  |
# MAGIC
# MAGIC **Step 1: Local pre-dedup (before Shuffle 1)**
# MAGIC
# MAGIC Remove duplicate `(city, cust_id)` pairs within each partition:
# MAGIC - Partition 1: (boston, C001), (boston, C002)   ← duplicate C001 dropped
# MAGIC - Partition 2: (nyc, C001), (boston, C002)
# MAGIC - Partition 3: (nyc, C003), (boston, C001)
# MAGIC
# MAGIC **Step 2: Shuffle 1 — hashpartitioning(city, cust_id, 200)**
# MAGIC
# MAGIC All rows with the same `(city, cust_id)` move to the same partition:
# MAGIC - Partition A: (boston, C001) ×2   ← from partitions 1 and 3
# MAGIC - Partition B: (boston, C002) ×2   ← from partitions 1 and 2
# MAGIC - Partition C: (nyc, C001) ×1
# MAGIC - Partition D: (nyc, C003) ×1
# MAGIC
# MAGIC **Step 3: Global dedup (after Shuffle 1)**
# MAGIC
# MAGIC Each `(city, cust_id)` pair is now fully unique per partition:
# MAGIC - Partition A: (boston, C001)
# MAGIC - Partition B: (boston, C002)
# MAGIC - Partition C: (nyc, C001)
# MAGIC - Partition D: (nyc, C003)
# MAGIC
# MAGIC **Step 4: Shuffle 2 — hashpartitioning(city, 200)**
# MAGIC
# MAGIC Re-group by city:
# MAGIC - Partition X: boston → [C001, C002]   ← from A and B
# MAGIC - Partition Y: nyc   → [C001, C003]   ← from C and D
# MAGIC
# MAGIC **Step 5: Final count**
# MAGIC
# MAGIC - boston: 2 unique customers
# MAGIC - nyc: 2 unique customers
# MAGIC
# MAGIC > This is how `groupBy("city").agg(countDistinct("cust_id"))` works: local dedup → shuffle by (city+cust_id) → global dedup → shuffle by (city) → final count. Two shuffles, two stage boundaries.
