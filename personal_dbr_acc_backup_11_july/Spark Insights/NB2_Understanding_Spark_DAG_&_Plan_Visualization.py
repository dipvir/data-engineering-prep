# Databricks notebook source
# DBTITLE 1,Imports
from pyspark.sql.types import *
import pyspark.sql.functions as F

# COMMAND ----------

# MAGIC %md
# MAGIC ## Topics
# MAGIC
# MAGIC 1. Reading Files (parquet)
# MAGIC 2. Narrow Operations
# MAGIC    - `filter`
# MAGIC    - `withColumn`: adding/modifying a column
# MAGIC    - `select`: selecting relevant column
# MAGIC 3. Wide Operations
# MAGIC    - Joins
# MAGIC      - Sort Merge Join
# MAGIC      - Broadcast Join
# MAGIC    - GroupBy
# MAGIC      - `count`
# MAGIC      - `sum`
# MAGIC      - `countDistinct`

# COMMAND ----------

# MAGIC %md
# MAGIC ## Understanding Spark DAG And Plan Visualization For Reading A File(Loading And Displaying Data)

# COMMAND ----------

# MAGIC %md
# MAGIC **DAG vs Plan Visualization in Spark**
# MAGIC
# MAGIC **Q: Are DAG (Directed Acyclic Graph) and Plan Visualization the same in Spark?**  
# MAGIC **A:** No, they are related but not exactly the same.  
# MAGIC - **DAG** represents the sequence of transformations and actions as a graph of stages and tasks.
# MAGIC - **Plan Visualization** (e.g., `DataFrame.explain()`, Spark UI) shows the logical and physical execution plan for a query.
# MAGIC
# MAGIC **Q: What does the DAG show?**  
# MAGIC **A:** The DAG illustrates job, stage, and task dependencies in Spark.
# MAGIC
# MAGIC **Q: What does Plan Visualization show?**  
# MAGIC **A:** Plan Visualization details the logical and physical steps Spark will use to execute a query.
# MAGIC
# MAGIC **Q: How do both help?**  
# MAGIC **A:** Both help understand Spark's execution, but DAG is about dependencies, while Plan Visualization is about query execution steps.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Example: How to view plan visualization for a DataFrame?**
# MAGIC
# MAGIC python
# MAGIC transactions_df.explain(True)

# COMMAND ----------

# MAGIC %md
# MAGIC **When Job is Created By Spark**
# MAGIC
# MAGIC In Spark, a Directed Acyclic Graph (DAG) represents the sequence of computations (transformations and actions) on data. A job is created **when an action** (like `count`, `collect`, `show`, or `display`) is called on a DataFrame or RDD. Until an action is triggered, Spark only builds the DAG of transformations. Once an action is invoked, Spark submits the job to the cluster, breaking it into stages and tasks for execution.

# COMMAND ----------

# DBTITLE 1,Load and Preview Sample Transactions Data
transactions_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/transactions.parquet/")
display(transactions_df.limit(5))

# COMMAND ----------

# DBTITLE 1,Checking Number of Partitions
# Checking number of partitions in transactions_df
transactions_df.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI Shows That Above Two LOC Created 2 Jobs**
# MAGIC
# MAGIC ![image_1782822027110.png](NB2_images/image_1782822027110.png "image_1782822027110.png")
# MAGIC
# MAGIC - Both jobs contains 1,1 stage because there is **no shuffle involved here**.
# MAGIC
# MAGIC - As seen below in stage 1(belongs to job 1) input = 8.0 MiB, its for action `display` so it reads/loads the data and in the stage 0(belongs to job 0) input is empty because it just fetches metadata about file. 
# MAGIC ![image_1782822314283.png](NB2_images/image_1782822314283.png "image_1782822314283.png")

# COMMAND ----------

# MAGIC %md
# MAGIC **Why are there 2 jobs when only 1 action appears in the code?**
# MAGIC
# MAGIC ```python
# MAGIC transactions_df = spark.read.parquet("...")   # Line 1
# MAGIC display(transactions_df.limit(5))              # Line 2
# MAGIC ```
# MAGIC
# MAGIC | Job | Triggered By | What it does |
# MAGIC |-----|-------------|--------------|
# MAGIC | Job 1 | `spark.read.parquet()` | Spark reads the **parquet file footers/metadata** from the directory to infer the schema. Even though `read` is lazy, Spark internally submits a job to scan file metadata. |
# MAGIC | Job 2 | `display(...)` | The actual action — reads and collects the data rows (8.0 MiB) to render in the notebook output. |
# MAGIC
# MAGIC **Key Insight**: `spark.read.parquet()` on a **directory** triggers a background metadata job for schema inference, even before any explicit action is called. This is why you see 2 jobs from just 2 lines of code.

# COMMAND ----------

# MAGIC %md
# MAGIC **Plan Visualization Of Cell 5 Line 2**
# MAGIC
# MAGIC
# MAGIC ![image_1782826940306.png](NB2_images/image_1782826940306.png "image_1782826940306.png") ![image_1782827318387.png](NB2_images/image_1782827318387.png "image_1782827318387.png")
# MAGIC
# MAGIC **If we expand the `+`, lots of information is present:-**
# MAGIC
# MAGIC **Example:-**
# MAGIC - number of files read = 163 (i.e. because count of parquet file present in adls path is 163)
# MAGIC - input read data size = 8.0 MiB
# MAGIC - size of files read = 862.7 MiB
# MAGIC - **And Many More.**
# MAGIC
# MAGIC **Batches In Spark**<br>
# MAGIC **What does `number of input batches = 1` and `rows output = 4,096` mean in Spark plan visualization?**
# MAGIC
# MAGIC - **number of input batches = 1**: Spark processes the data in a single batch for this operation, since the `limit(5)` action is simple and does not require multiple batches.
# MAGIC - **rows output = 4,096**: Spark reads up to 4,096 rows from the source before applying the `limit(5)`. This is an internal optimization—Spark may read more rows than requested to efficiently fulfill the `limit` operation, but only 5 rows are actually returned to the user.

