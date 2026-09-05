-- How to create views in sql.
-- Firstly to define it, its just a queres code stored in an object 
-- which is called to run that specific query.

-- Creating view
Create view dedup_view as
select 
	*
From
	(select 
		*,
		row_number() over(partition by emp_id order by salary desc) as ranked
	From
		staging_employees) as tbl
where 
	ranked = 1;
    
-- So, now we can directly query this view like a table....
SELECT * FROM dedup_view;
