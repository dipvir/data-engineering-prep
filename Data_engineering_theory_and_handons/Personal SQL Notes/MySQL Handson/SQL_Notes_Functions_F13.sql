-- Functions(User Defined Functions) in MySQL are predefined or user-defined saved
-- programs (routines) that perform operations on data and return a single value.
-- They are very useful for manipulating data, performing calculations, and simplifying queries.	

-- Func -> 1) Creating a function square_it.
Delimiter //
Create Function square_it(x float)
Returns double
Deterministic
Begin
	Return round(x*x,2);
End //

Delimiter ;

-- Using the function square_it.
Select 
	unit_price,
    square_it(unit_price) as squared_unit_price
From
	dim_product;
    
-- Func -> 2) Creating a function fn_GetTaxBracket.
DELIMITER //

CREATE FUNCTION fn_GetTaxBracket(emp_salary INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
    DECLARE bracket VARCHAR(20);
    
    IF emp_salary >= 110000 THEN
        SET bracket = 'Tier 1 (High)';
    ELSEIF emp_salary >= 90000 THEN
        SET bracket = 'Tier 2 (Medium)';
    ELSE
        SET bracket = 'Tier 3 (Standard)';
    END IF;
    
    RETURN bracket;
END //

DELIMITER ;

-- Using the function fn_GetTaxBracket.
SELECT 
    emp_id, 
    emp_name, 
    salary,
    fn_GetTaxBracket(salary) AS tax_tier
FROM 
    staging_employees;