# COMMAND ----------

# DBTITLE 1,Load and Preview Sample Customers Data
customers_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/customers.parquet/")
display(customers_df.limit(5))

# COMMAND ----------

# DBTITLE 1,Checking Number of Partitions
customers_df.rdd.getNumPartitions()

# COMMAND ----------

# MAGIC %md
# MAGIC **Note:** The similar process occurs for the customers data above.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Understanding Spark DAG And Plan Visualization For Narrow Transformations
# MAGIC **Narrow Transformations**
# MAGIC - `filter` rows where `city='boston'`
# MAGIC - `add` a new column: adding `first_name` and `last_name`
# MAGIC - `alter` an exisitng column: adding 5 to `age` column
# MAGIC - `select` relevant columns

# COMMAND ----------

# DBTITLE 1,Understanding Narrow Transformations DAG/Plan Visualization
df_narrow_transform = (
    customers_df
    .filter(F.col("city") == "boston")
    .withColumn("first_name", F.split("name", " ").getItem(0))
    .withColumn("last_name", F.split("name", " ").getItem(1))
    .withColumn("age", F.col("age") + F.lit(5))
    .select("cust_id", "first_name", "last_name", "age", "gender", "birthday")
) # Lazy operation so no job created

# Using 'noop'(no operation) format here as a placeholder; 'noop' does not actually write any data, but can be used for testing write logic or plan visualization without output.
df_narrow_transform.write.format("noop").mode("overwrite").save("../data/test/df_narrow_transform.parquet") # write is an action so job is created

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI Shows That Above Cell Created 1 Job**
# MAGIC
# MAGIC Transformations are lazy and do not trigger a Spark job until an action is performed. The action in above cell is writing the transformed DataFrame using `.write.format("noop")`, which causes Spark to execute the DAG. Since all operations are narrow (no shuffle), the job consists of a single stage.
# MAGIC
# MAGIC ![image_1782837950546.png](NB2_images/image_1782837950546.png "image_1782837950546.png")
# MAGIC
# MAGIC - The job contains 1 stage because there is **no shuffle involved here**.
# MAGIC - As seen below in stage 4(belongs to job 4) input = ~150 KiB, its because of action `write`. so the data has to be read first to apply transformation and then write it to the location.
# MAGIC
# MAGIC ![image_1782837984008.png](NB2_images/image_1782837984008.png "image_1782837984008.png")

# COMMAND ----------

# DBTITLE 1,Count Total Customers in DataFrame
customers_df.count()

# COMMAND ----------

# MAGIC %md
# MAGIC **Plan Visualization For df_narrow_transform**
# MAGIC
# MAGIC ![image_1782838553659.png](NB2_images/image_1782838553659.png "image_1782838553659.png")![image_1782838972729.png](NB2_images/image_1782838972729.png "image_1782838972729.png")
# MAGIC
# MAGIC - As seen in image it loads all 5k records from file first and make 2 batches of it.
# MAGIC - Then convert columnar to row format for efficient downstream operation.
# MAGIC - Then applies filters and all other tranformations in project section.
# MAGIC - Finally simulate write operation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Understanding Spark DAG And Plan Visualization For Wide Transformations
# MAGIC **Wide Transformations**
# MAGIC 1. Joins
# MAGIC    - Sort Merge Join
# MAGIC    - Broadcast Join
# MAGIC 2. GroupBy
# MAGIC    - `count`
# MAGIC    - `countDistinct`
# MAGIC    - `sum`

# COMMAND ----------

# MAGIC %md
# MAGIC ### Joins

# COMMAND ----------

# MAGIC %md
# MAGIC #### Sort Merge Join With Auto Broadcast Join And AQE Disabled

# COMMAND ----------

# DBTITLE 1,Understanding Sort Merge Join DAG/Plan Visualization
# Disable broadcast join by setting threshold to -1
# This forces Spark to use sort merge join instead of broadcast join.
# As customer table is very small so ideally spark will broadcast it but to understand the dag we are disabling the setting.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)

# Also disabling AQE to prevent dynamic broadcast join
spark.conf.set("spark.sql.adaptive.enabled", "false")  

# Performing sort merge join between transactions and customers on 'cust_id'
df_joined = (
    transactions_df.join(
        customers_df,
        how="inner",
        on="cust_id"
    )
)

# Write the joined DataFrame using 'noop' format (simulates write, no actual output)
df_joined.write.format("noop").mode("overwrite").save("../data/test/df_joined.parquet")

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI Shows That Sort Merge Join Operation(Wide) Created Only 1 Job With Many Stages And Tasks**
# MAGIC
# MAGIC ![image_1782898256724.png](NB2_images/image_1782898256724.png "image_1782898256724.png")
# MAGIC
# MAGIC ---
# MAGIC ![image_1782898520239.png](NB2_images/image_1782898520239.png "image_1782898520239.png")
# MAGIC
# MAGIC - So as seen in images sort merge join created 1 job, 3 stages and 213 tasks.
# MAGIC - The 3 stages is created because of 2 shuffle operation. each df took 1 stage to read plus shuffle the data to disk and then 3rd stage performed joined.
# MAGIC - As **1 Task Works On 1 Partition**, So we see 1 task for customer as it has 1 partition and 12 tasks for transaction as it has 12 partitions (Above in 1st section i have printed the partitions for each).
# MAGIC - For the join stage, Spark creates 200 partitions by default, thats why there are 200 tasks in the join stage. We can also manually change it using `spark.conf.set("spark.sql.shuffle.partitions", 24)`.
# MAGIC
# MAGIC **Plan Visualization For df_joined**
# MAGIC
# MAGIC ![image_1782902604918.png](NB2_images/image_1782902604918.png "image_1782902604918.png")![image_1782916333611.png](NB2_images/image_1782916333611.png "image_1782916333611.png")![image_1782916391594.png](NB2_images/image_1782916391594.png "image_1782916391594.png")

