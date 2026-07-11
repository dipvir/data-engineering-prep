# Databricks notebook source
# DBTITLE 1,Imports
import pyspark.sql.functions as F
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %md
# MAGIC ### *Small File Problem* :- An Analogy of *Reading A 300-Page Novel In PDF Format*
# MAGIC
# MAGIC * **The Analogy**: Imagine if that novel wasn't stored in one single file, but instead split into 300 individual files—one for every single page. To read the entire book, you would have to spend significant time performing repetitive actions: **finding** the file, **opening** the file, **reading** it, and **closing** it for every single page.
# MAGIC * **The Data Engineering Reality**: This overhead of opening, closing, and performing metadata lookups for thousands of small files (instead of a few neatly packed larger ones) causes **wasted compute resources** and **poor I/O performance**.
# MAGIC * **The Conclusion**: When your data is scattered across too many small files, the system spends more time managing the overhead of those files than actually processing the data, which leads to significant performance degradation.

# COMMAND ----------

# MAGIC %md
# MAGIC ### How *Delta Lake* solves the *Small File Problem* primarily through the *OPTIMIZE* command, which uses a *Bin Packing Algorithm*.
# MAGIC
# MAGIC *   **How it works**: The *OPTIMIZE* command reads the numerous tiny files, groups them into larger, ideally-sized blocks (targeting a default of **1GB**), and then writes them out as more efficient, larger files. This replaces the scattered, fragmented data with a streamlined layout that is significantly faster for query engines to process.
# MAGIC *   **Other mechanisms**: 
# MAGIC     *   **Auto Compaction**: Delta can automatically compact small files into larger ones during write operations.
# MAGIC     *   **Optimized Writes**: This feature reshuffles data before writing to ensure that the data being written to the storage is already optimally sized, preventing the small file problem from occurring in the first place.
# MAGIC *   **Cleanup**: Once the files are optimized, the **VACUUM** command is used to remove the now-obsolete "tombstone" files, ensuring the storage is clean and costs are minimized.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Demonstration Code To Mimic Small Files Problem `with Manual Optimize(Traditional Writes)`

# COMMAND ----------

# MAGIC %md
# MAGIC **Manual Optimize (Traditional Writes)** refers to the process where you manually optimize a Delta table by running the `OPTIMIZE` command after writing data, especially when the write operation creates many small files (e.g., due to repartitioning). This approach is used to compact those small files into larger, more efficient files, improving query performance and reducing storage overhead. Unlike auto-optimization, manual optimize requires explicit action from the user.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC **What is the OPTIMIZE Command in Delta Lake?**
# MAGIC
# MAGIC The **OPTIMIZE** command in Delta Lake is used to compact small files within a Delta table into larger, more efficient files. This process improves query performance and reduces storage overhead by minimizing the number of files the system needs to manage.
# MAGIC
# MAGIC ---
# MAGIC ##### How OPTIMIZE Works
# MAGIC - **Bin Packing Algorithm:** OPTIMIZE reads many small files and groups them into larger files, targeting a default size (typically 1GB per file).
# MAGIC - **Compaction:** The command rewrites the data, replacing scattered small files with fewer, larger files.
# MAGIC - **Partition Pruning:** You can optimize specific partitions to target only the data that needs compaction.
# MAGIC
# MAGIC ##### Benefits
# MAGIC - Faster query performance due to reduced file management overhead.
# MAGIC - Lower storage costs by eliminating unnecessary small files.
# MAGIC - Improved efficiency for downstream processing and analytics.
# MAGIC
# MAGIC ---
# MAGIC ##### Usage Example
# MAGIC using sql
# MAGIC ```
# MAGIC OPTIMIZE delta_catalog.delta_db.optimize_ex1;
# MAGIC ```
# MAGIC
# MAGIC using Python API:
# MAGIC ```
# MAGIC from delta.tables import DeltaTable
# MAGIC delta_table = DeltaTable.forName(spark, "delta_catalog.delta_db.optimize_ex1")
# MAGIC delta_table.optimize().executeCompaction()
# MAGIC ```
# MAGIC
# MAGIC ##### After OPTIMIZE
# MAGIC - Old files are retained for time travel and versioning.
# MAGIC - Use the **VACUUM** command to permanently remove obsolete files and free up storage.
# MAGIC
# MAGIC ---
# MAGIC ##### Summary:  
# MAGIC The OPTIMIZE command is a key Delta Lake feature for solving the small file problem, ensuring your data lake remains performant and cost-effective.

# COMMAND ----------

# DBTITLE 1,Loading Sample Parquet File As Dataframe
# Using this parquet file to create delta table with small files to mimic small files problem in delta lake
df = spark.read.parquet(
    "abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_201_99457.parquet"
)
display(df.limit(5))

# COMMAND ----------

# DBTITLE 1,Some Data Insights
print(df.count())
display(df.select("category").distinct()) 
print(df.select("category").distinct().count()) 

# COMMAND ----------

