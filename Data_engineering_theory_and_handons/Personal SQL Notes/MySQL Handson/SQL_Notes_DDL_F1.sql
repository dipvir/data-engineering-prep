-- Note :- In MYSQL Database/Schema are same thing under which tables are created (i.e 2-Tier Namespaces).
-- But in some other Databases the structure is like Database -> Schema -> Table (i.e 3-Tier Namespaces).

-- This files mainly documents syntax for DDL(Data Definition Language) commands.
-- Those commands are Create, Alter, Drop, Truncate, Rename etc.

-- Syntax to Create schema/database in MYSQL DB.
Create Database example_db_1;
Create Schema example_db_2;

-- Syntax to Drop schema/database in MYSQL DB.
Drop Database example_db_1;
Drop Schema example_db_2;
-- Note :- Database/Schema both keywords can be used as shown above.

-- Syntax to Create Table.
-- Firstly, We have to select a Database/Schema under which the table will be created.
use sales; 
-- either using 'use Database/Schema' or just double click the Database/Schema from left panel 
-- and it will become bold means selected.
Create Table stores
(
store_id INT,
store_name VARCHAR(200)
);

-- Syntax to insert records into the table for all columns.
Insert Into stores
values 
(1, "Mi store"),
(2, "samsung store");

-- Syntax to insert records into the table for selected columns.
Insert Into stores (store_id)
values 
(3),
(4);
-- Note :- As we didnt pass values for some columns those will be filled with null.
-- Also we can ristrict that using constraints concept.

-- Syntax to query the table.
Select * from stores;
-- Keywords, Table, Database, Column Names are case-insensitive in MYSQL.
SELECT store_Name ,store_ID FROM stoRES; 

-- So now we are creating new table by using some constraints.
-- 1) UNIQUE Constraint :- This wont allow duplicate values, but can be null.
-- 2) NOT NULL Constraint :- This forces to pass a value as cant be null.
Create Table new_stores
(
store_id INT UNIQUE,
store_name VARCHAR(200) NOT NULL
);

-- This is satisfying the constraints.
Insert Into new_stores
values 
(1, "Mi store"),
(2, "samsung store");

-- This will throw error as same store_id are repeated.
Insert Into new_stores
values 
(1, "oppo store"),
(2, "vivo store");

-- This will also throw error as store_name cant be null.
-- Also we didnt defined any default value.
Insert Into new_stores (store_id)
values 
(3),
(4);

-- This is also satisfying the constraints.
Insert Into new_stores
values 
(3, "oppo store"),
(4, "vivo store");

-- query new table to test constraints concept.
Select * from new_stores;

-- Syntax to Drop Table.
-- Permanently deletes the entire object container and all data rows inside it from the disk.
Drop Table dummy_schema.networkhospitallist; 

-- Syntax to Truncate Table.
-- Instantly wipes out all rows inside a table but keeps the empty structure intact.
Truncate Table dummy_schema.customers; 


-- Syntax for Alter command.
-- Modifies the structure of an existing table (e.g. ADD, DROP, or MODIFY columns).
Alter Table new_stores
Add Column store_city varchar(100); -- Adds new column

Alter Table new_stores
Rename Column address to store_address; -- Renames existing column

Alter Table new_stores
Drop Column store_address; -- Drops existing column

Select * from new_stores;




