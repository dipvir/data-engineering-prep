# Databricks notebook source
# DBTITLE 1,Imports
from pyspark.sql.types import *
import pyspark.sql.functions as F

# COMMAND ----------

# DBTITLE 1,Disable AQE And Set Spark Shuffle Partitions
spark.conf.set("spark.sql.adaptive.enabled", "false") 
spark.conf.set("spark.sql.shuffle.partitions", "50")

# COMMAND ----------

# DBTITLE 1,Loading Data
transactions_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/transactions.parquet/")

# COMMAND ----------

# DBTITLE 1,Getting Number of RDD Partitions
transactions_df.rdd.getNumPartitions()

# COMMAND ----------

# DBTITLE 1,Count Distinct Transactions per Customer
(
    transactions_df
    .groupBy("cust_id")
    .agg(F.countDistinct("txn_id").alias("ct"))
    .orderBy(F.desc("ct"))
    .show()
)

# COMMAND ----------

# DBTITLE 1,Check Current Spark Max Partition Bytes Setting
spark.conf.get("spark.sql.files.maxPartitionBytes")
# by default maxPartitionBytes is 134217728b =  128Mb 

# COMMAND ----------

# DBTITLE 1,Set and Verify Spark Max Partition Bytes Configuration
spark.conf.set("spark.sql.files.maxPartitionBytes", "200217728")
spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

# DBTITLE 1,Loading Data
transactions_df = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/spark-experiments-main/data/data_skew/transactions.parquet/")

# COMMAND ----------

# DBTITLE 1,Getting Number of RDD Partitions
transactions_df.rdd.getNumPartitions()

# COMMAND ----------

# DBTITLE 1,Count Distinct Transactions per Customer
(
    transactions_df
    .groupBy("cust_id")
    .agg(F.countDistinct("txn_id").alias("ct"))
    .orderBy(F.desc("ct"))
    .show()
)

# COMMAND ----------

# DBTITLE 1,Notebook Summary
# MAGIC %md
# MAGIC ### Summary of this notebook
# MAGIC
# MAGIC This notebook shows how `spark.sql.files.maxPartitionBytes` influences **file scan partition planning** when Spark reads Parquet files.
# MAGIC
# MAGIC #### What the notebook demonstrates
# MAGIC
# MAGIC * With the default setting, `spark.conf.get("spark.sql.files.maxPartitionBytes")` returned **`134217728b`**, which is **128 MiB**.
# MAGIC * After reading the transactions Parquet data, `transactions_df.rdd.getNumPartitions()` returned **12**.
# MAGIC * Then the setting was changed to **`200217728` bytes** (about **191 MiB**).
# MAGIC * After re-reading the same Parquet data, `transactions_df.rdd.getNumPartitions()` returned **8**.
# MAGIC
# MAGIC #### Interpretation
# MAGIC
# MAGIC * Increasing `maxPartitionBytes` lets Spark pack **more file data into each input partition**.
# MAGIC * Because of that, Spark created **fewer scan partitions** after the setting was increased.
# MAGIC * In this notebook, the change from roughly **128 MiB** to **191 MiB** reduced the planned read partitions from **12 to 8**.
# MAGIC
# MAGIC #### Important observation
# MAGIC
# MAGIC The aggregation result did **not** change. The top customer still had **17,539,732** distinct transactions, while the next customers were around **8K**.
# MAGIC
# MAGIC That means:
# MAGIC * `spark.sql.files.maxPartitionBytes` changes **how Spark reads the files**
# MAGIC * it does **not** change the actual data
# MAGIC * it does **not** fix the skew on `cust_id`
# MAGIC
# MAGIC #### Final takeaway
# MAGIC
# MAGIC This notebook is a good demonstration that `spark.sql.files.maxPartitionBytes` is a **scan-stage tuning parameter**. It affects how many input partitions Spark creates while reading files, but it is **not a shuffle-skew optimization setting**.
# MAGIC

# COMMAND ----------

# DBTITLE 1,Chat Discussion Summary
# MAGIC %md
# MAGIC ### Important points from the chat discussion
# MAGIC
# MAGIC #### 1. `spark.sql.files.maxPartitionBytes` vs `getNumPartitions()`
# MAGIC
# MAGIC These two are related, but they are not the same:
# MAGIC
# MAGIC * `spark.sql.files.maxPartitionBytes` = Spark's **target input size per read partition**
# MAGIC * `transactions_df.rdd.getNumPartitions()` = the **actual number of partitions** Spark created for that DataFrame
# MAGIC
# MAGIC So one is the **planning rule**, and the other is the **observed result**.
# MAGIC
# MAGIC #### 2. Why 163 Parquet files did not become 163 partitions
# MAGIC
# MAGIC Spark does **not** always use one partition per file.
# MAGIC
# MAGIC When reading Parquet, Spark can combine multiple small files into one scan partition. The final partition count depends on:
# MAGIC
# MAGIC * total file sizes
# MAGIC * split planning
# MAGIC * `spark.sql.files.maxPartitionBytes`
# MAGIC * file open cost planning
# MAGIC
# MAGIC That is why many physical files can still become only **12** or **8** Spark input partitions.
# MAGIC
# MAGIC #### 3. What “enough cores” means
# MAGIC
# MAGIC Your current compute is a **single-node `Standard_DS3_v2`** cluster, which is roughly **4 vCPUs**.
# MAGIC
# MAGIC For learning Spark, you can think of that as about **4 task slots**.
# MAGIC
# MAGIC That means:
# MAGIC * Spark can run about **4 tasks at the same time**
# MAGIC * if there are **12 partitions**, they run in about **3 waves**
# MAGIC * if there are **8 partitions**, they run in about **2 waves**
# MAGIC
# MAGIC This is why more partitions do not always mean faster execution.
# MAGIC
# MAGIC #### 4. One task per core
# MAGIC
# MAGIC As a default mental model in Spark:
# MAGIC
# MAGIC * **1 partition -> 1 task**
# MAGIC * **1 CPU slot/core -> 1 task at a time**
# MAGIC
# MAGIC So if the machine has about **4 usable CPU slots**, Spark usually runs about **4 tasks concurrently**.
# MAGIC
# MAGIC #### 5. Why this setting may help loading time
# MAGIC
# MAGIC This setting can help only in the **file read stage**:
# MAGIC
# MAGIC * Lower value -> more, smaller scan tasks
# MAGIC * Higher value -> fewer, larger scan tasks
# MAGIC
# MAGIC It may improve read performance if the original file splits are too large and the cluster has enough parallel compute to benefit.
# MAGIC
# MAGIC But it does **not** solve:
# MAGIC * join skew
# MAGIC * groupBy skew
# MAGIC * shuffle imbalance
# MAGIC
# MAGIC Those need different techniques such as **AQE, broadcast join, or salting**.
# MAGIC
# MAGIC #### 6. Practical conclusion from this notebook
# MAGIC
# MAGIC This notebook confirms the main idea clearly:
# MAGIC
# MAGIC * default `128 MiB` target -> **12 partitions**
# MAGIC * larger `~191 MiB` target -> **8 partitions**
# MAGIC
# MAGIC So increasing `spark.sql.files.maxPartitionBytes` reduced the number of input partitions because Spark packed more scan data into each one.
# MAGIC