# MAGIC %md
# MAGIC **Note :- Read This First** 
# MAGIC - Ideally according to the lab next cell should be `Saving/Writing Dataframe As Delta Table`, but mostly because for serverless compute in my case, the operation is not creating 5 partition per category instead creating just one file per category.
# MAGIC - This is happening because serverless has optimizeWrite and autoCompact setting enabled, which is good thing but for demonstration we need to create such scenario.
# MAGIC - So, I am disabling that property first below.

# COMMAND ----------

# DBTITLE 1,Disabling Auto-Optimization
# MAGIC %sql
# MAGIC -- Disable Auto-Optimization directly on the table blueprint
# MAGIC ALTER TABLE delta_catalog.delta_db.optimize_ex1 
# MAGIC SET TBLPROPERTIES (
# MAGIC   'delta.autoOptimize.optimizeWrite' = 'false',
# MAGIC   'delta.autoOptimize.autoCompact' = 'false'
# MAGIC );

# COMMAND ----------

# DBTITLE 1,Saving/Writing Dataframe As Delta Table With Small File Problem
# here we are using repartition to change the number of partitions to create 5 file per category
# This is to mimic scenario of having a lot of small files in delta table
# And we are doing partitionBy to create the partitioning/sharding/folders based on the column category
# So, In adls we will have 5 partitions for each category

df.repartition(5).write.mode("overwrite").partitionBy("category").saveAsTable("delta_catalog.delta_db.optimize_ex1")

# COMMAND ----------

# MAGIC %md
# MAGIC **Note :- Read This First** 
# MAGIC - Also, as for the first time when we ran above cell it created one file per category in adls because of optimizeWrite and autoCompact setting.
# MAGIC - And then i disabled and reran the write operation again which ran correctly with 5 new file per category, but the old file was still there in adls as part of time travel(i.e total 6 file per category).
# MAGIC - So, in order to remove that old file which is not in use anymore, I ran `vacuum` command and also reset the retention duration back to the default 7 days in the next cell. 

# COMMAND ----------

# DBTITLE 1,Vacuum
# MAGIC %sql
# MAGIC -- STEP 1: Set the physical retention duration property natively on the table level (Serverless option)
# MAGIC ALTER TABLE delta_catalog.delta_db.optimize_ex1 
# MAGIC SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours');
# MAGIC
# MAGIC -- STEP 2: Run VACUUM without the "RETAIN" clause 
# MAGIC -- (It will automatically read the 0 hours property we just set above)
# MAGIC VACUUM delta_catalog.delta_db.optimize_ex1;
# MAGIC
# MAGIC -- Reset the deleted file retention duration back to the default 7 days
# MAGIC ALTER TABLE delta_catalog.delta_db.optimize_ex1 
# MAGIC SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 7 days');

# COMMAND ----------

# DBTITLE 1,Count Total Records
# MAGIC %sql
# MAGIC SELECT count(*) FROM delta_catalog.delta_db.optimize_ex1;

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.optimize_ex1;
# MAGIC
# MAGIC -- The reason there is so many versions is explained in notes above, so as workaround the table end with such history.
# MAGIC -- Also now its corrected as per scenario in version 2 CTAS numFiles:40(i.e 5X8 categories) in operationMetrics column.

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table `optimize_ex1(with small file problem)` data files in ADLS**
# MAGIC
# MAGIC - We repartitioned by 5 and then partitionby category, which means 5 partition per category.
# MAGIC - below is the image for one of the category.
# MAGIC
# MAGIC ![image_1782135325120.png](NB8_images/image_1782135325120.png "image_1782135325120.png")

# COMMAND ----------

# DBTITLE 1,Testing Execution Time With Small File Problem In Table
# MAGIC %%time
# MAGIC df_ex1 = spark.read.table("delta_catalog.delta_db.optimize_ex1")
# MAGIC result = df_ex1.filter(df_ex1.category == "Clothing").collect()

# COMMAND ----------

# MAGIC %md
# MAGIC **Note :- Read This First**
# MAGIC
# MAGIC *   **OPTIMIZE** command reads the numerous tiny files, groups them into larger, ideally-sized blocks (targeting a default of **1GB**), and then writes them out as more efficient, larger files. This replaces the scattered, fragmented data with a streamlined layout that is significantly faster for query engines to process.
# MAGIC *   **Cleanup**: Once the files are optimized, the **VACUUM** command is used to remove the now-obsolete "tombstone" files, ensuring the storage is clean and costs are minimized.
# MAGIC *   **Other mechanisms**: 
# MAGIC     *   **Auto Compaction**: Delta can automatically compact small files into larger ones during write operations.
# MAGIC     *   **Optimized Writes**: This feature reshuffles data before writing to ensure that the data being written to the storage is already optimally sized, preventing the small file problem from occurring in the first place.

# COMMAND ----------

# DBTITLE 1,Optimize Delta Table Using Delta Python API
from delta.tables import DeltaTable

# ── Option 1: Using spark.sql() (python + SQL approach) ──────────────────────────────
# spark.sql("OPTIMIZE delta_catalog.delta_db.optimize_ex1")

