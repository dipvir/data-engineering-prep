# Databricks notebook source
# MAGIC %md
# MAGIC ### Note :- I am following Ansh Lamba SQL Course on YT, And he is using MYSQL database.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q1.What is a Database, and how does it function in a production environment?
# MAGIC
# MAGIC #### **1. Core Definition**
# MAGIC
# MAGIC A **Database** is an organized, electronic collection of structured or unstructured data stored and accessed digitally from a computer system. Instead of saving data in scattered, flat text files (like Excel sheets or CSVs), a database uses a specialized software suite called a **DBMS (Database Management System)** to manage data security, concurrent user access, data integrity, and fast retrieval.
# MAGIC
# MAGIC #### **2. The Two Primary Database Categories (with Production Examples)**
# MAGIC
# MAGIC ##### **A. Relational Databases (RDBMS / SQL)**
# MAGIC
# MAGIC * **How it works:** Data is strictly organized into two-dimensional tables with rows and columns. Tables are linked together using relational keys (Primary and Foreign keys), and queries are written in structured query language (SQL). They strictly enforce **ACID properties** to guarantee absolute transactional reliability.
# MAGIC * **Best Used For:** Standard transaction-heavy business systems (OLTP) where data accuracy is critical (e.g., banking, e-commerce checkouts).
# MAGIC * **Production Tool Examples:** PostgreSQL, MySQL, Oracle DB, Microsoft SQL Server.
# MAGIC
# MAGIC ##### **B. Non-Relational Databases (NoSQL)**
# MAGIC
# MAGIC * **How it works:** Data does not follow a rigid tabular schema. Instead, it is stored using flexible design structures like Key-Value pairs, JSON Documents, Wide-Columns, or Graph networks. They favor speed and massive horizontal scalability over strict relational rules.
# MAGIC * **Best Used For:** High-velocity, semi-structured or unstructured big data workloads (e.g., live chat history, real-time user profiles, social media connections).
# MAGIC * **Production Tool Examples:** MongoDB (Document), Cassandra (Wide-Column), Redis (Key-Value), Neo4j (Graph).
# MAGIC
# MAGIC #### **3. The Practical Difference: Spreadsheet vs. Database**
# MAGIC
# MAGIC | Feature | Spreadsheet (Excel / CSV) | Production Database (DBMS) |
# MAGIC | --- | --- | --- |
# MAGIC | **Data Size** | Breaks down or lags heavily with large volumes (~1 million rows). | Easily handles millions to billions of data rows. |
# MAGIC | **Concurrency** | If multiple users edit a file simultaneously, changes overwrite or lock. | Hundreds of users can read and write data at the exact same millisecond. |
# MAGIC | **Data Integrity** | Anyone can type text into a date column by accident. | Enforces strict data types and constraints, instantly rejecting corrupt input. |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q2.What is SQL, and why is it used? (Summarized)
# MAGIC
# MAGIC #### **1. What is SQL?**
# MAGIC
# MAGIC **SQL** (Structured Query Language) is the standard programming language used to communicate with, manage, and query data inside **Relational Databases** (like PostgreSQL or MySQL) and modern **Cloud Data Warehouses** (like Snowflake or BigQuery).
# MAGIC
# MAGIC It is a **declarative** language: you only specify *what* data you want, and the database engine handles the complex work of figure out *how* to fetch it.
# MAGIC
# MAGIC #### **2. Why SQL? (Key Reasons)**
# MAGIC
# MAGIC * **Universal Standard:** It is the undisputed global language of data. Whether you are using a traditional database, cloud storage, or Big Data engines like Apache Spark (via Spark SQL), the same core SQL knowledge applies everywhere.
# MAGIC * **Decades of Optimization:** Built-in database optimizers automatically rewrite your SQL queries to run as fast and efficiently as possible, saving memory and CPU power under the hood.
# MAGIC * **Simplifies Data Pipelines (ETL):** It allows you to filter, join, and aggregate millions of rows of data cleanly with just a few lines of code, replacing complex programming logic.
# MAGIC * **Connects Engineering to Business:** Because SQL is used by business analysts, data scientists, and BI tools (like PowerBI and Tableau), it acts as the bridge for sharing clean data across the entire company.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q3.What are DDL Commands in SQL, and how do they control database architecture?
# MAGIC
# MAGIC #### **1. Core Definition**
# MAGIC
# MAGIC **DDL** stands for **Data Definition Language**. DDL commands form the architectural layer of SQL. They are used explicitly to **create, modify, and destroy the structural blueprints of database objects** (such as databases, schemas, tables, views, indexes, and constraints).
# MAGIC
# MAGIC Unlike DML commands—which manipulate the internal data rows—DDL commands define the rules, columns, data types, and structural containers that hold those rows.
# MAGIC
# MAGIC > **Interview Tip (The Auto-Commit Rule):** In almost all standard relational database management systems (like MySQL and Oracle SQL), DDL commands are **instantly auto-committed**. This means that the moment a DDL query is executed, the changes are written permanently to the database dictionary disk and cannot be reversed with a `ROLLBACK` command.
# MAGIC
# MAGIC ---
# MAGIC #### **2. DDL Commands Reference List (MySQL)**
# MAGIC
# MAGIC | Command | Target Object | Purpose | Auto-Committed? |
# MAGIC | --- | --- | --- | --- |
# MAGIC | **`CREATE`** | `DATABASE` / `TABLE` / `INDEX` / `VIEW` | Builds a brand-new database object from scratch. | **Yes** (Instant) |
# MAGIC | **`ALTER`** | `TABLE` | Modifies the structure of an existing table (e.g., `ADD`, `DROP`, or `MODIFY` columns). | **Yes** (Instant) |
# MAGIC | **`DROP`** | `DATABASE` / `TABLE` / `VIEW` | Permanently deletes the entire object container and all data rows inside it from the disk. | **Yes** (Instant) |
# MAGIC | **`TRUNCATE`** | `TABLE` | Instantly wipes out **all rows** inside a table, leaving the structural blueprint completely empty and ready. | **Yes** (Instant) |
# MAGIC | **`RENAME`** | `TABLE` | Changes the name of an existing table to a new name. | **Yes** (Instant) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC
# MAGIC #### **3. Detailed Breakdown of Core DDL Commands**
# MAGIC
# MAGIC ##### **A. `CREATE DATABASE` and `CREATE SCHEMA`**
# MAGIC
# MAGIC Used to initialize the highest-level logical boundaries in your database server before tables are ever created. A database acts as the primary container instance, while a schema acts as a distinct namespace or folder within that database to group related tables together (e.g., separating raw staging tables from production analytics tables).
# MAGIC
# MAGIC ```sql
# MAGIC -- In MySQL, these two commands do the exact same thing under the hood
# MAGIC CREATE DATABASE corporate_data;
# MAGIC CREATE SCHEMA sales_data;
# MAGIC
# MAGIC -- To see them, you will notice both appear in the database list
# MAGIC SHOW DATABASES;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC > ⚠️ **Critical Interview Watch-out:** > While practicing in **MySQL**, `DATABASE` and `SCHEMA` are treated as exact synonyms (running either command simply creates a database).
# MAGIC > However, if an interviewer asks you about this, you must demonstrate cross-platform knowledge: *In standard ANSI SQL architecture (used by PostgreSQL, SQL Server, and Cloud Warehouses like Snowflake), they are nested tiers: a **Database** represents the entire physical instance, which contains multiple **Schemas** (logical folders/namespaces), which then contain the physical **Tables**.*
# MAGIC
# MAGIC ##### **B. `CREATE TABLE` **
# MAGIC
# MAGIC Used to establish a brand-new database object from scratch, explicitly setting up table definitions, columns, exact data types, and primary/foreign key constraints.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE target_sales_data (
# MAGIC     transaction_id INT PRIMARY KEY,
# MAGIC     customer_id INT NOT NULL,
# MAGIC     product_sku VARCHAR(20),
# MAGIC     sale_amount DECIMAL(10, 2),
# MAGIC     transaction_date DATE DEFAULT (CURRENT_DATE)
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **C. `ALTER` (Evolving Architecture)**
# MAGIC
# MAGIC Used to modify the structural design of an existing database container. In production data pipelines, this is heavily used when an upstream source team changes an API payload, forcing you to adjust your data lake schema or target table definitions dynamically.
# MAGIC
# MAGIC ```sql
# MAGIC -- Pattern 1: Injecting a brand-new column into an active production table
# MAGIC ALTER TABLE target_sales_data ADD COLUMN region_code VARCHAR(10);
# MAGIC
# MAGIC -- Pattern 2: Modifying an existing column data type to prevent string truncation
# MAGIC ALTER TABLE target_sales_data ALTER COLUMN product_sku TYPE VARCHAR(50);
# MAGIC
# MAGIC -- Pattern 3: Purging an outdated column completely from the structural layout
# MAGIC ALTER TABLE target_sales_data DROP COLUMN region_code;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **D. `DROP` (Total Destruction)**
# MAGIC
# MAGIC Used to completely erase an entire database object along with its underlying structure, metadata, index references, and **all stored data rows permanently from the disk**. It completely removes the container from the system catalog.
# MAGIC
# MAGIC ```sql
# MAGIC -- This wipes out both the structural container and every row inside it instantly
# MAGIC DROP TABLE target_sales_data;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **E. `TRUNCATE` (Rapid Container Re-initialization)**
# MAGIC
# MAGIC Used to instantly clear out **all rows** from a target table while preserving the empty table structure, column constraints, privileges, and indices intact.
# MAGIC
# MAGIC ```sql
# MAGIC -- Safely clears out data rows while leaving the table structure completely ready for the next ingestion batch
# MAGIC TRUNCATE TABLE target_sales_data;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **4. Advanced System Mechanics: `DROP` vs. `TRUNCATE**`
# MAGIC
# MAGIC Interviewers regularly test candidates on this distinction to see if they understand system-level data storage and logging overhead.
# MAGIC
# MAGIC | Architectural Metric | `DROP` | `TRUNCATE` |
# MAGIC | --- | --- | --- |
# MAGIC | **System Impact** | Destroys the table structure, schemas, mappings, and all data rows. | Keeps the table structure, column mappings, and schemas, but empties the rows. |
# MAGIC | **Memory / Disk Status** | Completely de-allocates all storage space and deletes the table name descriptor from the system registry. | Instantly drops the data blocks and resets the storage pointer back to the beginning of the table container. |
# MAGIC | **Dependent Objects** | Automatically invalidates all dependent views, stored procedures, or foreign keys pointing to it. | Keeps foreign key structural mappings intact (though it may block execution if active child tables contain reference rows). |
# MAGIC | **Primary Use Case** | Used during environment teardowns, schema migrations, or when a data model is completely deprecated. | Used heavily in daily ETL pipelines to clear out temporary staging/loading tables before a fresh batch run. |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC In database engineering, **Integrity** means **Accuracy, Consistency, and Reliability**. It ensures that your data remains completely correct and trustworthy throughout its entire lifecycle, protecting it from accidental corruption, human error, or system bugs.
# MAGIC
# MAGIC Think of it as the **quality control system** for your database. If a database loses its integrity, the data becomes useless garbage.
# MAGIC
# MAGIC To make this completely clear for an interview, database integrity is broken down into **three fundamental types**:
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### **1. Entity Integrity (Row-Level Accuracy)**
# MAGIC
# MAGIC * **The Concept:** Every row in a table must be uniquely identifiable. You cannot have completely duplicate rows, and you cannot have rows that are missing their primary identifier.
# MAGIC * **How it's enforced:** By using a **`PRIMARY KEY`** constraint.
# MAGIC * **Example:** In a company database, two employees can have the exact same name (e.g., "Rahul Sharma"), but they *must* have distinct Employee IDs so the system can tell them apart. The ID column cannot be empty (`NULL`).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### **2. Referential Integrity (Relationship Accuracy)**
# MAGIC
# MAGIC * **The Concept:** Relationships between tables must always remain valid and synchronized. It ensures that a child table cannot reference a parent record that doesn't actually exist (preventing "orphan" data).
# MAGIC * **How it's enforced:** By using a **`FOREIGN KEY`** constraint.
# MAGIC * **Example:** If your `orders` table points to a `customer_id` of `105`, Referential Integrity guarantees that Customer `105` exists in the master `customers` table. It also prevents someone from deleting Customer `105` from the master table while they still have active orders open.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### **3. Domain Integrity (Column-Level Accuracy)**
# MAGIC
# MAGIC * **The Concept:** Every entry in a specific column must fall within a valid range of acceptable values, correct data types, and formatting rules.
# MAGIC * **How it's enforced:** By using **Data Types** (like `INT`, `VARCHAR`, `DATE`), and constraints like **`NOT NULL`**, **`DEFAULT`**, or **`CHECK`**.
# MAGIC * **Example:** If a column is defined as an `INT` for `age`, domain integrity stops a user from typing letters like "abc" into it. If you add a `CHECK (salary > 0)` constraint, it blocks anyone from entering a negative salary by accident.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### **💡 Summary for Your Playbook**
# MAGIC
# MAGIC > Data Integrity means **protecting data from garbage entry**. We use constraints as the gatekeepers to ensure that every `INSERT` or `UPDATE` follows the strict rules of Entity, Referential, and Domain integrity before hitting the physical storage disk.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q4.What are Constraints in SQL, and how do they enforce data integrity in a database?
# MAGIC
# MAGIC #### **1. Core Definition**
# MAGIC
# MAGIC **Constraints** are a set of rules and validation policies enforced directly on a database table's columns at the architectural layer (DDL). Their primary engineering purpose is to **maintain data integrity and accuracy**.
# MAGIC
# MAGIC If any incoming application transaction or manual DML statement (`INSERT`, `UPDATE`) tries to input data that violates these active constraints, the MySQL engine will instantly block the transaction, raise an error, and protect the table from getting corrupted.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **2. The Core SQL Constraints (With Production Examples)**
# MAGIC
# MAGIC ##### **A. `NOT NULL**`
# MAGIC
# MAGIC * **The Rule:** Enforces that a column **cannot accept or store a `NULL` (empty/missing) value**. You must provide a valid data entry for this column during every single record insertion.
# MAGIC * **Production Example:** Every transaction table must have a timestamp; an undated transaction is data corruption.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE orders (
# MAGIC     order_id INT,
# MAGIC     order_timestamp TIMESTAMP NOT NULL
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **B. `UNIQUE**`
# MAGIC
# MAGIC * **The Rule:** Guarantees that every single value stored within this column across all rows must be completely distinct and different from one another.
# MAGIC * **MySQL Nuance:** Unlike a Primary Key, a `UNIQUE` constraint column **can accept a `NULL` value** (in fact, it can accept multiple `NULL` values in MySQL, because `NULL` is treated as an unknown value, not a duplicate value).
# MAGIC * **Production Example:** Storing user profile information where every account must lock onto an individual, unique email address.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE users (
# MAGIC     user_id INT,
# MAGIC     email_id VARCHAR(100) UNIQUE
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **C. `PRIMARY KEY**`
# MAGIC
# MAGIC * **The Rule:** A structural hybrid of **`NOT NULL` and `UNIQUE**`. It uniquely identifies each record in a table. A table can contain **only one** Primary Key, and it cannot contain any duplicate or `NULL` values.
# MAGIC * **Production Example:** Tracking an employee ID or customer account master number.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE employees (
# MAGIC     emp_id INT PRIMARY KEY,
# MAGIC     emp_name VARCHAR(50)
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **D. `FOREIGN KEY` (Referential Integrity)**
# MAGIC
# MAGIC * **The Rule:** A column in a "child" table that points directly to a `PRIMARY KEY` in a "parent" table. It prevents orphans by ensuring you cannot insert a row into the child table if the linking value doesn't exist in the parent table.
# MAGIC * **Production Example:** You cannot place an order for a `customer_id = 999` if Customer 999 does not exist in your master customer list.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE orders (
# MAGIC     order_id INT PRIMARY KEY,
# MAGIC     cust_id INT,
# MAGIC     -- Establishing the linking constraint boundary
# MAGIC     FOREIGN KEY (cust_id) REFERENCES employees(emp_id)
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **E. `DEFAULT**`
# MAGIC
# MAGIC * **The Rule:** Provides a fallback, automated value to a column if an explicit value is omitted or not specified during the `INSERT` operation.
# MAGIC * **Production Example:** Automatically setting an account status to "Active" when a user signs up.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE accounts (
# MAGIC     account_id INT PRIMARY KEY,
# MAGIC     status_flag VARCHAR(15) DEFAULT 'ACTIVE'
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **F. `CHECK**`
# MAGIC
# MAGIC * **The Rule:** Enforces a specific mathematical or logical condition that every data row must satisfy before it is written to the physical storage disk.
# MAGIC * **Production Example:** Ensuring an e-commerce order quantity is never allowed to drop below 1.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE cart_items (
# MAGIC     item_id INT PRIMARY KEY,
# MAGIC     quantity INT,
# MAGIC     CHECK (quantity >= 1)
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **3. High-Yield Interview Question: `PRIMARY KEY` vs. `UNIQUE KEY**`
# MAGIC
# MAGIC | Evaluation Metric | `PRIMARY KEY` | `UNIQUE KEY` |
# MAGIC | --- | --- | --- |
# MAGIC | **Count Per Table** | A table can have **only one** Primary Key constraint. | A table can have **multiple** columns defined with Unique Key constraints. |
# MAGIC | **`NULL` Acceptance** | Strictly **prohibits** `NULL` values. | **Allows** `NULL` entries (MySQL permits multiple `NULL`s). |
# MAGIC | **Index Creation** | Automatically creates a **Clustered Index** under the hood (physically ordering rows on disk). | Automatically creates a **Non-Clustered Index** (a separate lookup structure). |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q6.List of keywords used exclusively when defining, modifying, or handling **Constraints** in MySQL:
# MAGIC
# MAGIC #### **Constraint Keywords Reference List (MySQL)**
# MAGIC
# MAGIC | Keyword | Operational Role | Primary Function |
# MAGIC | --- | --- | --- |
# MAGIC | **`PRIMARY KEY`** | Constraint Type | Uniquely identifies each row in a table; cannot be `NULL`. |
# MAGIC | **`FOREIGN KEY`** | Constraint Type | Establishes a link to a column in another table (Referential Integrity). |
# MAGIC | **`REFERENCES`** | Constraint Definition | Used alongside `FOREIGN KEY` to specify the parent table and column being linked. |
# MAGIC | **`UNIQUE`** | Constraint Type | Ensures all values in a column are distinct, but allows `NULL`s. |
# MAGIC | **`NOT NULL`** | Constraint Type | Prevents a column from accepting or storing blank/missing (`NULL`) values. |
# MAGIC | **`CHECK`** | Constraint Type | Validates that values meet a specific logical condition (e.g., `age >= 18`). |
# MAGIC | **`DEFAULT`** | Column Property | Assigns a fallback value automatically if no value is explicitly provided. |
# MAGIC | **`AUTO_INCREMENT`** | Column Property | Automatically generates a sequential integer for new rows (heavily used on Primary Keys). |
# MAGIC | **`CONSTRAINT`** | Constraint Naming | An optional keyword used to give a custom, recognizable name to a constraint. |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Quick Code Example to See Them in Action:
# MAGIC
# MAGIC This is how you use these specific keywords together in a real MySQL table definition:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE tcs_employees (
# MAGIC     emp_id INT AUTO_INCREMENT,
# MAGIC     email_id VARCHAR(100),
# MAGIC     age INT,
# MAGIC     status_flag VARCHAR(20) DEFAULT 'ACTIVE',
# MAGIC     
# MAGIC     -- Using the CONSTRAINT keyword to give a custom name to our Primary Key
# MAGIC     CONSTRAINT pk_employee_id PRIMARY KEY (emp_id),
# MAGIC     
# MAGIC     -- Using UNIQUE and CHECK keywords
# MAGIC     CONSTRAINT unique_email UNIQUE (email_id),
# MAGIC     CONSTRAINT check_working_age CHECK (age >= 18)
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q7.Case-Insensitivity in MYSQL.
# MAGIC #### 1. SQL Keywords (Always Case-Insensitive)
# MAGIC
# MAGIC All commands, constraints, data types, and built-in functions do not care about casing across **any** database engine (MySQL, PostgreSQL, Oracle, SQL Server).
# MAGIC
# MAGIC ```sql
# MAGIC -- Both of these are identical to the SQL compiler
# MAGIC SELECT * FROM employees WHERE status = 'ACTIVE';
# MAGIC select * from employees where status = 'ACTIVE';
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC > **Best Practice:** In data engineering pipelines, we always write SQL keywords in **UPPERCASE** and identifiers (table/column names) in **lowercase**. It makes complex queries instantly scannable and readable.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 2. Database and Table Names (It Depends on the OS!)
# MAGIC
# MAGIC This is the hidden trap. In MySQL, databases and tables correspond to **actual directories and files** on the underlying hard drive. Because of this, their case sensitivity depends entirely on the Operating System your MySQL server is running on:
# MAGIC
# MAGIC * **Windows:** Windows file paths are case-insensitive. Therefore, table names in MySQL on Windows are **case-insensitive**. (`employees` and `EMPLOYEES` point to the same table).
# MAGIC * **Linux / macOS:** Linux file systems are strictly case-sensitive. Therefore, table names in MySQL on Linux are **strictly case-sensitive**. (`employees` and `EMPLOYEES` are treated as two completely different tables).
# MAGIC
# MAGIC > **Why this matters for Data Engineers:** If you develop your SQL queries on a Windows laptop, you might carelessly mix cases. The exact moment you deploy that code into a production cloud environment (which almost always runs on Linux servers), your data pipeline will instantly crash with a "Table not found" error.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 3. Column Names (Always Case-Insensitive)
# MAGIC
# MAGIC Regardless of the operating system or the database engine, column names are practically always **case-insensitive** in MySQL.
# MAGIC
# MAGIC ```sql
# MAGIC -- MySQL will execute all of these perfectly
# MAGIC SELECT emp_id FROM employees;
# MAGIC SELECT EMP_ID FROM employees;
# MAGIC SELECT Emp_Id FROM employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 4. Data Values (Case-Insensitive by Default in MySQL)
# MAGIC
# MAGIC In MySQL, string comparisons inside a `WHERE` clause are **case-insensitive by default** because of the default character collation (usually `utf8mb4_0900_ai_ci`, where the `_ci` literally stands for **Case Insensitive**).
# MAGIC
# MAGIC ```sql
# MAGIC -- Both queries will return 'Rahul Sharma'
# MAGIC SELECT * FROM employees WHERE emp_name = 'rahul';
# MAGIC SELECT * FROM employees WHERE emp_name = 'RAHUL';
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC *(Note: If you ever need a strict case-sensitive data search in MySQL, you have to explicitly use the `BINARY` keyword, like: `WHERE BINARY emp_name = 'Rahul'`).*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for Your Playbook
# MAGIC
# MAGIC * **Keywords (`SELECT`, `CREATE`, `INT`):** Always case-insensitive everywhere.
# MAGIC * **Table/Database Names:** Case-sensitive on Linux, insensitive on Windows. **Always use lowercase to stay safe.**
# MAGIC * **Column Names:** Case-insensitive.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q8.KEYS IN SQL.
# MAGIC #### 🔑 The Practical MySQL Key Guide
# MAGIC #### **1. UNIQUE KEY**
# MAGIC
# MAGIC * **What it does:** Guarantees that no two rows have the exact same value in the column.
# MAGIC * **The Blueprint Rule:** Unlike a Primary Key, a `UNIQUE KEY` allows `NULL` values. In MySQL, you can actually have multiple rows with `NULL` in a Unique column because MySQL treats each `NULL` as an unknown, distinct value.
# MAGIC * **Capacity:** You can have as many `UNIQUE` columns as you want in a single table.
# MAGIC * **Example:** `email_id` or `phone_number`.
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | emp_id | emp_name | email_id (**UNIQUE KEY**) |
# MAGIC | --- | --- | --- |
# MAGIC | 1 | Rahul Sharma | rahul@tcs.com |
# MAGIC | 2 | Priya Patel | priya@tcs.com |
# MAGIC | 3 | Amit Kumar | *NULL* (Allowed to be blank) |
# MAGIC | 4 | Rohit Singh | *NULL* (Another blank is also allowed) |
# MAGIC
# MAGIC > **❌ The Rejection Action:** If you try to run an `INSERT` statement to add a new employee with the email `rahul@tcs.com`, MySQL will instantly block it and throw an error: *“Duplicate entry 'rahul@tcs.com' for key 'email_id'”*.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **2. PRIMARY KEY**
# MAGIC
# MAGIC * **What it does:** uniquely identifies each record in a table.
# MAGIC * **The Golden Rule:** It is strictly **`NOT NULL` + `UNIQUE**`. It cannot be blank, and it cannot repeat.
# MAGIC * **Capacity:** only **one** Primary Key is allowed per table.
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | **emp_id (PRIMARY KEY)** | emp_name | department |
# MAGIC | --- | --- | --- |
# MAGIC | 101 | Rahul Sharma | Data Engineering |
# MAGIC | 102 | Priya Patel | Cloud Operations |
# MAGIC | 103 | Amit Kumar | Human Resources |
# MAGIC
# MAGIC > **❌ The Rejection Action:** > * If you try to insert a row with `emp_id = 101`, MySQL blocks it because 101 already exists.
# MAGIC > * If you try to insert a row and leave `emp_id` empty (`NULL`), MySQL blocks it because a Primary Key cannot be blank.
# MAGIC > 
# MAGIC > 
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **3. FOREIGN KEY**
# MAGIC
# MAGIC * **What it does:** The connector. It points to a `PRIMARY KEY` in another table to link them together and maintain referential integrity.
# MAGIC * **Example:** `customer_id` inside an `orders` table ensures you can't place an order for a customer who doesn't exist.
# MAGIC
# MAGIC **Master `customers` Table:**
# MAGIC
# MAGIC | **customer_id (PRIMARY KEY)** | customer_name |
# MAGIC | --- | --- |
# MAGIC | **5** | Rahul Sharma |
# MAGIC | **9** | Priya Patel |
# MAGIC
# MAGIC **`orders` Table:**
# MAGIC
# MAGIC | order_id | order_item | **customer_id (FOREIGN KEY)** |
# MAGIC | --- | --- | --- |
# MAGIC | 5001 | Laptop | **5** (Valid! Points back to Rahul) |
# MAGIC | 5002 | Mouse | **9** (Valid! Points back to Priya) |
# MAGIC
# MAGIC > **❌ The Rejection Action:** If you try to insert an order with `customer_id = 12`, MySQL will block it because Customer `12` does not exist in your master customer list.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **4. CANDIDATE KEY**
# MAGIC
# MAGIC * **What it does:** This is a conceptual design term. Any column, or set of columns, that qualifies or has the capability to uniquely identify a record. A table can have multiple Candidate Keys. Primary Key is chosen from Candidate Keys.
# MAGIC * **How it relates:** If a table has `emp_id` and `pan_card`, both are Candidate Keys. You choose one (e.g., `emp_id`) to be the official `PRIMARY KEY`, and you put a `UNIQUE KEY` constraint on the other (`pan_card`).
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | emp_id (Chosen Primary Key) | pan_card (**Candidate Key**) | aadhaar_no (**Candidate Key**) |
# MAGIC | --- | --- | --- |
# MAGIC | 1 | ABCDE1234F | 1234-5678-9012 |
# MAGIC | 2 | XYZWR5678G | 9876-5432-1098 |
# MAGIC
# MAGIC > **💡 The Design Choice:** Both `pan_card` and `aadhaar_no` are perfectly unique. The database designer simply chose `emp_id` as the official Primary Key, and set `pan_card` and `aadhaar_no` as `UNIQUE KEY` columns to protect data integrity.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **5. COMPOSITE KEY**
# MAGIC
# MAGIC * **What it does:** This is when you combine **two or more columns together** to act as your `PRIMARY KEY`. Uniquely identifies a record using a combination of columns.
# MAGIC * **When you need it:** When a single column isn't enough to guarantee uniqueness.
# MAGIC * **Example:** In a `student_attendance` table, `student_id` repeats every day, and `date` repeats for every student. But the combination of `(student_id, date)` is completely unique.
# MAGIC
# MAGIC **The Success `attendance` Table:**
# MAGIC
# MAGIC | student_id | attendance_date | **Composite Key Identity** | status |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 10 | 2026-06-01 | `(10, 2026-06-01)` | Present |
# MAGIC | 10 | 2026-06-02 | `(10, 2026-06-02)` | Present |
# MAGIC | 11 | 2026-06-01 | `(11, 2026-06-01)` | Absent |
# MAGIC
# MAGIC > **❌ The Rejection Action:** If you try to insert a row with `student_id = 10` and `attendance_date = '2026-06-01'`, MySQL blocks it because that *exact combination* already exists in the table.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **6. SURROGATE KEY (Super Important for Data Engineers!)**
# MAGIC
# MAGIC * **What it does:** An artificial key, usually an auto-increment number. Used when natural keys are inconvenient or too long. It has no real-world business meaning and is built purely for database optimization.
# MAGIC * **How it's made:** In MySQL, we create this using the `AUTO_INCREMENT` property.
# MAGIC * **Why we use it:** Imagine a `products` table. Instead of using a long, messy, alphanumeric text string like the manufacturer's serial number (`PROD-XYZ-99882-BLU`) as the Primary Key, we create a clean, simple integer Surrogate Key called `product_id` (like `1`). Integers are vastly faster for the database to index and join on than long text strings!
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | **product_id (SURROGATE KEY)** | manufacturer_serial_no (Natural Text Key) | product_name |
# MAGIC | --- | --- | --- |
# MAGIC | **1** (Auto-Created) | PROD-XYZ-99882-BLU-LARGE | Dell Monitor |
# MAGIC | **2** (Auto-Created) | PROD-ABC-11223-BLK-SMALL | HP Keyboard |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q9.What are CHARACTER SET and COLLATION in Databases, and why do they matter?
# MAGIC
# MAGIC To understand these two concepts, use this simple layman analogy:
# MAGIC
# MAGIC * **CHARACTER SET (The Alphabet):** The dictionary of characters you are allowed to store. It dictates *what* symbols the database understands.
# MAGIC * **COLLATION (The Rules):** The set of rules used to compare, sort, and match those characters. It dictates *how* the database orders and searches data.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 1. CHARACTER SET (Charset)
# MAGIC
# MAGIC A character set defines what characters (alphabets, numbers, emojis, symbols) can be stored in a column, table, or database, and how many bytes it takes to store each one.
# MAGIC
# MAGIC ##### **The Gold Standards in MySQL:**
# MAGIC
# MAGIC * **`latin1` (Old Standard):** Uses 1 byte per character. It can only store Western European characters. If you try to insert a Hindi string or an emoji into a `latin1` column, it will turn into garbled text (like `???` or `Ã¢â`).
# MAGIC * **`utf8mb4` (The Modern Production Standard):** Uses up to 4 bytes per character. It supports the full Unicode character set, including all global languages (Hindi, Japanese, Arabic) and **emojis**.
# MAGIC
# MAGIC > **Data Engineer Rule:** Always use `utf8mb4` for modern data pipelines. Never use the older `utf8` (which is an alias for `utf8mb3` in older MySQL versions) because it cannot store emojis and will crash your pipeline if a user enters a 🌟 or 😂.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 2. COLLATION
# MAGIC
# MAGIC Once the database knows *how* to store characters, it needs rules to compare them when you run `WHERE`, `ORDER BY`, or `JOIN` clauses. Collation defines whether the database is Case-Insensitive or Accent-Insensitive.
# MAGIC
# MAGIC You can instantly identify a collation's behavior by looking at its suffix in MySQL:
# MAGIC
# MAGIC * **`_ci`** = Case Insensitive (`'A'` is treated exactly the same as `'a'`).
# MAGIC * **`_cs`** = Case Sensitive (`'A'` and `'a'` are completely different).
# MAGIC * **`_bin`** = Binary (`'A'` and `'a'` are compared purely by their raw binary/hex values).
# MAGIC
# MAGIC ##### **The Gold Standard Collation:**
# MAGIC
# MAGIC * **`utf8mb4_0900_ai_ci`**: This is the default collation in modern MySQL (8.0+).
# MAGIC * `utf8mb4` $\rightarrow$ The character set it belongs to.
# MAGIC * `0900` $\rightarrow$ Refers to the Unicode Collation Algorithm version 9.0.0.
# MAGIC * `ai` $\rightarrow$ **Accent Insensitive** (treats `'e'`, `'è'`, and `'é'` as the same).
# MAGIC * `ci` $\rightarrow$ **Case Insensitive** (treats `'A'` and `'a'` as the same).
# MAGIC
# MAGIC
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📋 The Success vs. Rejection Impact
# MAGIC
# MAGIC Let's look at how changing your collation completely rewrites the behavior of your SQL queries.
# MAGIC
# MAGIC ##### **Scenario A: Using Case-Insensitive Collation (`utf8mb4_0900_ai_ci`)**
# MAGIC
# MAGIC The database treats variations of the same letter as a match.
# MAGIC
# MAGIC **The Data Table:**
# MAGIC
# MAGIC | emp_id | emp_name |
# MAGIC | --- | --- |
# MAGIC | 1 | Rahul |
# MAGIC
# MAGIC **Query Results:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT * FROM employees WHERE emp_name = 'rahul'; -- ✅ RETURNS ROW 1
# MAGIC SELECT * FROM employees WHERE emp_name = 'RAHUL'; -- ✅ RETURNS ROW 1
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **Scenario B: Using Binary Collation (`utf8mb4_bin`)**
# MAGIC
# MAGIC The database compares the raw binary ASCII values (`'R'` = `0x52`, `'r'` = `0x72`). They must be a 100% exact match.
# MAGIC
# MAGIC **The Data Table:**
# MAGIC
# MAGIC | emp_id | emp_name |
# MAGIC | --- | --- |
# MAGIC | 1 | Rahul |
# MAGIC
# MAGIC **Query Results:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT * FROM employees WHERE emp_name = 'rahul'; -- ❌ RETURNS NOTHING (Mismatched 'R' vs 'r')
# MAGIC SELECT * FROM employees WHERE emp_name = 'Rahul'; -- ✅ RETURNS ROW 1
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💻 How to Write This in DDL Code
# MAGIC
# MAGIC You can set charsets and collations at the Database level, Table level, or down to a specific Column.
# MAGIC
# MAGIC ```sql
# MAGIC -- 1. Setting it at the Database Level
# MAGIC CREATE DATABASE tcs_data_lake
# MAGIC   CHARACTER SET utf8mb4
# MAGIC   COLLATE utf8mb4_0900_ai_ci;
# MAGIC
# MAGIC -- 2. Setting it at the Table Level
# MAGIC CREATE TABLE user_profiles (
# MAGIC     user_id INT PRIMARY KEY,
# MAGIC     bio VARCHAR(255)
# MAGIC ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
# MAGIC
# MAGIC -- 3. Overriding it at a specific Column Level (Great for passwords or unique codes)
# MAGIC CREATE TABLE secure_login (
# MAGIC     username VARCHAR(50),
# MAGIC     -- Forcing the token to be strictly case-sensitive using binary collation
# MAGIC     session_token VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Why this is a Critical Data Engineering Trap
# MAGIC
# MAGIC 1. **Performance Bottlenecks:** If you try to `JOIN` two tables on a text column (like `customer_id`), and Table A uses `latin1` while Table B uses `utf8mb4`, MySQL cannot use the database indexes. It forces an on-the-fly internal data conversion for millions of rows, slowing your query down to a crawl.
# MAGIC 2. **Cloud Migration Errors:** If you develop locally on a database with one collation and push code to a cloud environment (AWS RDS / Azure SQL) with a different default collation, your string sorting and match metrics will completely change, breaking reports.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q10.What are CHARACTER SET and COLLATION, and do they apply to Modern Big Data Systems?
# MAGIC
# MAGIC #### 📌 Core Concept Definition
# MAGIC
# MAGIC * **Character Set:** Defines the allowed symbols, alphabets, and their binary numeric encodings (how text is **stored** on disk).
# MAGIC * **Collation:** A specific set of rules used to compare, match, and sort those characters (how text is **evaluated**, e.g., case-insensitivity or accent-insensitivity).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🚀 Application in the Big Data Landscape (Spark & Delta Lake)
# MAGIC
# MAGIC * **Historical Context:** Originally developed for traditional RDBMS (MySQL, SQL Server, PostgreSQL) to handle localized text sorting and searching.
# MAGIC * **Modern Reality:** Modern lakehouses like **Apache Spark** and **Databricks Delta Lake** support native Collations. It is no longer just an RDBMS concept.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🛠️ Why it Matters for Performance Tuning
# MAGIC
# MAGIC Using explicit string manipulation functions in big data engines destroys performance because it hides data patterns from the query optimizer. Native collations completely bypass this bottleneck.
# MAGIC
# MAGIC | Scenario | Code Approach | Execution Behavior | Performance Impact |
# MAGIC | --- | --- | --- | --- |
# MAGIC | **Traditional Big Data Way** | `df.filter(lower(col("name")) == "apple")` | Forces the engine to apply a functional transformation on every single string across billions of rows. | **Slow.** Completely breaks data pruning and forces a heavy full-table scan. |
# MAGIC | **Modern Collation Way** | `name STRING COLLATE UTF8_LCASE` | Defines the column rules at the schema level. Delta Lake handles case-insensitivity natively. | **Fast.** Enables up to **22x faster execution** by allowing Delta to use internal statistics for immediate **File-Skipping**. |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q11.What are Outliers in Data Engineering, and why is handling them critical for data pipelines?
# MAGIC ### CONCEPT: Outlier Detection & Data Cleansing
# MAGIC The word your lead was using is **"Outliers"** (pronounced *out-liars*).
# MAGIC
# MAGIC An **outlier** is a data point that is drastically different from the rest of the data in your dataset. It is an anomaly—either an extreme high or an extreme low value that looks completely out of place compared to the normal pattern.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🪵 A Real-World Woodworking Analogy
# MAGIC
# MAGIC Since you enjoy DIY woodworking, think of it this way:
# MAGIC Imagine you are sorting through a batch of wood fragments to build a wall-mounted folding desk. Most of the planks you cut are around **4 feet to 5 feet** long. But suddenly, you pull out a random fragment that is only **2 inches** long, and another one that is **45 feet** long.
# MAGIC
# MAGIC Those two weird pieces are **outliers**. They don’t fit the normal batch, and if you try to include them without looking, they will ruin your desk measurements.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💻 A Data Engineering Example (Why Your Lead Cared)
# MAGIC
# MAGIC In data pipelines, outliers usually happen because of **system bugs, human entry errors, or extreme fraud**.
# MAGIC
# MAGIC Imagine you are processing an `employees` table or a banking transactions stream:
# MAGIC
# MAGIC | transaction_id | user_id | amount_in_rupees | Type of Data |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 1001 | 45 | 150 | Normal |
# MAGIC | 1002 | 12 | 1,200 | Normal |
# MAGIC | 1003 | 88 | 350 | Normal |
# MAGIC | 1004 | 19 | **9,99,99,999** 😲 | **OUTLIER (Extreme High)** |
# MAGIC | 1005 | 64 | **-5,000** 🤯 | **OUTLIER (Extreme Low / Bug)** |
# MAGIC
# MAGIC ##### **Why your lead was talking about them:**
# MAGIC
# MAGIC If your lead asked you to calculate the **Average Transaction Amount** for a daily report, look at what happens:
# MAGIC
# MAGIC * Without filtering outliers, that single `9,99,99,999` row will skew the average, making it look like the normal user spends lakhs of rupees per day. The report becomes useless.
# MAGIC * The negative `-5,000` value could break downstream financial calculations because a transaction amount shouldn't be negative.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🛠️ What Data Engineers Do With Outliers
# MAGIC
# MAGIC When your lead flags outliers, they want you to handle them in your pipeline (using PySpark, SQL, or Databricks) in one of three ways:
# MAGIC
# MAGIC 1. **Drop them:** Filter them out completely (`WHERE amount_in_rupees > 0 AND amount_in_rupees < 100000`).
# MAGIC 2. **Cap them (Winsorization):** If a value is too high, automatically reset it to a maximum allowable threshold.
# MAGIC 3. **Isolate them:** Route them to an "Error/Audit Table" so the business team can investigate if it's a system glitch or fraud.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q12.What is the logical execution order of a SQL query, and why does it differ from the written syntax()?
# MAGIC ### CONCEPT: SQL Query Execution Flow
# MAGIC When you write a SQL query, you write it for human readability. But when the database engine executes it, it needs to pull the data from disk first, filter it, group it, and only then format the output.
# MAGIC
# MAGIC #### 🏃‍♂️ The 8-Step Execution Lifecycle
# MAGIC
# MAGIC Here is the exact sequential order in which the database engine executes a query:
# MAGIC
# MAGIC 1. **`FROM` / `JOIN`:** The engine goes to the hard drive and loads the base tables. If there are joins, it merges the tables together in memory first.
# MAGIC 2. **`WHERE`:** It filters out individual raw rows that don't match the condition (this happens *before* any data aggregation).
# MAGIC 3. **`GROUP BY`:** It collapses the remaining rows into buckets based on the specified column(s).
# MAGIC 4. **`HAVING`:** It filters the aggregated groups (this works exactly like a `WHERE` clause, but it only applies to grouped data).
# MAGIC 5. **`SELECT`:** It finally looks at the columns you actually asked for and evaluates any analytical expressions or functions (like `COUNT()` or `AVG()`).
# MAGIC 6. **`DISTINCT`:** It removes any duplicate rows from the selected output.
# MAGIC 7. **`ORDER BY`:** It sorts the final result set (ascending or descending).
# MAGIC 8. **`LIMIT` / `OFFSET`:** It clips the output to return only the requested number of rows.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📋 A Real-World Data Pipeline Example
# MAGIC
# MAGIC Imagine you are running a report on an `orders` table to find cities that generated more than ₹50,000 in revenue, sorted from highest to lowest, but you only want the top 3 cities.
# MAGIC
# MAGIC ##### **How you WRITE the query:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT city, SUM(amount) AS total_revenue   -- Written 1st
# MAGIC FROM orders                                 -- Written 2nd
# MAGIC WHERE status = 'DELIVERED'                  -- Written 3rd
# MAGIC GROUP BY city                               -- Written 4th
# MAGIC HAVING SUM(amount) > 50000                  -- Written 5th
# MAGIC ORDER BY total_revenue DESC                 -- Written 6th
# MAGIC LIMIT 3;                                    -- Written 7th
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **How the Database ENGINE actually runs it:**
# MAGIC
# MAGIC * **Step 1 (`FROM orders`):** The engine pulls the entire `orders` table into memory.
# MAGIC * **Step 2 (`WHERE status = 'DELIVERED'`):** It throws away all canceled or pending orders. Only delivered orders remain.
# MAGIC * **Step 3 (`GROUP BY city`):** It groups the remaining orders bucket-by-bucket based on cities (e.g., Nagpur, Mumbai, Pune).
# MAGIC * **Step 4 (`HAVING SUM(amount) > 50000`):** It calculates the sum for each city and drops any city group whose total is less than or equal to ₹50,000.
# MAGIC * **Step 5 (`SELECT city, SUM(amount)...`):** It generates the final two columns you asked for.
# MAGIC * **Step 6 (`ORDER BY total_revenue DESC`):** It sorts those final rows from highest revenue to lowest.
# MAGIC * **Step 7 (`LIMIT 3`):** It chops off everything below the top 3 rows and hands you the result.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ####💡 Why this is a Critical Interview Trap!
# MAGIC
# MAGIC ##### **The Alias Trap**
# MAGIC
# MAGIC An interviewer might show you this broken query and ask why it throws an error:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT city, SUM(amount) AS total_revenue
# MAGIC FROM orders
# MAGIC WHERE total_revenue > 50000 -- ❌ ERROR!
# MAGIC GROUP BY city;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC **Why it fails:** Look at the execution flow! The `WHERE` clause runs in **Step 2**, but the alias `total_revenue` isn't created until the `SELECT` clause runs in **Step 5**. The database engine has no idea what `total_revenue` means yet!
# MAGIC
# MAGIC ##### **Why Order By works with Aliases**
# MAGIC
# MAGIC On the other hand, this query works perfectly:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT city, SUM(amount) AS total_revenue
# MAGIC FROM orders
# MAGIC GROUP BY city
# MAGIC ORDER BY total_revenue DESC; -- ✅ WORKS!
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC **Why it works:** The `ORDER BY` clause runs in **Step 7**, which is *after* the `SELECT` clause (**Step 5**). By the time it sorts, the alias `total_revenue` is fully live and available in memory.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q13.What are the types of joins supported by MySQL, and how do they differ from other database engines?
# MAGIC ### CONCEPT: Joins in MySQL
# MAGIC In MySQL, joins are used to combine rows from two or more tables based on a related column between them. While standard SQL theory talks about 5 or 6 types of joins, MySQL natively implements **4 types** using its execution engine.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🗂️ The Sample Datasets
# MAGIC
# MAGIC To understand how these joins behave, let's use two simple tables: `employees` and `departments`.
# MAGIC
# MAGIC ##### **Table 1: `employees**`
# MAGIC
# MAGIC | emp_id | emp_name | dept_id |
# MAGIC | --- | --- | --- |
# MAGIC | 1 | Rahul | 10 |
# MAGIC | 2 | Priya | 20 |
# MAGIC | 3 | Amit | *NULL* (No department assigned) |
# MAGIC
# MAGIC ##### **Table 2: `departments**`
# MAGIC
# MAGIC | dept_id | dept_name |
# MAGIC | --- | --- |
# MAGIC | 10 | Data Engineering |
# MAGIC | 20 | Cloud Operations |
# MAGIC | 30 | Human Resources |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The 4 Native MySQL Joins with Examples
# MAGIC
# MAGIC ##### **1. INNER JOIN**
# MAGIC
# MAGIC * **What it does:** Returns only the records that have **matching values in both tables**. If a row doesn't have an exact match on both sides, it is completely dropped.
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT e.emp_id, e.emp_name, d.dept_name
# MAGIC FROM employees e
# MAGIC INNER JOIN departments d ON e.dept_id = d.dept_id;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **The Output:**
# MAGIC | emp_id | emp_name | dept_name |
# MAGIC | :--- | :--- | :--- |
# MAGIC | 1 | Rahul | Data Engineering |
# MAGIC | 2 | Priya | Cloud Operations |
# MAGIC *(Note: Amit is dropped because his `dept_id` is NULL, and HR is dropped because no employee matches `dept_id` 30).*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ##### **2. LEFT JOIN (LEFT OUTER JOIN)**
# MAGIC
# MAGIC * **What it does:** Returns **all records from the left table**, and the matched records from the right table. If there is no match, the right side will fill with `NULL`.
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT e.emp_id, e.emp_name, d.dept_name
# MAGIC FROM employees e
# MAGIC LEFT JOIN departments d ON e.dept_id = d.dept_id;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **The Output:**
# MAGIC | emp_id | emp_name | dept_name |
# MAGIC | :--- | :--- | :--- |
# MAGIC | 1 | Rahul | Data Engineering |
# MAGIC | 2 | Priya | Cloud Operations |
# MAGIC | 3 | Amit | **NULL** |
# MAGIC *(Note: Amit is preserved because he belongs to the Left table, even though he has no matching department).*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ##### **3. RIGHT JOIN (RIGHT OUTER JOIN)**
# MAGIC
# MAGIC * **What it does:** Returns **all records from the right table**, and the matched records from the left table. If there is no match, the left side will fill with `NULL`.
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT e.emp_id, e.emp_name, d.dept_name
# MAGIC FROM employees e
# MAGIC RIGHT JOIN departments d ON e.dept_id = d.dept_id;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **The Output:**
# MAGIC | emp_id | emp_name | dept_name |
# MAGIC | :--- | :--- | :--- |
# MAGIC | 1 | Rahul | Data Engineering |
# MAGIC | 2 | Priya | Cloud Operations |
# MAGIC | **NULL** | **NULL** | Human Resources |
# MAGIC *(Note: HR is preserved because it belongs to the Right table, even though no employee works there).*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ##### **4. CROSS JOIN (Cartesian Product)**
# MAGIC
# MAGIC * **What it does:** Joins **every single row** of the first table with **every single row** of the second table. No `ON` filtering clause is used. Since we have 3 employees and 3 departments, this results in 3 times 3 = 9 rows.
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT e.emp_name, d.dept_name
# MAGIC FROM employees e
# MAGIC CROSS JOIN departments d;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **The Partial Output:**
# MAGIC | emp_name | dept_name |
# MAGIC | :--- | :--- |
# MAGIC | Rahul | Data Engineering |
# MAGIC | Rahul | Cloud Operations |
# MAGIC | Rahul | Human Resources |
# MAGIC | Priya | Data Engineering |
# MAGIC | ... *(continues for all 9 combinations)* | |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### ⚠️ The Data Engineering Interview Workaround: FULL OUTER JOIN
# MAGIC
# MAGIC Because **MySQL DOES NOT natively support `FULL OUTER JOIN**`, trying to use that keyword will throw a syntax error.
# MAGIC
# MAGIC To get all employees (including those without departments) AND all departments (including those without employees) in a single result set, you must write a `LEFT JOIN` and a `RIGHT JOIN`, then stitch them together using **`UNION`**.
# MAGIC
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT e.emp_id, e.emp_name, d.dept_name
# MAGIC FROM employees e
# MAGIC LEFT JOIN departments d ON e.dept_id = d.dept_id
# MAGIC
# MAGIC UNION
# MAGIC
# MAGIC SELECT e.emp_id, e.emp_name, d.dept_name
# MAGIC FROM employees e
# MAGIC RIGHT JOIN departments d ON e.dept_id = d.dept_id;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **The Output:**
# MAGIC | emp_id | emp_name | dept_name |
# MAGIC | :--- | :--- | :--- |
# MAGIC | 1 | Rahul | Data Engineering |
# MAGIC | 2 | Priya | Cloud Operations |
# MAGIC | 3 | Amit | **NULL** |
# MAGIC | **NULL** | **NULL** | Human Resources |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for your Notes
# MAGIC
# MAGIC > MySQL natively supports **4 Joins**: `INNER`, `LEFT`, `RIGHT`, and `CROSS`. To achieve a `FULL OUTER JOIN` layout, you must manually run a `LEFT JOIN` and a `RIGHT JOIN` bound together by a `UNION` operator. This deduplicates identical rows and safely builds a complete outer matrix.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q14.What are DML commands in SQL, and how do they differ from DDL commands?
# MAGIC ### CONCEPT: DML Commands in SQL
# MAGIC While **DDL (Data Definition Language)** is used to build or modify the empty structure of a database (like creating columns or setting constraints), **DML (Data Manipulation Language)** is used to manage the actual data *inside* those rows. DML allows you to insert, modify, and delete the actual records.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🗂️ The Baseline Table: `employees`
# MAGIC
# MAGIC To see how these commands change data, let's assume we start with an empty table or a basic setup.
# MAGIC
# MAGIC | emp_id | emp_name | salary | city |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 1 | Rahul | 60000 | Nagpur |
# MAGIC | 2 | Priya | 75000 | Pune |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The 3 Core DML Commands with Examples
# MAGIC
# MAGIC ##### **1. INSERT**
# MAGIC
# MAGIC * **What it does:** Adds brand-new rows of data into an existing table.
# MAGIC * **Layman Heading:** **Adding New Records**
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC INSERT INTO employees (emp_id, emp_name, salary, city)
# MAGIC VALUES (3, 'Amit', 50000, 'Mumbai');
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | emp_id | emp_name | salary | city |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 1 | Rahul | 60000 | Nagpur |
# MAGIC | 2 | Priya | 75000 | Pune |
# MAGIC | **3** | **Amit** | **50000** | **Mumbai** |
# MAGIC
# MAGIC > **❌ The Rejection Action:** If you try to run an `INSERT` statement but miss a column that has a `NOT NULL` constraint (and doesn't have a default value), MySQL will instantly reject it with an error: *"Field 'column_name' doesn't have a default value"*.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ##### **2. UPDATE**
# MAGIC
# MAGIC * **What it does:** Modifies existing data already sitting inside the table.
# MAGIC * **Layman Heading:** **Editing Existing Records**
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC UPDATE employees
# MAGIC SET salary = 65000, city = 'Nagpur'
# MAGIC WHERE emp_id = 1;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | emp_id | emp_name | salary | city |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 1 | Rahul | **65000** | **Nagpur** |
# MAGIC | 2 | Priya | 75000 | Pune |
# MAGIC | 3 | Amit | 50000 | Mumbai |
# MAGIC
# MAGIC > **⚠️ The Critical Data Engineering Trap:** If you forget to write the `WHERE` clause in an `UPDATE` statement, MySQL will update **every single row** in the table! Everyone's salary would instantly become 65,000. Always double-check your `WHERE` condition before running an update in production.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ##### **3. DELETE**
# MAGIC
# MAGIC * **What it does:** Removes specific rows from the table based on a condition.
# MAGIC * **Layman Heading:** **Removing Records**
# MAGIC * **The Code:**
# MAGIC
# MAGIC ```sql
# MAGIC DELETE FROM employees
# MAGIC WHERE emp_id = 3;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC **The Success Table:**
# MAGIC
# MAGIC | emp_id | emp_name | salary | city |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 1 | Rahul | 65000 | Nagpur |
# MAGIC | 2 | Priya | 75000 | Pune |
# MAGIC | *(Row 3 has been completely removed).* |  |  |  |
# MAGIC
# MAGIC > **⚠️ The Where Clause Trap:** Just like `UPDATE`, if you execute `DELETE FROM employees;` without a `WHERE` clause, MySQL will wipe out **all rows** from your table, leaving you with a completely blank dataset (though the empty column structure will remain intact).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 The Big Interview Question: DELETE vs. TRUNCATE
# MAGIC
# MAGIC Interviewers absolutely love asking this to catch Data Engineers off-guard because both commands remove data.
# MAGIC
# MAGIC [Image comparing delete and truncate commands in sql showing row by row removal vs page deallocation]
# MAGIC
# MAGIC | Feature | `DELETE` (DML) | `TRUNCATE` (DDL) |
# MAGIC | --- | --- | --- |
# MAGIC | **Type** | Data Manipulation Language | Data Definition Language |
# MAGIC | **Speed** | **Slower.** It deletes rows one-by-one and records each delete in the system log. | **Blazing Fast.** It drops the entire table page underneath and recreates an empty table structure. |
# MAGIC | **Where Clause** | **Allowed.** You can filter exactly which rows to delete. | **Not Allowed.** It is an all-or-nothing wipe. You cannot filter. |
# MAGIC | **Rollback (Undo)** | **Yes.** Since it logs row-by-row, you can roll it back if ran inside a transaction. | **No (Usually).** It commits instantly, making it incredibly hard to recover without backups. |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for your Notes
# MAGIC
# MAGIC > DML commands (`INSERT`, `UPDATE`, `DELETE`) deal purely with row-level records inside the database matrix. Unlike DDL operations which auto-commit and alter table anatomy, DML adjustments are transactional and strictly require precise `WHERE` clauses to prevent accidental table-wide modifications.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q15.How do we manipulate data formats on-the-fly, and what are the optimal ways to evaluate conditional logic in SQL?
# MAGIC ### CONCEPT: Data Transformations & Conditionals in SQL
# MAGIC Data transformation involves modifying raw values (strings, numbers, dates) into a cleaned, standard format during query execution. Conditionals allow the database engine to apply `IF-THEN-ELSE` logical routing directly within data streams.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔀 1. SQL Conditionals: The `CASE WHEN` Standard
# MAGIC
# MAGIC The `CASE` statement is SQL's native conditional expression. It acts exactly like an `if-elif-else` block in Python or an `IF` statement in Excel.
# MAGIC
# MAGIC #### **The Golden Rules of `CASE WHEN` Optimization:**
# MAGIC
# MAGIC * **Sequential Evaluation:** The database engine reads `WHEN` conditions from **top to bottom**. The moment it finds a condition that evaluates to `TRUE`, it returns the result and stops checking the rest.
# MAGIC * **The Performance Trick:** Always place your **most frequently occurring condition at the very top**. If 90% of your data falls under one bucket, checking that first saves the engine from wasting CPU cycles evaluating the remaining conditions for millions of rows.
# MAGIC
# MAGIC #### **The Production Syntax:**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC     emp_name,
# MAGIC     salary,
# MAGIC     CASE 
# MAGIC         WHEN salary >= 100000 THEN 'Tier 1 - Leadership'
# MAGIC         WHEN salary >= 70000 THEN 'Tier 2 - Senior/Lead'
# MAGIC         ELSE 'Tier 3 - Associate'
# MAGIC     END AS employee_bracket
# MAGIC FROM employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC > **⚠️ The Missing `ELSE` Trap:** If you don't provide an explicit `ELSE` clause and none of the `WHEN` conditions are met, SQL will automatically output a **`NULL`**. Always include an `ELSE` statement as a safety net to catch outliers or unmapped data.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🦺 2. High-Value Conditional Functions (Handling `NULL`s)
# MAGIC
# MAGIC Data engineers spend half their lives dealing with missing or `NULL` data. Two primary transformation functions handle this cleanly:
# MAGIC
# MAGIC #### **A. `IFNULL(column, fallback_value)**`
# MAGIC
# MAGIC * **What it does:** Checks if a value is `NULL`. If it is, it replaces it with your fallback value. If it isn't, it leaves it alone.
# MAGIC * **Syntax:** `SELECT IFNULL(commission, 0) FROM sales;`
# MAGIC
# MAGIC #### **B. `COALESCE(val1, val2, val3, ...)**`
# MAGIC
# MAGIC * **What it does:** A highly advanced version of `IFNULL`. It accepts a list of arguments and returns the **very first non-NULL value** it encounters from left to right.
# MAGIC * **Syntax:** `SELECT COALESCE(personal_email, work_email, 'No Email Found') FROM users;`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔤 3. Core String & Data Transformations
# MAGIC
# MAGIC When pulling data from source systems, text fields are often messy (mixed casing, extra spaces, wrong lengths).
# MAGIC
# MAGIC Here are the primary transformation tools you use to sanitize data columns:
# MAGIC
# MAGIC | Function | What it Does | Real-World Pipeline Use Case |
# MAGIC | --- | --- | --- |
# MAGIC | **`CONCAT(str1, str2)`** | Glues text strings together. | Merging `first_name` and `last_name` into `full_name`. |
# MAGIC | **`LOWER()` / `UPPER()**` | Enforces consistent text casing. | Standardizing email fields so `User@Tcs.com` matches `user@tcs.com`. |
# MAGIC | **`TRIM()`** | Strips out leading and trailing whitespaces. | Cleaning up text fields typed by users with accidental space bar hits. |
# MAGIC | **`SUBSTRING(str, pos, len)`** | Extracts a specific slice of text from a string. | Pulling the area code out of a full phone number string. |
# MAGIC
# MAGIC #### **Combined Transformation Example:**
# MAGIC
# MAGIC ```sql
# MAGIC -- Cleaning up messy user names and generating a clean profile tag
# MAGIC SELECT 
# MAGIC     CONCAT(UPPER(TRIM(emp_name)), ' - ', LOWER(city)) AS formatted_profile 
# MAGIC FROM employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Summary for your Notes
# MAGIC
# MAGIC > **Transformations** allow data engineers to scrub and standardize raw fields on-the-fly, while **Conditionals (`CASE WHEN`)** act as logical gateways. In high-volume pipelines, order your `CASE` conditions by data density (highest frequency first) and always defend against unexpected missing records by concluding with a robust `ELSE` fallback or a `COALESCE` layer.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q16.What are Window Functions, and how do they differ from regular aggregate functions with `GROUP BY`?
# MAGIC ### CONCEPT: Window Functions in SQL
# MAGIC A **Window Function** performs a calculation across a set of table rows that are somehow related to the current row.
# MAGIC
# MAGIC Unlike a regular `GROUP BY` clause—which collapses your distinct rows into a single summary row—a Window Function retains the identity of **every single individual row** in the final output while appending the calculated aggregate value next to it.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧬 The Anatomy of a Window Function
# MAGIC
# MAGIC Every window function follows a standard blueprint using the **`OVER()`** clause:
# MAGIC
# MAGIC ```sql
# MAGIC FUNCTION() OVER (
# MAGIC     PARTITION BY <column_names>
# MAGIC     ORDER BY <column_names>
# MAGIC     <WINDOW_FRAME_CLAUSE>
# MAGIC )
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC #### **The Core Engine Controls:**
# MAGIC
# MAGIC 1. **`PARTITION BY`:** Divides the rows into logical groups or "buckets" (like departments or countries). The calculation restarts from scratch for each bucket. If omitted, the entire table is treated as one giant bucket.
# MAGIC 2. **`ORDER BY`:** Sorts the rows *inside* each partition. This is mandatory for running totals or ranking functions.
# MAGIC 3. **`WINDOW_FRAME_CLAUSE`:** (Like `ROWS BETWEEN...`) Fine-tunes the moving sub-window relative to the current row.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🛠️ The 3 Main Families of Window Functions
# MAGIC
# MAGIC Data engineers group window functions into three functional categories based on what they compute:
# MAGIC
# MAGIC #### **1. Ranking Functions**
# MAGIC
# MAGIC Used to assign a sequential number or rank to rows within a partition.
# MAGIC
# MAGIC * **`ROW_NUMBER()`**: Assigns a strict sequential integer starting at 1. If two rows have identical values, it arbitrarily breaks the tie and gives them different numbers (e.g., `1, 2, 3, 4`).
# MAGIC * **`RANK()`**: Assigns ranks based on values. If there is a tie, it gives them the same rank, but **skips** the next ranks (e.g., `1, 2, 2, 4`).
# MAGIC * **`DENSE_RANK()`**: Assigns ranks based on values. If there is a tie, it gives them the same rank, but **never skips** a number (e.g., `1, 2, 2, 3`).
# MAGIC
# MAGIC ```sql
# MAGIC -- Interview Favorite: Finding the top ranks
# MAGIC SELECT 
# MAGIC     emp_name, dept_id, salary,
# MAGIC     ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) as row_num,
# MAGIC     RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) as rnk,
# MAGIC     DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) as dense_rnk
# MAGIC FROM employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **2. Value/Analytic Functions**
# MAGIC
# MAGIC Used to peek forward or backward in a data stream, or to grab boundary values.
# MAGIC
# MAGIC * **`LAG(column, N)`**: Reaches back and grabs the value from `N` rows *before* the current row. Essential for calculating month-on-month growth metrics.
# MAGIC * **`LEAD(column, N)`**: Reaches forward and grabs the value from `N` rows *after* the current row.
# MAGIC * **`FIRST_VALUE(column)`**: Grabs the very first value in the sorted partition window.
# MAGIC * **`LAST_VALUE(column)`**: Grabs the very last value in the sorted partition window.
# MAGIC
# MAGIC ```sql
# MAGIC -- Delta Analysis: Comparing current row to previous row
# MAGIC SELECT 
# MAGIC     order_date, daily_sales,
# MAGIC     LAG(daily_sales, 1) OVER(ORDER BY order_date) AS previous_day_sales
# MAGIC FROM revenue;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **3. Aggregate Window Functions**
# MAGIC
# MAGIC Standard aggregates (`SUM`, `AVG`, `MIN`, `MAX`, `COUNT`) combined with an `OVER()` clause to build moving boundaries.
# MAGIC
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC     emp_name, dept_id, salary,
# MAGIC     AVG(salary) OVER(PARTITION BY dept_id) AS dept_average_salary,
# MAGIC     SUM(salary) OVER(ORDER BY emp_name ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
# MAGIC FROM employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Summary for your Notes
# MAGIC
# MAGIC > **Window Functions** allow analytical computing to scale row-by-row. Use **Ranking** functions to isolate top elements, **Value** functions (`LAG`/`LEAD`) to build chronological sequence differences, and **Aggregate** windows to establish moving trends—all while protecting the underlying row anatomy from collapsing.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q17.What are Frames in SQL?
# MAGIC A **frame** (or window frame) is a dynamic sub-window defined inside a **Window Function** (a query using the `OVER()` clause).
# MAGIC
# MAGIC While a window function allows you to perform calculations across an entire group or partition of data, a **frame** allows you to narrow that focus even further. It defines a moving subset of rows **relative to the current row** being processed.
# MAGIC
# MAGIC As the database engine moves down your table row-by-row, the frame slides, expands, or shrinks along with it, dictating exactly which rows should be included in that immediate calculation.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The Core Syntax
# MAGIC
# MAGIC A frame is specified at the very end of the `OVER()` clause using this structural blueprint:
# MAGIC
# MAGIC ```sql
# MAGIC ROWS|RANGE BETWEEN <start_boundary> AND <end_boundary>
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **The Boundary Controls:**
# MAGIC
# MAGIC * **`CURRENT ROW`**: The row currently being evaluated.
# MAGIC * **`UNBOUNDED PRECEDING`**: Every single row from the very beginning of the partition up to the current row.
# MAGIC * **`UNBOUNDED FOLLOWING`**: Every single row from the current row to the absolute end of the partition.
# MAGIC * **`N PRECEDING`**: Exactly `N` physical rows or value-ranges before the current row.
# MAGIC * **`N FOLLOWING`**: Exactly `N` physical rows or value-ranges after the current row.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Why do we use them?
# MAGIC
# MAGIC Without frames, you cannot build cumulative or moving metrics. Frames are the underlying engine mechanism used to calculate:
# MAGIC
# MAGIC 1. **Running Totals / Cumulative Sums** (e.g., tracking revenue growth from day 1 to today).
# MAGIC 2. **Moving/Rolling Averages** (e.g., a stock's 7-day moving average price, where the frame continually drops the oldest day and adds the newest day).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q18.What is the fundamental difference between the `ROWS` and `RANGE` frame types, and how do they alter analytical calculations when duplicate values exist?
# MAGIC ### CONCEPT: Window Framing — `ROWS` vs `RANGE`
# MAGIC
# MAGIC Both `ROWS` and `RANGE` are used to define the boundaries of a sliding window frame inside an `OVER()` clause. The core difference lies in how they evaluate the data grid: **`ROWS`** is strictly physical-position-based, while **`RANGE`** is logical-value-based.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧬 The Two Frame Core Definitions
# MAGIC
# MAGIC #### **1. `ROWS` (Physical Window)**
# MAGIC
# MAGIC * **How it works:** It treats every single row completely independently based on its physical position index in the sorted dataset. It does not care if the values in your `ORDER BY` column are identical.
# MAGIC * **Best used for:** Smooth running totals, true moving averages (e.g., a strict 3-row moving average), and precise step-by-step transformations.
# MAGIC
# MAGIC #### **2. `RANGE` (Logical Value Window)**
# MAGIC
# MAGIC * **How it works:** It looks at the actual *values* inside the `ORDER BY` column. If multiple rows share the exact same sorted value (a tie/duplicate), `RANGE` treats them as a single logical entity and groups them together for the calculation.
# MAGIC * **Best used for:** Value-based lookbacks (e.g., "calculate the sum of all orders placed within 2 days of the current order date", regardless of how many orders happened on those days).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💻 Code Snippets & Execution Breakdown
# MAGIC
# MAGIC Let's look at the exact code behavior using your `dim_product` dataset, assuming a tie where two items share the exact same `launch_date`:
# MAGIC
# MAGIC #### **The Baseline Table (`dim_product`):**
# MAGIC
# MAGIC | product_id | product_name | launch_date | unit_price |
# MAGIC | --- | --- | --- | --- |
# MAGIC | P1 | Keyboard | Jan 01 | 100 |
# MAGIC | P2 | Mouse | **Jan 02** *(Tie)* | 200 |
# MAGIC | P3 | Monitor | **Jan 02** *(Tie)* | 300 |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **Query 1: The Omitted Frame (The Hidden `RANGE` Default)**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT
# MAGIC     product_name,
# MAGIC     launch_date,
# MAGIC     unit_price,
# MAGIC     SUM(unit_price) OVER(ORDER BY launch_date) AS default_running_total
# MAGIC FROM 
# MAGIC     dim_product;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **Engine Reality:** Because the frame clause is completely omitted, MySQL automatically executes it as `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.
# MAGIC * **The Output Grid:**
# MAGIC | product_name | launch_date | unit_price | default_running_total |
# MAGIC | :--- | :--- | :--- | :--- |
# MAGIC | Keyboard | Jan 01 | 100 | **100** |
# MAGIC | Mouse | **Jan 02** | 200 | **600** 🚨 *(Jumps straight to 600)* |
# MAGIC | Monitor | **Jan 02** | 300 | **600** |
# MAGIC
# MAGIC > **Why the jump?** When the engine evaluates `Jan 02`, it scans ahead for duplicates. Because Mouse and Monitor match, it pulls *both* into the frame at the same time, sums them ($200 + 300 = 500$), and adds it to the baseline ($100$).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **Query 2: Strict Physical Running Total (`ROWS`)**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC     product_name,
# MAGIC     launch_date,
# MAGIC     unit_price,
# MAGIC     SUM(unit_price) OVER(ORDER BY launch_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS strict_running_total
# MAGIC FROM 
# MAGIC     dim_product;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **Engine Reality:** Explicitly uses physical coordinates. It ignores matching dates and focuses purely on line positions.
# MAGIC * **The Output Grid:**
# MAGIC | product_name | launch_date | unit_price | strict_running_total |
# MAGIC | :--- | :--- | :--- | :--- |
# MAGIC | Keyboard | Jan 01 | 100 | **100** |
# MAGIC | Mouse | **Jan 02** | 200 | **300** ($100 + 200$) |
# MAGIC | Monitor | **Jan 02** | 300 | **600** ($300 + 300$) |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### **Query 3: Full Table Wide Open Frame**
# MAGIC
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC     product_name,
# MAGIC     launch_date,
# MAGIC     unit_price,
# MAGIC     SUM(unit_price) OVER(ORDER BY launch_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS grand_total
# MAGIC FROM 
# MAGIC     dim_product;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC * **Engine Reality:** Locks the frame completely open from the absolute first row to the absolute last row of the dataset, processing the total sum ($100 + 200 + 300 = 600$) and printing it across every row.
# MAGIC * **The Output Grid:**
# MAGIC | product_name | launch_date | unit_price | grand_total |
# MAGIC | :--- | :--- | :--- | :--- |
# MAGIC | Keyboard | Jan 01 | 100 | **600** |
# MAGIC | Mouse | Jan 02 | 200 | **600** |
# MAGIC | Monitor | Jan 02 | 300 | **600** |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Production Default Alert
# MAGIC
# MAGIC > **Data Engineering Best Practice:** To avoid unexpected data spikes or incorrect aggregations in your production pipelines due to duplicate timestamps, always explicitly declare **`ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`** when building running totals.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 💡 Summary for your Notes
# MAGIC
# MAGIC > * **`ROWS`** operates on **where the row is** (physical index sequence).
# MAGIC > * **`RANGE`** operates on **what the row value is** (logical value clumps).
# MAGIC > When data tracking requires a strict cumulative line item build, explicit position-based `ROWS` framing must be specified to protect the pipeline matrix from value-clumping distortion.
# MAGIC > 
# MAGIC > 
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q19.What is the difference between a Subquery and a CTE, and why are CTEs the industry standard for production data engineering pipelines?
# MAGIC ### CONCEPT: Subqueries vs. CTEs (Common Table Expressions)
# MAGIC
# MAGIC Both subqueries and CTEs allow you to use the result of a temporary query inside another query. The fundamental difference comes down to **readability, reusability, and code architecture**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The Core Breakdown
# MAGIC
# MAGIC ##### **1. Subqueries (The Inline Approach)**
# MAGIC
# MAGIC A subquery is an inner query nested completely inside an outer query (usually in the `FROM`, `WHERE`, or `SELECT` clause).
# MAGIC
# MAGIC * **The Problem:** They are written "inside-out." To understand a complex query with multiple nested subqueries, a data engineer has to read from the deepest indentation level upward, making the code incredibly hard to debug and maintain.
# MAGIC
# MAGIC ```sql
# MAGIC -- Inline Subquery Example (Harder to read as it grows)
# MAGIC SELECT emp_name, salary 
# MAGIC FROM (
# MAGIC     SELECT *, ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) as rnk
# MAGIC     FROM staging_employees
# MAGIC ) as ranked_tbl
# MAGIC WHERE rnk = 1;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **2. CTEs (The Common Table Expression Approach)**
# MAGIC
# MAGIC A CTE acts like a temporary, named result set that you define **before** your main query execution using the **`WITH`** keyword. Think of it like creating a temporary, virtual table that exists only for the duration of that single query execution.
# MAGIC
# MAGIC * **The Benefit:** They read from "top-to-bottom" in logical order, matching how human brains naturally think.
# MAGIC
# MAGIC ```sql
# MAGIC -- CTE Example (Clean, modular, and readable)
# MAGIC WITH RankedEmployees AS (
# MAGIC     SELECT *, 
# MAGIC            ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) as rnk
# MAGIC     FROM staging_employees
# MAGIC )
# MAGIC SELECT emp_name, salary 
# MAGIC FROM RankedEmployees
# MAGIC WHERE rnk = 1;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 The Comparison Matrix
# MAGIC
# MAGIC | Feature | Subquery | CTE (Common Table Expression) |
# MAGIC | --- | --- | --- |
# MAGIC | **Readability** | Poor. Leads to deeply nested "spaghetti code." | Excellent. Reads sequentially from top to bottom. |
# MAGIC | **Reusability** | **No.** Cannot be referenced multiple times in the same query. | **Yes.** Can be referenced multiple times in the main query block. |
# MAGIC | **Recursion** | No. | **Yes.** Supports `WITH RECURSIVE` (crucial for processing hierarchical data like manager-employee trees). |
# MAGIC | **Performance** | Usually identical. Modern SQL engines optimize both into the same execution plan. | Usually identical. (Though some engines materialize CTEs, helping with heavy calculations). |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 When to use which in an Interview?
# MAGIC
# MAGIC * **Use a Subquery:** Only for very quick, simple checks (e.g., a basic lookup inside a `WHERE id IN (SELECT id FROM...)`).
# MAGIC * **Use a CTE:** Every single time you need to write complex analytical logic, multi-step data transformations, or when using window functions (like your deduplication query). It instantly signals to the interviewer that you write production-grade, maintainable pipelines.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for your Notes
# MAGIC
# MAGIC > **Subqueries** run nested inside the code structure, while **CTEs** declare temporary virtual boundaries upfront using the `WITH` keyword. Always default to **CTEs** for multi-step logic to keep data tracking steps highly modular, readable, and easily maintainable.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q20.What are Views in SQL?
# MAGIC
# MAGIC A **View** is essentially a **virtual table** based on the result-set of an SQL statement. It does not store the physical data itself; instead, it stores the SQL query template inside the database engine. Every time you query a view, the database runs the underlying query on the fly to show you the fresh, real-time data from the base tables.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The Core Syntax & Example
# MAGIC
# MAGIC Imagine you have a large production table called `staging_employees` containing sensitive information like salaries, along with common business attributes:
# MAGIC
# MAGIC ##### **1. The Base Table Configuration**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE staging_employees (
# MAGIC     emp_id INT PRIMARY KEY,
# MAGIC     emp_name VARCHAR(50),
# MAGIC     department VARCHAR(50),
# MAGIC     salary INT,
# MAGIC     location VARCHAR(50)
# MAGIC );
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **2. Creating the View Layer**
# MAGIC
# MAGIC If your non-HR data analysts need access to employee details by department, but you **must mask the salary column** for privacy reasons, you can create a View:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE VIEW vw_public_employee_registry AS
# MAGIC SELECT 
# MAGIC     emp_id,
# MAGIC     emp_name,
# MAGIC     department,
# MAGIC     location
# MAGIC FROM 
# MAGIC     staging_employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **3. Querying the View**
# MAGIC
# MAGIC Now, users can query this view exactly like a normal, physical table, completely unaware of the masked columns or complex transformations happening underneath:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT * FROM vw_public_employee_registry 
# MAGIC WHERE department = 'Data Engineering';
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 The Strategic Value for Data Engineers
# MAGIC
# MAGIC * **Data Security & Masking:** It acts as a security filter by restricting user access to specific rows or columns without modifying underlying permissions on the source tables.
# MAGIC * **Simplifying Complex Queries:** If you have an ugly query with 5 inner joins and a window function, you can wrap it inside a single view. Users can query the view with a simple `SELECT * FROM view_name`, keeping downstream application scripts pristine.
# MAGIC * **Logical Abstraction Layer:** If the structure of your physical staging tables changes tomorrow, you only need to update the query definition inside the view. Any external pipeline or report reading from the view won't break.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for your Notes
# MAGIC
# MAGIC > **Views** store the **query definition**, not the data grid itself. They provide a secure, abstract virtual layer on top of raw physical tables to mask sensitive attributes, encapsulate multi-join logic, and simplify access for downstream consumption.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q21.What are Stored Procedures in SQL?
# MAGIC
# MAGIC A **Stored Procedure** is a collection of pre-compiled SQL statements stored directly inside the database engine. Think of it exactly like a **Function** in standard programming languages: you write a multi-step sequence of database logic once, save it under a name, and then invoke it anywhere using a simple command.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The Core Syntax & Example
# MAGIC
# MAGIC To write a stored procedure in MySQL, you have to use a special command called a **`DELIMITER`**. Because a procedure contains multiple lines of SQL that each end with a semicolon `;`, we temporarily change the database's statement-ending character to something else (like `//`) so the engine knows to compile the *entire block* as a single program instead of running it line-by-line.
# MAGIC
# MAGIC ##### **1. Creating a Stored Procedure (With Input Parameters)**
# MAGIC
# MAGIC Let’s say you want to build a routine that automatically shifts an employee's department and updates their salary in a single transaction pass:
# MAGIC
# MAGIC ```sql
# MAGIC DELIMITER //
# MAGIC
# MAGIC CREATE PROCEDURE sp_UpdateEmployeeProfile(
# MAGIC     IN input_emp_id INT,
# MAGIC     IN new_dept VARCHAR(50),
# MAGIC     IN salary_increment INT
# MAGIC )
# MAGIC BEGIN
# MAGIC     -- Step 1: Execute the profile modification
# MAGIC     UPDATE staging_employees
# MAGIC     SET department = new_dept,
# MAGIC         salary = salary + salary_increment
# MAGIC     WHERE emp_id = input_emp_id;
# MAGIC     
# MAGIC     -- Step 2: Fetch the freshly modified record to verify
# MAGIC     SELECT emp_id, emp_name, department, salary 
# MAGIC     FROM staging_employees 
# MAGIC     WHERE emp_id = input_emp_id;
# MAGIC END //
# MAGIC
# MAGIC DELIMITER ;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ##### **2. Executing (Calling) the Stored Procedure**
# MAGIC
# MAGIC Instead of writing out the `UPDATE` and `SELECT` blocks manually every time an employee changes roles, you simply call the compiled procedure with your inputs:
# MAGIC
# MAGIC ```sql
# MAGIC -- Syntax: CALL procedure_name(arguments);
# MAGIC CALL sp_UpdateEmployeeProfile(104, 'Data Engineering', 15000);
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 The Strategic Value for Data Engineers
# MAGIC
# MAGIC * **Massive Network Savings:** Instead of a Python script or Databricks notebook sending 20 lines of raw SQL code over the network to the database engine, it only sends a single short line: `CALL sp_name();`. This reduces latency drastically in high-frequency data pipelines.
# MAGIC * **Encapsulated Business Logic:** If your business logic for calculation changes, you only modify the code inside the procedure once on the database server. You don't have to change or redeploy any external application code.
# MAGIC * **Security Boundaries:** You can restrict users from directly altering raw staging tables, but grant them explicit permissions to execute specific stored procedures. This acts as a controlled gateway for data manipulation.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for your Notes
# MAGIC
# MAGIC > **Stored Procedures** are compiled, multi-statement functions saved directly on the database server. They accept parameters, wrap complex sequence workflows (like updates and log entries) into a single execution step, and optimize network overhead for operational pipelines.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q22.What are User-Defined Functions (UDFs) in Databases?
# MAGIC A **User-Defined Function (UDF)** is a custom, reusable block of logic that you write to perform a calculation or manipulate data, and it **must return exactly one single value**.
# MAGIC
# MAGIC While SQL comes with built-in functions (like `UPPER()`, `ROUND()`, or `CONCAT()`), UDFs allow you to build your own specialized tools for repetitive transformations unique to your business data.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🧬 The Core Syntax & Example
# MAGIC
# MAGIC Just like Stored Procedures, creating a UDF in MySQL requires changing the `DELIMITER` so the engine compiles the entire function block together.
# MAGIC
# MAGIC Let's build a practical data engineering function that takes an employee's salary as an input and automatically categorizes them into a structural Tax Bracket string.
# MAGIC
# MAGIC ##### **1. Creating the Function**
# MAGIC
# MAGIC ```sql
# MAGIC DELIMITER //
# MAGIC
# MAGIC CREATE FUNCTION fn_GetTaxBracket(emp_salary INT)
# MAGIC RETURNS VARCHAR(20)
# MAGIC DETERMINISTIC
# MAGIC BEGIN
# MAGIC     DECLARE bracket VARCHAR(20);
# MAGIC     
# MAGIC     IF emp_salary >= 90000 THEN
# MAGIC         SET bracket = 'Tier 1 (High)';
# MAGIC     ELSEIF emp_salary >= 75000 THEN
# MAGIC         SET bracket = 'Tier 2 (Medium)';
# MAGIC     ELSE
# MAGIC         SET bracket = 'Tier 3 (Standard)';
# MAGIC     END IF;
# MAGIC     
# MAGIC     RETURN bracket;
# MAGIC END //
# MAGIC
# MAGIC DELIMITER ;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC > **Note on `DETERMINISTIC`:** This keyword tells MySQL that for the exact same input salary, the function will *always* return the exact same tax bracket string. This allows the engine to optimize performance.
# MAGIC
# MAGIC ##### **2. Using the Function in a Query**
# MAGIC
# MAGIC Unlike a Stored Procedure (which you have to execute using `CALL`), a User-Defined Function is used inline **directly inside your standard SQL statements**—exactly like `COUNT()` or `SUM()`:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT 
# MAGIC     emp_id, 
# MAGIC     emp_name, 
# MAGIC     salary,
# MAGIC     fn_GetTaxBracket(salary) AS tax_tier
# MAGIC FROM 
# MAGIC     staging_employees;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 Stored Procedures vs. User-Defined Functions (Crucial Interview Knowledge)
# MAGIC
# MAGIC | Feature | Stored Procedure (`sp_`) | User-Defined Function (`fn_`) |
# MAGIC | --- | --- | --- |
# MAGIC | **Return Value** | Can return multiple values, full result-set tables, or **nothing at all**. | **Must** return exactly one single, scalar value. |
# MAGIC | **How it's Called** | Executed standalone using the **`CALL`** keyword. | Called inline directly inside `SELECT`, `WHERE`, or `HAVING` clauses. |
# MAGIC | **Permitted Statements** | Can perform data modification (like `INSERT`, `UPDATE`, `DELETE`). | Strictly used for reading and computing data. Cannot modify table data. |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 💡 Summary for your Notes
# MAGIC
# MAGIC > **User-Defined Functions (UDFs)** are custom scalar tools built to handle repetitive business calculations inline. They accept inputs, compute calculations or conditional mapping transformations, and must pass back a single consolidated data point directly into the active query string.
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q23.Define DDL in the context of Databricks Unity Catalog and classify the setup commands.
# MAGIC
# MAGIC #### 🔬 The Classification Breakdown
# MAGIC
# MAGIC Every command that begins with words like `CREATE`, `ALTER`, `DROP`, or `RENAME` is classified as DDL. Let's look at your cell's commands:
# MAGIC
# MAGIC ##### **1. `CREATE EXTERNAL LOCATION` ➔ DDL**
# MAGIC
# MAGIC * **Why:** You are defining a new architectural security object inside the Unity Catalog metastore layer. You aren't processing records; you are defining a management boundary.
# MAGIC
# MAGIC ##### **2. `CREATE CATALOG` ➔ DDL**
# MAGIC
# MAGIC * **Why:** You are creating the top-level container of the three-level namespace. This defines the structural metadata bucket where databases will eventually live.
# MAGIC
# MAGIC ##### **3. `CREATE SCHEMA` ➔ DDL**
# MAGIC
# MAGIC * **Why:** You are defining a logical namespace database layer inside the catalog.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 DDL vs. DML: The Interview Contrast
# MAGIC
# MAGIC To make sure this never gets confused in a technical round, always contrast **DDL** with **DML** (Data Manipulation Language):
# MAGIC
# MAGIC | Language Type | Core Purpose | Common Keywords | Your Code Example |
# MAGIC | --- | --- | --- | --- |
# MAGIC | **DDL** *(Data Definition)* | Building or altering the **structures, tables, and paths** themselves. | `CREATE`, `DROP`, `ALTER` | `CREATE CATALOG delta_catalog;` |
# MAGIC | **DML** *(Data Manipulation)* | Modifying or querying the **actual data rows** sitting inside those structures. | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` | `INSERT INTO delta_catalog.delta_db.invoices SELECT * ...` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📊 Interview Flashcard
# MAGIC
# MAGIC > **Q: Is managing Unity Catalog objects like External Locations and Storage Credentials considered DDL or DML?**
# MAGIC > It is strictly **DDL**. These commands define and register the logical metadata governance structures and access pathways within the architecture metastore. They do not manipulate or evaluate individual transactional row entries, which would fall under DML.
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ### Q24. What is the difference between row-oriented and column-oriented storage?
# MAGIC
# MAGIC To understand why modern data engineering tools are so fast, we have to look directly at how data is physically arranged on a hard drive or cloud storage disk.
# MAGIC
# MAGIC When you store a table, computer memory and disks don't actually see a nice, 2D grid of rows and columns. A disk can only write data in a single, continuous line of bytes.
# MAGIC
# MAGIC The two main ways to arrange that data are **Row-Oriented Storage** (often called traditional or raw row layout) and **Columnar Storage** (like Parquet or ORC).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏢 1. Row-Oriented Storage (The Traditional Layout)
# MAGIC
# MAGIC In a row-oriented database (like traditional PostgreSQL, MySQL, or OLTP systems), data is written to the disk **one full row at a time**, sequentially. All fields of Row 1 are written, then all fields of Row 2, and so on.
# MAGIC
# MAGIC #### 📊 The Example Data
# MAGIC
# MAGIC Imagine we have a small dataset of store invoices:
# MAGIC
# MAGIC | Invoice_ID | Customer_Name | Total_Amount | Store_City |
# MAGIC | --- | --- | --- | --- |
# MAGIC | 101 | Dipesh | 4500 | Nagpur |
# MAGIC | 102 | Amit | 1200 | Mumbai |
# MAGIC | 103 | Rahul | 8500 | Pune |
# MAGIC
# MAGIC #### 💾 How it is written physically on the disk:
# MAGIC
# MAGIC The disk writes the rows continuously, back-to-back:
# MAGIC
# MAGIC ```text
# MAGIC [Row 1: 101, Dipesh, 4500, Nagpur] ──► [Row 2: 102, Amit, 1200, Mumbai] ──► [Row 3: 103, Rahul, 8500, Pune]
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC #### 🟢 Pros of Row Storage:
# MAGIC
# MAGIC * **Blazing Fast Writes & Inserts:** If you want to add a brand-new invoice to the system, the database engine just travels straight to the very end of the file and dumps the entire row at once.
# MAGIC * **Perfect for Transactional Apps (OLTP):** If a bank teller needs to pull up *everything* about `Invoice_ID = 101`, the engine reads one single chunk of disk and instantly gets the name, amount, and city.
# MAGIC
# MAGIC #### ❌ Cons of Row Storage (The Big Data Bottleneck):
# MAGIC
# MAGIC Imagine running an analytics query to find the average sales:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT AVG(Total_Amount) FROM invoices;
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC To calculate this, the engine only needs the `Total_Amount` column. However, because the data is trapped in a row layout, the disk is forced to scan and load the `Invoice_ID`, `Customer_Name`, and `Store_City` into memory for every single record, just to throw them away. This creates massive, wasteful disk I/O at petabyte scale.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚡ 2. Columnar Storage (The Big Data Layout)
# MAGIC
# MAGIC In a columnar database or file format (like **Apache Parquet** used in Delta Lake), the arrangement is completely flipped. Data is written to the disk **one full column at a time**. All values for Column 1 are written together, then all values for Column 2, and so on.
# MAGIC
# MAGIC #### 💾 How that exact same table looks physically on the disk:
# MAGIC
# MAGIC The disk groups the columns together sequentially:
# MAGIC
# MAGIC ```text
# MAGIC [Invoice_ID: 101, 102, 103] ──► [Customer_Name: Dipesh, Amit, Rahul] ──► [Total_Amount: 4500, 1200, 8500] ──► [Store_City: Nagpur, Mumbai, Pune]
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC #### 🟢 Pros of Columnar Storage (Why Big Data Loves It):
# MAGIC
# MAGIC ##### **A. Aggressive Data Skipping (Incredible Read Speeds)**
# MAGIC
# MAGIC When you run that same analytical query: `SELECT AVG(Total_Amount) FROM invoices;`, the execution engine looks at the file metadata, calculates the exact starting position of the `Total_Amount` column block, and reads **only** those bytes `[4500, 1200, 8500]`.
# MAGIC It completely skips reading names, IDs, or cities from the disk. This reduces your disk read operations by 70% to 90%!
# MAGIC
# MAGIC ##### **B. Extreme Data Compression**
# MAGIC
# MAGIC Because data of the exact same data type is packed tightly together, compression algorithms work like magic.
# MAGIC
# MAGIC * In a row-oriented block, you have an integer, a string, a number, and text all mixed together. You can't compress that easily because there are no repeating patterns.
# MAGIC * In a columnar block, you have a solid stream of text strings like `[Nagpur, Nagpur, Nagpur, Mumbai, Mumbai]`. Compression algorithms (like Snappy or ZSTD) can compress that down to a fraction of its original size by using dictionary encoding (e.g., storing "Nagpur" once and noting it repeats 3 times). This saves massive amounts of cloud storage costs.
# MAGIC
# MAGIC #### ❌ Cons of Columnar Storage:
# MAGIC
# MAGIC * **Slow Row-Level Writes:** If you want to insert a single new row `(104, Priya, 3000, Delhi)`, the engine cannot just append it to the end of the file. It has to physically open the file, locate the end of the ID column block to insert `104`, locate the Name block to insert `Priya`, locate the Amount block, and so on. This causes heavy write amplification, which is why columnar formats are meant for analytical workloads (OLAP), not live transactional apps.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 📝 Summary: Row-Oriented vs. Columnar Storage
# MAGIC
# MAGIC * **Row-Oriented Storage** is optimized for **OLTP (Online Transactional Processing)** workloads. It writes data sequentially by rows, making it the perfect engine for systems that require millions of individual, real-time inserts, updates, and specific single-row lookups.
# MAGIC * **Columnar Storage** is optimized for **OLAP (Online Analytical Processing)** workloads. It groups data vertically by columns, making it the perfect engine for big data analytics, reporting, and scanning billions of rows to perform rapid math aggregations.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC #### 🔍 Real-World Architecture Examples
# MAGIC
# MAGIC ##### 1. Row-Oriented E-Commerce System (MySQL / PostgreSQL)
# MAGIC
# MAGIC * **The Scenario:** You are building the backend for an online shopping application. Every single second, 10,000 users are clicking "Buy Now," checking their user profiles, or modifying their shipping addresses.
# MAGIC * **Why Row Storage Wins:** When a user checks out, the database instantly appends an entire row containing `(Order_ID, User_ID, Product, Price, Timestamp)` to the very end of the disk layout. Because it writes the full row together, the transaction is instant, ensuring the app handles heavy traffic without a stutter.
# MAGIC
# MAGIC ##### 2. Columnar Data Analytics Platform (Parquet / Delta Lake / Snowflake)
# MAGIC
# MAGIC * **The Scenario:** At midnight, the company's Business Intelligence (BI) team runs a massive dashboard query to calculate the total revenue generated across the entire country during the last quarter.
# MAGIC * **The Query:** `SELECT SUM(Price) FROM sales_history;` (Evaluating 500 Million rows).
# MAGIC * **Why Columnar Wins:** The engine completely ignores user names, delivery addresses, and order IDs. It travels directly to the isolated `Price` column block on the disk, pulls *only* those numeric values into memory, and sums them up instantly. If this were a row-based database, scanning 500 million full rows just to get the price would completely crash the server or take hours to run.
# MAGIC

