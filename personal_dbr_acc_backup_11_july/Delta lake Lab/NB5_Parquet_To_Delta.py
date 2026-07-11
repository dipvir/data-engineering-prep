# Databricks notebook source
# DBTITLE 1,Listing Sample Parquet Files From ADLS
# MAGIC %fs ls abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/

# COMMAND ----------

# DBTITLE 1,Creating A Copy Of Parquet Files For Delta Conversion
# Reading/loading the parquet file 
df_invoices_101_200 = spark.read.parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet")

# Creating two copies of the parquet file in two different folders.
df_invoices_101_200.write.mode("overwrite").parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_101_200_v1")
df_invoices_101_200.write.mode("overwrite").parquet("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_101_200_v2")

# COMMAND ----------

# DBTITLE 1,Converting V1 Copy To Delta Using SQL
# MAGIC %sql
# MAGIC CONVERT TO DELTA
# MAGIC PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_101_200_v1`

# COMMAND ----------

# DBTITLE 1,Converting V2 To Delta Using Python
from delta.tables import DeltaTable

DeltaTable.convertToDelta(
    spark,
    "PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_101_200_v2`"
)

# COMMAND ----------

# DBTITLE 1,Reading Delta File From ADLS
# Reading/loading converted parquet to delta file 
df_invoices_101_200 = spark.read.format("delta").load("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_101_200_v1")
display(df_invoices_101_200)

# COMMAND ----------

# DBTITLE 1,Checking History Of Delta File In ADLS
delta_table = DeltaTable.forPath(spark, "abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_101_200_v1")
display(delta_table.history())

# COMMAND ----------

# DBTITLE 1,Converting CSV To Delta
# Reading/loading the source csv file 
df_Gold_reserves_tonnes = spark.read.option("header", "true").option("inferSchema", "true").csv("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/Gold_reserves_tonnes.csv")
# Correcting the column name for delta table compatibility
df_Gold_reserves_tonnes = df_Gold_reserves_tonnes.withColumnRenamed("Average gold reserves", "Average_gold_reserves")
display(df_Gold_reserves_tonnes)

# Converting csv file to delta file
df_Gold_reserves_tonnes.write.mode("overwrite").format("delta").save("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/Gold_reserves_tonnes_delta")

# COMMAND ----------

# DBTITLE 1,Reading Delta File From ADLS
# Reading/loading converted csv to delta file 
df_Gold_reserves_tonnes = spark.read.format("delta").load("abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/Gold_reserves_tonnes_delta")
display(df_Gold_reserves_tonnes)

# COMMAND ----------

# DBTITLE 1,Creating EXTERNAL Delta Table
# MAGIC %sql
# MAGIC -- Till now whatever delta tables we have created in prevous notebooks were managed tables.
# MAGIC -- Now we will create an external table in delta format.
# MAGIC
# MAGIC CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_ext
# MAGIC   USING DELTA
# MAGIC   LOCATION 'abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices_ext' AS
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`

# COMMAND ----------

# DBTITLE 1,Sanity Check
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_ext;
# MAGIC
# MAGIC DESCRIBE EXTENDED delta_catalog.delta_db.invoices_ext;
