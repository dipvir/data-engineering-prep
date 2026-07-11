-- Databricks notebook source
-- MAGIC %md
-- MAGIC ### Creating Reference Delta Table (To Be Used For This Lab)
-- MAGIC
-- MAGIC - **invoices_tbl_clone_reference** will be used as a reference table for the following exercises
-- MAGIC - For that first we are creating invoices_tbl_clone_reference and performing some operations over it to have some versions/history.

-- COMMAND ----------

-- DBTITLE 1,Creating Delta Table To Use In Cloning Reference
-- This is not a clone table, it will be used to create clone tables in this lab.

CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_tbl_clone_reference AS
SELECT
  *
FROM
  PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

-- COMMAND ----------

-- DBTITLE 1,Sanity Check
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference
LIMIT 5;

-- COMMAND ----------

-- DBTITLE 1,Delta Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- DBTITLE 1,Delete, Update, Insert On invoices_clone_reference
-- Delete
DELETE FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference
WHERE
  customer_id = 4;

-- Update
UPDATE
  delta_catalog.delta_db.invoices_tbl_clone_reference
SET
  quantity = 1000
WHERE
  customer_id = 5;

-- Insert
INSERT INTO delta_catalog.delta_db.invoices_tbl_clone_reference
VALUES (101, '1000', 'Female', 20, 'Category 1', 1000, 1000, 'Credit Card', '2022-01-01', 'Mall 1', null);

-- COMMAND ----------

-- DBTITLE 1,Delta Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;
-- DROP TABLE delta_catalog.delta_db.invoices_shallow_clone_v0_tbl;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Shallow Clone

-- COMMAND ----------

-- DBTITLE 1,Creating Shallow Clone Table
CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_tbl_shallow_clone SHALLOW CLONE delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- DBTITLE 1,Checking Shallow Clone Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_shallow_clone;

-- operationParameters column in history gives imp metadata.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Updating customer_id = 10 from reference table to verify that the changes occurs in shallow clone table as well or not.

-- COMMAND ----------

-- DBTITLE 1,Updating Reference Table
UPDATE
  delta_catalog.delta_db.invoices_tbl_clone_reference
SET
  quantity = 2000
WHERE
  customer_id = 10;

-- COMMAND ----------

-- DBTITLE 1,Checking Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- So update is reflected in the history of reference table.

-- COMMAND ----------

-- DBTITLE 1,Verifying Reference Table
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference
WHERE
  customer_id = 10;

-- Record is updated in Reference table.

-- COMMAND ----------

-- DBTITLE 1,Checking Shallow Clone Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_shallow_clone;

-- So, Update customer_id = 10 is not there in shallow clone table history.
-- Reason is changes made to reference table does'nt effect shallow clone table eventhough it refereces it.
-- Once shallow clone table is created, it will maintain its own history.

-- COMMAND ----------

-- DBTITLE 1,Verifying Shallow Clone Table
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone
WHERE
  customer_id = 10;

