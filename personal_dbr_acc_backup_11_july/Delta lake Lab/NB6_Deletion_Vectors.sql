-- Databricks notebook source
-- DBTITLE 1,Data We Are Consuming In This Lab/Notebook
SELECT
  *
FROM
  PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
LIMIT 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### COPY-ON-WRITE(COW) (i.e 'delta.enableDeletionVectors' = false)

-- COMMAND ----------

-- DBTITLE 1,Creating Delta Table With Disabled Deletion Vectors
CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_cow
  TBLPROPERTIES ('delta.enableDeletionVectors' = false) AS
SELECT
  *
FROM
  PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

-- COMMAND ----------

-- DBTITLE 1,Verifying Deletion Vector Is Disabled
DESCRIBE EXTENDED delta_catalog.delta_db.invoices_cow;

-- COMMAND ----------

-- DBTITLE 1,Drop Table
-- DROP TABLE delta_catalog.delta_db.invoices_cow;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC **This is the state of invoices_cow data files in ADLS**
-- MAGIC
-- MAGIC ![image_1781958735638.png](NB6_images/image_1781958735638.png "image_1781958735638.png")

-- COMMAND ----------

-- DBTITLE 1,Updating A Record To Verify Operation BTS With COW
UPDATE
  delta_catalog.delta_db.invoices_cow
SET
  age = 50
WHERE
  customer_id = 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_cow data files in ADLS (After Update Operation With Copy-On-Write)**
-- MAGIC
-- MAGIC ![image_1781958952847.png](NB6_images/image_1781958952847.png "image_1781958952847.png")

-- COMMAND ----------

-- DBTITLE 1,Deleting A Record To Verify Operation BTS With COW
DELETE FROM
  delta_catalog.delta_db.invoices_cow
WHERE
  customer_id = 6;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_cow data files in ADLS (After Delete Operation With Copy-On-Write)**
-- MAGIC
-- MAGIC ![image_1781959519569.png](NB6_images/image_1781959519569.png "image_1781959519569.png")

-- COMMAND ----------

-- DBTITLE 1,DESCRIBE HISTORY invoices_cow
DESCRIBE HISTORY delta_catalog.delta_db.invoices_cow;

-- Conclusion On What Happened BTS With Copy-On-Write
-- So to get idea we can check operationMetrics column from History.

-- Update and Delete
-- So, In Copy-on-write(i.e 'delta.enableDeletionVectors' = false) 
-- what happens after an update and delete operations is that, it reads, applies changes and rewrites whole new parquet file again with updated/deleted changes in both cases(i.e new file after update and new file after delete thats because parquet file is immutable).

-- COMMAND ----------

-- DBTITLE 1,Sanity Check
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_cow;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### MERGE-ON-READ(MOR) (i.e 'delta.enableDeletionVectors' = true)

-- COMMAND ----------

-- DBTITLE 1,Creating Delta Table With Enabled Deletion Vectors
CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_mor
  TBLPROPERTIES ('delta.enableDeletionVectors' = true) AS
SELECT
  *
FROM
  PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

-- COMMAND ----------

-- DBTITLE 1,Verifying Deletion Vector Is Enabled
DESCRIBE EXTENDED delta_catalog.delta_db.invoices_mor;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_mor data files in ADLS**
-- MAGIC
-- MAGIC ![image_1781960360869.png](NB6_images/image_1781960360869.png "image_1781960360869.png")

-- COMMAND ----------

-- DBTITLE 1,Updating A Record To Verify Operation BTS With MOR
UPDATE
  delta_catalog.delta_db.invoices_mor
SET
  age = 50
WHERE
  customer_id = 5;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_mor data files in ADLS (After Update Operation With Merge-On-Read)**
-- MAGIC
-- MAGIC ![image_1781960533511.png](NB6_images/image_1781960533511.png "image_1781960533511.png")

-- COMMAND ----------

-- DBTITLE 1,DESCRIBE HISTORY invoices_mor
DESCRIBE HISTORY delta_catalog.delta_db.invoices_mor;

-- Conclusion On What Happened BTS With Merge-On-Read
-- So to get idea we can check operationMetrics column from History.
-- So, In Merge-on-read(i.e 'delta.enableDeletionVectors' = true) 

