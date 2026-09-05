-- Subqueries in SQL.

Select avg(unit_price) from dim_product;

-- Subqueries Example
-- Q1)
Select
	*
from
	dim_product
Where 
	unit_price > (Select avg(unit_price) from dim_product);

-- Q2)
Select
	*
from (
	Select
		product_key,
        product_name, 
        brand, 
        unit_price
	from
		dim_product
	Where 
		unit_price > (Select avg(unit_price) from dim_product)
) as Subquery_table
where brand = 'BrandA';

-- CTEs(Common Table Expressions) in SQL.

-- Q1)
With cte_table as
(
Select
	*
from
	dim_product
Where 
	unit_price > (Select avg(unit_price) from dim_product)
),
cte_table_2 as
(
	SELECT 
		product_key,
        product_name, 
        brand, 
        unit_price 
	FROM 
		cte_table
	WHERE 
		product_name IN ('Figure Method', 'Huge Change', 'Film Finally')
)
SELECT 
	*
FROM 
	cte_table_2
WHERE
	product_name = 'Figure Method';
