# Databricks notebook source
# DBTITLE 1,Imports
import pyspark.sql.functions as F
from datetime import datetime

# COMMAND ----------

# MAGIC %md
# MAGIC ###What is Z-Order?
# MAGIC
# MAGIC **Z-Order (ZORDER BY)** is a data layout optimization in Delta Lake that co-locates related data in the same set of files, enabling Delta to skip large amounts of irrelevant data during queries via **data skipping**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **How it works**
# MAGIC When you run `OPTIMIZE ... ZORDER BY (col1, col2)`, Delta Lake rewrites the table's data files using a **Z-order space-filling curve** — a multi-dimensional indexing technique. It maps multiple columns into a single linear ordering such that values that are close together in N-dimensional space remain close together in the file layout. The result: rows with similar values in the Z-ordered columns end up in the same files.
# MAGIC
# MAGIC Delta tracks **min/max statistics** per file per column. At query time, if a `WHERE` clause filter can be evaluated against those stats, entire files are skipped without being read — this is called **file skipping**.
# MAGIC
# MAGIC ---
# MAGIC **When to use Z-Order**
# MAGIC
# MAGIC Z-Order is effective when:
# MAGIC * Queries frequently filter on specific columns (e.g., `WHERE user_id = ...` or `WHERE event_date = ...`)
# MAGIC * The column has **high cardinality** (many distinct values like user_id, transaction_id)
# MAGIC * You have large tables where file skipping yields meaningful I/O savings
# MAGIC * You can't or don't want to use partitioning (Z-Order works inside partitions too)
# MAGIC
# MAGIC ---
# MAGIC **Z-Order vs Partitioning vs Liquid Clustering**
# MAGIC
# MAGIC | Feature | Partitioning | Z-Order | Liquid Clustering |
# MAGIC |---|---|---|---|
# MAGIC | Works on | Low-cardinality cols | Any column | Any column (auto) |
# MAGIC | Maintenance | Manual | Manual (`OPTIMIZE`) | Automatic (incremental) |
# MAGIC | Multi-column | No | Yes (up to ~4 cols) | Yes |
# MAGIC | Recommended for | Legacy/external tables | UC tables w/ manual ops | UC managed tables (preferred) |
# MAGIC
# MAGIC ---
# MAGIC **Key limitations**
# MAGIC
# MAGIC * Z-Order must be re-run manually via `OPTIMIZE` — it does not apply to newly added files automatically
# MAGIC * Effectiveness degrades with too many Z-ordered columns (diminishing returns beyond 3-4)
# MAGIC * It rewrites data files, which can be expensive on large tables
# MAGIC * **Liquid Clustering** (with `CLUSTER BY`) is the modern replacement — it supports incremental clustering and is the recommended approach for Unity Catalog managed tables
# MAGIC
# MAGIC ---
# MAGIC **Basic syntax**
# MAGIC
# MAGIC ```sql
# MAGIC OPTIMIZE schema.table_name
# MAGIC ZORDER BY (column1, column2);
# MAGIC ```
# MAGIC
# MAGIC
# MAGIC **Summary**
# MAGIC - Z-Order is best understood as: *sort the data so that what you query together lives together*, giving Delta's file-skipping the best chance to skip irrelevant files entirely.
# MAGIC - In Simple words Z-Order logically sorts and repartitions/rewrites similar data in same file. 

# COMMAND ----------

# DBTITLE 1,Loading Sample Parquet File As Dataframe
df = spark.read.parquet(
    "abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_201_99457.parquet"
)
print(df.count())

# COMMAND ----------

# MAGIC %md
# MAGIC - We are doing union on same data below to mimic a seen where most file contains a overlaping row/same data between all files which will cause performance degradation.
# MAGIC - Then will apply Z-order to validate the performance improvement.

# COMMAND ----------

# DBTITLE 1,Union On Same Data
df_union = df
expected_rows = 10000000 #1cr

while df_union.count() <= expected_rows:
    df_union = df_union.union(df_union)

print("df_union rows count :- ", df_union.count())

# COMMAND ----------