# ── Option 2: Using Delta Python API (idiomatic Python approach) ────────────
delta_table = DeltaTable.forName(spark, "delta_catalog.delta_db.optimize_ex1")
delta_table.optimize().executeCompaction()

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table `optimize_ex1(with small file problem)` data files after running `OPTIMIZE`**
# MAGIC
# MAGIC - As shown below **OPTIMIZE** Created one new larger parquet file which combines all 5 files data, thereby solving small file problem.
# MAGIC - The old files are sill there because of time travel fearture, will run **VACUUM** next to remove those files.
# MAGIC
# MAGIC ![image_1782136151937.png](NB8_images/image_1782136151937.png "image_1782136151937.png")
# MAGIC
# MAGIC **This is json file from delta log for that `OPTIMIZE` transection version**
# MAGIC
# MAGIC - https://adb-7405609743131312.12.azuredatabricks.net/editor/files/2475877354770909?o=7405609743131312
# MAGIC - It removes(not from adls) all 40(5 per category) files and adds 8 new file per category.

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.optimize_ex1;

# COMMAND ----------

# DBTITLE 1,Retention Duration Property
# MAGIC %sql
# MAGIC -- Set the physical retention duration property natively on the table level (Serverless option)
# MAGIC ALTER TABLE delta_catalog.delta_db.optimize_ex1 
# MAGIC SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours');

# COMMAND ----------

# DBTITLE 1,Vacuum With Delta Python API
delta_table.vacuum(0);  

# COMMAND ----------

# MAGIC %md
# MAGIC **Finally `VACUUM` has cleaned/removed all old files from ADLS**
# MAGIC
# MAGIC ![image_1782138043745.png](NB8_images/image_1782138043745.png "image_1782138043745.png")

# COMMAND ----------

# MAGIC %md
# MAGIC **Now after Resolving Small File Problem, lets test execution time it takes to run same code**

# COMMAND ----------

# DBTITLE 1,Testing Execution Time After Resolving Small File Problem
# MAGIC %%time
# MAGIC df_ex1 = spark.read.table("delta_catalog.delta_db.optimize_ex1")
# MAGIC result = df_ex1.filter(df_ex1.category == "Clothing").collect()

# COMMAND ----------

# MAGIC %md
# MAGIC **Performance Improvement After Running The `OPTIMIZE` Commands On Delta Table**
# MAGIC
# MAGIC - After re-executing the same query, the runtime improved to `1.13 seconds` compared to the `2.3 seconds` it took before optimization. while this specific improvement may seem modest(not much) due to the small size of the experimental data, the technique provides significant performance gains on larger, real-world datasets.
# MAGIC
# MAGIC **Note:-**
# MAGIC
# MAGIC **OPTIMIZE** : 
# MAGIC * **Goal**: Fixes the "Small File Problem" by using a **Bin Packing Algorithm** to combine many tiny files into larger, efficiently sized files (typically ~1GB).
# MAGIC * **Benefit**: Improves read performance and reduces metadata lookup overhead.
# MAGIC
# MAGIC **VACUUM** :
# MAGIC * **Goal**: Performs physical cleanup of storage by permanently deleting files that were replaced (tombstoned) by operations like *OPTIMIZE*, *UPDATE*, or *DELETE*.
# MAGIC * **Benefit**: Reduces storage costs and keeps the data lake clean, though it limits the ability to perform *Time Travel* on data older than the retention period.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Optimizing Specific Partitions using Predicates
# MAGIC
# MAGIC how to use **predicates (filters/WHERE clauses)** with the `OPTIMIZE` command to target specific data partitions rather than the entire table.
# MAGIC
# MAGIC *   **Use Case**: This is essential for **incremental data pipelines**. If you ingest data daily, you typically only want to optimize the specific partition corresponding to the new arrival rather than running a costly compaction on the entire historical dataset.
# MAGIC *   **How it works**: By appending a `WHERE` clause (e.g., `WHERE category = 'fruit'`), the `OPTIMIZE` command limits its scope to just that filter criteria. The system reads only the files relevant to that partition, merges them into a single larger file, and leaves the rest of the table untouched.
# MAGIC *   **Practicality**: This approach saves significant compute resources, especially as tables grow over time, by ensuring that optimization efforts are focused solely on the most recently modified or high-traffic data regions.

# COMMAND ----------

# DBTITLE 1,Creating New Category To Replicate Incremental Data
# Workaround, to replicate/copy existing category to create new category data
df_fruits_data = df_ex1.filter(df_ex1.category == "Clothing").withColumn("category", F.lit("Fruits"))

# snaity check - count should be 1
df_fruits_data.select("category").distinct().count()

# COMMAND ----------

# DBTITLE 1,Writing New Category To Replicate Incremental Data
# Like prevously we are writing the data with 5 partition for incremental category data
df_fruits_data.repartition(5).write.mode("append").partitionBy("category").saveAsTable("delta_catalog.delta_db.optimize_ex1")

# COMMAND ----------

