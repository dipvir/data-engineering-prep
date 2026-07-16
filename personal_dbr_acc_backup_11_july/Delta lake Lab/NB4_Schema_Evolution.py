# Databricks notebook source
# DBTITLE 1,Required Imports
from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta.tables import DeltaTable

# COMMAND ----------

# MAGIC %md
# MAGIC ### Schema Evolution
# MAGIC 1. Adding New Columns (Manual / Automatic)
# MAGIC
# MAGIC 2. Widening Data Types (Supported Delta >= 3.2): Sometimes we need to expand a column's data type to accommodate larger values. Delta Lake allows "widening" type conversions that won't lose data, such as:
# MAGIC - `INT` to `BIGINT`
# MAGIC - `FLOAT` to `DOUBLE`
# MAGIC - `VARCHAR(10)` to `VARCHAR(20)`
# MAGIC
# MAGIC 3. Nested Structure Evolution (Manual / Automatic): Delta Lake supports evolution of complex data types like structs and arrays. We can:
# MAGIC - Add new fields to structs
# MAGIC - Modify nested field types
# MAGIC - Add new elements to arrays
# MAGIC
# MAGIC 4. Column Position Changes (Manual / Automatic): we can reorganize our columns
# MAGIC
# MAGIC ### Quick Note To Remember:
# MAGIC - `INSERT` works by matching columns by position
# MAGIC - `MERGE` works by matching columns by name

# COMMAND ----------

# MAGIC %md
# MAGIC ### Detail Summary On Schema Evolution in Delta Lake
# MAGIC
# MAGIC #### 📌 Core Architectural Meaning
# MAGIC
# MAGIC While **Schema Validation** is the aggressive gatekeeper that blocks unexpected changes, **Schema Evolution** is the feature that allows a table to safely grow, change, and adapt over time. It allows you to update a table's schema dynamically to accommodate changing business requirements *without* having to delete the table, rewrite historical data, or recreate your pipelines.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📋 The 4 Drivers of Schema Evolution
# MAGIC
# MAGIC ##### 1. Adding New Columns (Expanding the Blueprint)
# MAGIC
# MAGIC * **The Meaning:** The most common form of evolution. It happens when an upstream application introduces a brand-new field that your table needs to store moving forward.
# MAGIC * **The Manual Way:** You explicitly execute a DDL command (`ALTER TABLE ... ADD COLUMN`) to update the table’s metadata blueprint manually before running your data stream.
# MAGIC * **The Automatic Way:** You pass the explicit operational parameter **`.option("mergeSchema", "true")`** inside a PySpark write stream, or set the SQL environment configuration property `spark.databricks.delta.schema.autoMerge.enabled = true`. Delta will automatically detect the new column, append it to the log metadata, fill historical rows with `NULL`, and write the data cleanly.
# MAGIC
# MAGIC ##### 2. Type Widening (Scaling Data Capacity)
# MAGIC
# MAGIC * **The Meaning:** Introduced in newer Delta Lake versions, this allows you to safely upgrade a column's data type to a larger, compatible container if your numbers grow too big.
# MAGIC * **The Rule:** You cannot randomly change a data type from an `INT` to a `STRING` because that would corrupt the underlying Parquet files. However, you can widen a column from **`INT` to `BIGINT**` (or `FLOAT` to `DOUBLE`) when your transactions span beyond ordinary integer limits.
# MAGIC * **The Mechanics:** Once enabled via table properties (`delta.enableTypeWidening = true`), you alter the column type. Delta gracefully maps the wider data type in the log metadata layer, allowing old files to coexist safely with newly appended wide files.
# MAGIC
# MAGIC ##### 3. Nested Structure Evolution (Managing Complex Schemas)
# MAGIC
# MAGIC * **The Meaning:** Handles changes occurring inside complex, multi-layered data columns like `STRUCT` types (e.g., a `purchase_details` column that groups nested fields like `mall_pin_code` and `store_code`).
# MAGIC * **The Rule:** Just like flat schemas, nested structs can evolve. You can manually alter or use automatic schema merging to inject a brand-new sub-attribute (like `staff_id`) right into the middle of an existing struct container. Delta maintains absolute consistency by automatically assigning `NULL` to the new inner sub-attribute across all older historical records.
# MAGIC
# MAGIC ##### 4. Column Position Changes (Reordering Layouts)
# MAGIC
# MAGIC * **The Meaning:** Dictates where a newly introduced column physically or logically falls inside your table sequence (e.g., forcing a new `age` column to sit explicitly *after* `price` rather than automatically getting dumped at the very end).
# MAGIC * **The Rule:** Standard positional `INSERT` statements will crash or mismatch if you change the expected order. However, if you utilize a robust **`MERGE INTO`** statement or write using data frames with schema merging active, Delta completely bypasses the positioning trap. It resolves the layout **by name**, appends the new column exactly where specified in the metadata index, and properly shifts the logical visibility schema layout for end-users.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 Interview-Ready Summary
# MAGIC
# MAGIC * **Schema Evolution** is Delta Lake's mechanism for gracefully adapting table frameworks to changes in upstream data streams without requiring resource-heavy table rewrites. By explicitly enabling properties like **`mergeSchema = true`** or utilizing native DDL alterations, developers can dynamically append new columns, evolve complex nested `STRUCT` elements, change logical column positioning, and execute **Type Widening** (such as `INT` to `BIGINT`) while completely preserving operational uptime and data lineage stability.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Creating New Delta Table For This Lab

