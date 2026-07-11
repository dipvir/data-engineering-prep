# Databricks notebook source
# DBTITLE 1,Importing Modules
from pyspark.sql.types import *
import pyspark.sql.functions as F

# COMMAND ----------

# DBTITLE 1,Loading and Counting Transactions and Customers Data
transactions_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/transactions.parquet/")
print(transactions_df.count())

customers_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/customers.parquet/")
print(customers_df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### What is Data Skew in Spark?
# MAGIC
# MAGIC **Data skew** occurs when the distribution of data across partitions is uneven. This means some partitions contain significantly more records than others, causing certain tasks to take much longer to process. In Spark, data skew can lead to:
# MAGIC
# MAGIC - Slow job execution (straggler tasks)
# MAGIC - Inefficient resource utilization
# MAGIC - Increased shuffle and memory pressure
# MAGIC
# MAGIC **Example:**  
# MAGIC If your `transactions_df` has 39.7M records split across 12 partitions, but one partition holds 10M records while others have much less, the task processing that partition will be much slower.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Join Over Skewed Data

# COMMAND ----------

# DBTITLE 1,Counting Distinct Transactions by Customer ID
(
    transactions_df
    .groupBy("cust_id")
    .agg(F.countDistinct("txn_id").alias("ct"))
    .orderBy(F.desc("ct"))
    .show()
)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### What does the output of the above cell tells?
# MAGIC
# MAGIC The code groups `transactions_df` by `cust_id`, counts distinct `txn_id` values for each customer, and sorts the result from highest to lowest.
# MAGIC
# MAGIC **What the actual output shows:**
# MAGIC * One customer, `C0YDPQWPBJ`, has **17,539,732** distinct transactions.
# MAGIC * The next highest customers are only around **7,992 to 7,999** transactions each.
# MAGIC * Spark is only showing the top 20 rows, but even that sample is enough to reveal the pattern.
# MAGIC
# MAGIC **Interpretation:**
# MAGIC * This is **extreme data skew** on the `cust_id` key.
# MAGIC * One customer value is dramatically larger than the rest, so any partition or shuffle task handling that key will do far more work than others.
# MAGIC * In joins and aggregations, this creates a **straggler task** problem: most tasks finish quickly, while one or a few tasks run much longer.
# MAGIC
# MAGIC **Why this matters for Spark:**
# MAGIC * Work is no longer evenly distributed across partitions.
# MAGIC * Shuffle stages become slower because one partition can receive a very large share of the data.
# MAGIC * CPU, memory, and disk spill pressure can become concentrated on a small number of tasks.
# MAGIC
# MAGIC **Conclusion:**  
# MAGIC This output is strong evidence that the dataset is intentionally skewed. The customer `C0YDPQWPBJ` is a hot key, and that hot key will likely make joins on `cust_id` much slower unless skew-mitigation techniques are used.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# DBTITLE 1,Performing Join On Skewed Data Without Any Optimizations
# Disable broadcast join by setting threshold to -1.
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
# MAGIC ---
# MAGIC ### Observations from the Spark UI for the SMJ On Skewed Data Without AQE
# MAGIC
# MAGIC ---
# MAGIC ![image_1783071813786.png](NB3_images/image_1783071813786.png "image_1783071813786.png")
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **What stands out:**
# MAGIC * There are **200 completed tasks**.
# MAGIC * Most tasks are very fast: the **25th percentile is 0.2 s**, **median is 0.3 s**, and **75th percentile is 0.4 s**.
# MAGIC * But the **slowest task took 43 s**, which is dramatically higher than the rest.
# MAGIC
# MAGIC **Why this indicates skew:**
# MAGIC * A healthy shuffle stage usually has task durations that are relatively close to each other.
# MAGIC * Here, one task is an extreme outlier, which means one partition received much more data than the others.
# MAGIC * That matches the earlier finding that customer `C0YDPQWPBJ` is a hot key with far more rows than the rest.
# MAGIC
# MAGIC **Shuffle evidence:**
# MAGIC * Typical shuffle read is only around **5.8–7.8 MiB**.
# MAGIC * The maximum shuffle read jumps to **1.1 GiB** and **17,684,814 records**.
# MAGIC * This is a very strong sign that one reduce task handled a disproportionately large partition during the join.
# MAGIC
# MAGIC **Spill evidence:**
# MAGIC * Most tasks spilled **0 B**.
# MAGIC * But the worst task spilled up to **3.5 GiB in memory spill** and **980.6 MiB in disk spill**.
# MAGIC * This means the skewed partition became large enough that Spark could not process it fully in memory and had to spill intermediate data.
# MAGIC
# MAGIC **Execution context note:**
# MAGIC * The timeline shows only the **driver**, and your cluster currently has **0 worker nodes**, so this is effectively a **single-node execution**.
# MAGIC * That is why **Shuffle Remote Reads = 0 B** — the shuffle is not moving data across worker machines.
# MAGIC * Even without network shuffle, skew still hurts badly because one task ends up doing far more sorting and merge work than the others.
# MAGIC
# MAGIC **Conclusion:**  
# MAGIC The Spark UI confirms that the Sort Merge Join is suffering from **severe data skew**. Most tasks finish quickly, but one skewed partition becomes a straggler, reads far more shuffle data, and spills heavily. This is exactly the kind of performance problem caused by joining on a highly imbalanced key.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Common Techniques to Handle Data Skew
# MAGIC
# MAGIC 1. **Salting the Skewed Key**
# MAGIC    - Add a random suffix to the skewed key before join/aggregation, then remove it after.
# MAGIC    - Example: For `cust_id`, create a new column like `cust_id_salted = cust_id + "_" + rand_bucket`.
# MAGIC    - Group or join on the salted key, then aggregate results in a second stage.
# MAGIC
# MAGIC 2. **Broadcast Join**
# MAGIC    - If one side of the join (e.g., `customers_df`) is very small, Spark can broadcast it to all worker nodes.
# MAGIC    - This avoids shuffle and can mitigate skew, since the large table is not partitioned by the skewed key.
# MAGIC    - Relevant configs:
# MAGIC      - `spark.sql.autoBroadcastJoinThreshold` (default: 10MB)
# MAGIC      - `spark.sql.adaptive.autoBroadcastJoinThreshold` (for AQE)
# MAGIC    - In your case, `customers_df` (~5K records, 1 partition) is small enough for broadcast join.
# MAGIC    - **Note:** Broadcast join is not always possible if the small table exceeds the threshold or if disabled.
# MAGIC
# MAGIC 3. **Adaptive Query Execution (AQE) Skew Join Handling**
# MAGIC    - Spark can automatically split skewed partitions during joins if AQE is enabled.
# MAGIC    - Relevant configs:
# MAGIC      - `spark.sql.adaptive.enabled = true`
# MAGIC      - `spark.sql.adaptive.skewJoin.enabled = true`
# MAGIC      - Adjust thresholds:  
# MAGIC        - `spark.sql.adaptive.skewJoin.skewedPartitionFactor` (default: 5)
# MAGIC        - `spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes` (default: 256MB)
# MAGIC    - Example: If median partition is 200MB, any partition > 1GB is considered skewed.
# MAGIC
# MAGIC 4. **Increase Number of Partitions**
# MAGIC    - Use `.repartition()` to spread data more evenly, but this alone may not fix hot keys.
# MAGIC
# MAGIC 5. **Skew Hints**
# MAGIC    - Explicitly tell Spark which keys are skewed using DataFrame join hints.
# MAGIC
# MAGIC 6. **Liquid Clustering (for stored tables)**
# MAGIC    - Use liquid clustering to optimize data layout and reduce skew in Delta tables.
# MAGIC
# MAGIC #### Example: Salting for GroupBy
# MAGIC
# MAGIC python
# MAGIC ```
# MAGIC from pyspark.sql.functions import col, concat, lit, rand
# MAGIC
# MAGIC # Add salt for skewed key
# MAGIC salted_df = transactions_df.withColumn("salt", (F.rand() * 10).cast("int"))
# MAGIC salted_df = salted_df.withColumn("cust_id_salted", concat(col("cust_id"), lit("_"), col("salt")))
# MAGIC
# MAGIC # First stage aggregation
# MAGIC agg_stage1 = salted_df.groupBy("cust_id_salted").agg(F.countDistinct("txn_id").alias("ct"))
# MAGIC
# MAGIC # Second stage aggregation (remove salt)
# MAGIC agg_stage2 = agg_stage1.withColumn("cust_id", F.expr("split(cust_id_salted, '_')[0]")) \
# MAGIC     .groupBy("cust_id").agg(F.sum("ct").alias("ct"))
# MAGIC ```
# MAGIC
# MAGIC #### When to Use Each Technique
# MAGIC
# MAGIC - **Broadcast join:** Best when one table is very small (like your `customers_df`), avoids shuffle and skew.
# MAGIC - **Salting:** Best for extreme skew (one or few hot keys).
# MAGIC - **AQE:** Works automatically for moderate skew if enabled.
# MAGIC - **Repartition:** Helps with mild unevenness, not hot keys.
# MAGIC - **Skew hints:** Useful for joins with known skewed keys.
# MAGIC - **Liquid clustering:** For persistent skew in Delta tables.
# MAGIC
# MAGIC ---
# MAGIC **In your Spark UI:**  
# MAGIC - If max task duration is much higher than the 75th percentile (e.g., 43s vs 0.4s), you have severe skew.
# MAGIC - If max shuffle read is much higher than median (e.g., 1.1 GiB vs 7.8 MiB), skew is confirmed.
# MAGIC
# MAGIC **Summary:**  
# MAGIC Choose the right mitigation based on your skew pattern. For your dataset, broadcast join (if not disabled), salting, or AQE skew join handling are most effective.

# COMMAND ----------

# DBTITLE 1,Performing Join With AQE On Skewed Data
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
# MAGIC ---
# MAGIC ### Observations from the Spark UI for the SMJ On Skewed Data With AQE
# MAGIC
# MAGIC ---
# MAGIC ![image_1783076257092.png](NB3_images/image_1783076257092.png "image_1783076257092.png")
# MAGIC
# MAGIC ---
# MAGIC **What stands out:**
# MAGIC * There are only **36 completed tasks**, compared with **200 tasks** in the non-AQE run.
# MAGIC * Task durations are much more balanced: **25th percentile = 2 s**, **median = 2 s**, **75th percentile = 3 s**, and **max = 6 s**.
# MAGIC * The worst task is no longer a huge outlier.
# MAGIC
# MAGIC **Why this is important:**
# MAGIC * In the earlier run without AQE, one task took **43 s** while most others finished in **0.2–0.4 s**.
# MAGIC * Here, the spread is much tighter, which means AQE has made the shuffle/join work far more even.
# MAGIC * This is exactly what you want to see when skew handling is helping: fewer extreme stragglers.
# MAGIC
# MAGIC **Shuffle evidence:**
# MAGIC * Shuffle read now ranges roughly from **14.2 MiB** to **103.3 MiB**.
# MAGIC * The median shuffle read is **59.1 MiB**, and even the maximum is not dramatically larger than the rest.
# MAGIC * Compare that with the non-AQE run, where one task read **1.1 GiB** and **17.7M records**.
# MAGIC * So AQE has clearly reduced the skew concentration in a single partition.
# MAGIC
# MAGIC **Spill and stability interpretation:**
# MAGIC * The screenshot no longer shows the severe spill pattern seen earlier.
# MAGIC * That suggests AQE prevented one oversized reduce-side partition from becoming a memory-heavy bottleneck.
# MAGIC * The stage looks much healthier and more uniform overall.
# MAGIC
# MAGIC **Execution context note:**
# MAGIC * This is still a **single-node cluster** with **0 worker nodes**, so **Shuffle Remote Reads = 0 B** is expected.
# MAGIC * Even on one node, AQE still helps because it improves how Spark handles skewed shuffle partitions.
# MAGIC
# MAGIC **Conclusion:**  
# MAGIC The Spark UI strongly suggests that **AQE improved the skewed Sort Merge Join significantly**. Compared with the non-AQE run, task times are more uniform, the largest shuffle read is far smaller, and the extreme straggler behavior is gone. In short, AQE made the join much more balanced and efficient even though broadcast join remained disabled.

# COMMAND ----------

# DBTITLE 1,Performing Broadcast Join On Skewed Data
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
# MAGIC ---
# MAGIC ### Observations from the Spark UI for the Broadcast Join on Skewed Data
# MAGIC
# MAGIC ---
# MAGIC ![image_1783081676263.png](NB3_images/image_1783081676263.png "image_1783081676263.png")
# MAGIC
# MAGIC **What stands out:**
# MAGIC * There are only **12 completed tasks**, which is fewer than both the non-AQE SMJ (**200 tasks**) and the AQE-enabled SMJ (**36 tasks**).
# MAGIC * Task durations are also quite uniform: **min = 4 s**, **25th percentile = 7 s**, **median = 8 s**, **75th percentile = 9 s**, and **max = 10 s**.
# MAGIC * There is no extreme straggler like the **43 s** task seen in the non-AQE sort merge join.
# MAGIC
# MAGIC **Why broadcast join helps here:**
# MAGIC * In a broadcast join, the small table (`customers_df`) is sent to each executor/task, so Spark does **not** need to reshuffle both sides on `cust_id`.
# MAGIC * That avoids the reduce-side skew problem that hurt the sort merge join.
# MAGIC * Even though `transactions_df` is skewed on `cust_id`, the large table can now be scanned partition by partition without creating one oversized shuffled partition for the hot key.
# MAGIC
# MAGIC **Shuffle evidence:**
# MAGIC * The most important signal is that **Shuffle Read Size / Records is 0.0 B / 0** for nearly all tasks.
# MAGIC * Even the maximum shuffle read is only **289.8 KiB / 5000**, which is tiny compared with the SMJ runs.
# MAGIC * Compare that with the earlier non-AQE SMJ, where one task had to read **1.1 GiB** and **17.7M records**.
# MAGIC * This confirms that broadcast join effectively removed the heavy shuffle bottleneck.
# MAGIC
# MAGIC **Input balance:**
# MAGIC * Input sizes per task are fairly close: roughly **54.1 MiB to 82.4 MiB** and **2.5M to 3.66M records**.
# MAGIC * That is a much healthier distribution than the skewed shuffle partition seen in SMJ.
# MAGIC * The remaining variation comes from scanning partitions of the large input, not from one massive reduce-side hot partition.
# MAGIC
# MAGIC **Execution context note:**
# MAGIC * This is still running on your **single-node cluster** with **0 worker nodes**, so the benefit is not from distributed network transfer.
# MAGIC * The improvement comes from Spark choosing a join strategy that avoids the expensive shuffle on the skewed key.
# MAGIC
# MAGIC **Conclusion:**  
# MAGIC The Spark UI shows that **broadcast join is the best strategy so far for this skewed dataset**. It eliminates the large shuffle, avoids the reduce-side skew problem, removes the severe straggler behavior, and keeps task work much more balanced. Since `customers_df` is very small, broadcasting it is an effective way to handle the skew on `cust_id`.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC #### Handling Skew with Salting
# MAGIC
# MAGIC **Salting** is a technique used to reduce data skew by splitting one hot key into multiple smaller buckets so Spark can process that key in parallel.
# MAGIC
# MAGIC In this notebook, the skewed key is `C0YDPQWPBJ`. Without salting, all rows for that customer tend to land in the same shuffle partition, which creates one very large task. With salting, we add a small extra column such as `salt = 0, 1, 2, ...` so the hot key is no longer treated as one single bucket.
# MAGIC
# MAGIC #### How salting works in a join
# MAGIC
# MAGIC * On the **large table** (`transactions_df`), add a random salt only for the hot key.
# MAGIC * On the **small table** (`customers_df`), duplicate the matching hot-key row across all salt buckets.
# MAGIC * Join using both `cust_id` and `salt`.
# MAGIC
# MAGIC This spreads the skewed customer across multiple tasks instead of forcing one task to process nearly all of its rows.
# MAGIC
# MAGIC #### Why this helps
# MAGIC
# MAGIC * Reduces straggler tasks
# MAGIC * Lowers spill risk on one partition
# MAGIC * Makes shuffle work more balanced
# MAGIC * Helps when broadcast join is disabled or not possible
# MAGIC
# MAGIC #### Important note
# MAGIC
# MAGIC Salting does **not** change the final business result. It only changes how the work is physically distributed during execution.
# MAGIC
# MAGIC ---
# MAGIC

# COMMAND ----------

# DBTITLE 1,Performing Join With Salting On Skewed Data
# Disable broadcast join so the salting technique is what improves the join
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.adaptive.enabled", "false")

spark.conf.set("spark.sql.shuffle.partitions", 35)

# spark.conf.set("spark.sql.adaptive.enabled", "true")
# spark.conf.set("spark.sql.adaptive.autoBroadcastJoinThreshold", -1)

# Hot key identified earlier from the skew analysis
skewed_cust_id = "C0YDPQWPBJ"
num_salt_buckets = 20

# Add random salt only to the skewed key(i.e. C0YDPQWPBJ) on the large table
# For the hot key (skewed_cust_id), assign a random integer in [0, num_salt_buckets) as salt.
# This spreads the skewed records across multiple salt buckets, mitigating partition imbalance during join.
# For all other keys, assign salt=0 (no salting needed).
# This technique ensures only the skewed key is distributed, while non-skewed keys remain unchanged.
transactions_salted = (
    transactions_df
    .withColumn(
        "salt",
        F.when(
            F.col("cust_id") == skewed_cust_id,
            (F.rand(seed=42) * num_salt_buckets).cast("int")
        ).otherwise(F.lit(0))
    )
)

# Replicate only the skewed key(i.e. C0YDPQWPBJ) on the small table across all salt buckets
skewed_customers = (
    customers_df
    .filter(F.col("cust_id") == skewed_cust_id)
    .withColumn("salt", F.explode(F.array(*[F.lit(i) for i in range(num_salt_buckets)])))
)

non_skewed_customers = (
    customers_df
    .filter(F.col("cust_id") != skewed_cust_id)
    .withColumn("salt", F.lit(0))
)

customers_salted = skewed_customers.unionByName(non_skewed_customers)

# Join on the original key plus salt so the hot key is spread across buckets
salted_join_df = (
    transactions_salted
    .join(customers_salted, on=["cust_id", "salt"], how="inner")
    .drop("salt")
)

# Trigger execution without writing output data
salted_join_df.write.format("noop").mode("overwrite").save("../data/test/df_salted_joined.parquet")

# COMMAND ----------

# DBTITLE 1,rough
# Disable broadcast join so the salting technique is what improves the join
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)
spark.conf.set("spark.sql.adaptive.enabled", "false")