# MAGIC %md
# MAGIC **Note:- Read This**
# MAGIC
# MAGIC - *Below we are optimizing only one category using predicates(filters/WHERE clauses) pretending its incremental data*
# MAGIC - *Just to remind, rest of the categories are already optimized and vacuumed above*

# COMMAND ----------

# DBTITLE 1,Optimize Delta Table With Predicates Using Delta Python API
# optimize the table
delta_table.optimize().where("category = 'Fruits'").executeCompaction()

# COMMAND ----------

# DBTITLE 1,Optimize Delta Table With Predicates Using SQL
# MAGIC %sql
# MAGIC OPTIMIZE delta_catalog.delta_db.optimize_ex1
# MAGIC WHERE category = 'Fruits';

# COMMAND ----------

# DBTITLE 1,Vacuum With Delta Python API
# First Set Retention Duration = 'interval 0 hours' for this cell

delta_table.vacuum(0);

# COMMAND ----------

# MAGIC %md
# MAGIC **So this is how we can optimize and vacuum in only for newly incremented partitions using predicates.**
# MAGIC
# MAGIC While `OPTIMIZE` works brilliantly with predicates (like `WHERE category = 'Fruits'`), **`VACUUM` does not accept predicates.** You cannot run a command like `VACUUM ... WHERE category = 'Fruits'`.
# MAGIC
# MAGIC Here is the exact theoretical breakdown of why the engine handles these two operations completely differently under the hood.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏗️ Why `OPTIMIZE` and `VACUUM` Have Different Rules
# MAGIC
# MAGIC The difference comes down to what these two commands are trying to accomplish physically inside your cloud storage directory.
# MAGIC
# MAGIC #### 1. `OPTIMIZE` is a Data Layout Action (Localized)
# MAGIC
# MAGIC The `OPTIMIZE` command is designed to solve the small file problem by compacting data. Because data in a partitioned table is physically segregated into separate folders on disk (e.g., `category=Fruits/`, `category=Electronics/`), the engine can isolate its work.
# MAGIC
# MAGIC When you run `OPTIMIZE ... WHERE category = 'Fruits'`, you are telling the engine:
# MAGIC
# MAGIC > *"Only look inside the `Fruits` folder, ignore every other directory on cloud storage, and merge the tiny files there into one big file."*
# MAGIC
# MAGIC Because this operation creates brand-new, healthy files, it only needs to touch the specific partitions you filter for. This saves massive amounts of cluster compute and execution time in production.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 2. `VACUUM` is a Garbage Collection Action (Global Table State)
# MAGIC
# MAGIC The `VACUUM` command does not care about data layout or folder partitions. Its sole job is to clean up **Tombstones (`remove` actions)** across the entire table's transactional timeline.
# MAGIC
# MAGIC When you run `VACUUM`, the engine performs a complete checklist scan:
# MAGIC
# MAGIC 1. It reads the **entire history** of the Delta log (`_delta_log/`) from Version 0 to the current version.
# MAGIC 2. It compiles a master list of *every single file* that was ever covered by a tombstone marker (`remove` action).
# MAGIC 3. It checks the timestamps of those tombstones against your retention threshold (like `0 hours` or `7 days`).
# MAGIC 4. It checks the physical cloud storage directory to see if those files are still sitting there. If they are older than the threshold, it deletes them.
# MAGIC
# MAGIC #### 🚫 Why the Engine Blocks Predicates on Vacuum
# MAGIC
# MAGIC If Delta Lake allowed you to run a command like `VACUUM ... WHERE category = 'Fruits'`, it would create a massive risk of **Data Corruption**.
# MAGIC
# MAGIC Imagine an `UPDATE` or `MERGE` statement statement ran earlier, which modified records across *multiple* categories, shifting data around and generating tombstone files globally across your storage container. If you vacuumed only a specific filtered partition, the transaction log and the physical files on disk would fall out of sync. You would end up with a broken history timeline where some old files are purged and others are floating around as zombies.
# MAGIC
# MAGIC To prevent metadata corruption and guarantee **ACID compliance**, the engine forces `VACUUM` to be an **all-or-nothing, table-wide operation**. It must scan the entire metadata tree to safely commit hard deletes to storage.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📝 Core Takeaway for your Playbook:
# MAGIC
# MAGIC * **`OPTIMIZE` is targeted:** It can safely target a single folder or partition to save compute.
# MAGIC * **`VACUUM` is global:** It must scan the complete metadata timeline of the entire table to safely purge real files without corrupting your Time Travel logs.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Root Causes of the Small File Problem
# MAGIC
# MAGIC The instructor outlines three primary **Root Causes of the Small File Problem**:
# MAGIC
# MAGIC 1. **Repartitioning to a very large number**: If you have a relatively small dataset (e.g., 10GB) and repartition it into a massive number of chunks (e.g., 10,000 partitions), each individual file becomes tiny (e.g., ~1MB). This creates significant overhead during read operations.
# MAGIC
# MAGIC 2. **Partitioning on a high-cardinality column**: If you use a column with many distinct values (e.g., 'category' with thousands of unique types) to partition your table, the system creates a separate folder/file structure for every single unique value. This leads to an explosion of small files.
# MAGIC
# MAGIC 3. **Frequently updated data sets**: In scenarios where data is ingested or updated in small batches every few minutes (e.g., streaming or micro-batching), the system writes new, small files for every update cycle. 
# MAGIC
# MAGIC **Key Takeaway**: While the first two causes are technical issues that can often be resolved by adjusting code configurations, the third cause is often a business requirement. For these cases, the instructor recommends using optimization techniques like **OPTIMIZE** at scheduled intervals to compact the accumulated small files.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Demonstration Code To Mimic Small Files Problem `with Automatic Optimize(Optimized Writes)`

