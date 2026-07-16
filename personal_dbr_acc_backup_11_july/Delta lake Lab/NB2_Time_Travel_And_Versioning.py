# Databricks notebook source
# MAGIC %md
# MAGIC ###Using SQL To Work With Delta Table.

# COMMAND ----------

# DBTITLE 1,DDL Command :- Creating A Delta Table From Parquet File Stored In ADLSG2
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_ttv AS --(CTAS)
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

# COMMAND ----------

# DBTITLE 1,Querying The Delta Table
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Performing Delete,Update,Write operation to have some history in delta table for this TTV lab

# COMMAND ----------

# DBTITLE 1,DML Command :- Deleting A Record Of Delta Table
# MAGIC %sql
# MAGIC DELETE FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv
# MAGIC WHERE
# MAGIC   customer_id = 1;

# COMMAND ----------

# DBTITLE 1,DML Command :- Updating A Record Of Delta Table
# MAGIC %sql
# MAGIC UPDATE
# MAGIC   delta_catalog.delta_db.invoices_ttv
# MAGIC SET
# MAGIC   quantity = 25
# MAGIC WHERE
# MAGIC   customer_id = 2;

# COMMAND ----------

# DBTITLE 1,DML Command :- Appending/Inserting More Data From Another Parquet File In Delta Table
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_ttv
# MAGIC   SELECT
# MAGIC     *
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_101_200.parquet`;

# COMMAND ----------

# DBTITLE 1,Verifying The Changes Done
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_ttv;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Time Travel

# COMMAND ----------

# DBTITLE 1,Querying On Latest Version Of Delta Table
# MAGIC %sql
# MAGIC -- Latest Version
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv
# MAGIC WHERE
# MAGIC   customer_id IN (1,2);
# MAGIC -- Note :- customer_id 1 is deleted, customer_id 2 is updated Above.

# COMMAND ----------

# DBTITLE 1,Querying On Older Version Of Delta Table Using "VERSION AS OF"
# MAGIC %sql
# MAGIC -- Time Travel
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv VERSION AS OF 0
# MAGIC WHERE
# MAGIC   customer_id IN (1,2);

# COMMAND ----------

# DBTITLE 1,Querying An Older Version Of Delta Table Using "TIMESTAMP AS OF"
# MAGIC %sql
# MAGIC --(0th version)
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv TIMESTAMP AS OF '2026-07-16T11:10:03.000+00:00'
# MAGIC WHERE
# MAGIC   customer_id IN (1, 2);
# MAGIC
# MAGIC -- Note :- If provided timestamp is not the one given in the history but lies between the timestamp of first and last versions, then it will return the previous version of the table from the given timestamp. else it will throw the error.
# MAGIC
# MAGIC -- So below i provided timestamp which is not in the history but lies between the timestamp of first and last versions.
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv TIMESTAMP AS OF '2026-07-16T11:10:05.000+00:00'
# MAGIC WHERE
# MAGIC   customer_id IN (1, 2);

# COMMAND ----------

# DBTITLE 1,DML Command :- To Restore/Go Back To Any Previous Version OF Delta Table
# MAGIC %sql
# MAGIC RESTORE TABLE delta_catalog.delta_db.invoices_ttv TO VERSION AS OF 0;
# MAGIC
# MAGIC -- OR alternatively using timestamp
# MAGIC -- RESTORE TABLE delta_catalog.delta_db.invoices_ttv TO TIMESTAMP AS OF '2026-07-16T11:11:15.000+00:00';

# COMMAND ----------

# DBTITLE 1,Verifying After Reverting To Older Version
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ttv
# MAGIC WHERE
# MAGIC   customer_id IN (1,2);
# MAGIC
# MAGIC -- Note :- As expected, the result has customer_id = 1 present, customer_id 2 with not update as we have reverted to 0th version.

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_ttv
# MAGIC -- operationMetrics shows the number of files removed and restored and more.
# MAGIC -- operationParameters shows the version restored.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Note :- We have reverted delta table to 0st version Above. 

# COMMAND ----------

# MAGIC %md
# MAGIC ###Using Python To Work With Delta Table.

# COMMAND ----------

# DBTITLE 1,Imports
import pyspark.sql.functions as f

# COMMAND ----------

# DBTITLE 1,Querying Different Version Of Delta Table Using "versionAsOf"
# Version 2 will have delete and update changes.
df = spark.read.option("versionAsOf", "2").table("delta_catalog.delta_db.invoices_ttv")
display(df.filter(f.col("customer_id").isin(1,2) ))
print("No. of row",df.count())

# Version 1 will have only the deleted changes.
df = spark.read.option("versionAsOf", "1").table("delta_catalog.delta_db.invoices_ttv")
display(df.filter(f.col("customer_id").isin(1,2) ))
print("No. of row",df.count())

# Latest version is reverted to version 0th in above some cell.
df = spark.read.table("delta_catalog.delta_db.invoices_ttv")
display(df.filter(f.col("customer_id").isin(1,2) ))
print("No. of row",df.count())

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_ttv;

# COMMAND ----------

# DBTITLE 1,Querying Different Version Of Delta Table Using "timestampAsOf"
# Timestamp for V2 is 2026-07-16T11:12:15.000+00:00
# Version 2 will have delete and update changes.
df = spark.read.option("timestampAsOf", "2026-07-16T11:12:15.000+00:00").table("delta_catalog.delta_db.invoices_ttv")
display(df.filter(f.col("customer_id").isin(1,2) ))
print("No. of row",df.count())

# Timestamp for V1 is 2026-07-16T11:11:15.000+00:00
# Version 1 will have only the deleted changes.
df = spark.read.option("timestampAsOf", "2026-07-16T11:11:15.000+00:00").table("delta_catalog.delta_db.invoices_ttv")
display(df.filter(f.col("customer_id").isin(1,2) ))
print("No. of row",df.count())

# Setting incorect timestamp btw V3 and V4, V3 will be returned. 
df = spark.read.option("timestampAsOf", "2026-07-16T11:20:22.000+00:00").table("delta_catalog.delta_db.invoices_ttv")
display(df.filter(f.col("customer_id").isin(1,2) ))
print("No. of row",df.count())