spark.conf.set("spark.sql.shuffle.partitions", 35)

# spark.conf.set("spark.sql.adaptive.enabled", "true")
# spark.conf.set("spark.sql.adaptive.autoBroadcastJoinThreshold", -1)

# Hot key identified earlier from the skew analysis
num_salt_buckets = 20

# Add random salt only to the skewed key(i.e. C0YDPQWPBJ) on the large table
# For the hot key (skewed_cust_id), assign a random integer in [0, num_salt_buckets) as salt.
# This spreads the skewed records across multiple salt buckets, mitigating partition imbalance during join.
# For all other keys, assign salt=0 (no salting needed).
# This technique ensures only the skewed key is distributed, while non-skewed keys remain unchanged.
transactions_salted = transactions_df.withColumn(
    "salt", (F.rand(seed=42) * num_salt_buckets).cast("int")
)

# Replicate only the skewed key(i.e. C0YDPQWPBJ) on the small table across all salt buckets
customers_salted = customers_df.withColumn(
    "salt", F.explode(F.array(*[F.lit(i) for i in range(num_salt_buckets)]))
)

# Join on the original key plus salt so the hot key is spread across buckets
salted_join_df = transactions_salted.join(
    customers_salted, on=["cust_id", "salt"], how="inner"
).drop("salt")