# COMMAND ----------

# MAGIC %md
# MAGIC #### Automatic Optimize (Optimized Writes)
# MAGIC
# MAGIC **Automatic Optimize (Optimized Writes)** is a Delta Lake feature that improves write performance and prevents the small file problem by intelligently reshuffling and combining data before writing it to storage. When enabled, Delta Lake automatically groups data into optimally sized files (typically ~1GB) during write operations, reducing the number of tiny files and improving query efficiency.
# MAGIC
# MAGIC - **How it works:** Data is reorganized in memory before being written, so each file is efficiently sized.
# MAGIC - **Benefits:** Faster reads, reduced metadata overhead, and less need for manual compaction.
# MAGIC - **Enable via:** Table properties or write options (e.g., `.option("delta.autoOptimize.optimizeWrite", "true")`).
# MAGIC
# MAGIC **Summary:**  
# MAGIC Optimized Writes automatically create larger, well-sized files during data ingestion, helping maintain healthy Delta tables and boosting performance.

# COMMAND ----------

# DBTITLE 1,Saving/Writing Dataframe As Delta Table With Small File Problem
# here we are using repartition to change the number of partitions to create 288 file/partitons per category
# This is to mimic scenario of having a lot of small files in delta table
# And we are doing partitionBy to create the partitioning/sharding/folders based on the column category
# So, In adls we will have 288 partitions for each category

# option1 :- 1. Here repartition does'nt work because of serverless optimizeWrite and autoCompact settings are enable and we cant set it to off globally in serverless.
# df.repartition(288).write.mode("overwrite").partitionBy("category").saveAsTable("delta_catalog.delta_db.optimize_ex_test")

# option1 :- 2. Serverless option to dissable the setting on the fly.
# Write on the fly while embedding the serverless safety overrides
(df.repartition(288).write
 .mode("overwrite")
 .partitionBy("category")
 .option("delta.autoOptimize.optimizeWrite", "false")
 .option("delta.autoOptimize.autoCompact", "false")
 .saveAsTable("delta_catalog.delta_db.optimize_ex2"))

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table `optimize_ex2(with small file problem)` data files in ADLS**
# MAGIC
# MAGIC - We repartitioned by 288 and then partitionby category, which means 288 partition per category.
# MAGIC - below is the image for first few partitons from one of the category.
# MAGIC
# MAGIC ![image_1782300388052.png](NB8_images/image_1782300388052.png "image_1782300388052.png")

# COMMAND ----------

# DBTITLE 1,Testing Execution Time With Small File Problem In Table
# MAGIC %%time
# MAGIC df_ex2 = spark.read.table("delta_catalog.delta_db.optimize_ex2")
# MAGIC result = df_ex2.filter(df_ex2.category == "Clothing").collect()

# COMMAND ----------

# DBTITLE 1,Writing With Small File Problem And Optimized Writes
# Automatic Optimize(Optimized Writes)
(
    df.repartition(288)
    .write.mode("overwrite")
    .partitionBy("category")
    .option("optimizeWrite", "true")
    .option("delta.autoOptimize.optimizeWrite", "false")
    .option("delta.autoOptimize.autoCompact", "false")
    .saveAsTable("delta_catalog.delta_db.optimize_ex3")
)

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table optimize_ex3(with small file problem And optimized writes) data files in ADLS**
# MAGIC
# MAGIC - We repartitioned by 288 here as well and then partitionby category, which means 288 partition per category.
# MAGIC - And we also used optimized writes which created appropreate sized partiton per category.
# MAGIC - below is the image for one of the category, as the dataset size is very small it grouped all 288 partitions in just 1 partiton per category.
# MAGIC
# MAGIC ![image_1782302539222.png](NB8_images/image_1782302539222.png "image_1782302539222.png")

# COMMAND ----------

# DBTITLE 1,Testing Execution Time After Resolving Small File Problem
# MAGIC %%time
# MAGIC df_ex3 = spark.read.table("delta_catalog.delta_db.optimize_ex3")
# MAGIC result = df_ex3.filter(df_ex3.category == "Clothing").collect()

# COMMAND ----------

# MAGIC %md
# MAGIC **Performance Improvement With Automatic Optimize(Optimized Writes) On Delta Table**
# MAGIC
# MAGIC - After re-executing the same query, the runtime improved around `4 seconds` compared to around `16 seconds` it took before optimization. the technique provided significant performance gain.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Auto Compaction