# COMMAND ----------

# DBTITLE 1,Query For Data Consumed Used In Creation Of invoices_se Delta Table
# MAGIC %sql
# MAGIC SELECT
# MAGIC   customer_id,
# MAGIC   invoice_no,
# MAGIC   price,
# MAGIC   invoice_date
# MAGIC FROM
# MAGIC   PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC WHERE
# MAGIC   customer_id BETWEEN 1 AND 5;

# COMMAND ----------

# DBTITLE 1,DDL Command :- Creating A Sample Delta Table For Schema Evolution Exercise
# MAGIC %sql
# MAGIC -- In prevous notebooks(i.e NB1, NB2), we created delta table using parquet files directly with CTAS.
# MAGIC -- Here we are first creating a schema for the delta table and then inserting data into it.
# MAGIC
# MAGIC CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_se (
# MAGIC   customer_id INT NOT NULL,
# MAGIC   invoice_no STRING,
# MAGIC   price FLOAT,
# MAGIC   invoice_date DATE
# MAGIC );
# MAGIC
# MAGIC -- Used parquet files has many columns but we are using the below ones only.
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     price,
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 1 AND 5;

# COMMAND ----------

# DBTITLE 1,DDL Command To DROP/UNDROP Table
# MAGIC %sql
# MAGIC -- DROP TABLE delta_catalog.delta_db.invoices_se;
# MAGIC -- UNDROP TABLE delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,Sanity Check Of Data
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,Rough Cell To Check Source File Columns And Data
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC ORDER BY price DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 1: Adding New Columns (Manual/Automatic)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Manual Way Of Adding New Columns

# COMMAND ----------

# DBTITLE 1,invoices_se Schema (Before)
# MAGIC %sql
# MAGIC DESCRIBE TABLE delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,DDL Command :- Manually Adding New Column Quantity
# MAGIC %sql
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC ADD COLUMN quantity INT;

# COMMAND ----------

# DBTITLE 1,invoices_se Schema (After)
# MAGIC %sql
# MAGIC DESCRIBE TABLE delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,DML Command :- Appending New Records In invoices_se
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     price,
# MAGIC     invoice_date,
# MAGIC     quantity
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 6 AND 10;

# COMMAND ----------

# DBTITLE 1,Verfying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with new records for customer_id 6 to 10, containing data for all old columns and new column quantity and nulls for historical quantity records, which means manual schema evolution worked for delta table.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY customer_id;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Automatic Way Of Adding New Columns Using INSERT INTO

# COMMAND ----------

