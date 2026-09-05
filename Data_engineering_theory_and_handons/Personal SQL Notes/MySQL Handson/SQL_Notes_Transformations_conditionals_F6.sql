-- This File will cover how we can do transformations over data.
-- Note :- Some of them will be covered here as there are plenty of options. 

-- 1) Numeric Transformation
Select
	product_id,
	product_name,
    category,
    unit_price,
    unit_price * .90 as discounted_price, -- 10% off
    unit_price + 10 as taxed_price,
    unit_price / 10 as fractioned_price,
    round(unit_price, 1) as rounded_price,
    unit_price * unit_price as new_price
From 
	dim_product;

-- 2) Date Transformation
-- Q1)
Select 
	*,
    now() as 'current_timestamp',
    utc_date(),
    utc_time(),
    utc_timestamp(),
    date(utc_timestamp()),
    time(utc_timestamp())
From
	dim_date;
-- Note:- current_timestamp is a reserved keyword in MYSQL.
-- If we have to use still then we have to put quotes around it.

-- Q2)
Select 
	date_key,
    date,
    is_weekend,
    year(date) as get_year,
    month(date) as get_month,
    day(date) as get_day,
    weekday(date) as get_weekday,
    week(date) as get_week,
    weekofyear(date) as get_weekofyear,
    dayname(date) as get_dayname,
    adddate(date , 4) as get_adddate,
    subdate(date , 4) as get_subdate,
    date(utc_timestamp()) as current_utc_date,
    datediff(date(utc_timestamp()) , date) as total_days
From
	dim_date
order by 
	date;
    
-- Q3) Date Format And Type Casting
SELECT 
    *,
    DATE_FORMAT(date, '%W %M %e %Y') AS formated_date,
    CAST(day AS CHAR) AS day_char,
    CAST(date_key AS DATETIME) AS date_key_datetime
FROM
    dim_date;

-- 3) String Functions
SELECT 
    first_name,
    last_name,
    gender,
    country,
    email,
    concat(first_name, " " ,last_name) as full_name,
    concat_ws(" ", first_name, last_name, gender, country) as name_gender_location,
    length(country),
    lower(country),
    substr(email, 1, 4),
    substr(email, 2, 4),
    replace(email, '@' , '_'),
    left(email, 4),
    right(email, 3),
    reverse(email),
    repeat(first_name, 3)
FROM
    dim_customer;

-- 4) Conditonal Statements

-- Q1)
Select 
	product_key,
    product_name,
    Category,
    unit_price,
    Case 
	When unit_price <= 200 Then "Low Category"
    When unit_price <= 500 Then "Mid Category"
    Else "Rich Category" End As unit_price_Category,
    Case 
	When unit_price <= 200 Then "Low Category"
    When unit_price <= 500 Then "Mid Category"
    Else unit_price End As unit_price_Category_2    
From
	dim_product;

-- Q2)
Select 
	product_key,
    product_name,
    Category,
    unit_price,
    Case 
	When unit_price <= 200 and Category = "Clothing" Then "Low Category"
    When unit_price <= 500  and Category = "Clothing" Then "Mid Category"
    When unit_price > 500  and Category = "Clothing" Then "Rich Category"
    Else Concat("Not Applicable For " ,Category) End As Clothing_price_Category
From
	dim_product;


-- extra rough queries below
Select
	*
From
	fact_sales
where 
	date_key > subdate(
    (select max(date_key) from fact_sales ) 
		,30)
order by date_key










    
    