# COMMAND ----------

# DBTITLE 1,To Manually Change Spark Shuffle Partitions Configuration
# spark.conf.set("spark.sql.shuffle.partitions", 200)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Sort Merge Join With Auto Broadcast Join And AQE's Only broadcast join optimization Disabled (Rest AQE Optimization Stays On)

# COMMAND ----------

# DBTITLE 1,Understanding Sort Merge Join DAG/Plan Visualization
# Disable broadcast join by setting threshold to -1.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)

# Enable AQE
spark.conf.set("spark.sql.adaptive.enabled", "true")  

# disabling only AQE's broadcast join optimization(AQE stays ON)
spark.conf.set("spark.sql.adaptive.autoBroadcastJoinThreshold", -1) 

# Performing sort merge join between transactions and customers on 'cust_id'
df_joined = (
    transactions_df.join(
        customers_df,
        how="inner",
        on="cust_id"
    )
)

# Write the joined DataFrame using 'noop' format (simulates write, no actual output)
df_joined.write.format("noop").mode("overwrite").save("../data/test/df_joined.parquet")

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI Shows That Sort Merge Join Operation(Wide) Created 3 Jobs**
# MAGIC
# MAGIC **Note :-**
# MAGIC - *With AQE enabled, Spark executes shuffle map stages in separate jobs, collects runtime statistics, and then re-optimizes the downstream join stage. The skipped stages/tasks shown in the final job are usually previously completed shuffle stages whose outputs are reused, or stages from the original pre-adaptive plan that AQE replaced.*
# MAGIC
# MAGIC ![image_1782917010923.png](NB2_images/image_1782917010923.png "image_1782917010923.png")
# MAGIC
# MAGIC ---
# MAGIC ![image_1782917194030.png](NB2_images/image_1782917194030.png "image_1782917194030.png")
# MAGIC
# MAGIC ---
# MAGIC ![image_1782917222401.png](NB2_images/image_1782917222401.png "image_1782917222401.png")
# MAGIC
# MAGIC - So first 2 jobs loads each dataframes plus shuffle the data to disk to read is back for join job/operation.
# MAGIC - Same as mentioned above **1 Task Works On 1 Partition**, So we see 1 task for customer as it has 1 partition and 12 tasks for transaction as it has 12 partitions (Above in 1st section i have printed the partitions for each).
# MAGIC - As AQE is enabled, In the 3rd job which is for sort merge join there is only 36 partitions instead 200 we saw in previous code with AQE disabled.
# MAGIC
# MAGIC **Plan Visualization For df_joined**
# MAGIC
# MAGIC <img src="NB2_images/image_1782917972334.png"  width="300"/>![image_1782918247210.png](NB2_images/image_1782918247210.png "image_1782918247210.png")
# MAGIC
# MAGIC - `AdaptiveSparkPlan` means AQE is enabled.
# MAGIC - As shown in the images initially partition were 200 but then AQE optimized it to 36 partitions to make data distribution more even.
# MAGIC - AQE coalesced the 200 partitions down to 24 groups (many original partitions merged together), then split the 1 skewed partition into 12 sub-partitions → 24 + 12 = 36
# MAGIC -  AQE also partitions customer data to 36, to ensures both sides partitions match as required by merge-sort to work correctly.
# MAGIC - The skew split is the critical win here — without it, the 1 skewed partition (164x larger than median) would become a straggler task, forcing all 199 other tasks to sit idle while that single task finishes. Splitting it into 12 sub-partitions parallelizes that bottleneck. The coalescing of 200 → 24 small groups reduces task scheduling overhead from near-empty partitions. Together, both optimizations improve load balancing and prevent any single task from becoming the bottleneck.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Broadcast Join
# MAGIC
# MAGIC **Conditions for Broadcast Join:**
# MAGIC - The smaller DataFrame must fit into each executor's memory.
# MAGIC - Its size must be less than the assigned threshold property: `spark.sql.autoBroadcastJoinThreshold` (default: 10 MB).

# COMMAND ----------

# DBTITLE 1,Understanding Broadcast Join DAG/Plan Visualization
# Enable broadcast join by setting threshold to 10 MB (10485760 bytes)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10485760)

# Perform broadcast join between transactions and customers on 'cust_id'
df_broadcast_joined = (
    transactions_df.join(
        F.broadcast(customers_df),  # Explicitly broadcast customers_df
        how="inner",
        on="cust_id"
    )
)

