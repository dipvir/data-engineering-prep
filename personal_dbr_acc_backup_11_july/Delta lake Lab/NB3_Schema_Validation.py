# Databricks notebook source
# MAGIC %md
# MAGIC ### Schema Validation
# MAGIC 1. What is Schema-on-read / Schema-on-write?
# MAGIC 2. Column Order Validation
# MAGIC 3. Data Type Validation
# MAGIC 4. Column Name Validation
# MAGIC 5. Nullability Validation
# MAGIC 6. Extra Columns Validation

# COMMAND ----------

# MAGIC %md
# MAGIC ### What is Schema-on-read / Schema-on-write?
# MAGIC
# MAGIC ---
# MAGIC These terms represent two fundamentally different approaches to how data systems handle structure, validation, and storage. The easiest way to think about the difference is **when** the rules (the schema) are enforced: before the data lands on disk, or when you write a query to read it.
# MAGIC
# MAGIC ---
# MAGIC ### 🗺️ The Concepts Visualized
# MAGIC ---
# MAGIC
# MAGIC ### 1. Schema-on-Write (The Gatekeeper Approach)
# MAGIC
# MAGIC In a Schema-on-Write system, the database management system **enforces the structure upfront**. Before a single row of data is physically written to disk, the engine checks it against a strict, pre-defined blueprint (columns, data types, constraints).
# MAGIC
# MAGIC * **How it works:** If your table expects an `INT` for `customer_id`, and a pipeline tries to insert the string `'ABC'`, the storage engine instantly rejects the write and throws an error.
# MAGIC * **Where it's used:** Traditional Data Warehouses (like Snowflake, Synapse) and **Delta Lake** (via Schema Enforcement).
# MAGIC * **Pros:** Absolute data quality. Downstream BI reports and analytics jobs will never crash due to corrupted or missing columns.
# MAGIC * **Cons:** Less flexible. If an upstream application adds a new column, your ingestion pipeline will break until you manually alter the table structure.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 2. Schema-on-Read (The "Dump Now, Figure It Out Later" Approach)
# MAGIC
# MAGIC In a Schema-on-Read system, the storage layer is completely indifferent to what the data looks like. You can dump structured, semi-structured (JSON), or completely unstructured data into a directory, and the storage layer will blindly accept it.
# MAGIC
# MAGIC * **How it works:** The data just sits as raw files on disk. The "schema" is only applied when a developer or query engine reads the data by overlaying a structure on top of it at execution time.
# MAGIC * **Where it's used:** Traditional, raw **Data Lakes** (like raw Parquet, CSV, or JSON folders sitting on Azure ADLS Gen2 or AWS S3).
# MAGIC * **Pros:** Massive ingestion speed and total flexibility. Pipelines never break due to upstream format changes because the storage layer never blocks a write.
# MAGIC * **Cons:** It can easily turn a Data Lake into a **Data Swamp**. If a file format changes down the line, your downstream production models and dashboards will suddenly crash with type-mismatch exceptions.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Quick-Reference Comparison
# MAGIC
# MAGIC | Feature | Schema-on-Write (e.g., Delta Lake) | Schema-on-Read (e.g., Raw Parquet Lake) |
# MAGIC | --- | --- | --- |
# MAGIC | **Enforcement Time** | **During Ingestion** (Before writing to disk). | **During Querying** (When reading from disk). |
# MAGIC | **Data Quality** | **High & Guaranteed**. Clean and reliable. | **Unpredictable**. Risk of hidden corruption. |
# MAGIC | **Write Performance** | Slower (Compute spent validating schemas). | Faster (Blind data dumping). |
# MAGIC | **Flexibility** | Rigid (Requires Schema Evolution rules). | Highly flexible (Accepts any payload). |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 The Delta Lake Connection
# MAGIC
# MAGIC This concept is exactly why layers like Delta Lake exist. A traditional data lake is purely **Schema-on-Read**. By mapping a transaction log over your Parquet files, **Delta Lake converts your data lake into a Schema-on-Write system**, giving you the cost benefits of a data lake with the strict quality guarantees of a database warehouse.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Interview Flashcard
# MAGIC
# MAGIC > **Q: Why does a raw Data Lake follow Schema-on-Read, and how does Delta Lake change that behavior?**
# MAGIC > * A raw Data Lake stores data in unmanaged object storage files, applying structure only when a query parses the files (*Schema-on-Read*). Delta Lake introduces a transactional metadata layer that validates incoming records against a strict schema blueprint *before* committing the write (*Schema-on-Write*), protecting the lakehouse from schema corruption.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Detail Summary On Schema Enforcement & Validation in Delta Lake
# MAGIC
# MAGIC #### 📌 Core Architectural Meaning
# MAGIC
# MAGIC Delta Lake utilizes a **Schema-on-Write** paradigm. Before any write transaction (`INSERT`, `APPEND`, `MERGE`) is officially committed to disk, Delta compares the structure of the incoming data against the table's current master schema stored in the transaction log (`_delta_log/`). If the incoming structure violates the integrity rules, Delta kills the transaction instantly to prevent **Data Swamp** corruption.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📋 The 5 Pillars of Schema Validation
# MAGIC
# MAGIC ##### **1. Column Order Validation (The Position Trap)**
# MAGIC
# MAGIC * **The Meaning:** In traditional SQL, standard `INSERT INTO` statements map data fields from left to right based strictly on **ordinal position**, completely ignoring column names.
# MAGIC * **The Rule:** If you shuffle the order of columns in a query but the data types still match (e.g., swapping `customer_id` and `quantity` because both are integers), Delta will allow the write, but it will cause **silent data corruption**.
# MAGIC * **The Guardrail:** To prevent this layout trap, always declare explicit target columns in your insert statements, or rely on `MERGE INTO` which matches columns securely **by name** rather than position.
# MAGIC
# MAGIC ##### **2. Data Type Validation (The Type Guardian)**
# MAGIC
# MAGIC * **The Meaning:** Ensures that the data type of every incoming record field strictly matches the data type defined in the table schema.
# MAGIC * **The Rule:** Delta will proactively attempt safe implicit casting (e.g., converting a valid numeric string like `'99499'` into an `INT`, or a date string into a `DATE`). However, if an upstream system passes raw garbage text (like `'ABC'`) into an integer column, Delta kills the write immediately with a casting exception to protect structural integrity.
# MAGIC
# MAGIC ##### **3. Column Name Validation (The Name Check)**
# MAGIC
# MAGIC * **The Meaning:** Validates that the structural labels of the incoming dataset align cleanly with the target destination attributes.
# MAGIC * **The Rule:** Similar to column order, a standard positional `INSERT` statement is blind to names and will let a column named `C_ID` write directly into a column defined as `customer_id` as long as it sits in the right index position. Conversely, a `MERGE` or a data frame write requires an absolute, explicit name alignment and will fail immediately if a name mismatch is detected.
# MAGIC
# MAGIC ##### **4. Nullability Validation (The Constraint Gate)**
# MAGIC
# MAGIC * **The Meaning:** Enforces strict compliance with `NOT NULL` data design constraints set during table creation.
# MAGIC * **The Rule:** If a critical business operational field (like `customer_id`) is defined as `NOT NULL`, Delta scans incoming records before writing. The moment a transaction attempts to pass a `NULL` value into that protected slot, Delta aborts the write operation, throwing a constraint violation error.
# MAGIC
# MAGIC ##### **5. Extra Columns Validation (The Payload Shield)**
# MAGIC
# MAGIC * **The Meaning:** Prevents rogue or unmapped attributes from entering a cleanly defined production table layout.
# MAGIC * **The Rule:** If an upstream system introduces a brand-new, unexpected column (e.g., adding `customer_type` to a schema that doesn't expect it), Delta blocks the write instantly with a `SchemaMismatchedException`. This acts as a protective shield, forcing the data engineer to consciously choose to evolve the schema using **Schema Evolution** parameters (`mergeSchema = true`) before the data is allowed to land.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 Interview-Ready Summary
# MAGIC
# MAGIC * Delta Lake implements **Schema Enforcement** at the storage tier to guarantee that no write operation can corrupt the table’s structural blueprint. It validates structural alignment across five dimensions: checking ordinal positioning, rejecting incompatible data types, blocking unmapped extra columns, tracking explicit column names during advanced merges, and throwing immediate exceptions upon `NOT NULL` constraint violations.
# MAGIC

