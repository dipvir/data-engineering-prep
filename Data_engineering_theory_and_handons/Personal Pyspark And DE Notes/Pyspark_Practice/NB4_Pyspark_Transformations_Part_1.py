# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# DBTITLE 1,Read Delta Table As Pyspark DataFrame
df=spark.read.table("samples.bakehouse.sales_franchises")
display(df)

# COMMAND ----------

# DBTITLE 1,Query Delta Table With SQL
# MAGIC %sql
# MAGIC select * from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Get Columns - PySpark
df.columns

# COMMAND ----------

# DBTITLE 1,Get Column - SQL
# MAGIC %sql
# MAGIC SHOW COLUMNS IN samples.bakehouse.sales_franchises;

# COMMAND ----------

# DBTITLE 1,Select - PySpark
df2=df.select("name","country")
display(df2)

# COMMAND ----------

# DBTITLE 1,Select - SQL
# MAGIC %sql
# MAGIC select name,country from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Expr - PySpark
from pyspark.sql.functions import expr
# df2=df.select("name",expr("country as my_country"))
df2=df.select("name",expr("concat(city,'_',country) as location"))
display(df2)

# COMMAND ----------

# DBTITLE 1,SelectExpr - PySpark
from pyspark.sql.functions import expr
df2=df.selectExpr("name","country as my_country")
display(df2)

# COMMAND ----------

# DBTITLE 1,Alias - PySpark
from pyspark.sql.functions import expr
df2=df.select("name",expr("concat(city,'_',country)").alias("location"))
display(df2)

# COMMAND ----------

# DBTITLE 1,Expr,Alias - SQL
# MAGIC %sql
# MAGIC select name,concat(city,'_',country) as location from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Add New Column - PySpark
df2=df.withColumn("location",expr("concat(city,'_',country)"))
display(df2)

# COMMAND ----------

# DBTITLE 1,Add new Column - SQL
# MAGIC %sql
# MAGIC select *,concat(city,'_',country) as location from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Constant Value - PySaprk
from pyspark.sql.functions import lit
df2=df.withColumn("one",lit(1))
display(df2)

# COMMAND ----------

# DBTITLE 1,Constant - SQL
# MAGIC %sql
# MAGIC select *,1 as one from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Drop Column - PySpark
df2=df.drop("country")
display(df2)

# COMMAND ----------

# DBTITLE 1,Drop Column - SQL
# MAGIC %sql
# MAGIC select * except(country)  from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Cast - PySpark
from pyspark.sql.functions import col
df2=df.withColumn("supplier_id_double", col("supplierID").cast("double"))
display(df2)

# COMMAND ----------

# DBTITLE 1,Cast - SQL
# MAGIC %sql
# MAGIC select *,cast(supplierID as double) as supplier_id_double  from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Filter - PySpark
df2=df.filter(col("country")=='US')
# df2=df.where("country =='US'")
display(df2)

# COMMAND ----------

# DBTITLE 1,Filter - SQL
# MAGIC %sql
# MAGIC select * from samples.bakehouse.sales_franchises where country='US'

# COMMAND ----------

# DBTITLE 1,Distinct - PySpark
df2=df.distinct()
# df2=df.select("country").distinct()
# df2=df.select("country","city").distinct()
display(df2)

# COMMAND ----------

# DBTITLE 1,Distinct - SQL
# MAGIC %sql
# MAGIC -- select distinct * from samples.bakehouse.sales_franchises;
# MAGIC select distinct country from samples.bakehouse.sales_franchises

# COMMAND ----------

# DBTITLE 1,Union - PySpark
df2=df
display(df)

df3=df.union(df2)
display(df3)

# COMMAND ----------

