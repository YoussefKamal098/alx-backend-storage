-- Create a table named 'users' if it does not already exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- 'id' is an integer that auto-increments and serves as the primary key
    email VARCHAR(255) NOT NULL UNIQUE,     -- 'email' is a variable character field, must be unique and cannot be null
    name VARCHAR(255)                        -- 'name' is a variable character field that can be null
);
