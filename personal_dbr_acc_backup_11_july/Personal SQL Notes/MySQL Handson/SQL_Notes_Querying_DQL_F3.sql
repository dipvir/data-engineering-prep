-- In this file i am just getting started with how to query tables mainly from ECOM Schema/Database.
-- In SQL it is called DQL (Data Query Language).

-- Tables from ECOM Schema/Database.
Select * from dim_customer;
Select * from dim_date;
Select * from dim_product;
Select * from dim_store;
Select * from fact_sales;

-- Below Q stands for Query for this notes.
-- Q1) Queries whole table with all cols and rows.
Select 
	*
from 
	dim_customer;
    
-- Q2) Queries table with selected cols but with all data(rows/records).
Select 
	customer_key,
    first_name,
    gender,
    country
from 
	dim_customer;

-- Q3) Queries table with selected cols and limited data(rows/records).
Select 
	customer_key,
    first_name,
    gender,
    country
from 
	dim_customer
limit 
	30;
  
-- Q4) Sorting/Ordering the data based on specified field using 'order by'.
-- a) In ascending order.
Select 
	*
from 
	dim_product
order by
	unit_price asc -- For ascending asc is optional its default.
limit 
	30;
    
-- b) In descending  order.
Select 
	*
from 
	dim_product
order by
	unit_price desc
limit 
	30;

-- Q5) Using 'Where' keyword to filter the records based on given conditions.
-- a) With single condition.
select 
	*
from
	dim_customer
where
	gender = 'f';
    
-- b) With Multiple conditions using 'And'.
select 
	*
from
	dim_customer
where
	gender = 'f' and country = 'Zambia';
    
-- c) Using 'and' plus 'or' keyword together with parentheses() to get right results.
select 
	*
from
	dim_customer
where
	gender = 'f' and (country = 'Zambia' or join_date >= '2025-10-01');


-- Q6) Use of 'Like' Operator in sql, So like also filter records.
-- a) here we see 's%' where '%' means any no. of character.
-- i.e query returns records where first_name starts with s.
select 
	*
from
	dim_customer
where
	first_name like "s%";

-- b) here we see 's%n' and as '%' means any no. of character.
-- So query will return records where first_name starts with s and ends with n.
select 
	*
from
	dim_customer
where
	first_name like "s%n";

-- c) here we see 't__f%y' where '_' means one character.
-- Query returns rows where first_name starts with t + any two character + f + any no. of character in btw + ends with y.
select 
	*
from
	dim_customer
where
	first_name like "t__f%y";

-- Q7) Alias in sql.
-- It is used to rename existing column name or to name derived columns.
Select 
	product_key,
    product_id,
    product_name as productname,
    product_name as `product name`,
    category,
    unit_price,
    unit_price * .90 as discounted_unit_price
from 
	dim_product;

-- Q8) Grouping of data in sql.
-- a) Use of group by to get aggregated result like avg , sum , count etc.
select 
	category,
    avg(unit_price) as avg_price,
    sum(unit_price) as total_price,
    count(unit_price) as quantity,
    sum(unit_price)/count(unit_price) as cal_avg_price
from
	dim_product
group by 
	category;
    
-- b) Use of group by with having Clause in sql.
-- having is like a pro version of where clause.
-- where is used to filter on raw data(i.e On existing columns in the table).
-- whereas having is used to filter grouped/aggregated data(i.e On derived columns).
select 
	category,
    avg(unit_price) as avg_price,
    sum(unit_price) as total_price,
    count(unit_price) as quantity,
    sum(unit_price)/count(unit_price) as cal_avg_price
from
	dim_product
group by 
	category
having 
	avg_price > 500 ;

    
    
    
    