# MAGIC %md
# MAGIC ---
# MAGIC
# MAGIC ### Core Concept: Automatic Schema Evolution
# MAGIC
# MAGIC **Definition:** The ability of a Delta Lake table to dynamically update its metadata structural blueprint to accommodate newly added or changed columns from incoming data streams, without requiring manual `ALTER TABLE` DDL commands or heavy table rewrites.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 1) SQL Implementation (Requires User-Managed Cluster)
# MAGIC
# MAGIC ##### 📝 The Technical "Why" (How it works under the hood)
# MAGIC
# MAGIC This approach relies on a **Global Spark Session Configuration** (`SET spark.databricks...`). When you run this command, you are telling the entire underlying Apache Spark execution engine to globally modify its validation rules for the remainder of your notebook session.
# MAGIC
# MAGIC Because traditional SQL `INSERT INTO` statements match data fields strictly by **ordinal position (left-to-right alignment)** rather than column names, turning on this session flag tells the compiler: *"If you see an extra column at the end of a positional insert, don't throw a structural mismatch error; instead, dynamically expand the target schema metadata."*
# MAGIC
# MAGIC ##### 🛑 Why it FAILS on Serverless Compute
# MAGIC
# MAGIC * **Environment Sandboxing (Shared Access Mode):** Databricks Serverless clusters are multi-tenant and highly secure. To ensure cluster stability and isolate users, Serverless operates in **Shared Access Mode**, which explicitly blocks users from altering global Spark session environments via `SET` commands.
# MAGIC * **The Column Mapping Guardrail:** By default, Serverless turns on advanced **Column Mapping** (mapping logical column names to internal immutable physical IDs). Because Column Mapping demands strict, name-resolved mapping to assign these internal IDs, the engine completely bars blind positional SQL `INSERT` statements from altering the schema layout to prevent accidental structure corruption.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 2) Python / PySpark Implementation (Universal: Serverless & User-Managed)
# MAGIC
# MAGIC ##### 📝 The Technical "Why" (How it works under the hood)
# MAGIC
# MAGIC This approach shifts the configuration from the global cluster scope down to the **DataFrame Writer scope** using `.option("mergeSchema", "true")`. Instead of altering the entire Spark platform environment, you are passing an isolation property tied strictly to that single write transaction.
# MAGIC
# MAGIC The PySpark DataFrame API natively processes records using **Name-Based Evaluation**. When saving a table, the engine does not care about the left-to-right order of the columns in your file. It explicitly matches the text labels of the DataFrame columns against the target table's metadata attributes. If it detects a new column name like `payment_method`, it seamlessly allocates a new entry in the Delta transaction log (`_delta_log/`) and writes the data safely.
# MAGIC
# MAGIC ##### 🟢 Why it WORKS Natively on Serverless
# MAGIC
# MAGIC * **Zero Shared Impact:** Because `.option()` changes the property of the specific *write stream* and not the *global cluster*, it complies perfectly with Serverless security boundaries.
# MAGIC * **Explicit ID Assignment:** Because the DataFrame contains explicit string column names, the modern Serverless Column Mapping engine can easily read the name, instantly generate a fresh hidden physical ID for the new column, and safely update the metadata wrapper without a single collision.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 Summary Cheat Sheet for Your Notebook Review
# MAGIC
# MAGIC | Metric / Feature | 1) SQL Positional Ingestion | 2) PySpark DataFrame API |
# MAGIC | --- | --- | --- |
# MAGIC | **Configuration Scope** | **Global / Session Level** (Alters entire cluster rule). | **Local / Operational Level** (Isolated to specific table write). |
# MAGIC | **Attribute Evaluation** | **Ordinal Position** (Left-to-right matrix matching). | **Name-Based Matching** (Resolves mapping explicitly by column label). |
# MAGIC | **Serverless Compatibility** | ❌ **Blocked** (Throws environment configuration exceptions). | 🟢 **Native Support** (The enterprise standard for portable pipelines). |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC - To do **automatic Schema Evolution using pure SQL in Databricks**, you don't use an `.option()` configuration. Instead, you change a **Session Configuration Variable** right before you run your ingestion queries (`INSERT` or `MERGE`).
# MAGIC - **`.option("mergeSchema", "true")`** in PySpark is **scoped to a single target table write**. It is very safe because it only affects that specific dataframe pipeline.
# MAGIC - **`SET spark.databricks.delta.schema.autoMerge.enabled = true;`** in SQL is **global for your entire session**. If you have 5 different `INSERT` queries running in the same notebook after this command, *all* of them will dynamically change their target tables if a column structure shifts.
# MAGIC - **Best Practice Advice:** Always remember to turn it back off (`SET spark.databricks.delta.schema.autoMerge.enabled = false;`) at the end of your specific data loading block so you don't accidentally evolve other tables by mistake!

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Python Code (Works On Serverless and User-Managed Cluster Both)