# Write the joined DataFrame using 'noop' format (simulates write, no actual output)
df_broadcast_joined.write.format("noop").mode("overwrite").save("../data/test/df_broadcast_joined.parquet")

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI Shows That Broadcast Join Operation(Wide) Created 2 Jobs**
# MAGIC
# MAGIC ![image_1782924696368.png](NB2_images/image_1782924696368.png "image_1782924696368.png")
# MAGIC
# MAGIC | Job | Duration | Stages | Tasks | What it does |
# MAGIC |-----|----------|--------|-------|--------------|
# MAGIC | Job 4 | 0.5 s | 1/1 | 1/1 | Reads `customers_df` (small side) and **builds the broadcast relation** in memory |
# MAGIC | Job 5 | 25 s | 1/1 (1 skipped) | 12/12 (1 skipped) | Scans `transactions_df` (large side), probes the broadcast table, writes output |
# MAGIC
# MAGIC - The **skipped stage/task in Job 5** is AQE reusing the already-completed broadcast build from Job 4 — no need to redo it.
# MAGIC - Unlike sort merge join which had a **200-task shuffle stage just for the join**, broadcast join has **no such stage at all**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ![image_1782924668971.png](NB2_images/image_1782924668971.png "image_1782924668971.png")
# MAGIC ![image_1782924639307.png](NB2_images/image_1782924639307.png "image_1782924639307.png")
# MAGIC
# MAGIC **Stage-Level Breakdown:**
# MAGIC
# MAGIC | Stage | Tasks | Input | Shuffle Read | Shuffle Write | What happened |
# MAGIC |-------|-------|-------|-------------|---------------|---------------|
# MAGIC | Stage 4 (Job 4) | 1/1 | 149.9 KiB | — | 289.8 KiB | Reads `customers_df` (5K rows, 1 partition), serializes it into broadcast format (289.8 KiB) |
# MAGIC | Stage 6 (Job 5) | 12/12 | 899.0 MiB | 289.8 KiB | — | Scans `transactions_df` (39.7M rows, 12 partitions), receives broadcast data (289.8 KiB) on each executor |
# MAGIC
# MAGIC - **Stage 4** is lightning fast (0.4 s) — it only reads the tiny customers table (149.9 KiB) and prepares the broadcast payload.
# MAGIC - **Stage 6** reads the full transactions data (899.0 MiB across 12 partitions). The `Shuffle Read = 289.8 KiB` here is the broadcast data being delivered to each executor — not a traditional shuffle, just Spark's way of accounting for broadcast transfer.
# MAGIC - **No join shuffle stage** — compare this to sort merge join where we had a dedicated 200-task stage just to hash-partition both sides before the join. Here that entire stage is gone.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Plan Visualization For df_broadcast_joined**
# MAGIC
# MAGIC <img src="NB2_images/image_1782925072951.png"  width="250"/>
# MAGIC
# MAGIC - **`AdaptiveSparkPlan (12)`** — AQE is enabled (we only disabled its broadcast-upgrade threshold, not AQE itself).</span>
# MAGIC - **Left branch** (`transactions_df` — probe side): `Scan parquet → ColumnarToRow → Filter → BroadcastHashJoin` — 39,790,092 rows flow through without any repartitioning.</span>
# MAGIC - **Right branch** (`customers_df` — build side): `Scan parquet → ColumnarToRow → Filter → Exchange (4)` — only 5,000 rows; the `Exchange` here is a **BroadcastExchange**, not a shuffle exchange. It serializes the small table and sends it to all executors.</span>
# MAGIC - **`BroadcastHashJoin (9)`** — the actual join operator. Spark probes the in-memory hash table (built from customers) for each row of transactions. No sort, no merge, no 200 partitions.</span>
# MAGIC - **`WholeStageCodegen (2)` duration = 1.6 min** — the main scan + join + project logic for all 39.7M transaction rows, fused into a single compiled code block for maximum CPU efficiency.</span>
# MAGIC - **`WholeStageCodegen (1)` duration = 212 ms** — the fast broadcast build side (just 5K customers rows).</span>
# MAGIC
# MAGIC **Key Takeaway — Broadcast vs Sort Merge Join:**
# MAGIC
# MAGIC | Metric         | Sort Merge Join (AQE OFF) | Sort Merge Join (AQE ON) | Broadcast Join |
# MAGIC |----------------|--------------------------|--------------------------|---------------|
# MAGIC | Jobs           | 1                        | 3 (1 stage each)                        | 2             |
# MAGIC | Stages         | 3 (2 shuffle + 1 join)   | 3 (2 shuffle + 1 join)   | 2 (1 build + 1 probe) |
# MAGIC | Max tasks      | 213 (200 for join stage) | 36 (AQE coalesced/skew split) | 13 (1 build + 12 probe) |
# MAGIC | Shuffle for join | Yes — both sides repartitioned | Yes — both sides repartitioned (but AQE optimizes partitions) | No — only broadcast transfer |
# MAGIC | Join operator  | SortMergeJoin            | SortMergeJoin (Adaptive) | BroadcastHashJoin |
# MAGIC
# MAGIC - **Sort Merge Join (AQE OFF):** 1 job, 3 stages, 200 join tasks (default shuffle partitions), both sides shuffled.
# MAGIC - **Sort Merge Join (AQE ON):** 3 jobs (due to AQE), 3 stages, AQE reduces join stage to 36 tasks by coalescing and splitting skewed partitions, both sides shuffled.
# MAGIC - **Broadcast Join:** 2 jobs (1 for broadcast build, 1 for probe), 2 stages, no shuffle for join, only broadcast transfer, 1 build + 12 probe tasks.
# MAGIC     - **Rule of thumb:** if one side fits under `spark.sql.autoBroadcastJoinThreshold` (default 10 MB), broadcast join will almost always be faster.

# COMMAND ----------

# MAGIC %md
# MAGIC ### GroupBy

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy With Count()

# COMMAND ----------

# DBTITLE 1,Understanding GroupBy DAG/Plan Visualization
# GroupBy with count(): computes number of transactions per city
df_city_counts = (
    transactions_df
    .groupBy("city")
    .count()
)