# DBTITLE 1,UnionAll - PySpark
df3=df.unionAll(df2)
display(df3)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### `Union` vs. `UnionAll` in PySpark
# MAGIC
# MAGIC * **Identical Functionality in PySpark:** Unlike standard SQL (where `UNION` removes duplicates and `UNION ALL` retains duplicates), both `union()` and `unionAll()` in PySpark **preserve duplicate rows** without performing deduplication.
# MAGIC * **`unionAll()` is Deprecated:** `unionAll()` is an alias for `union()`. Starting from Spark 2.0+, `union()` is the standard recommended method, while `unionAll()` is kept solely for backward compatibility.
# MAGIC * **Resolution by Column Position (Not Name):** Both methods resolve schemas **by column position/index**, not by column name. If DataFrame A has columns `(id, name)` and DataFrame B has `(name, id)`, a regular union will mistakenly pair `id` with `name` unless the schemas are aligned beforehand.
# MAGIC * **Alternative for Name-Based Matching:** To merge DataFrames by column names (and handle mismatched schemas), use `unionByName()`, which also supports missing columns via the `allowMissingColumns=True` parameter.
# MAGIC * **Eliminating Duplicates:** To achieve standard SQL `UNION` behavior (deduplication), chain `.distinct()` or `.dropDuplicates()` after the union:
# MAGIC     * df_unique = df1.union(df2).distinct()

# COMMAND ----------

# DBTITLE 1,UnionByName - PySpark
df3=df.unionByName(df2)
display(df3)

# COMMAND ----------

# DBTITLE 1,Union - SQL
# MAGIC %sql
# MAGIC select * from samples.bakehouse.sales_franchises
# MAGIC -- union
# MAGIC union all
# MAGIC select * from samples.bakehouse.sales_franchises;

# COMMAND ----------

# DBTITLE 1,OrderBy - PySpark
from pyspark.sql.functions import desc
# df2=df.orderBy("country")
df2=df.orderBy(col("country").desc())
display(df2)

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### `orderBy()` vs. `sort()` in PySpark
# MAGIC
# MAGIC * **Identical Functionality:** `orderBy()` is an alias for `sort()`, provided to maintain consistency with standard SQL syntax; both produce the exact same execution plan.
# MAGIC * **Global Sorting (Wide Transformation):** Both methods perform a global sort across all partitions, requiring a full cluster shuffle via Range Partitioning.
# MAGIC * **Default Order:** Sorts in ascending order (`asc`) by default.
# MAGIC * **Default Null Ordering:** `NULL` values appear first in ascending order (`asc_nulls_first`) and last in descending order (`desc_nulls_last`).
# MAGIC * **Contrast with `sortWithinPartitions()`:** Unlike `orderBy`/`sort`, `sortWithinPartitions()` only sorts data locally inside each partition (narrow transformation), avoiding network shuffle while improving downstream Parquet/Delta compression and file skipping.
# MAGIC
# MAGIC ```python
# MAGIC from pyspark.sql.functions import col
# MAGIC
# MAGIC # Global sorting (identical)
# MAGIC df_sorted = df.orderBy(col("salary").desc())
# MAGIC df_sorted = df.sort(col("salary").desc())
# MAGIC
# MAGIC # Local partition sorting (no shuffle)
# MAGIC df_local = df.sortWithinPartitions("salary")
# MAGIC
# MAGIC ```

# COMMAND ----------

# DBTITLE 1,SQL
# MAGIC %sql
# MAGIC select * from samples.bakehouse.sales_franchises order by country
# MAGIC desc

# COMMAND ----------

# DBTITLE 1,Limit - PySpark
df2=df.limit(10)
display(df2)

# COMMAND ----------

# DBTITLE 1,Limit - SQL
# MAGIC %sql
# MAGIC select * from samples.bakehouse.sales_franchises limit 10

# COMMAND ----------

# DBTITLE 1,Limit & Offset - SQL
# MAGIC %sql
# MAGIC -- Skip the first 4 rows (OFFSET 4) and return the next 5 rows (LIMIT 5)
# MAGIC select * from samples.bakehouse.sales_franchises order by franchiseID limit 5 offset 4