# COMMAND ----------

# MAGIC %md
# MAGIC #### 🗜️ Deep Dive: Auto Compaction in Delta Lake
# MAGIC
# MAGIC **Auto Compaction** is a Delta Lake feature that automatically merges small files into larger ones during write operations, improving read performance and reducing storage overhead.
# MAGIC
# MAGIC ---
# MAGIC ##### What Is Auto Compaction?
# MAGIC - **Automatic file merging:** When enabled, Delta Lake monitors the number and size of files written to a table. If too many small files are detected, it triggers compaction to combine them into fewer, larger files.
# MAGIC - **Triggered during writes:** Compaction happens automatically after write operations, based on configurable thresholds.
# MAGIC
# MAGIC ---
# MAGIC ##### Why Is Auto Compaction Important?
# MAGIC - **Improves query performance:** Large numbers of small files slow down read operations due to increased metadata and file access overhead.
# MAGIC - **Reduces storage costs:** Fewer files mean less metadata and more efficient storage usage.
# MAGIC - **Simplifies maintenance:** Reduces the need for manual OPTIMIZE commands.
# MAGIC
# MAGIC ---
# MAGIC ##### How Does Auto Compaction Work?
# MAGIC 1. **Thresholds:** Compaction is triggered when the number of files in a partition exceeds `spark.databricks.delta.autoCompact.minNumFiles` (default: 50) or when file sizes are below `spark.databricks.delta.autoCompact.minFileSize` (default: 50MB).
# MAGIC 2. **Automatic merging:** Small files are merged into larger files during the write process.
# MAGIC 3. **Configurable:** Can be enabled/disabled via table properties or write options.
# MAGIC
# MAGIC ---
# MAGIC ##### Key Properties
# MAGIC - `delta.autoOptimize.autoCompact`: Enables/disables auto compaction (`true`/`false`).
# MAGIC - `spark.databricks.delta.autoCompact.minNumFiles`: Minimum number of files to trigger compaction.
# MAGIC - `spark.databricks.delta.autoCompact.minFileSize`: Minimum file size to trigger compaction.
# MAGIC
# MAGIC ---
# MAGIC ##### Enabling Auto Compaction
# MAGIC **Via Table Properties:**
# MAGIC sql
# MAGIC ```
# MAGIC ALTER TABLE <table_name>
# MAGIC SET TBLPROPERTIES ('delta.autoOptimize.autoCompact' = 'true');
# MAGIC ```
# MAGIC
# MAGIC **Via Write Options:**
# MAGIC python
# MAGIC ```
# MAGIC df.write.option("delta.autoOptimize.autoCompact", "true").saveAsTable("<table_name>")
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC ##### Best Practices
# MAGIC - **Enable auto compaction** for frequently updated tables to avoid small file problems.
# MAGIC - **Adjust thresholds** for your workload and data size.
# MAGIC - **Monitor table performance** and storage usage to optimize settings.
# MAGIC
# MAGIC ---
# MAGIC **Summary:**  
# MAGIC Auto Compaction is a powerful Delta Lake feature that helps maintain healthy tables by automatically merging small files, improving performance, and reducing storage costs. Use it alongside optimized writes and periodic OPTIMIZE commands for best results.

# COMMAND ----------

# DBTITLE 1,Changing AutoCompact To Smaller Value For This Lab
# MAGIC %sql
# MAGIC -- default value of spark.databricks.delta.autoCompact.minNumFiles is 50.(need user-managed cluster)
# MAGIC -- print(spark.conf.set("spark.databricks.delta.autoCompact.minNumFiles", 3)) # setting the value to 3
# MAGIC -- print(spark.conf.get("spark.databricks.delta.autoCompact.minNumFiles")) # getting the value
# MAGIC
# MAGIC -- In serverless, manual Spark config overrides are not supported. Use Delta table properties instead.
# MAGIC -- ALTER TABLE delta_catalog.delta_db.optimize_ex3
# MAGIC -- SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'false');
# MAGIC
# MAGIC -- ALTER TABLE delta_catalog.delta_db.optimize_ex3
# MAGIC -- SET TBLPROPERTIES ('delta.autoOptimize.autoCompact' = 'true');
# MAGIC
# MAGIC -- ALTER TABLE delta_catalog.delta_db.optimize_ex3
# MAGIC -- SET TBLPROPERTIES ('spark.databricks.delta.autoCompact.minNumFiles' = '3');
# MAGIC
# MAGIC -- SHOW TBLPROPERTIES delta_catalog.delta_db.optimize_ex3;

# COMMAND ----------

# MAGIC %md
# MAGIC - Auto-Compaction setting to minNumFiles=3 wasnt working in serverless so will create 51 partitions to trigger auto compaction.
# MAGIC - Because default value of spark.databricks.delta.autoCompact.minFileSize is 50.

# COMMAND ----------

