-- This file will cover joins concept of sql.

-- Creating sample table 'orders'.
Create Table orders
(
	o_id int,
    cust_id int,
    price int
);
-- Inserting some data in orders
Insert Into orders 
Values
(1,101,1000),
(2,201,1100),
(3,501,1200);

-- Creating sample table 'customers'.
Create Table customers
(
	id int,
    name varchar(100),
    email varchar(100)
);
-- Inserting some data in customers
Insert Into customers 
Values
(101,'love','aa'),
(201,'ansh','bb'),
(301,'lamba','cc');

select * from orders;
select * from customers;

-- Different types of joins
-- 1) Inner Join
Select 
	-- * if we dont want all cols from both table we can use below way to choose req. ones.  
    o.*,
    c.name,
    c.email
From
	orders o 
Inner Join 
	Customers c
on 
	o.cust_id = c.id;

-- 2) Left Join
Select 
	*
From
	orders o 		-- Left Table
Left Join 
	Customers c		-- Right Table
on 
	o.cust_id = c.id;

-- 3) Right Join
Select 
	*
From
	orders o		-- Left Table
Right Join 
	Customers c 	-- Right Table
on 
	o.cust_id = c.id;

-- 4) Full Join
-- Below Code will throw error, bec MySQl does'nt provide syntax for full join like other databases.
-- But there is a workaround to achieve that through union. 
-- Select 
-- 	*
-- From
-- 	orders o		-- Left Table
-- Full Join 
-- 	Customers c 	-- Right Table
-- on 
-- 	o.cust_id = c.id;

-- So here we are acheiving that through union by combining left and right join outputs.
-- Taking Left Join result
Select 
	*
From
	orders o 		-- Left Table
Left Join 
	Customers c		-- Right Table
on 
	o.cust_id = c.id
Union
-- Taking Right Join result
Select 
	*
From
	orders o		-- Left Table
Right Join 
	Customers c 	-- Right Table
on 
	o.cust_id = c.id;

-- 5) Cross Join
Select 
	* 
From
	orders o 
Cross Join 
	Customers c;


-- extra (below is rough work)
Select 
	*
from 
	fact_sales fs
left join 
	dim_customer dc on fs.customer_key = dc.customer_key
left join 
	dim_product dp on fs.product_key = dp.product_key
left join 
	dim_store ds on fs.store_key = ds.store_key
left join 
	dim_date dd on fs.date_key = dd.date_key
-- where
-- 	dc.customer_key is null;
    