# COMMAND ----------

# DBTITLE 1,Repartition and Coalesce
df2=df.repartition(2)
# df2=df.coalesce(2)
display(df2)

# COMMAND ----------

# DBTITLE 1,Check Number of Partitions in DataFrame RDD
df.rdd.getNumPartitions()

# COMMAND ----------

# DBTITLE 1,Collect
df.collect()

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC ### How to use intermediate df in sql query in pyspark
# MAGIC
# MAGIC To use an intermediate PySpark DataFrame inside a SQL query, you register it as a **temporary view** (or temporary table). Once registered, you can query it directly using `spark.sql()`.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Core Approaches
# MAGIC
# MAGIC ##### 1. Session-Scoped Temporary View (Most Common)
# MAGIC
# MAGIC Visible only within the current `SparkSession`. It is automatically dropped when the session terminates.
# MAGIC
# MAGIC ```python
# MAGIC # Intermediate DataFrame
# MAGIC df_filtered = df.filter(df.salary > 50000)
# MAGIC
# MAGIC # Register as a local temporary view
# MAGIC df_filtered.createOrReplaceTempView("temp_filtered_emp")
# MAGIC
# MAGIC # Use it directly in Spark SQL
# MAGIC df_result = spark.sql("""
# MAGIC     SELECT department_id, COUNT(*) as high_earners, AVG(salary) as avg_sal
# MAGIC     FROM temp_filtered_emp
# MAGIC     GROUP BY department_id
# MAGIC """)
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### 2. Global Temporary View (Cross-Session)
# MAGIC
# MAGIC Shared across multiple Spark sessions on the same cluster. It lives under the dedicated system database `global_temp`.
# MAGIC
# MAGIC ```python
# MAGIC
# MAGIC # Register as a global view
# MAGIC df_filtered.createOrReplaceGlobalTempView("global_emp_view")
# MAGIC
# MAGIC # Query with the `global_temp` qualifier
# MAGIC df_global_result = spark.sql("""
# MAGIC     SELECT * 
# MAGIC     FROM global_temp.global_emp_view
# MAGIC     WHERE age > 30
# MAGIC """)
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### Comparison of Methods
# MAGIC
# MAGIC | Method | Scope | Lifetime | SQL Access Syntax |
# MAGIC | --- | --- | --- | --- |
# MAGIC | `createOrReplaceTempView()` | Local `SparkSession` | Current Session | `FROM view_name` |
# MAGIC | `createTempView()` | Local `SparkSession` | Current Session (Throws error if name exists) | `FROM view_name` |
# MAGIC | `createOrReplaceGlobalTempView()` | Entire Spark Application | Cluster / App Lifetime | `FROM global_temp.view_name` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Interview & Production Tips
# MAGIC
# MAGIC * **Lazy Evaluation:** Registering a DataFrame as a temporary view does **not** trigger an action or cache the data in memory. Spark evaluates it lazily when the SQL query executes.
# MAGIC * **Avoid Hard Table Writes:** Use temp views for pipeline staging rather than writing intermediate DataFrames back to storage (ADLS/Delta), avoiding unnecessary disk I/O.
# MAGIC * **Dropping Views:** You can explicitly drop temporary views when done to clean the catalog:
# MAGIC     * spark.catalog.dropTempView("temp_filtered_emp")
# MAGIC     * spark.catalog.dropGlobalTempView("global_emp_view")

# COMMAND ----------

# DBTITLE 1,Create TempView (Dataframe To SQL)
# Create a temporary view with the first 5 rows
# Use temp views to query DataFrames with SQL - they're session-scoped and auto-cleaned on session end
df.limit(5).createOrReplaceTempView("myview")

# COMMAND ----------

# DBTITLE 1,Using TempView
# MAGIC %sql
# MAGIC select * from myview

# COMMAND ----------

# DBTITLE 1,SQL to Dataframe
df2=spark.sql("select * from myview limit 2")
display(df2)
