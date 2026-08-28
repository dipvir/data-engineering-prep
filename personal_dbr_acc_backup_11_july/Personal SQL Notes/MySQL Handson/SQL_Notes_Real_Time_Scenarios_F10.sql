>-- Real Time Scenarios (Questions).

Select * From dim_product;

-- 1) Find the Top Nth expensive unit_price from dim_product.
select
	*
From
	(
	Select 
		*,
		dense_rank() over(order by unit_price desc) as unique_id
	From
		dim_product) as tbl
where
	unique_id = 5;
    
-- 2) Find the Top Nth expensive unit_price from dim_product for each category.
select
	*
From
	(
	Select 
		*,
		dense_rank() over(partition by category order by unit_price desc) as unique_id
	From
		dim_product) as tbl
where
	unique_id = 5;
    
-- 3) Removing Duplicates.
-- I have Created a dummy table staging_employees for this question in through file F9.

select * from staging_employees;
-- main solution
select 
	*
From
	(select 
		*,
		row_number() over(partition by emp_id order by salary desc) as ranked
	From
		staging_employees) as tbl
    where ranked = 1
    ;
    
-- 4) To get the temperature of prevous and next day (Lad and Lead usecase).
Select
	*,
    lag(temp) over(order by day) as a_day_ago_temp,
    lead(temp) over(order by day) as a_day_after_temp,
    
    -- if we want move more then 1 day
    lag(temp ,3) over(order by day) as `3days_ago_temp`,
    lead(temp ,3) over(order by day) as `3days_after_temp`,
    
    -- We can change what to put in missing blocks.
    lag(temp ,3, 0) over(order by day) as `3days_ago_temp`,
    lead(temp ,3, 0) over(order by day) as `3days_after_temp`
From
	weather;
    
    
    
    
    
    
    
    
    
    
    

