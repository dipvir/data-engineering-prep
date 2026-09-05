-- Window Functions

Select * From dim_product;
Select sum(unit_price) From dim_product;
Select Avg(unit_price) From dim_product;

-- Q1) 
Select 
	*,
    -- Running Total (Cumulative Sum)
    sum(unit_price) over(order by launch_date) as running_total, 
    -- Moving Average
    avg(unit_price) over(order by launch_date) as moving_average
From
	dim_product;

-- Q2) Frames in sql 
Select 
	*,
    -- Running Total (Cumulative Sum) using rows
    sum(unit_price) over(order by launch_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total_with_row,
    -- Running Total (Cumulative Sum) using range (Same as running_total calculated in Q1 above as this is default frame)
    sum(unit_price) over(order by launch_date Range BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total_with_range,
    
    -- moving_average using rows
    avg(unit_price) over(order by launch_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as moving_average_with_row,
    -- moving_average using range (Same as moving_average calculated in Q1 above as this is default frame)
    avg(unit_price) over(order by launch_date Range BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as moving_average_with_range
From
	dim_product;
    
-- Q3) 
Select 
	*,
	sum(unit_price) over(order by launch_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED Following) as total,
    avg(unit_price) over(order by launch_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED Following) as average,
    
    -- 3-Day Running Total (Cumulative Sum)
    Sum(unit_price) OVER(ORDER BY launch_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS Running_Total_3days,
    -- 3-Day Moving Average
    AVG(unit_price) OVER(ORDER BY launch_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_3days_avg
From
	dim_product;
    
-- Ranking Functions

-- Q1)
Select 
	total_amount,
    row_number() over(order by total_amount) as unique_id,
    rank() over(order by total_amount) as rank_num,
    dense_rank() over(order by total_amount) as dense_rank_num
From
	fact_sales;
    
-- Q2) Partition By
Select 
	date_key,
    quantity_sold,
    row_number() over(partition by date_key order by quantity_sold) as unique_id,
    rank() over(partition by date_key order by quantity_sold) as rank_num,
    dense_rank() over(partition by date_key order by quantity_sold) as dense_rank_num
From
	fact_sales;
    
    
    
    
    
    
    