# Show top 5 city-level transaction counts
df_city_counts.show(5, False)

# COMMAND ----------

# DBTITLE 1,Display City Counts DataFrame Row Count Summary
df_city_counts.count()

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI Shows That GroupBy With count() Operation(Wide) Created 2 Jobs**
# MAGIC
# MAGIC ![image_1782987428056.png](NB2_images/image_1782987428056.png "image_1782987428056.png")
# MAGIC
# MAGIC | Job | Duration | Stages | Tasks | What it does |
# MAGIC |-----|----------|--------|-------|--------------|
# MAGIC | Job 6 | 4 s | 1/1 | 9/9 | Scans `transactions_df`, applies **map-side partial aggregation**, shuffles result to disk |
# MAGIC | Job 7 | 0.2 s | 1/1 (1 skipped) | 1/1 (9 skipped) | Reads shuffle data, applies **reduce-side final aggregation**, collects 5 rows for `show()` |
# MAGIC
# MAGIC > **Note on task count:** Job 6 shows **9 tasks** even though `transactions_df` has 12 partitions. The exact reason can vary — likely a combination of: Databricks estimating projected column size (~90 MiB for just `city`) rather than full file size (899 MiB) when planning scan tasks, small trailing parquet files being packed together by Spark's file-packing logic, or AQE-related scan adjustments on DBR 17.3. Regardless, all 39.7M rows were processed (confirmed by `ColumnarToRow: rows output = 39,790,092`) — only the task boundary changed, not the data.
# MAGIC
# MAGIC - AQE is ON, so Spark **splits the groupBy into 2 jobs**: first job completes the shuffle map stage (Stage 7), then AQE collects statistics and re-optimizes before launching the second job (Stage 9) for final aggregation.
# MAGIC - The **9 skipped tasks** in Job 7 = Stage 7's 9 tasks were already done in Job 6; AQE reuses their shuffle output directly.
# MAGIC - This 2-job split is the **same AQE pattern** we saw in sort merge join — AQE needs runtime statistics between shuffle stages.
# MAGIC
# MAGIC ---
# MAGIC ![image_1782987560149.png](NB2_images/image_1782987560149.png "image_1782987560149.png")
# MAGIC
# MAGIC **Stage-Level Breakdown:**
# MAGIC
# MAGIC | Stage | Tasks | Input | Shuffle Write | Shuffle Read | Duration | What happened |
# MAGIC |-------|-------|-------|--------------|-------------|----------|---------------|
# MAGIC | Stage 7 (Job 6) | 9/9 | 90.6 MiB | 6.3 KiB | — | 4 s | Scans `transactions_df` (only `city` column via column pruning), partial aggregation reduces 39.7M rows → 90 rows, shuffles 6.3 KiB |
# MAGIC | Stage 9 (Job 7) | 1/1 | — | — | 6.3 KiB | 0.1 s | Reads 6.3 KiB shuffle data, final aggregation, outputs 6 rows for `show()` |
# MAGIC
# MAGIC - **Column Pruning:** Input is only 90.6 MiB even though the full `transactions_df` is 899 MiB (12 columns). Spark reads **only the `city` column** from parquet since `count()` needs no other column — a free optimization by the query optimizer.
# MAGIC - **Map-side partial aggregation is the key win:** Each task pre-aggregates its partition locally (39.7M → 90 rows) before the shuffle. Only **6.3 KiB** crosses the network instead of 90 MiB — a ~14,500x shuffle reduction.
# MAGIC - **Stage 9 is instant (0.1s):** Only 1 task, 6.3 KiB of data, 90 rows to finalize. The heavy lifting was already done in Stage 7.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Plan Visualization For df_city_counts**
# MAGIC
# MAGIC ![image_1782987680478.png](NB2_images/image_1782987680478.png "image_1782987680478.png")![image_1782988103886.png](NB2_images/image_1782988103886.png "image_1782988103886.png")![image_1782988107643.png](NB2_images/image_1782988107643.png "image_1782988107643.png")
# MAGIC
# MAGIC **Bottom-up walkthrough of the plan:**
# MAGIC
# MAGIC - **`Scan parquet (1)` → `ColumnarToRow (2)`:** Reads 39,790,092 rows from parquet in **9,796 column batches** (columnar format for fast I/O), then converts to row format for the hash aggregator. Only the `city` column is scanned due to column pruning.
# MAGIC
# MAGIC - **`HashAggregate (3)` (map-side / partial):**  
# MAGIC   Performs a **local pre-aggregation per task** before the shuffle.  
# MAGIC   - rows output = **90** (down from 39,790,092 — one row per distinct city, per partition)  
# MAGIC   - peak memory total = 2.3 MiB, time in aggregation build = 11.9s (spread across 9 tasks)  
# MAGIC   - spill size = 0.0 B — no disk spill, everything fit in memory  
# MAGIC   All inside `WholeStageCodegen (1)` (duration: 13.1s, Stage 7) — scan + partial agg fused into one compiled code path.
# MAGIC
# MAGIC - **`Exchange (4)` (shuffle write):**  
# MAGIC   Writes 90 aggregated rows to shuffle, creating 200 partitions by default.  
# MAGIC   - shuffle records written = **90**, local bytes written = **6.3 KiB**  
# MAGIC   - number of partitions = 200, but **skew empty partitions = 191** — 191 of 200 partitions are completely empty (only 90 cities, spread across 9 non-empty partitions)  
# MAGIC   - This is classic over-partitioning: Spark created 200 slots for a dataset with only 90 distinct values.
# MAGIC
# MAGIC - **`AQEShuffleRead (6)` (AQE coalescing):**  
# MAGIC   AQE reads the shuffle output statistics and immediately coalesces:  
# MAGIC   - number of partitions = **1** (down from 200)  
# MAGIC   - number of coalesced partitions = 1, number of empty partitions = 191  
# MAGIC   - partition data size = 6.8 KiB  
# MAGIC   Since all 90 city rows fit in 6.8 KiB, AQE merges all 200 partitions into **1 single partition** — so the final aggregation runs on 1 task instead of 200.
# MAGIC
# MAGIC - **`HashAggregate (7)` (reduce-side / final):**  
# MAGIC   Merges the partial counts from all tasks to produce the final `city → count` result.  
# MAGIC   - rows output = **6** (only 5-6 rows needed for `show(5)`)  
# MAGIC   - estimated rows output = 90 (10X) — Spark's estimate was off by 10x, but AQE's coalescing decision was still correct  
# MAGIC   - peak memory = 32.3 MiB, time in aggregation build = 2ms — instant because data is tiny  
# MAGIC   Inside `WholeStageCodegen (2)` (duration: 0ms, Stage 9).
# MAGIC
# MAGIC - **`CollectLimit (8)` → `ResultQueryStage (9)` → `AdaptiveSparkPlan (10)`:**  
# MAGIC   `show(5, False)` uses `CollectLimit` to stop collecting after 5 rows. `AdaptiveSparkPlan` confirms AQE is active throughout.
# MAGIC
# MAGIC **Key Takeaway — How GroupBy Works In Spark:**
# MAGIC
# MAGIC | Phase | Stage | Location | Input | Output | Insight |
# MAGIC |-------|-------|----------|-------|--------|---------|
# MAGIC | Partial agg | Stage 7 | Map side (each task) | 39,790,092 rows | 90 rows | Pre-aggregates locally — massive data reduction before shuffle |
# MAGIC | Shuffle | Exchange (4) | Network | 90 rows | 6.3 KiB in 200 partitions | Only tiny pre-aggregated data crosses the wire |
# MAGIC | AQE coalesce | AQEShuffleRead (6) | Post-shuffle | 200 partitions (191 empty) | 1 partition | Eliminates 199 empty/near-empty tasks |
# MAGIC | Final agg | Stage 9 | Reduce side (1 task) | 6.3 KiB | X rows | Merges partial counts into final result |
# MAGIC
# MAGIC - **GroupBy is a wide transformation** because it requires a shuffle — all rows for the same city must land on the same partition for the final aggregation.
# MAGIC - **Two-phase aggregation (partial + final)** is Spark's key optimization: doing partial work locally before the shuffle minimizes what travels over the network.
# MAGIC - **AQE's coalescing** is critical here — without it, the final stage would launch 200 tasks to process a 6.3 KiB dataset, 191 of which would immediately complete with zero work.

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy With Sum()