# DBTITLE 1,Creating New Category
# Workaround, to replicate/copy existing category to create new category data
df_detergents_data = df.filter(df.category == "Clothing").withColumn("category", F.lit("detergents"))

# snaity check - count should be 1
df_detergents_data.select("category").distinct().count()

# COMMAND ----------

# DBTITLE 1,Writing New Category/Partition To optimize_ex3 Table
(
    df_detergents_data.repartition(51)
    .write.mode("append")
    .partitionBy("category")
    .saveAsTable("delta_catalog.delta_db.optimize_ex3")
)

# COMMAND ----------

# MAGIC %md
# MAGIC **What happend after writing detergents category in `optimize_ex3` table with 51 partitions and auto compaction enabled**
# MAGIC
# MAGIC - As, the deafult size for auto compaction is 50 so it gets triggred after getting 51 repartition to write.
# MAGIC - And it removes/soft deletes all 51 files and creates new larger files with appropreate partition.
# MAGIC - In our case it created one final file combining all 51 files.
# MAGIC
# MAGIC first few files
# MAGIC ![image_1782320156547.png](NB8_images/image_1782320156547.png "image_1782320156547.png")
# MAGIC
# MAGIC last few file
# MAGIC ![image_1782320184224.png](NB8_images/image_1782320184224.png "image_1782320184224.png")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Vacuum
# MAGIC (When it can — and cannot — limit time travel)

# COMMAND ----------

# MAGIC %md
# MAGIC #### 🧹 Deep Dive: VACUUM in Delta Lake
# MAGIC **VACUUM** is a Delta Lake garbage-collection command. It permanently deletes files that are no longer needed by the current table state after the configured retention period has passed.
# MAGIC
# MAGIC ---
# MAGIC ##### What Does VACUUM Do?
# MAGIC - **Removes obsolete files:** Deletes data files that were already removed logically in the Delta log.
# MAGIC - **Frees up storage:** Helps reduce cloud storage cost by cleaning up old, unused files.
# MAGIC - **Preserves transactional safety:** Delta only deletes files that are no longer part of the active snapshot.
# MAGIC
# MAGIC ---
# MAGIC ##### How VACUUM Relates to Time Travel
# MAGIC A very important nuance is that **VACUUM does not automatically make every old version unreadable**.
# MAGIC
# MAGIC Time travel fails only when **the version you query still depends on a file that VACUUM has physically deleted**.
# MAGIC
# MAGIC So the real rule is:
# MAGIC - **If an older version still has all of its required files, time travel can still work.**
# MAGIC - **If one or more required files were permanently removed, that older version can no longer be reconstructed.**
# MAGIC
# MAGIC ---
# MAGIC ##### How VACUUM Works
# MAGIC 1. **Reads Delta log history:** Reviews file add/remove actions across the table timeline.
# MAGIC 2. **Finds obsolete files:** Identifies files already removed from the active table state.
# MAGIC 3. **Applies retention threshold:** Only files older than the configured retention window are eligible.
# MAGIC 4. **Physically deletes them:** Removes those files from storage.
# MAGIC
# MAGIC ---
# MAGIC ##### Key Properties
# MAGIC - **Retention Period:** Default is 7 days. Lower values reduce rollback/time-travel safety.
# MAGIC - **Global Operation:** VACUUM always works at the full-table level; it does not support partition predicates.
# MAGIC
# MAGIC ---
# MAGIC ##### Why Predicates Are Not Allowed
# MAGIC VACUUM must reason about the table's complete file history. Allowing partial cleanup such as `WHERE category = 'Fruits'` could leave metadata and physical storage out of sync.
# MAGIC
# MAGIC ---
# MAGIC ##### Best Practices
# MAGIC - **Do not set retention to 0 in production** unless you fully understand the rollback and recovery impact.
# MAGIC - **Use `DESCRIBE HISTORY` plus current file layout** to understand what operation created obsolete files.
# MAGIC - **Do not assume that a successful VACUUM means every old version should fail immediately.** The outcome depends on which files each version needs.
# MAGIC
# MAGIC ---
# MAGIC **Summary:**  
# MAGIC - VACUUM permanently removes files that are already obsolete.
# MAGIC - VACUUM limits time travel only for versions that still require those removed files.
# MAGIC - Therefore, seeing an older version still query successfully after VACUUM does not mean VACUUM failed; it means that version is still reconstructible in this specific setup.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Code to explore when VACUUM can limit time travel

# COMMAND ----------

# DBTITLE 1,Load and Filter Invoice Data by Customer ID Ranges
df_1k_45k = spark.read.parquet(
    "abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_201_99457.parquet"
).filter(F.col("customer_id").between(1000, 45000))

df_46k_99k = spark.read.parquet(
    "abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_201_99457.parquet"
).filter(F.col("customer_id").between(46000, 99000))

print(df_1k_45k.count())
print(df_46k_99k.count())

# COMMAND ----------

# DBTITLE 1,Writing Dataframe to Delta Table with Overwrite Mode
df_1k_45k.write.mode("overwrite").saveAsTable("delta_catalog.delta_db.vacuum_ex_tt")

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.vacuum_ex_tt