# DBTITLE 1,Writing The Final Dataframe
df_union.write.mode("overwrite").saveAsTable("delta_catalog.delta_db.zorder_tbl_ex1")

# COMMAND ----------

# DBTITLE 1,Getting No. Of Added Parquet File Count
# MAGIC %sql
# MAGIC -- UC-managed tables block direct dbutils.fs.ls() on __unitystorage paths.
# MAGIC -- Use _metadata.file_path to list physical files for the partition instead.
# MAGIC SELECT count(DISTINCT _metadata.file_path) AS file_count
# MAGIC FROM delta_catalog.delta_db.zorder_tbl_ex1

# COMMAND ----------

# DBTITLE 1,Testing Query Performance
import time

start = time.time()

result = spark.sql("""
    WITH base AS (
        SELECT
            customer_id,
            category,
            gender,
            shopping_mall,
            quantity * price   AS line_total,
            quantity,
            price,
            invoice_date
        FROM delta_catalog.delta_db.zorder_tbl_ex1 VERSION AS OF 0
        -- Narrow, highly selective filter -> forces file skipping to matter
        WHERE customer_id BETWEEN 5000 AND 8000
    ),
    agg AS (
        SELECT
            category,
            gender,
            shopping_mall,
            COUNT(*)                         AS txn_count,
            COUNT(DISTINCT customer_id)      AS unique_customers,
            SUM(line_total)                  AS total_sales,
            AVG(line_total)                  AS avg_sale,
            MAX(line_total)                  AS max_sale,
            MIN(line_total)                  AS min_sale,
            SUM(quantity)                    AS total_qty,
            SUM(line_total) / SUM(quantity)  AS revenue_per_unit
        FROM base
        GROUP BY category, gender, shopping_mall
    )
    SELECT
        category,
        gender,
        shopping_mall,
        txn_count,
        unique_customers,
        ROUND(total_sales, 2)                                               AS total_sales,
        ROUND(avg_sale, 2)                                                  AS avg_sale,
        ROUND(max_sale, 2)                                                  AS max_sale,
        ROUND(min_sale, 2)                                                  AS min_sale,
        total_qty,
        ROUND(revenue_per_unit, 2)                                          AS revenue_per_unit,
        RANK() OVER (PARTITION BY category ORDER BY total_sales DESC)       AS rank_in_category,
        ROUND(
            total_sales * 100.0 / SUM(total_sales) OVER (PARTITION BY category),
            2
        )                                                                   AS pct_of_category
    FROM agg
    ORDER BY category, rank_in_category
""")
# display() triggers actual execution
display(result)

end = time.time()
print(f"\n>>> WITHOUT Z-Order (VERSION 0): {end - start:.2f}s")

# COMMAND ----------

# DBTITLE 1,Applying Z-order (SQL Code)
# MAGIC %sql
# MAGIC OPTIMIZE delta_catalog.delta_db.zorder_tbl_ex1
# MAGIC ZORDER BY customer_id; --In ZORDER By we put columns that we are using on our queries to filter/prune the table.

# COMMAND ----------

# DBTITLE 1,Applying Z-order (Delta Python API Code)
# from delta.tables import DeltaTable

# delta_table = DeltaTable.forName(spark, "delta_catalog.delta_db.zorder_tbl_ex1")
# delta_table.optimize().executeZOrderBy("customer_id")

# COMMAND ----------

# DBTITLE 1,Getting Updated Count Of Added Parquet File After Zorder
# MAGIC %sql
# MAGIC -- UC-managed tables block direct dbutils.fs.ls() on __unitystorage paths.
# MAGIC -- Use _metadata.file_path to list physical files for the partition instead.
# MAGIC SELECT count(DISTINCT _metadata.file_path) AS file_count
# MAGIC FROM delta_catalog.delta_db.zorder_tbl_ex1

# COMMAND ----------

# MAGIC %md
# MAGIC - So the Z-order tumstoned all old 1024 files and created 15 new files with colocated data **(when input was 10cr)**.
# MAGIC - So the Z-order tumstoned all old 128 files and created 1 new files with colocated data **(when input was 1cr)**.
# MAGIC - Now lets test same query.