# COMMAND ----------

# DBTITLE 1,Understanding GroupBy DAG/Plan Visualization
# GroupBy with sum(): computes total transaction amount per city
df_txn_amt_city = (
    transactions_df
    .groupBy("city")
    .agg(F.sum("amt").alias("txn_amt"))
)

# Show top 5 city-level transaction sums
df_txn_amt_city.show(5, False)

# COMMAND ----------

# MAGIC %md
# MAGIC **Spark UI — GroupBy With sum() Follows The Same Pattern As count(), With One Key Difference**
# MAGIC
# MAGIC ![image_1782990921329.png](NB2_images/image_1782990921329.png "image_1782990921329.png")
# MAGIC
# MAGIC | Job | Duration | Stages | Tasks | What it does |
# MAGIC |-----|----------|--------|-------|--------------|
# MAGIC | Job 18 | 7 s | 1/1 | 9/9 | Scans `city` + `amt` columns, partial sum per task, shuffles result |
# MAGIC | Job 19 | 0.1 s | 1/1 (1 skipped) | 1/1 (9 skipped) | Final aggregation — merges partial sums, collects 5 rows for `show()` |
# MAGIC
# MAGIC - Same **2-job AQE split** as `count()` — identical structure.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ![image_1782991004336.png](NB2_images/image_1782991004336.png "image_1782991004336.png")
# MAGIC ![image_1782991040774.png](NB2_images/image_1782991040774.png "image_1782991040774.png")
# MAGIC
# MAGIC **The only meaningful difference vs count() — column pruning reads more data:**
# MAGIC
# MAGIC | Metric | `groupBy().count()` | `groupBy().sum("amt")` | Why |
# MAGIC |--------|--------------------|-----------------------|-----|
# MAGIC | Stage input | 90.6 MiB | **200.3 MiB** | `count()` only needs `city` (1 col); `sum("amt")` needs `city` + `amt` (2 cols) |
# MAGIC | Shuffle write | 6.3 KiB | **6.5 KiB** | Still just 90 city rows — partial sums are tiny regardless |
# MAGIC | Duration | 4 s | **7 s** | Slightly longer — more parquet data scanned |
# MAGIC | Tasks | 9/9 | 9/9 | Same |
# MAGIC
# MAGIC - **Column pruning still applies** — Spark doesn't read all 12 columns. But `sum("amt")` forces it to pull 2 columns instead of 1, which is why input jumps from 90.6 MiB → 200.3 MiB (~2x, as expected for 2 numeric columns vs 1 string column).
# MAGIC - **Shuffle size is almost unchanged (6.3 → 6.5 KiB)** — partial aggregation compresses 39.7M rows down to 90 city-level partial sums before the shuffle, regardless of whether the aggregation is a count or a sum.
# MAGIC - Everything else — 2 jobs, AQE coalescing 200 partitions → 1, final agg on 1 task — is **identical to count()**.