# COMMAND ----------

# DBTITLE 1,Automatic Schema Evolution Using Pyspark
# 1. Define your cloud storage path variables
source_parquet_path = "abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet"
target_table_name = "delta_catalog.delta_db.invoices_se"

# 2. Read the raw parquet file into a Spark DataFrame
df_source = (spark.read
             .format("parquet")
             .load(source_parquet_path)
             .select("customer_id",
                    "invoice_no",
                     col("price").cast("float"),
                    "invoice_date",
                    "quantity",
                    "payment_method") # New column for automatic schema evolution.
             .filter("customer_id BETWEEN 16 AND 20"))
# display(df_source)

# 3. Write data with explicit Schema Evolution option.
(df_source.write
 .format("delta")
 .mode("append")
 .option("mergeSchema", "true") # 👈 The golden alternative to the SQL SET command
 .saveAsTable(target_table_name))

# COMMAND ----------

# DBTITLE 1,Verifying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with new record from 16-20 customer_id, containing data for all old columns and new column payment_method and nulls for historical payment_method records, which means automatic schema evolution worked.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY customer_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ##### SQL Equivalent Code (Not For Serverless / Need User-Managed Cluster To Work)

# COMMAND ----------

# DBTITLE 1,Enabling Automatic Schema Evolution Setting
# MAGIC %sql
# MAGIC -- option 1
# MAGIC -- Enables auto-merge at global level
# MAGIC -- Session scoped
# MAGIC -- The SQL alternative to python code .option("mergeSchema", "true").
# MAGIC SET spark.databricks.delta.schema.autoMerge.enabled = true; --This setting is not supported in serverless environments, For safety reasons as it does it at global level.
# MAGIC
# MAGIC -- option 2
# MAGIC -- 1. Enable auto-merge strictly at the table metadata level (For Serverless if above is not working)
# MAGIC -- Table scoped
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC SET TBLPROPERTIES ('spark.databricks.delta.schema.autoMerge.enabled' = 'true');

# COMMAND ----------

# DBTITLE 1,Verifying Automatic Schema Evolution Is Enabled Through Table Properties
# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_catalog.delta_db.invoices_se;
# MAGIC
# MAGIC -- Check the 'Detailed Table Information' section to verify the setting is set to true.

# COMMAND ----------

# DBTITLE 1,DML Command :- Appending New Records In invoices_se
# MAGIC %sql
# MAGIC -- Note :- This cell needs user-managed cluster and setting SET spark.databricks.delta.schema.autoMerge.enabled = true;
# MAGIC
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se 
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     price,
# MAGIC     invoice_date,
# MAGIC     quantity,
# MAGIC     payment_method,
# MAGIC     age -- New column for automatic schema evolution.
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 11 AND 15;

# COMMAND ----------

# DBTITLE 1,Verifying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with new record from 11-15 customer_id, containing data for all old columns and new column age and nulls for historical age records, which means automatic schema evolution worked.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY customer_id;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Automatic Way Of Adding New Columns Using MERGE INTO

# COMMAND ----------

# DBTITLE 1,invoices_se Schema
# MAGIC %sql
# MAGIC DESCRIBE TABLE delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,SQL Code For Automatic Schema Evolution Using MERGE INTO
# MAGIC %sql
# MAGIC -- 'WITH SCHEMA EVOLUTION' Enables upsert and automatically add new columns on the fly.
# MAGIC MERGE WITH SCHEMA EVOLUTION INTO delta_catalog.delta_db.invoices_se AS target
# MAGIC USING (
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     price,
# MAGIC     current_date() AS invoice_date, 
# MAGIC     quantity,
# MAGIC     payment_method,
# MAGIC     age,                -- if above sql code for automatic schema evolution using 'Insert Into' is not executed, then this will also be a new column.
# MAGIC     shopping_mall       -- New column for automatic schema evolution.
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 19 AND 25
# MAGIC ) AS source
# MAGIC ON target.customer_id = source.customer_id
# MAGIC WHEN MATCHED THEN       -- If customer exists, overwrite all fields with fresh data & adds new column.
# MAGIC   UPDATE SET * 
# MAGIC WHEN NOT MATCHED THEN   -- If customer is brand new, insert the entire row.
# MAGIC   INSERT *; 