# COMMAND ----------

# DBTITLE 1,Testing Query Performance After Zorder
import time

start = time.time()

result = spark.sql("""
    WITH base AS (
        SELECT
            customer_id,
            category,
            gender,
            shopping_mall,
            quantity * price   AS line_total,
            quantity,
            price,
            invoice_date
        FROM delta_catalog.delta_db.zorder_tbl_ex1
        -- Same narrow filter on Z-ordered column -> Delta skips most files
        WHERE customer_id BETWEEN 5000 AND 8000
    ),
    agg AS (
        SELECT
            category,
            gender,
            shopping_mall,
            COUNT(*)                         AS txn_count,
            COUNT(DISTINCT customer_id)      AS unique_customers,
            SUM(line_total)                  AS total_sales,
            AVG(line_total)                  AS avg_sale,
            MAX(line_total)                  AS max_sale,
            MIN(line_total)                  AS min_sale,
            SUM(quantity)                    AS total_qty,
            SUM(line_total) / SUM(quantity)  AS revenue_per_unit
        FROM base
        GROUP BY category, gender, shopping_mall
    )
    SELECT
        category,
        gender,
        shopping_mall,
        txn_count,
        unique_customers,
        ROUND(total_sales, 2)                                               AS total_sales,
        ROUND(avg_sale, 2)                                                  AS avg_sale,
        ROUND(max_sale, 2)                                                  AS max_sale,
        ROUND(min_sale, 2)                                                  AS min_sale,
        total_qty,
        ROUND(revenue_per_unit, 2)                                          AS revenue_per_unit,
        RANK() OVER (PARTITION BY category ORDER BY total_sales DESC)       AS rank_in_category,
        ROUND(
            total_sales * 100.0 / SUM(total_sales) OVER (PARTITION BY category),
            2
        )                                                                   AS pct_of_category
    FROM agg
    ORDER BY category, rank_in_category
""") 
# display() triggers actual execution
display(result)

end = time.time()
print(f"\n>>> WITH Z-Order (latest version): {end - start:.2f}s")

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.zorder_tbl_ex1;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Z-order With Hive Style Partition

# COMMAND ----------

# MAGIC %md
# MAGIC **Hive-style partitioning** is a method of organizing data in a directory structure where each partition column and its value form a subfolder, such as `invoice_date=2021-01-01`. This approach allows data to be physically separated based on partition column values, making queries on those columns more efficient. For example, a table partitioned by `invoice_date` will have folders like `invoice_date=2021-01-01`, `invoice_date=2021-01-02`, etc., each containing only the data for that date. Hive-style partitioning is widely used in big data systems like Apache Hive and Spark, enabling fast filtering and pruning of data during query execution. While Delta Lake supports partitioning, Hive-style partitioning refers specifically to this folder-based layout, which is not part of the Delta Lake protocol but is commonly used with Parquet and other file formats.

# COMMAND ----------

# DBTITLE 1,Writing The Final Dataframe
df.write.mode("overwrite").partitionBy("invoice_date").saveAsTable("delta_catalog.delta_db.zorder_tbl_ex2")

# COMMAND ----------

# DBTITLE 1,Vacuum Rough
# spark.sql("""
#     ALTER TABLE delta_catalog.delta_db.zorder_tbl_ex2
#     SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours')
# """)

# spark.sql("""
#     VACUUM delta_catalog.delta_db.zorder_tbl_ex2
# """)

# 
for m in dir(F): 
    if "date" in m : print(m)

# COMMAND ----------

# MAGIC %md
# MAGIC - In Case Of Hive Style Partition: i.e Data is distributed in among column example invoice_date folders/partitions
# MAGIC - Then we ZORDER BY: customer_id
# MAGIC - For each of those invoice_date

# COMMAND ----------

# DBTITLE 1,Creating New invoice_date Data To Replicate Incremental Data
df_new_partiton = df.filter(F.col("invoice_date") == "2021-01-01").withColumn("invoice_date", F.lit(F.current_date()))
display(df_new_partiton.limit(5))
print(df_new_partiton.select("invoice_date").distinct().count())

