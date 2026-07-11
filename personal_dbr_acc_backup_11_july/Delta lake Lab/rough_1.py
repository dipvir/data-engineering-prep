# Databricks notebook source
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

# COMMAND ----------

# DBTITLE 1,Cell 2
# MAGIC %sql
# MAGIC -- UC-managed tables block direct dbutils.fs.ls() on __unitystorage paths.
# MAGIC -- Use _metadata.file_path to list physical files for the partition instead.
# MAGIC SELECT count(DISTINCT _metadata.file_path) AS file_count
# MAGIC FROM delta_catalog.delta_db.invoices
# MAGIC -- WHERE category = 'detergents'

# COMMAND ----------

spark.sql("""
    ALTER TABLE delta_catalog.delta_db.optimize_ex1
    SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = '7 days')
""")

# COMMAND ----------

display(spark.sql("""
        SELECT
        DISTINCT category
        FROM
        delta_catalog.delta_db.optimize_ex3
        """))

display(spark.sql("""
        SELECT
        DISTINCT category
        FROM
        delta_catalog.delta_db.optimize_ex3 VERSION AS OF 0
        """))
display(spark.sql("""
        SELECT
        DISTINCT category
        FROM
        delta_catalog.delta_db.optimize_ex1
        """))

display(spark.sql("""
        SELECT
        DISTINCT category
        FROM
        delta_catalog.delta_db.optimize_ex1 VERSION AS OF 0
        """))
           