# COMMAND ----------

# DBTITLE 1,Verifying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with updated and new record from 19-25 customer_id, containing data for all old columns and new column shopping_mall(And Age Maybe) and nulls for historical shopping_mall(And Age Maybe) records, which means automatic schema evolution worked.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY customer_id;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 2: Data Types Widening

# COMMAND ----------

# MAGIC %md
# MAGIC #### Manual Way Of Data Types Widening

# COMMAND ----------

# DBTITLE 1,Enabling Type Widening Setting
# MAGIC %sql
# MAGIC -- Enabling Type Widening strictly at the table level.
# MAGIC -- Table scoped
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC SET TBLPROPERTIES ('delta.enableTypeWidening' = 'true');

# COMMAND ----------

# DBTITLE 1,Verifying Type Widening Is Enabled Through DESCRIBE EXTENDED
# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_catalog.delta_db.invoices_se;
# MAGIC
# MAGIC -- Check the 'Detailed Table Information' section to verify the setting is set to true.

# COMMAND ----------

# DBTITLE 1,Manually Changing The Data Type
# MAGIC %sql
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC ALTER COLUMN customer_id TYPE LONG;

# COMMAND ----------

# DBTITLE 1,Verifying The Data Type
# MAGIC %sql
# MAGIC DESCRIBE Table delta_catalog.delta_db.invoices_se;
# MAGIC -- manual type widening worked customer_id column changed from int to long.

# COMMAND ----------

# DBTITLE 1,Appending A Single Record With Long Type Integer
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC VALUES(987654321012345, 'I8888', 100, '2022-01-01', 33, 'Credit Card', "22", "Mall of Istanbul");

# COMMAND ----------

# DBTITLE 1,Verifying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with customer_id = 987654321012345.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC WHERE
# MAGIC   customer_id = 987654321012345;    

# COMMAND ----------

# MAGIC %md
# MAGIC #### Automatic Way Of Data Types Widening

# COMMAND ----------

# DBTITLE 1,Automatic Type Widening Using SQL And MERGE INTO
# MAGIC %sql
# MAGIC -- Enable type widening feature on the table ('delta.enableTypeWidening' = 'true').
# MAGIC -- Execute Merge with Schema Evolution
# MAGIC MERGE WITH SCHEMA EVOLUTION INTO
# MAGIC   delta_catalog.delta_db.invoices_se AS target
# MAGIC USING (
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     price, -- automatic type widening price from float to double.
# MAGIC     date_sub(current_date(), 10) AS invoice_date,
# MAGIC     quantity,
# MAGIC     payment_method,
# MAGIC     age,
# MAGIC     shopping_mall
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 30 AND 35
# MAGIC ) AS source
# MAGIC ON
# MAGIC   target.customer_id = source.customer_id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *;

# COMMAND ----------

# DBTITLE 1,Automatic Type Widening Using Pyspark And MERGE INTO
# Enable type widening feature on the table ('delta.enableTypeWidening' = 'true').
# Load data, fix customer_id to match target, and let quantity widen automatically.
df_incoming = (
    spark.read.format("parquet")
    .load(
        "abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet"
    )
    .filter(col("customer_id").between(40, 43))
    .selectExpr(
        "CAST(customer_id AS LONG) AS customer_id",  #added as we manually type widening customer_id from int to bigint in target table
        "invoice_no",
        "price",
        "date_sub(current_date(), 15) AS invoice_date",
        "CAST(quantity AS LONG) AS quantity",  # automatic type widening quantity from int to bigint
        "payment_method",
        "age",
        "shopping_mall",
    )
)
# display(df_incoming)

