CREATE DATABASE IF NOT EXISTS optimization_db;
USE optimization_db;

-- We intentionally create this table WITHOUT a Primary Key or Indexes
CREATE TABLE IF NOT EXISTS users_raw (
    user_id INT,
    first_name VARCHAR(50),
    email VARCHAR(100),
    signup_date DATE,
    country VARCHAR(50)
);

-- Populating 1 Million Rows
DELIMITER $$

CREATE PROCEDURE PopulatedData()
BEGIN
    DECLARE i INT DEFAULT 1;
    -- Turn off autocommit and checks to make inserts blazing fast
    SET autocommit = 0;
    SET unique_checks = 0;
    SET foreign_key_checks = 0;

    WHILE i <= 1000000 DO
        INSERT INTO users_raw (user_id, first_name, email, signup_date, country) 
        VALUES (
            i, 
            CONCAT('User', i), 
            CONCAT('user', i, '@example.com'), 
            DATE_ADD('2020-01-01', INTERVAL (i % 2000) DAY),
            CASE i % 4 
                WHEN 0 THEN 'India' 
                WHEN 1 THEN 'USA' 
                WHEN 2 THEN 'UK' 
                ELSE 'Canada' 
            END
        );
        
        -- CommitPopulatedData in batches of 50,000 to keep memory stable
        IF i % 50000 = 0 THEN
            COMMIT;
        END IF;
        
        SET i = i + 1;
    END WHILE;
    
    COMMIT;
END$$

DELIMITER ;

-- Execute the procedure to load the data
CALL PopulatedData();