# Trigger execution without writing output data
salted_join_df.write.format("noop").mode("overwrite").save(
    "../data/test/df_salted_joined.parquet"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Salting With Groupby

# COMMAND ----------

# DBTITLE 1,Setting Spark Shuffle Partitions to One
spark.conf.set("spark.sql.shuffle.partitions", 1)

# COMMAND ----------

# DBTITLE 1,GroupBy on skewed data without salting
# AQE is disabled here so you can compare the raw effect of salting more clearly.
spark.conf.set("spark.sql.adaptive.enabled", "false")

# This aggregation will suffer from severe skew: the hot key (C0YDPQWPBJ) will dominate one partition,
# causing a straggler task and heavy shuffle/spill.
groupby_without_salting_df = (
    transactions_df
    .groupBy("cust_id")
    .agg(F.count("*").alias("txn_count"))
    .orderBy(F.desc("txn_count"))
)

# Trigger full execution so you can inspect the Spark UI
# Then show the top customers by transaction count
(groupby_without_salting_df
    .write
    .format("noop")
    .mode("overwrite")
    .save("../data/test/groupby_without_salting.parquet"))

display(groupby_without_salting_df.limit(20))

# COMMAND ----------

# DBTITLE 1,GroupBy on skewed data with salting
# Salting spreads the hot key across multiple buckets before the first aggregation,
# then combines the partial aggregates back to the original key.
spark.conf.set("spark.sql.adaptive.enabled", "false")

skewed_cust_id = "C0YDPQWPBJ"
num_salt_buckets = 10

transactions_salted_for_groupby = (
    transactions_df
    .withColumn(
        "salt",
        F.when(
            F.col("cust_id") == skewed_cust_id,
            (F.rand(seed=42) * num_salt_buckets).cast("int")
        ).otherwise(F.lit(0))
    )
)

groupby_with_salting_df = (
    transactions_salted_for_groupby
    .groupBy("cust_id", "salt")
    .agg(F.count("*").alias("partial_txn_count"))
    .groupBy("cust_id")
    .agg(F.sum("partial_txn_count").alias("txn_count"))
    .orderBy(F.desc("txn_count"))
)

# Trigger full execution so you can inspect the Spark UI
# Then show the top customers by transaction count
(groupby_with_salting_df
    .write
    .format("noop")
    .mode("overwrite")
    .save("../data/test/groupby_with_salting.parquet"))

display(groupby_with_salting_df.limit(20))

# COMMAND ----------

print(1)