# 3. Save using mergeSchema
(
    df_incoming.write.format("delta")
    .option("mergeSchema", "true")
    .mode("append")
    .saveAsTable("delta_catalog.delta_db.invoices_se")
)

# COMMAND ----------

# DBTITLE 1,Sanity check
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se; 
# MAGIC
# MAGIC -- check the price column datatype to verify as automatic type widening changed the type from float to double 

# COMMAND ----------

# DBTITLE 1,Verifying The Data Type
# MAGIC %sql
# MAGIC DESCRIBE Table delta_catalog.delta_db.invoices_se;
# MAGIC
# MAGIC -- Automatic type widening worked with sql and pyspark using merge into.
# MAGIC -- price column changed from float to double.
# MAGIC -- And quantity column changed from int to long.

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 3: Nested Structure Evolution (Manual / Automatic)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Manual Nested Structure Evolution

# COMMAND ----------

# DBTITLE 1,Manually Adding Column Of Type STRUCT
# MAGIC %sql
# MAGIC ALTER TABLE
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ADD COLUMN
# MAGIC   purchase_details
# MAGIC   STRUCT<mall_pin_code INT, store_code INT>;

# COMMAND ----------

# DBTITLE 1,Appending A Single Record
# MAGIC %sql
# MAGIC -- target table columns
# MAGIC
# MAGIC -- customer_id
# MAGIC -- invoice_no
# MAGIC -- price
# MAGIC -- invoice_date
# MAGIC -- quantity
# MAGIC -- payment_method
# MAGIC -- age
# MAGIC -- shopping_mall
# MAGIC -- purchase_details
# MAGIC
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC VALUES(50, 'I0000', 100, '2022-01-01', 33, 'Credit Card', "22", "Mall of Istanbul", struct(12345, 1000));  

# COMMAND ----------

# DBTITLE 1,Verfying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with data for customer_id = 50 and newly created struct column purchase_details.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY
# MAGIC   customer_id;

# COMMAND ----------

# DBTITLE 1,Verifying The Data Type
# MAGIC %sql
# MAGIC DESCRIBE TABLE delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,Manually Changing The Data Type Of STRUCT(mall_pin_code)
# MAGIC %sql
# MAGIC -- Manual Type widening For Struct Type
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC ALTER COLUMN purchase_details.mall_pin_code TYPE LONG;

# COMMAND ----------

# DBTITLE 1,Appending A Single Record To Verify Type widening
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC VALUES(51, 'I0001', 100, '2026-06-19', 33, 'Credit Card', "23", "Mall of Istanbul", struct(987654321012345, 12345));  

# COMMAND ----------

# DBTITLE 1,Verfying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with data for customer_id = 51 and long value for mall_pin_code in purchase_details.
# MAGIC -- This means manual Type widening worked for struct type as well.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY
# MAGIC   customer_id;

# COMMAND ----------

# DBTITLE 1,Manually Adding New Column Within STRUCT Object
# MAGIC %sql
# MAGIC ALTER TABLE
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ADD COLUMN
# MAGIC   purchase_details.store_loc STRING;

# COMMAND ----------

# DBTITLE 1,Appending A Single Record To Verify Schema Evolution Nested Structure
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC VALUES(52, 'I0002', 100, '2026-05-19', 33, 'Credit Card', "24", "Mall of Istanbul", struct(012345, 12345, "Istanbul"));  

# COMMAND ----------

# DBTITLE 1,Verfying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with data for customer_id = 52 and string value for store_loc in purchase_details with historical store_loc as nulls.
# MAGIC -- This means adding new column(schema evolution) worked for struct type as well.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY
# MAGIC   customer_id;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Automatic Nested Structure Evolution

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Using INSERT INTO (Need User-Managed Cluster)

# COMMAND ----------

# DBTITLE 1,Verifying Type Widening Is Enabled Through DESCRIBE EXTENDED
# MAGIC %sql
# MAGIC DESCRIBE EXTENDED delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# DBTITLE 1,Enable Column Mapping by Name
# MAGIC %sql
# MAGIC -- Enable Column Mapping by Name so Delta can map structural keys natively
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name');

# COMMAND ----------

