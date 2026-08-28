use optimization_db;

-- Test 1: Find a user near the end of the table (Without Index)
SELECT * FROM users_raw WHERE email = 'user987654@example.com'; -- 2.2 sec

-- EXPLAIN SELECT * FROM users_raw WHERE email = 'user987654@example.com';

-- This creates the index structure
CREATE INDEX idx_user_email ON users_raw(email);

-- Test 2: Find a user near the end of the table (With Index)
SELECT * FROM users_raw WHERE email = 'user987654@example.com'; -- 0.02 sec

-- Test 3: Look for emails ending in a specific pattern using a wildcard at the START (With Index but its skiped)
SELECT * FROM users_raw WHERE email LIKE '%user987654@example.com'; -- 2.4 sec


-- select count(*) from users_raw;
-- truncate table users_raw
-- DROP INDEX idx_user_email ON users_raw;