# COMMAND ----------

# DBTITLE 1,Appending Dataframe to Delta Table
df_46k_99k.write.mode("append").saveAsTable("delta_catalog.delta_db.vacuum_ex_tt")

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.vacuum_ex_tt

# COMMAND ----------

# DBTITLE 1,Sanity
# MAGIC %sql
# MAGIC SELECT
# MAGIC   count(*) total_rows,
# MAGIC   min(customer_id) AS min_cid,
# MAGIC   max(customer_id) As max_cid
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.vacuum_ex_tt

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table `vacuum_ex_tt` data files in ADLS**
# MAGIC
# MAGIC - The 1st parquet file contains records from 101-150  and the 2nd contains records from 151-200.
# MAGIC
# MAGIC ![image_1782381867985.png](NB8_images/image_1782381867985.png "image_1782381867985.png")

# COMMAND ----------

# MAGIC %md
# MAGIC **Now I am deleting rows with customer IDs between 151 and 200**
# MAGIC - In this layout, the 2nd file contains only these rows, so Delta can tombstone/remove that entire file.

# COMMAND ----------

# DBTITLE 1,Delete Rows with Customer IDs Between 151 and 200
# MAGIC %sql
# MAGIC -- Disable Deletion Vectors on the table blueprint
# MAGIC ALTER TABLE delta_catalog.delta_db.vacuum_ex_tt
# MAGIC SET TBLPROPERTIES ('delta.enableDeletionVectors' = 'false');
# MAGIC
# MAGIC DELETE FROM
# MAGIC   delta_catalog.delta_db.vacuum_ex_tt
# MAGIC WHERE
# MAGIC   customer_id BETWEEN 46000 AND 99000;

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table vacuum_ex_tt data files in ADLS(After Delete)**
# MAGIC - Deletion vector is added.
# MAGIC
# MAGIC ![image_1782381455292.png](NB8_images/image_1782381455292.png "image_1782381455292.png")

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.vacuum_ex_tt

# COMMAND ----------

# DBTITLE 1,Sanity On Current Version
# MAGIC %sql
# MAGIC SELECT
# MAGIC   count(*) total_rows,
# MAGIC   min(customer_id) AS min_cid,
# MAGIC   max(customer_id) As max_cid,
# MAGIC   sum(customer_id) AS sum_cid
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.vacuum_ex_tt

# COMMAND ----------

# DBTITLE 1,Sanity On Version 1(File Marked For Deleted For This Version)
# MAGIC %sql
# MAGIC -- Time Travel is possible because vacuum is still not ran.
# MAGIC SELECT
# MAGIC   count(*) total_rows,
# MAGIC   min(customer_id) AS min_cid,
# MAGIC   max(customer_id) As max_cid,
# MAGIC   sum(customer_id) AS sum_cid
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.vacuum_ex_tt VERSION AS OF 1

# COMMAND ----------

# DBTITLE 1,Setting Zero Hour Retention Duration on Delta Table
# MAGIC %sql
# MAGIC -- Set the physical retention duration property natively on the table level (Serverless option)
# MAGIC ALTER TABLE delta_catalog.delta_db.vacuum_ex_tt 
# MAGIC SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours');

# COMMAND ----------

# DBTITLE 1,Run Vacuum Command to Clean Delta Table
# MAGIC %sql
# MAGIC VACUUM delta_catalog.delta_db.vacuum_ex_tt;

# COMMAND ----------

# MAGIC %md
# MAGIC **This is the state of delta table `vacuum_ex_tt` data files in ADLS(After Vacuum Operation)**
# MAGIC
# MAGIC - 2nd file is deleted as expected.
# MAGIC - The retention period from cloud storage(here adls) should be off for this vacuum section
# MAGIC - Else even after vacuum file will be deleted from cloud storage with available retention period, because of which tumstoned files will still be accesible.
# MAGIC
# MAGIC ![image_1782382004516.png](NB8_images/image_1782382004516.png "image_1782382004516.png")

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.vacuum_ex_tt

# COMMAND ----------

# MAGIC %md
# MAGIC **Now let's see if we can do time travel**

# COMMAND ----------

# DBTITLE 1,Setting Default Retention Duration
# MAGIC %sql
# MAGIC -- Set the physical retention duration property natively on the table level (Serverless option)
# MAGIC ALTER TABLE delta_catalog.delta_db.vacuum_ex_tt 
# MAGIC SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = '7 days');

# COMMAND ----------

# DBTITLE 1,Final Check After Vacuum
# MAGIC %sql
# MAGIC SELECT
# MAGIC   count(*) total_rows,
# MAGIC   min(customer_id) AS min_cid,
# MAGIC   max(customer_id) As max_cid,
# MAGIC   sum(customer_id) AS sum_cid
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.vacuum_ex_tt VERSION AS OF 1;
# MAGIC
# MAGIC -- So, as expected it gave error for version 1 with the file which is now deleted permanently
# MAGIC -- And ran properly for other versions as its required set of file was present.