# COMMAND ----------

with tbl as (
SELECT
	province_id,
    sum(height) toatl_height
    --birth_date
    --count(*) as c
FROM
	patients 
group by
	province_id)
SELECT	
	doctor_id,
	concat(first_name,' ',last_name),
    min(admission_date),
    max(admission_date)
FROM
	admissions a
join 
	doctors d
On
	a.attending_doctor_id = d.doctor_id
group by doctor_id
order by admission_date
--join 
	--admissions a
--On
	--p.patient_id = a.patient_id
Where 
	allergies in  ('Penicillin' , 'Morphine')
--group by
	--first_name
--having count(first_name) =1
order by
	allergies , first_name ,last_name
    
    
    
with tbl as (SELECT
	admission_date,
	count(*) admissions_per_day
FROM
	admissions
group by
	admission_date)
Select  
	max(admissions_per_day) as max_visits,
	MIn(admissions_per_day) as min_visits,
    round(Avg(admissions_per_day), 2) as avg_visits
From
	tbl

order by
	first_name desc

SELECT
	concat(first_name,' ',last_name) as full_name,
    round(height/30.48, 1) as height_in_feet,
    round(weight*2.205) as weight_in_pounds,
    birth_date,
    Case when gender = "M" Then "Male" Else "Female" End as gender
FROM
	patients p
    
    

having
	num_of_dups > 1
    

SELECT
	concat(p.first_name,' ',p.last_name) as p_full_name,
    concat(d.first_name,' ',d.last_name) as d_full_name,
	--p.patient_id,
    max(admission_date) as last_admission_date
    --count(*) as num_of_adm_per_pat
FROM
	patients p
join 
	admissions a
On
	p.patient_id = a.patient_id
join 
	doctors d
On
	a.attending_doctor_id = d.doctor_id 
group by
	p.patient_id
    

order by
	total_patients desc

Where 
	allergies in  ('Penicillin' , 'Morphine')


# --------------
with tbl as (
  select 
		province_name,
  		gender,
  		count(province_name) as gender_count_per_province
  from
      patients p
  join province_names pn on p.province_id = pn.province_id
  group by province_name, gender
--  join doctors d ON a.attending_doctor_id = d.doctor_id
  --where
  		--diagnosis = 'Epilepsy' and d.first_name = 'Lisa'
)
select 
	province_name
from
	tbl
group by
	province_name 
             