# COMMAND ----------

# DBTITLE 1,DDL Command :- Creating A Sample Delta Table For Schema Validation Exercise
# MAGIC %sql
# MAGIC -- In prevous notebook(i.e NB1, NB2), we created delta table using parquet files directly with --(CTAS).
# MAGIC -- Here we are creating a schema for the delta table and inserting data into it
# MAGIC
# MAGIC CREATE OR REPLACE TABLE delta_catalog.delta_db.invoices_sv (
# MAGIC   customer_id INT NOT NULL,
# MAGIC   invoice_no STRING,
# MAGIC   quantity INT,
# MAGIC   price FLOAT,
# MAGIC   invoice_date DATE
# MAGIC );
# MAGIC
# MAGIC -- Used parquet files has many columns but we are using the below ones only.
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     quantity,
# MAGIC     price,
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_1_100.parquet`;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_sv;

# COMMAND ----------

# DBTITLE 1,DDL Command :- Drop Table
# MAGIC %sql 
# MAGIC -- DROP TABLE delta_catalog.delta_db.invoices_sv;

# COMMAND ----------

# DBTITLE 1,Querying The Delta Table
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC LIMIT 5;

# COMMAND ----------

# DBTITLE 1,Sanity Check Of Data
# MAGIC %sql
# MAGIC SELECT
# MAGIC   MIN(customer_id) AS min_customer_id,
# MAGIC   MAX(customer_id) As max_customer_id,
# MAGIC   count(*) AS total_rows
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 1: Column Order Validation

# COMMAND ----------

# DBTITLE 1,DML Command :- Using INSERT INTO To Append A Single Row With Different Column Order
# MAGIC %sql
# MAGIC -- This cell attempts to insert a row into the delta_catalog.delta_db.invoices_sv table.
# MAGIC -- However, the SELECT statement's column order does not match the delta table's schema.
# MAGIC -- The table expects: customer_id, invoice_no, quantity, price, invoice_date.(In same order)
# MAGIC -- The SELECT statement provides the data in a different order: quantity, invoice_no, customer_id, price, invoice_date.
# MAGIC -- This may cause a schema mismatch or incorrect data insertion.
# MAGIC
# MAGIC -- Main query of cell startes here
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   SELECT
# MAGIC     quantity,
# MAGIC     invoice_no,
# MAGIC     customer_id,
# MAGIC     price,
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     VALUES(9999, 'I12345', 10, 100, '2022-01-01') 
# MAGIC     AS T(customer_id, invoice_no, quantity, price, invoice_date);
# MAGIC -- Main query of cell ends here
# MAGIC
# MAGIC -- Run only below code to see order of columns.
# MAGIC -- result of below query is not how the actual data is inserted.
# MAGIC SELECT
# MAGIC     quantity,
# MAGIC     invoice_no,
# MAGIC     customer_id,
# MAGIC     price,
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     VALUES(9999, 'I12345', 10, 100, '2022-01-01') 
# MAGIC     AS T(customer_id, invoice_no, quantity, price, invoice_date);

# COMMAND ----------

# DBTITLE 1,Verifying Data corruption - 1
# MAGIC %sql
# MAGIC -- let's see if the data was inserted correctly with customer_id = 9999
# MAGIC -- Ans : No (result is empty for this query)
# MAGIC -- This is because the column order in the SELECT statement does not match the table's schema.
# MAGIC -- The table expects: customer_id, invoice_no, quantity, price, invoice_date.
# MAGIC -- The SELECT statement provides the data in a different order: quantity, invoice_no, customer_id, price, invoice_date.
# MAGIC -- This has caused incorrect data insertion.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE customer_id = 9999;

# COMMAND ----------

# DBTITLE 1,Verifying Data corruption - 2
# MAGIC %sql
# MAGIC -- Now, let's see if the data was inserted with customer_id = 10.
# MAGIC -- Ans : Yes (result contains two records with customer_id = 10).
# MAGIC -- As, We already had one row for customer_id = 10.
# MAGIC -- This happend because the data was inderted based on column matching by position and not by column name.
# MAGIC -- customer_id, invoice_no, quantity, price, invoice_date (Column order in delta table).
# MAGIC -- quantity, invoice_no, customer_id, price, invoice_date (Column order in select statement).
# MAGIC -- Thats why we see row inserted for customer_id = 10 and not for customer_id = 9999.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE customer_id = 10;

# COMMAND ----------

# MAGIC %md
# MAGIC **In Apache Spark and Delta Lake, a standard INSERT INTO statement completely ignores column names in your SELECT clause. Instead, it maps data strictly by ordinal position (left-to-right).
# MAGIC Conclusion : Only use INSERT INTO when we are sure about the schema and column order of the table we want to write to, Else we would end up with corrupted data as shown above.**

# COMMAND ----------

# DBTITLE 1,Data Consumed In MERGE INTO
# MAGIC %sql
# MAGIC SELECT
# MAGIC   customer_id,
# MAGIC   invoice_no,
# MAGIC   quantity,
# MAGIC   price,
# MAGIC   invoice_date
# MAGIC FROM
# MAGIC   PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC ORDER BY
# MAGIC   customer_id
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC **A MERGE INTO statement natively resolves columns by name rather than position, completely avoiding this positional mismatch trap like INSERT INTO does.**

# COMMAND ----------

# DBTITLE 1,DML Command :- Using MERGE INTO To Append Data With Different Column Order
# MAGIC %sql
# MAGIC -- Now, here also we have put different column order in the select statement.
# MAGIC -- Only the first 5 rows(101-105) are being appended to the table.
# MAGIC MERGE INTO
# MAGIC   delta_catalog.delta_db.invoices_sv AS target
# MAGIC USING (
# MAGIC   SELECT
# MAGIC     quantity,
# MAGIC     invoice_no,
# MAGIC     customer_id,
# MAGIC     CAST(price AS FLOAT),
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC   ORDER BY
# MAGIC     customer_id
# MAGIC   LIMIT 5
# MAGIC ) AS source
# MAGIC ON
# MAGIC   target.customer_id = source.customer_id
# MAGIC WHEN MATCHED THEN UPDATE SET
# MAGIC   target.customer_id = source.customer_id,
# MAGIC   target.invoice_no = source.invoice_no,
# MAGIC   target.quantity = source.quantity,
# MAGIC   target.price = source.price,
# MAGIC   target.invoice_date = current_date
# MAGIC WHEN NOT MATCHED THEN INSERT *

# COMMAND ----------

# DBTITLE 1,Verifying The Data Insertion
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE customer_id > 100;
# MAGIC
# MAGIC -- The output shows customer_id, quantity from 101 to 105 inserted correctly in the table.
# MAGIC -- Thats means MERGE statement inserted the data correctly.

# COMMAND ----------

# DBTITLE 1,Sanity Check Of Data
# MAGIC %sql
# MAGIC SELECT
# MAGIC   MIN(customer_id) AS min_customer_id,
# MAGIC   MAX(customer_id) As max_customer_id,
# MAGIC   count(*) AS total_rows
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv;

# COMMAND ----------

# DBTITLE 1,Checking Delta Table History
# MAGIC %sql
# MAGIC DESCRIBE HISTORY delta_catalog.delta_db.invoices_sv;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 2: Data Type Validation

# COMMAND ----------

# DBTITLE 1,DML Command :- 1 - Using INSERT INTO To Append Data With Incorrect Type Of Input(String instead Int)
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   VALUES ('abc', 'I12345', 10, 100, '2022-01-01');
# MAGIC
# MAGIC -- This Code will throw error, because first value should be int or else string containing integers(i.e '12345').

# COMMAND ----------

# DBTITLE 1,DML Command :- 2 - Using INSERT INTO To Append Data With Incorrect Type Of Input(String instead Int)
# MAGIC %sql
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   VALUES ('12345', 'I12345', 10, 100, '2022-01-01');
# MAGIC
# MAGIC -- This Works because delta tries to convert the provided value to cooresponding data type of the column(here int), -- So, here string '12345' can be casted to int and '2022-01-01' can be casted to date.
# MAGIC -- But if you try to insert a value that can't be converted to cooresponding data type of the column, it will throw an error, as shown on above cell as well.

# COMMAND ----------

# DBTITLE 1,Verifying The Data Insertion
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE
# MAGIC   customer_id = 12345;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 3: Column Name Validation

# COMMAND ----------

# DBTITLE 1,Using INSERT INTO To Append Data And Verify Column Name Validation
# MAGIC %sql
# MAGIC -- This works.
# MAGIC -- invoices_s table schema has different columns name then select statement schema.
# MAGIC -- invoices_sv table schema = customer_id, invoice_no, quantity, price, invoice_date.
# MAGIC -- Again as discusssed above as well, INSERT INTO append data based on position of columns and does not check column name, resulting in data insertion irrespective of what column name is in select.
# MAGIC -- As long as data type of columns matches (Also if possible, tries to cast to appropriate data type), data will be inserted.
# MAGIC
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   SELECT
# MAGIC     customer_id AS c_id,
# MAGIC     invoice_no,
# MAGIC     quantity AS qty,
# MAGIC     price,
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     VALUES(9999, 'I12345', 10, 100, '2022-01-01') 
# MAGIC     AS T(customer_id, invoice_no, quantity, price, invoice_date);

# COMMAND ----------

# DBTITLE 1,INSERT INTO Updated The Records
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE
# MAGIC   customer_id = 9999;

# COMMAND ----------

# DBTITLE 1,Data Consumed In MERGE INTO
# MAGIC %sql
# MAGIC SELECT
# MAGIC     customer_id AS c_id,
# MAGIC     invoice_no,
# MAGIC     quantity AS qty,
# MAGIC     CAST(price AS FLOAT),
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC   ORDER BY
# MAGIC     customer_id desc
# MAGIC   LIMIT 5

# COMMAND ----------

# DBTITLE 1,DML Command :- Using MERGE INTO To Append Data And Verify Column Name Validation - 2
# MAGIC %sql
# MAGIC -- This code throws error.
# MAGIC -- invoices_s table schema has different columns name then select statement schema.
# MAGIC -- invoices_sv table schema = customer_id, invoice_no, quantity, price, invoice_date.
# MAGIC -- Again as discusssed above as well, A MERGE INTO statement appends data based on columns by name rather than position and as the column name itself renamed in select it won't able to match columns while inserting, thus the code throws error.
# MAGIC
# MAGIC MERGE INTO
# MAGIC   delta_catalog.delta_db.invoices_sv AS target
# MAGIC USING (
# MAGIC   SELECT
# MAGIC     customer_id AS c_id,
# MAGIC     invoice_no,
# MAGIC     quantity AS qty,
# MAGIC     CAST(price AS FLOAT),
# MAGIC     invoice_date
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC   ORDER BY
# MAGIC     customer_id desc
# MAGIC   LIMIT 5
# MAGIC ) AS source
# MAGIC ON
# MAGIC   target.customer_id = source.c_id
# MAGIC WHEN MATCHED THEN UPDATE SET
# MAGIC   target.customer_id = source.c_id,
# MAGIC   target.invoice_no = source.invoice_no,
# MAGIC   target.quantity = source.qty,
# MAGIC   target.price = source.price,
# MAGIC   target.invoice_date = current_date
# MAGIC WHEN NOT MATCHED THEN INSERT *

# COMMAND ----------

# DBTITLE 1,Verifying The Data Insertion
# MAGIC %sql
# MAGIC -- The query result won't contain the records from 196 to 200 in the table.
# MAGIC -- Explained in cell above.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE
# MAGIC   customer_id BETWEEN 196 AND 200;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 4: Nullability Validation

# COMMAND ----------

# DBTITLE 1,DML Command :- Nullability Validation - 1
# MAGIC %sql
# MAGIC -- Throws error, because customer_id is not nullable in the table schema and constraint is violated for column customer_id.
# MAGIC
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   VALUES (NULL,NULL, NULL, NULL,NULL);

# COMMAND ----------

# DBTITLE 1,DML Command :- Nullability Validation - 2
# MAGIC %sql
# MAGIC -- This works because customer_id is the only column that has non nullable in the table schema.
# MAGIC
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   VALUES (79123, NULL, NULL, NULL, NULL);

# COMMAND ----------

# DBTITLE 1,Verifying The Data Insertion
# MAGIC %sql
# MAGIC -- returns 1 row as expected.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE
# MAGIC   customer_id = 79123;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Scenario 4: Extra Columns Validation

# COMMAND ----------

# DBTITLE 1,DML Command :- Using INSERT INTO To Append Data And Verify Extra Columns Validation
# MAGIC %sql
# MAGIC -- This Cell throws error, because customer_type is not a column in invoices_sv table schema.
# MAGIC
# MAGIC INSERT INTO delta_catalog.delta_db.invoices_sv
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     quantity,
# MAGIC     price,
# MAGIC     invoice_date,
# MAGIC     "VIP" AS customer_type -- This column is not present in invoices_sv table schema.
# MAGIC   FROM
# MAGIC     VALUES(9999, 'I12345', 10, 100, '2022-01-01') 
# MAGIC     AS T(customer_id, invoice_no, quantity, price, invoice_date);

# COMMAND ----------

# DBTITLE 1,Data Consumed In MERGE INTO
# MAGIC %sql
# MAGIC SELECT
# MAGIC   customer_id,
# MAGIC   invoice_no,
# MAGIC   quantity,
# MAGIC   CAST(price AS FLOAT),
# MAGIC   invoice_date,
# MAGIC   "VIP" AS customer_type -- This column is not present in invoices_sv table schema.
# MAGIC FROM
# MAGIC   PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC WHERE 
# MAGIC   customer_id BETWEEN 150 AND 155

# COMMAND ----------

# DBTITLE 1,DML Command :- Using MERGE INTO To Append Data And Verify Extra Columns Validation
# MAGIC %sql
# MAGIC -- Now, this cell doesn't throw error, but only inserts the data for columns present in invoices_sv table schema and doesn't insert the additional column customer_type.
# MAGIC
# MAGIC MERGE INTO
# MAGIC   delta_catalog.delta_db.invoices_sv AS target
# MAGIC USING (
# MAGIC   SELECT
# MAGIC     customer_id,
# MAGIC     invoice_no,
# MAGIC     quantity,
# MAGIC     CAST(price AS FLOAT),
# MAGIC     invoice_date,
# MAGIC     "VIP" AS customer_type -- This column is not present in invoices_sv table schema.
# MAGIC   FROM
# MAGIC     PARQUET.`abfss://dalta-lake-lab-sacc-container@daltalakelabstorageacc.dfs.core.windows.net/invoices/invoices_101_200.parquet`
# MAGIC   WHERE
# MAGIC     customer_id BETWEEN 150 AND 155
# MAGIC ) AS source
# MAGIC ON
# MAGIC   target.customer_id = source.customer_id
# MAGIC WHEN MATCHED THEN UPDATE SET
# MAGIC   target.customer_id = source.customer_id,
# MAGIC   target.invoice_no = source.invoice_no,
# MAGIC   target.quantity = source.quantity,
# MAGIC   target.price = source.price,
# MAGIC   target.invoice_date = current_date
# MAGIC WHEN NOT MATCHED THEN INSERT *

# COMMAND ----------

# DBTITLE 1,Verifying The Data Insertion
# MAGIC %sql
# MAGIC -- returns inserted 6 row, but not the additonal column customer_type.
# MAGIC
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv
# MAGIC WHERE
# MAGIC   customer_id BETWEEN 150 AND 155;

# COMMAND ----------

# DBTITLE 1,Sanity Check Of Data
# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv;
# MAGIC
# MAGIC SELECT
# MAGIC   MIN(customer_id) AS min_customer_id,
# MAGIC   MAX(customer_id) As max_customer_id,
# MAGIC   count(*) AS total_rows
# MAGIC FROM
# MAGIC   delta_catalog.delta_db.invoices_sv;
