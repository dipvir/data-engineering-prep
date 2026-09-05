-- -- How to create Stored Procedure in sql.
-- A stored procedure in MySQL is a predefined set of SQL statements that are stored in
-- the database and can be executed (called) whenever needed.
-- Think of it like a function in programming: you write the logic once and then reuse it multiple times.
-- More advance then what views can do, mostly used to execute DML scripts.

-- Note :- This Syntax will stricky work on mysql and other databases 
-- have there own way of creating stored procedure.

-- SP -> 1) Creating Stored Procedure first_SP.
Delimiter //
Create Procedure first_SP(IN p_id Int, IN p_name char(100), IN p_mail char(100))
Begin
	Insert Into customers
    Values 
    (p_id, p_name, p_mail);
End //

Delimiter ;

-- So, now we can directly call this stored procedure like a function and pass inputs.
call ecom.first_SP(401, 'deep', 'dadd');

-- SP -> 2) Creating Stored Procedure sp_UpdateEmployeeProfile.
DELIMITER //

CREATE PROCEDURE sp_UpdateEmployeeProfile(
    IN input_emp_id INT,
    IN new_dept VARCHAR(50),
    IN salary_increment INT
)
BEGIN
    -- Step 1: Execute the profile modification
    UPDATE staging_employees
    SET department = new_dept,
        salary = salary + salary_increment
    WHERE emp_id = input_emp_id;
    
    -- Step 2: Fetch the freshly modified record to verify
    SELECT emp_id, emp_name, department, salary 
    FROM staging_employees 
    WHERE emp_id = input_emp_id;
END //

DELIMITER ;

-- So, now we can directly call this stored procedure like a function and pass inputs.
CALL sp_UpdateEmployeeProfile(103, 'Data Engineering', 88000);