# COMMAND ----------

# DBTITLE 1,Writing The Incremental Data
df_new_partiton.write.mode("append").partitionBy("invoice_date").saveAsTable("delta_catalog.delta_db.zorder_tbl_ex2")

# COMMAND ----------

# DBTITLE 1,Sanity
# MAGIC %sql
# MAGIC SELECT
# MAGIC   min(invoice_date),
# MAGIC   max(invoice_date)
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.zorder_tbl_ex2;

# COMMAND ----------

# DBTITLE 1,Applying Z-order With Hive Style Partitioning
# MAGIC %sql
# MAGIC OPTIMIZE
# MAGIC   delta_catalog.delta_db.zorder_tbl_ex2
# MAGIC WHERE
# MAGIC   invoice_date = '2026-06-26' --In Where we put whatever partition column we used.
# MAGIC ZORDER BY customer_id; --In ZORDER By we put columns that we are using on our queries to filter/prune the table.

# COMMAND ----------

# DBTITLE 1,Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.zorder_tbl_ex2;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Conlusion On data optimization method *Hive-style partitioning* and *Z-Ordering*
# MAGIC
# MAGIC *   **Hive-style Partitioning**: This organizes data by placing records into separate folders based on the value of a specific column (e.g., date). While this effectively skips irrelevant data during queries, it relies on static directory structures.
# MAGIC *   **Z-Ordering**: This is a space-filling curve technique that maps multi-dimensional data into a single dimension while preserving **locality**. By placing similar data points close together in files, it enables the engine to "skip" more data files, significantly reducing the amount of data sent over the wire.
# MAGIC *   **The Shared Limitation**: The instructor emphasizes that both approaches are **inflexible**. Because they require you to decide your partitioning and Z-Order columns **upfront** (at the time of table creation or during periodic maintenance), they cannot easily adapt to changing query patterns or uneven data growth (data skew) after the data has been laid out.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### What is Liquid Clustering(Advanced Optimization Technique) in detail?
# MAGIC
# MAGIC Liquid Clustering is the modern replacement for both Hive-style partitioning and Z-Order in Delta Lake on Unity Catalog managed tables. Here's a detailed breakdown:
# MAGIC
# MAGIC ---
# MAGIC **What it is**
# MAGIC - Liquid Clustering uses a flexible, file-level clustering strategy based on a **space-filling curve** (similar to Z-Order internally), but it is **incremental** and **adaptive** — it doesn't require rewriting the entire table when you run `OPTIMIZE`.
# MAGIC
# MAGIC ---
# MAGIC **How it differs from Z-Order / Partitioning**
# MAGIC
# MAGIC | | Hive Partitioning | Z-Order | Liquid Clustering |
# MAGIC |---|---|---|---|
# MAGIC | Column choice | At table creation | Any time, but full rewrite | At creation, changeable later |
# MAGIC | Rewrite scope | Full partition | Full table | Only unclustered files |
# MAGIC | Data skew handling | Poor | Poor | Built-in |
# MAGIC | Multi-column | No | Yes (~4 cols) | Yes |
# MAGIC | Auto-maintenance | No | No | Yes (via `OPTIMIZE`) |
# MAGIC | Recommended | Legacy | UC tables (manual) | UC managed tables |
# MAGIC
# MAGIC ---
# MAGIC **Key concepts**
# MAGIC
# MAGIC - **`CLUSTER BY` at table creation** — defines which columns to cluster on:
# MAGIC ```sql
# MAGIC CREATE TABLE my_table (id INT, event_date DATE, region STRING)
# MAGIC CLUSTER BY (event_date, region);
# MAGIC ```
# MAGIC
# MAGIC - **Incremental `OPTIMIZE`** — only newly added/unclustered files are processed. On a large table, this means `OPTIMIZE` gets cheaper over time, not more expensive.
# MAGIC
# MAGIC - **Changing cluster columns** — unlike partitioning, you can change `CLUSTER BY` columns without recreating the table:
# MAGIC ```sql
# MAGIC ALTER TABLE my_table CLUSTER BY (region);
# MAGIC ```
# MAGIC
# MAGIC - **No data skew** — Liquid Clustering distributes data evenly regardless of value frequency, solving the classic partition skew problem (e.g., one date having 10x more rows than others).
# MAGIC
# MAGIC - **Predictive Optimization** — on Serverless / Unity Catalog, Databricks can automatically run `OPTIMIZE` for you in the background.
# MAGIC
# MAGIC ---
# MAGIC **When to use it**
# MAGIC - UC managed Delta tables (your current setup)
# MAGIC - High-cardinality columns (user_id, transaction_id)
# MAGIC - Query patterns that change over time
# MAGIC - Tables with uneven data distribution

