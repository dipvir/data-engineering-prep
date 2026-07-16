# Databricks notebook source
# MAGIC %md
# MAGIC In Databricks, **`%fs ls`** is a file system command line shortcut used to **list the contents of a directory** inside your linked cloud storage.
# MAGIC
# MAGIC It is the Databricks notebook equivalent of running `ls` in a Linux terminal or `dir` in Windows Command Prompt.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔍 Breaking Down the Syntax
# MAGIC
# MAGIC * **`%fs`**: This is a Databricks **magic command**. It tells the notebook cell: *"Hey, don't execute this as Python or SQL. Execute this directly using the Databricks File System (DBFS) utility layer."*
# MAGIC * **`ls`**: Short for "list".
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ Real-World Code Examples
# MAGIC
# MAGIC #### **1. List the root DBFS directory**
# MAGIC
# MAGIC If you want to see the default system folders inside your workspace:
# MAGIC
# MAGIC ```bash
# MAGIC %fs ls /
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC #### **2. Inspect your custom Azure Data Lake (ADLS Gen2) folder**
# MAGIC
# MAGIC Since you are mapping your own external containers for the course, you can use it to verify if your Parquet or Delta files actually landed on Azure:
# MAGIC
# MAGIC ```bash
# MAGIC %fs ls abfss://lab-data@delta0lake0lab0storageac.dfs.core.windows.net/invoices/
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 What does the output look like?
# MAGIC
# MAGIC When you run `%fs ls`, Databricks returns a clean, scannable table with three structural columns:
# MAGIC
# MAGIC | path | name | size |
# MAGIC | --- | --- | --- |
# MAGIC | `dbfs:/invoices/invoices_1_100.parquet` | `invoices_1_100.parquet` | `59214` *(in bytes)* |
# MAGIC | `dbfs:/invoices/_delta_log/` | `_delta_log/` | `0` *(directories show as 0)* |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Programmatic Alternative (Python/PySpark)
# MAGIC
# MAGIC If you ever need to capture the file list inside a Python loop or store it in a variable (which magic commands cannot do), you drop the `%fs ls` shortcut and use the native production-grade **`dbutils`** package instead:
# MAGIC
# MAGIC ```python
# MAGIC # This does the exact same thing under the hood as %fs ls
# MAGIC files = dbutils.fs.ls("dbfs:/invoices/")
# MAGIC display(files)
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC You will see Afaque use `%fs ls` constantly throughout the course videos just to quickly check if a transaction created a new `.json` log or a fresh `.parquet` file back in your storage container!

# COMMAND ----------

# DBTITLE 1,List The Contents Of Root DBFS Directory
# MAGIC %fs ls /

# COMMAND ----------

# DBTITLE 1,List The Contents Of ADLS Container/Directory
# MAGIC %fs ls abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/

# COMMAND ----------

# DBTITLE 1,List The Contents By Programmatic Alternative
files = dbutils.fs.ls("/")
display(files)
# Sample Parquet files used in this lab are stored in this location.
files = dbutils.fs.ls("abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/")
display(files)

# COMMAND ----------

# DBTITLE 1,DDL Command :- Registering External Location And Creating Catalog, Schema
# MAGIC %sql
# MAGIC -- 1. registering an External Location and Catalog in Unity Catalog.
# MAGIC -- (Note: Use the exact name of the Storage Credential you created earlier)
# MAGIC CREATE EXTERNAL LOCATION IF NOT EXISTS delta_lake_lab_adlsg2_ext_location_delta URL
# MAGIC 'abfss://dbr-managed-tables-container@delta0lake0lab0storageac.dfs.core.windows.net/'
# MAGIC WITH (STORAGE CREDENTIAL `delta0lake0lab0storageac_adls_sa_el_azuremanagedidentity_1783847538585`);
# MAGIC
# MAGIC -- 2. Create the catalog pointing to your custom external location
# MAGIC CREATE CATALOG IF NOT EXISTS delta_catalog
# MAGIC MANAGED LOCATION 'abfss://dbr-managed-tables-container@delta0lake0lab0storageac.dfs.core.windows.net/';
# MAGIC
# MAGIC -- 3. Create your schema
# MAGIC CREATE SCHEMA IF NOT EXISTS delta_catalog.delta_db;

# COMMAND ----------

# DBTITLE 1,Querying The Sample Parquet Files
# MAGIC %sql
# MAGIC -- Below path is also registered as an External Location in Unity Catalog, thats why its accessible.
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC LIMIT 5;

# COMMAND ----------

# DBTITLE 1,DDL Command :- Creating MANAGED Delta Table From Sample Parquet File
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices AS --(CTAS)
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_101_200.parquet`;

# COMMAND ----------

# DBTITLE 1,Metadata Of Delta Table
# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,Querying The Created MANAGED Delta Table
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,DDL Command :- To Rename And Drop Table
# MAGIC %sql
# MAGIC -- ALTER TABLE delta_catalog.delta_db.invoices_101_200
# MAGIC -- RENAME TO delta_catalog.delta_db.invoices;
# MAGIC
# MAGIC -- DROP TABLE delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,DML Command :- Appending Data In Delta Table
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices
# MAGIC   SELECT
# MAGIC     *
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

# COMMAND ----------

# DBTITLE 1,Sanity Check
# MAGIC %sql
# MAGIC SELECT * FROM delta_catalog.delta_db.invoices; 

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,Sanity Check
# MAGIC %sql
# MAGIC SELECT
# MAGIC   MIN(customer_id) AS min_value,
# MAGIC   MAX(customer_id) AS max_value,
# MAGIC   COUNT(*) AS total_rows
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices

# COMMAND ----------

# DBTITLE 1,Querying Delta Table
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices
# MAGIC WHERE
# MAGIC   customer_id = 1;

# COMMAND ----------

# DBTITLE 1,DML Command :- Updating The Record
# MAGIC %sql
# MAGIC UPDATE
# MAGIC   delta_catalog.delta_db.invoices
# MAGIC SET
# MAGIC   quantity = 10
# MAGIC WHERE
# MAGIC   customer_id = 1;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,Querying Delta Table
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices
# MAGIC WHERE
# MAGIC   customer_id = 99;

# COMMAND ----------

# DBTITLE 1,DML Command :- Deleting The Record
# MAGIC %sql
# MAGIC DELETE FROM
# MAGIC   delta_catalog.delta_db.invoices
# MAGIC WHERE
# MAGIC   customer_id = 99;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,DML Command :- Appending More Data In Delta Table
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices
# MAGIC   SELECT
# MAGIC     *
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_201_99457.parquet`

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices;

# COMMAND ----------

# DBTITLE 1,Sanity Check
# MAGIC %sql
# MAGIC SELECT
# MAGIC   count(*) as total_rows
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices;

# COMMAND ----------

# display(_sqldf)
