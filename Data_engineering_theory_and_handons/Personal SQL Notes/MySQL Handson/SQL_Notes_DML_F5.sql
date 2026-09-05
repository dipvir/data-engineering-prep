-- This file will cover DML commands of sql.

-- DML -> 1) Insert Command (Btw we already Tried).
-- Lets first create a dummy table in ecom schema/database.
-- i.e we are writing DDL Command first.
Create Table employees
(
 emp_id int Primary key,
 emp_name varchar(100),
 dept_name varchar(100)
);

-- Now using Insert Command(DML) to add some records in above table.
-- a) Inserting data for all fields/Columns.
Insert Into employees
values 
(1 , 'Deep', 'Data Engineer'),
(2 , 'yash', 'Data Analyst'),
(3 , 'ram', 'Full stack'),
(4 , 'tej', 'Mobile Dev'),
(5 , 'om', 'Tester');

-- b) Inserting data for selected fields/Columns.
Insert Into employees(emp_id , emp_name)
values 
(6 , 'Deep'),
(7 , 'yash');

select * from employees;


-- DML -> 2) Update Command.
-- It is used to update existing records.
-- a) updates single row.
Update employees
Set emp_name = 'tejas'
Where emp_id = 4;

-- b) updates multipe rows.
Update employees
Set dept_name = 'Unknown'
Where dept_name is null;

-- c) updates multipe fields/Columns.
Update employees
Set emp_name = 'dip' , dept_name = 'Data Engineering' 
Where emp_id = 1;
-- Note :- Here 'Where Clause' is important
-- if we forget all values of those fields/Columns will be updated.


-- DML -> 3) Delete Command.
-- It is used to Delete all or selected records.
Delete From employees
Where emp_id = 5;
-- Note :- Here also 'Where Clause' is important
-- if we forget all records will be wiped out.