# COMMAND ----------

# MAGIC %md
# MAGIC #### GroupBy With Count Distinct

# COMMAND ----------

# DBTITLE 1,Understanding GroupBy DAG/Plan Visualization
# GroupBy with countDistinct: computes number of unique txn_id per city
df_txn_per_city = (
    transactions_df
    .groupBy("city")
    .agg(F.countDistinct("txn_id").alias("txn_count"))
)

# Show top 5 city-level distinct transaction counts
df_txn_per_city.show(5, False)

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC **Spark UI — countDistinct Creates 3 Jobs (2 Shuffles) Unlike count()/sum() Which Only Need 1 Shuffle**
# MAGIC
# MAGIC ![image_1782996595855.png](NB2_images/image_1782996595855.png "image_1782996595855.png")
# MAGIC
# MAGIC | Job | Duration | Stages | Tasks | What it does |
# MAGIC |-----|----------|--------|-------|--------------|
# MAGIC | Job 4 | 17 s | 1/1 | 9/9 | Scans `city` + `txn_id`, partial agg (barely reduces rows), **first shuffle** — 826.6 MiB |
# MAGIC | Job 5 | 13 s | 1/1 (1 skipped) | 15/15 (9 skipped) | Reads first shuffle, **counts distinct txn_ids per city**, **second shuffle** — 10.5 KiB |
# MAGIC | Job 6 | 0.2 s | 1/1 (2 skipped) | 1/1 (24 skipped) | Final merge aggregation, collects 5 rows for `show()` |
# MAGIC
# MAGIC - **3 jobs = 2 shuffles.** `count()` and `sum()` only needed 1 shuffle (2 jobs). `countDistinct` needs an extra round-trip because Spark must first redistribute all individual values by (city, txn_id) to deduplicate them, and then shuffle the per-city distinct counts a second time for the final merge.
# MAGIC - **24 skipped tasks in Job 6** = Job 4's 9 tasks + Job 5's 15 tasks — both already done, AQE reuses their shuffle outputs.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ![image_1782996641808.png](NB2_images/image_1782996641808.png "image_1782996641808.png")
# MAGIC ![image_1782996677254.png](NB2_images/image_1782996677254.png "image_1782996677254.png")
# MAGIC ![image_1782996704115.png](NB2_images/image_1782996704115.png "image_1782996704115.png")
# MAGIC
# MAGIC **Stage-Level Breakdown:**
# MAGIC
# MAGIC | Stage | Tasks | Input | Shuffle Write | Shuffle Read | Duration | What happened |
# MAGIC |-------|-------|-------|--------------|-------------|----------|---------------|
# MAGIC | Stage 4 (Job 4) | 9/9 | 659.0 MiB | **826.6 MiB** | — | 17 s | Scans `city` + `txn_id` (2 cols), partial agg barely helps, shuffles nearly all 39.7M rows |
# MAGIC | Stage 6 (Job 5) | 15/15 | — | 10.5 KiB | 826.6 MiB | 13 s | Reads all shuffled rows, deduplicates + counts distinct txn_ids per city, produces 150 intermediate rows |
# MAGIC | Stage 9 (Job 6) | 1/1 | — | — | 10.5 KiB | 0.1 s | Final merge — 6 rows for `show()` |
# MAGIC
# MAGIC - **Stage 4 input = 659.0 MiB** (vs 90.6 MiB for `count()`). Two columns are read now: `city` + `txn_id`. Column pruning still applies — only these 2 columns out of 12 are scanned.
# MAGIC - **Shuffle write = 826.6 MiB** — this is the critical difference. `count()`/`sum()` wrote only **6.3–6.5 KiB** after partial aggregation. `countDistinct` writes **826.6 MiB** because it cannot reduce rows before the shuffle (explained below).
# MAGIC - **Stage 6 has 15 tasks** (not 1 like in `count()`). AQE kept 15 partitions because 826.6 MiB of data needs real parallelism — coalescing to 1 partition would create a single 826 MiB task.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Why countDistinct Can't Pre-Aggregate (The Root Cause):**
# MAGIC
# MAGIC - `count()` / `sum()` are **associative + commutative**: each task can safely pre-aggregate its partition locally (e.g., city A has 100 rows in this partition → write `city=A, count=100` to shuffle). All partial results can be merged correctly.
# MAGIC - `countDistinct` is **not associative across partitions**: to count distinct `txn_id` values for a city, Spark must see **all** (city, txn_id) pairs together before it can deduplicate. A task can't know whether `txn_id=XYZ` also appeared in another partition, so it can't safely pre-count.
# MAGIC - Result: HashAggregate(3) on the map side produces **39,790,092 passthrough rows** — nearly all input rows pass through unchanged. Almost zero pre-aggregation benefit, hence 826.6 MiB of shuffle data.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Plan Visualization For df_txn_per_city**
# MAGIC
# MAGIC ![image_1782997067019.png](NB2_images/image_1782997067019.png "image_1782997067019.png")![image_1782997313720.png](NB2_images/image_1782997313720.png "image_1782997313720.png")![image_1782997444323.png](NB2_images/image_1782997444323.png "image_1782997444323.png")![image_1782997546356.png](NB2_images/image_1782997546356.png "image_1782997546356.png")
# MAGIC
# MAGIC **Bottom-up walkthrough:**
# MAGIC
# MAGIC - **`Scan parquet (1)` → `ColumnarToRow (2)`:** Reads 39,790,092 rows, 9,796 batches. Only `city` and `txn_id` columns scanned (column pruning).
# MAGIC
# MAGIC - **`HashAggregate (3)` (map-side partial) inside `WholeStageCodegen (1)` (1.0 min, Stage 4):**  
# MAGIC   > **Role: Try to pre-deduplicate (city, txn_id) pairs locally within each task before the shuffle — but since every txn_id is unique, almost nothing can be eliminated here.**  
# MAGIC   - passthrough output rows = **38,890,092** — almost all rows pass through unchanged  
# MAGIC   - rows output = **39,790,092** — essentially no reduction  
# MAGIC   - peak memory total = **324 MiB** across 9 tasks (36 MiB each), avg hash probes = 1,615–1,627 (already high — tracking many distinct pairs even per-partition)  
# MAGIC   - Since txn_ids are unique per transaction, there is very little deduplication to do at this stage — the hash table just fills up with individual (city, txn_id) pairs and passes them all through.
# MAGIC
# MAGIC - **`Exchange (4)` (first shuffle write):**  
# MAGIC   - shuffle records written = **39,790,092** (all rows), shuffle bytes = **826.6 MiB**  
# MAGIC   - 200 partitions, skew non-empty median partition size = 4,576,325 bytes (~4.5 MiB each)  
# MAGIC   - Unlike `count()` which wrote 90 rows. here, every individual (city, txn_id) record must cross the network.
# MAGIC
# MAGIC - **`AQEShuffleRead (6)` (first AQE coalesce):**  
# MAGIC   - 200 → **15 partitions** (not 1!), partition data total = 873.1 MiB, avg 61 MiB each  
# MAGIC   - AQE cannot coalesce to 1 partition here — 826 MiB in 1 task would be too slow. It keeps 15 partitions for parallel processing.
# MAGIC
# MAGIC - **`HashAggregate (7)` + `HashAggregate (8)` inside `WholeStageCodegen (2)` (45.2s, Stage 6):**  
# MAGIC   - **HashAggregate (7)**  
# MAGIC     > **Role: Full deduplication — builds a massive hash set of all (city, txn_id) pairs within each of the 15 partitions to eliminate duplicates across tasks.**  
# MAGIC     rows output = **39,790,092**, peak memory = **4.5 GiB** (320 MiB per task), avg hash probes = **1,639–1,646** — extremely high because the hash table is nearly full tracking all distinct (city, txn_id) pairs; time in aggregation build = **35.7s** — this is the single biggest bottleneck in the entire query.  
# MAGIC   - **HashAggregate (8)**  
# MAGIC     > **Role: Count the distinct txn_ids per city within each partition — now that duplicates are removed, just group by city and count.**  
# MAGIC     rows output = **150** — 15 partitions × ~10 city groups each produce a partial distinct count (same city can appear in multiple partitions, so counts will be merged again in the final stage).
# MAGIC
# MAGIC - **`Exchange (9)` (second shuffle write):**  
# MAGIC   - shuffle records written = **150** (city-level partial counts), bytes = **10.5 KiB**  
# MAGIC   - 200 partitions, but 191 are empty again — the second shuffle is tiny, just like `count()`.
# MAGIC
# MAGIC - **`AQEShuffleRead (11)` (second AQE coalesce):**  
# MAGIC   - 200 → **1 partition** (11.4 KiB) — now the data is tiny, AQE collapses everything.
# MAGIC
# MAGIC - **`HashAggregate (12)` inside `WholeStageCodegen (3)` (0ms, Stage 9):**  
# MAGIC   > **Role: Final merge — combines the 150 partial city-level distinct counts (from 15 partitions) into the final ~10 city totals.**  
# MAGIC   - rows output = **6** (only 5–6 rows needed for `show(5)`), peak memory = 32.3 MiB, time = 1ms — instant because data is already tiny.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Key Takeaway — countDistinct vs count() vs sum():**
# MAGIC
# MAGIC | Metric | `groupBy().count()` | `groupBy().sum()` | `groupBy().countDistinct()` |
# MAGIC |--------|---------------------|-------------------|-----------------------------|
# MAGIC | Jobs | 2 | 2 | **3** |
# MAGIC | Shuffles | 1 | 1 | **2** |
# MAGIC | Stage input | 90.6 MiB | 200.3 MiB | **659.0 MiB** |
# MAGIC | First shuffle write | 6.3 KiB | 6.5 KiB | **826.6 MiB** |
# MAGIC | Map-side row reduction | 39.7M → 90 | 39.7M → 90 | **39.7M → 39.7M** |
# MAGIC | Peak memory (agg stage) | 2.3 MiB | ~2.3 MiB | **4.5 GiB** |
# MAGIC | AQE post-first-shuffle | 200 → 1 partition | 200 → 1 partition | **200 → 15 partitions** |
# MAGIC | Total duration | ~4s | ~7s | **~30s** |
# MAGIC
# MAGIC - **`countDistinct` is expensive** — the inability to pre-aggregate on the map side makes the first shuffle balloon to 826.6 MiB, memory spikes to 4.5 GiB, and the total time jumps from ~4s to ~30s for the same dataset.
# MAGIC - **Use `approx_count_distinct()`** when exact precision isn't required — it uses the HyperLogLog algorithm which CAN pre-aggregate on the map side (HLL sketches are mergeable), reducing the shuffle to a tiny fraction of the full data.

# COMMAND ----------

print(1)

# COMMAND ----------

# DBTITLE 1,rough
# In Databricks markdown, you can resize images using HTML <img> tag:
# Example: <img src="NB2_images/image_1782898256724.png" width="400"/>

# You can also specify height:
# <img src="NB2_images/image_1782898256724.png" width="400" height="200"/>

# Standard markdown ![alt](url) does not support size, so use HTML for resizing.