# COMMAND ----------

# DBTITLE 1,Loading And Counting Multiple Parquet Invoice Files
df1 = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet")
df2 = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_1_100.parquet")
df3 = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_201_99457.parquet")

print("df1 count:", df1.count())
print("df2 count:", df2.count())
print("df3 count:", df3.count())

# COMMAND ----------

# DBTITLE 1,Expanding DataFrame By Repeated Union Until Target Rows
df_union = df1.union(df2).union(df3)
print("df_union rows count :- ", df_union.count())

# COMMAND ----------

# MAGIC %md
# MAGIC **Note :- Please Read This First**
# MAGIC
# MAGIC - First we creating a table with **hive style partitioning** and applying **z-order** over it.
# MAGIC - Then will create a table with **liquid clustering**.
# MAGIC - And will **compare the performace of both**.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Creating Delta Table With Hive Style Partitioning And Applying ZOrder

# COMMAND ----------

# DBTITLE 1,Saving Dataframe to Delta Table with Partitioning
df_union.write.mode("overwrite").partitionBy("invoice_date").saveAsTable("delta_catalog.delta_db.lc_tbl_ex1")

# COMMAND ----------

# DBTITLE 1,Applying Z-order (SQL Code)
# MAGIC %sql
# MAGIC OPTIMIZE delta_catalog.delta_db.lc_tbl_ex1
# MAGIC ZORDER BY customer_id; --In ZORDER By we put columns that we are using on our queries to filter/prune the table.

# COMMAND ----------

# DBTITLE 1,Sanity
# MAGIC %sql
# MAGIC SELECT count(*) FROM delta_catalog.delta_db.lc_tbl_ex1;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Creating Delta Table With Liquid Clustering.

# COMMAND ----------

# DBTITLE 1,Writing Dataframe Clustered By Invoice Date And Customer ID
df_union.write.mode("overwrite").clusterBy("invoice_date", "customer_id").saveAsTable("delta_catalog.delta_db.lc_tbl_ex2")

# COMMAND ----------

# DBTITLE 1,Sanity
# MAGIC %sql
# MAGIC SELECT
# MAGIC   count(*)
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.lc_tbl_ex2;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Comparing/Testing Both Tables Performance

# COMMAND ----------

# DBTITLE 1,Testing Delta Table With Hive Style Partitioning & Z-order
# MAGIC %%time
# MAGIC spark.sql("""
# MAGIC     SELECT
# MAGIC         category,
# MAGIC         SUM(price * quantity) AS total_sales
# MAGIC     FROM
# MAGIC         delta_catalog.delta_db.lc_tbl_ex1
# MAGIC     WHERE
# MAGIC         customer_id = 201
# MAGIC         AND (invoice_date BETWEEN '2022-01-01' AND '2023-12-31')
# MAGIC     GROUP BY
# MAGIC         category
# MAGIC         """)

# COMMAND ----------

# DBTITLE 1,Testing Delta Table With Liquid Clustering
# MAGIC %%time
# MAGIC spark.sql("""
# MAGIC     SELECT
# MAGIC         category,
# MAGIC         SUM(price * quantity) AS total_sales
# MAGIC     FROM
# MAGIC         delta_catalog.delta_db.lc_tbl_ex2
# MAGIC     WHERE
# MAGIC         customer_id = 201
# MAGIC         AND (invoice_date BETWEEN '2022-01-01' AND '2023-12-31')
# MAGIC     GROUP BY
# MAGIC         category
# MAGIC         """)