-- So, changes made to reference table has'nt effected shallow clone table.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Conclusion On Shallow Clone**
-- MAGIC
-- MAGIC - **Independence:** Even though a shallow clone(here `invoices_tbl_shallow_clone`) references the source table's(here `invoices_tbl_clone_reference`) underlying data files, But after cloning it maintains its own distinct history and set of operations.
-- MAGIC - **No Cross-Effect:** Any subsequent modifications, updates, or deletions performed on the source table will not affect the shallow clone table and **vice versa**.
-- MAGIC - **Encapsulation:** Once the clone is created, it functions as an independent entity with its own lifecycle, separate from the source table's ongoing activity.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_tbl_shallow_clone data files in ADLS**
-- MAGIC - As we havnt made any operation over it yet so there is no parquet files because it reference to source table parquet files.
-- MAGIC - Now, after cloning whatever operation we perform on shallow clone table will create its own logs and data files.
-- MAGIC
-- MAGIC ![image_1782051776230.png](NB7_images/image_1782051776230.png "image_1782051776230.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Deleting customer_id = 99 from shallow clone table to verify that the changes occurs in reference table.

-- COMMAND ----------

-- DBTITLE 1,Deleting A Record From Shallow Clone Table
DELETE FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone
WHERE
  customer_id = 99;

-- COMMAND ----------

-- DBTITLE 1,Verifying Shallow Clone Table
SELECT * FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone
WHERE
  customer_id = 99;

-- returns nothing, record is deleted from shallow clone table.

-- COMMAND ----------

-- DBTITLE 1,Checking Shallow Clone Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_shallow_clone;

-- New version history is also there for delete operation.

-- COMMAND ----------

-- DBTITLE 1,Verifying Reference Table
SELECT * FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference
WHERE
  customer_id = 99;

-- As expected, Record is present in reference table.

-- COMMAND ----------

-- DBTITLE 1,Checking Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- As expected, there is no delete history created in reference table.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_tbl_shallow_clone data files in ADLS (After Delete Operation)**
-- MAGIC - There is only a deletion vector added and no parquet because delete operation doesnt generate any.
-- MAGIC - If it be would insert/update operation then there would be parquet file added. 
-- MAGIC
-- MAGIC ![image_1782051863219.png](NB7_images/image_1782051863219.png "image_1782051863219.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Shallow Clone From Older Version Of Source/Reference Table

-- COMMAND ----------

-- DBTITLE 1,Creating Shallow Clone Table From Older Reference Table Version
CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_tbl_shallow_clone_v0 SHALLOW CLONE delta_catalog.delta_db.invoices_tbl_clone_reference VERSION AS OF 0;

-- alternatively
-- CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_tbl_shallow_clone_v0 SHALLOW CLONE delta_catalog.delta_db.invoices_tbl_clone_reference TIMESTAMP AS OF '2026-06-20T16:48:09.000+00:00';

-- COMMAND ----------

-- DBTITLE 1,Verifying Shallow Clone Table
-- getting the data from latest version of invoices_tbl_shallow_clone_v0 table which is cloned from 0th version of reference table(which wont have any operations).

SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone_v0
WHERE 
    customer_id in (4, 5, 10, 101);

-- COMMAND ----------

-- DBTITLE 1,Querying Latest Version Of Reference Table
-- getting the data from latest version of reference table for customer_id's we made changes on.

SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference -- (latest version)
WHERE 
    customer_id in (4, 5, 10, 101);

-- The Records will not match with invoices_tbl_shallow_clone_v0(i.e 0th version of reference tbl) as we had multiple changes on reference table 

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Time Travel On Shallow Clone

-- COMMAND ----------

-- DBTITLE 1,Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- DBTITLE 1,Creating New Shallow Clone Table
CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_tbl_shallow_clone_tt SHALLOW CLONE
delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- DBTITLE 1,Shallow Clone Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_shallow_clone_tt;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Note :-**
-- MAGIC - As seen above after creating shallow clone it create its own history and doesnt inherit source/reference table history.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Vacuum Behaviour On Source/Reference Table

-- COMMAND ----------

-- DBTITLE 1,Checking Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This are the list of operation we performed on source/reference(invoices_tbl_clone_reference) table so far**
-- MAGIC
-- MAGIC | version	| peration                          |
-- MAGIC | --- | --- |
-- MAGIC | 4	        | UPDATE                            |
-- MAGIC | 3	        | WRITE                             |
-- MAGIC | 2	        | UPDATE                            |
-- MAGIC | 1	        | DELETE                            |
-- MAGIC | 0	        | CREATE OR REPLACE TABLE AS SELECT |
-- MAGIC
-- MAGIC **And this is the ADLS Location of invoices_tbl_clone_reference table containing multiple data files as per above operations**
-- MAGIC
-- MAGIC ![image_1782110315931.png](NB7_images/image_1782110315931.png "image_1782110315931.png")
-- MAGIC
-- MAGIC - Now in v3 insert/write operation we appended just one row with customer_id = 101, which added one parquet file.
-- MAGIC - To demonstrate Vacuum behaviour on source/reference table will delete this record to see if that file gets deleted or not.

-- COMMAND ----------

-- DBTITLE 1,Deleting A Row From Reference Table
-- Delete
DELETE FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference
WHERE
  customer_id = 101;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **After delete just one deletion_vector is added(last one) as usual**
-- MAGIC
-- MAGIC ![image_1782110566477.png](NB7_images/image_1782110566477.png "image_1782110566477.png")

-- COMMAND ----------

-- DBTITLE 1,Verifying Reference Table
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_clone_reference
WHERE
  customer_id = 101;

-- So record with customer_id = 101 is deleted from invoices_tbl_clone_reference.

-- COMMAND ----------

-- DBTITLE 1,Running Vacuum On Reference Table
-- This Code was runing(with serverless) but Vacuum was'nt deleting the unused files from the adls as expected.

-- STEP 1: Set the physical retention duration property natively on the table level (Serverless option)
ALTER TABLE delta_catalog.delta_db.invoices_tbl_clone_reference 
SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours');

-- STEP 2: Run VACUUM without the "RETAIN" clause 
-- (It will automatically read the 0 hours property we just set above)
VACUUM delta_catalog.delta_db.invoices_tbl_clone_reference;

-- So, used global setting with user managed cluster
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
VACUUM delta_catalog.delta_db.invoices_tbl_clone_reference RETAIN 0 HOURS;

-- COMMAND ----------

-- DBTITLE 1,Checking Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **After Vacuum the parquet file(part-00000-06a04adf) is still not deleted**
-- MAGIC
-- MAGIC - Although some deletion vector got cleaned as seen on previous image its 4 now its 2.
-- MAGIC - The reason parquet file is still there, because we have used this `invoices_tbl_clone_reference` delta table to shallow clone couple of tables. 
-- MAGIC - This shallow clones still consumes that deleted record so, thats why it needs that parquet file.
-- MAGIC - Workaround is to delete that record for all shallow clone tables created from source `invoices_tbl_clone_reference`.
-- MAGIC
-- MAGIC ![image_1782110907470.png](NB7_images/image_1782110907470.png "image_1782110907470.png")

-- COMMAND ----------

-- DBTITLE 1,Verifying The Deleted Record In Shallow Clone
SELECT
  *
FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone
WHERE
  customer_id = 101;

-- So record with customer_id = 101 exist here.

-- COMMAND ----------

-- DBTITLE 1,Deleting Record From All Shallow Clones
-- invoices_tbl_shallow_clone
DELETE FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone
WHERE
  customer_id = 101;

-- invoices_tbl_shallow_clone_tt
DELETE FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone_tt
WHERE
  customer_id = 101;

-- invoices_tbl_shallow_clone_v0
DELETE FROM
  delta_catalog.delta_db.invoices_tbl_shallow_clone_v0
WHERE
  customer_id = 101;

-- COMMAND ----------

-- DBTITLE 1,Running Vacuum Again On Reference Table
-- This Code was runing(with serverless) but Vacuum was'nt deleting the unused files from the adls as expected.

-- STEP 1: Set the physical retention duration property natively on the table level (Serverless option)
ALTER TABLE delta_catalog.delta_db.invoices_tbl_clone_reference 
SET TBLPROPERTIES ('delta.deletedFileRetentionDuration' = 'interval 0 hours');

-- STEP 2: Run VACUUM without the "RETAIN" clause 
-- (It will automatically read the 0 hours property we just set above)
VACUUM delta_catalog.delta_db.invoices_tbl_clone_reference;

-- So, used global setting with user managed cluster
SET spark.databricks.delta.retentionDurationCheck.enabled = false;
VACUUM delta_catalog.delta_db.invoices_tbl_clone_reference RETAIN 0 HOURS;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Finally, After deleting all occurrence of 101 record from all shallow table refrencing the source table `invoices_tbl_clone_reference` and running vacuum on the source table, we can see that the parquet file(part-00000-06a04adf) is deleted from the adls path.**
-- MAGIC
-- MAGIC ![image_1782112847730.png](NB7_images/image_1782112847730.png "image_1782112847730.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Deep Clone

-- COMMAND ----------

-- DBTITLE 1,Checking Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- DBTITLE 1,Creating Deep Clone Table
CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_tbl_deep_clone DEEP CLONE
delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- DBTITLE 1,Deep Clone Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_deep_clone;

-- COMMAND ----------

-- DBTITLE 1,Dropped Table List (rough code)
-- Show all tables that have been dropped in the database, but can be undroped
SHOW TABLES DROPPED IN delta_catalog.delta_db;

-- There is no supported bulk SQL command to purge all dropped tables from a schema.
-- Dropped managed tables age out automatically after the retention period.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **This is the state of invoices_tbl_deep_clone data files in ADLS**
-- MAGIC
-- MAGIC - Deep Clone create exact copy of data/parquet files from the source(`invoices_tbl_clone_reference`) table parquet files.
-- MAGIC - Now, after cloning whatever operation we perform on deep clone table will create its own logs and data files.
-- MAGIC
-- MAGIC **invoices_tbl_deep_clone**
-- MAGIC ![image_1782116502032.png](./image_1782116502032.png "image_1782116502032.png")
-- MAGIC
-- MAGIC **invoices_tbl_clone_reference**
-- MAGIC ![image_1782112847730.png](NB7_images/image_1782112847730.png "image_1782112847730.png")

-- COMMAND ----------

-- MAGIC %md
-- MAGIC #### Updating customer_id = 6 In deep clone table to verify that the changes occurs in source/reference table as well or not.

-- COMMAND ----------

-- DBTITLE 1,Update On Deep Clone Table
UPDATE
  delta_catalog.delta_db.invoices_tbl_deep_clone
SET
  quantity = 2000
WHERE
  customer_id = 6;

-- COMMAND ----------

-- DBTITLE 1,Verifying Deep Clone Table
SELECT
  *
from
  delta_catalog.delta_db.invoices_tbl_deep_clone
WHERE customer_id = 6;

-- So, recors is updated in deep clone

-- COMMAND ----------

-- DBTITLE 1,Checking Deep Clone Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_deep_clone;

-- COMMAND ----------

-- DBTITLE 1,Verifying Reference Table
SELECT
  *
from
  delta_catalog.delta_db.invoices_tbl_clone_reference
WHERE customer_id = 6;

-- As expected, update/or any operation on deep clone does not affect the source/reference table
-- and vice versa.

-- COMMAND ----------

-- DBTITLE 1,Checking Reference Table History
DESCRIBE HISTORY delta_catalog.delta_db.invoices_tbl_clone_reference;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Conclusion On Deep Clone**
-- MAGIC
-- MAGIC - **Independence:** Deep clone copies all metadata ad data files from source to its location and after cloning it maintains its own distinct history and set of operations.
-- MAGIC - **No Cross-Effect:** Any subsequent modifications, updates, or deletions performed on the source table will not affect the deep clone table and **vice versa**.
-- MAGIC - **Encapsulation:** Once the clone is created, it functions as an independent entity with its own lifecycle, separate from the source table's ongoing activity.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC **Note :-**
-- MAGIC - Vacuum explaination is not required for deep clone becuase it copies all all data file from source, unlike shallow clone which references it from source.
-- MAGIC - Also to remind, we performed vacuum on reference table and shallow clone was referencing those data files while in deep clone it copies all file so that scenario is not applicable here. 

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### CTAS(CREATE TABLE AS SELECT) vs. Deep Clone
-- MAGIC
-- MAGIC * While both result in tables that look identical in output, they differ significantly in capability and process:
-- MAGIC * **Handling of Properties**: **CTAS** creates a new table based on the output of a query, causing it to lose metadata, partitioning properties, and constraints from the source table. **Deep Clone** is more robust as it automatically clones the metadata, data, and existing table properties.
-- MAGIC * **Incremental Processing**: A key advantage of **Deep Clone** is its support for **incremental syncing** . In scenarios like disaster recovery, if you need to update a replica, Deep Clone only copies the incremental changes (updates or deletes) rather than re-copying the entire dataset, making it far more performant for maintaining replicas.
-- MAGIC * **Incremental Processing Limitation**: INSERT / UPDATE / MERGE / DELETE operations are synced incrementally. However, SCHEMA changes or changes in PARTITIONING, COLUMN changes will trigger a full DEEP CLONE
