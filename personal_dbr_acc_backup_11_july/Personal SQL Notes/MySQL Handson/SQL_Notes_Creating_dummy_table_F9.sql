-- Some important scripts used while doing course.
-- 1) Creating table staging_employees.
use ecom;
CREATE TABLE IF NOT EXISTS staging_employees (
    row_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    emp_name VARCHAR(50),
    department VARCHAR(50),
    salary INT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Insert test data (Contains intentional duplicates)
INSERT INTO staging_employees (emp_id, emp_name, department, salary) VALUES
(101, 'Ansh', 'Data Engineering', 95000),  -- Unique entry
(102, 'Rahul', 'Analytics', 75000),         -- Duplicate baseline (Older record)
(102, 'Rahul', 'Analytics', 75000),         -- Exact duplicate row (Newer record)
(103, 'Sania', 'HR', 60000),                -- Unique entry
(104, 'Amit', 'DevOps', 85000),             -- Partial duplicate baseline (Different salary)
(104, 'Amit', 'DevOps', 90000),             -- Partial duplicate (Updated salary row)
(105, 'Vikram', 'Data Engineering', 95000), -- Duplicate baseline
(105, 'Vikram', 'Data Engineering', 95000); -- Exact duplicate row
select * from staging_employees;

-- 2) Creating table weather.
CREATE TABLE weather
(
`day` INT,
temp FLOAT
);
INSERT INTO weather
VALUES
(1,10),
(2,12),
(3,9),
(4,15),
(5,20),
(6,15),
(7,12);
select * from weather;