# DBTITLE 1,Appending A Single Record Using Insert Into
# MAGIC %sql
# MAGIC -- Appending A Single Record To Verify Schema Evolution Nested Structure
# MAGIC -- Enable automatic schema evolution Setting on the table ('spark.databricks.delta.schema.autoMerge.enabled' = 'true'). 
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC VALUES(88, 'I0003', 100, '2026-04-19', 33, 'Credit Card', "24", "Mall of Istanbul", 
# MAGIC named_struct( 'mall_pin_code',012345,
# MAGIC  'store_code', 12345,
# MAGIC  'store_loc', "Istanbul",
# MAGIC  'staff_id', "SID1235"
# MAGIC  )); 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##### Using MERGE INTO (Works On Serverless and User-Managed Cluster Both)

# COMMAND ----------

# DBTITLE 1,Appending A Single Record Using Merge Into
# MAGIC %sql
# MAGIC MERGE WITH SCHEMA EVOLUTION INTO delta_catalog.delta_db.invoices_se AS target
# MAGIC USING (
# MAGIC   SELECT 
# MAGIC     cast(54 AS bigint) AS customer_id,  -- Kept your bigint fix intact
# MAGIC     'I0003' AS invoice_no, 
# MAGIC     100.0 AS price, 
# MAGIC     '2026-04-19' AS invoice_date, 
# MAGIC     33 AS quantity, 
# MAGIC     'Credit Card' AS payment_method, 
# MAGIC     24 AS age, 
# MAGIC     'Mall of Istanbul' AS shopping_mall,
# MAGIC     named_struct(
# MAGIC       'mall_pin_code', 125,
# MAGIC       'store_code', 12345,
# MAGIC       'store_loc', 'Istanbul',
# MAGIC       'staff_id', 'SID1235'
# MAGIC     ) AS purchase_details  -- Giving the new struct an explicit column name
# MAGIC ) AS source
# MAGIC ON target.customer_id = source.customer_id
# MAGIC WHEN NOT MATCHED THEN
# MAGIC   INSERT *;

# COMMAND ----------

# DBTITLE 1,Command To Delete A Row And Column
# MAGIC %sql
# MAGIC -- by mistake added so deleted
# MAGIC -- DELETE FROM delta_catalog.delta_db.invoices_se WHERE customer_id = 53;
# MAGIC -- ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC -- DROP COLUMN shopping_mall_details;

# COMMAND ----------

# DBTITLE 1,Verfying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with data for customer_id = 54 and new added value for staff_id in purchase_details with historical staff_id as nulls.
# MAGIC -- This means aotumatic schema evolution worked for nested struct type as well.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY
# MAGIC   customer_id;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 4: Column Position Changes

# COMMAND ----------

# DBTITLE 1,Adding Column At Given Position
# MAGIC %sql
# MAGIC -- ALTER TABLE delta_catalog.delta_db.invoices_se ADD COLUMN (gender STRING FIRST);
# MAGIC ALTER TABLE delta_catalog.delta_db.invoices_se ADD COLUMN (gender STRING AFTER price);
# MAGIC
# MAGIC -- ALTER TABLE delta_catalog.delta_db.invoices_se
# MAGIC -- DROP COLUMN gender;

# COMMAND ----------

# DBTITLE 1,Verfying The Added Column Position
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC LIMIT 1;

# COMMAND ----------

# DBTITLE 1,DML Command :- Appending New Records In invoices_se
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_se
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     price,
# MAGIC     gender,
# MAGIC     invoice_date,
# MAGIC     quantity,
# MAGIC     payment_method,
# MAGIC     age,
# MAGIC     shopping_mall,
# MAGIC     Null AS purchase_details
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://sample-files-container@delta0lake0lab0storageac.dfs.core.windows.net/invoices/invoices_1_100.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 60 AND 65;

# COMMAND ----------

# DBTITLE 1,Verfying The Appended Data
# MAGIC %sql
# MAGIC -- Query returns the appropriate results with data for customer_id = 60-65 and new Column gender
# MAGIC -- at right position.
# MAGIC -- This means Column Position Change worked.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_se
# MAGIC ORDER BY
# MAGIC   customer_id;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_se;