-- Update
-- What happens after an update operations is that, it add tiny new parquet file with only updated records in it + add a deletion vector file(which contains details to skip reading updated records from old/main parquet file).

-- COMMAND ----------

-- DBTITLE 1,Deleting A Record To Verify Operation BTS With MOR
DELETE FROM
  delta_catalog.delta_db.invoices_mor
WHERE
  customer_id = 6;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_mor data files in ADLS (After Delete Operation With Merge-On-Read)**
-- MAGIC
-- MAGIC ![image_1781961601793.png](NB6_images/image_1781961601793.png "image_1781961601793.png")

-- COMMAND ----------

-- DBTITLE 1,DESCRIBE HISTORY invoices_mor
DESCRIBE HISTORY delta_catalog.delta_db.invoices_mor;

-- Conclusion On What Happened BTS With Merge-On-Read

-- Delete
-- What happens after an delete operations is that, it just adds deletion vector file(which contains details to skip reading deleted records from old/main parquet file).

-- COMMAND ----------

-- DBTITLE 1,Sanity Check
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_mor;

-- Note :- updated record is at the bottom of the file.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### How TO Clear The Mutiple Small Deletion Vector/Parquet Files Created With MERGE-ON-READ

-- COMMAND ----------

-- MAGIC %md
-- MAGIC - In the last image above we can see there are 2 deletion Vector and 2 parquet files present.
-- MAGIC - So, after OPTIMIZE all that upadate/delete operation will be applied and a single updated parquet file will be added.

-- COMMAND ----------

-- DBTITLE 1,DESCRIBE HISTORY invoices_mor
DESCRIBE HISTORY delta_catalog.delta_db.invoices_mor;

-- COMMAND ----------

-- DBTITLE 1,OPTIMIZE Command
OPTIMIZE delta_catalog.delta_db.invoices_mor;

-- COMMAND ----------

-- DBTITLE 1,DESCRIBE HISTORY invoices_mor
DESCRIBE HISTORY delta_catalog.delta_db.invoices_mor;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_mor data files in ADLS (After OPTIMIZE Operation)**
-- MAGIC - So, **OPTIMIZE** added one new consolidated parquet file, But it doesnt clear the old file because of time travel.
-- MAGIC - To clear/remove old files manually we have to use **VACUUM** Command explicitly.
-- MAGIC
-- MAGIC ![image_1781963610365.png](NB6_images/image_1781963610365.png "image_1781963610365.png")

-- COMMAND ----------

-- DBTITLE 1,Set Zero Retention and Vacuum Delta Table invoices_mor

-- SET 'spark.databricks.delta.retentionDurationCheck.enabled' = 'false' (Need User-managed cluster)

-- STEP 1: Set the physical retention duration property natively on the table level (Serverless option)
ALTER TABLE delta_catalog.delta_db.invoices_mor 
SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours');

-- STEP 2: Run VACUUM without the "RETAIN" clause 
-- (It will automatically read the 0 hours property we just set above)
VACUUM delta_catalog.delta_db.invoices_mor;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_mor data files in ADLS (After VACUUM Operation)**
-- MAGIC - Now, Vacuum cleared the old files, but also we can do time travel anymore.
-- MAGIC
-- MAGIC ![image_1781964949996.png](NB6_images/image_1781964949996.png "image_1781964949996.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Final Conclusion
-- MAGIC
-- MAGIC The conclusion is neither *Copy on Write* (COW) nor *Merge on Read* (MOR) is a universal solution; the choice depends on your specific workload:
-- MAGIC
-- MAGIC *   **Copy on Write (COW)**: Best suited for **read-heavy** workloads with infrequent(low) updates. Because it rewrites the entire file during changes, it is less efficient for high-frequency writes.
-- MAGIC *   **Merge on Read (MOR)**: Ideal for scenarios with **frequent updates**. By recording changes in a *deletion vector* file rather than rewriting the full data file, it significantly reduces write latency.
-- MAGIC
-- MAGIC In short, use **COW** when you want fast reads and have stable data, and **MOR** when your primary bottleneck is write performance.

-- COMMAND ----------

-- DBTITLE 1,DESCRIBE HISTORY invoices_mor
DESCRIBE HISTORY delta_catalog.delta_db.invoices_mor;
