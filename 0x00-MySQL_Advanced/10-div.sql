-- Drop the function SafeDiv if it already exists
DROP FUNCTION IF EXISTS SafeDiv;

-- Change the statement delimiter to $$ to allow the use of multiple statements in the function definition
DELIMITER $$

-- Create a new function called SafeDiv which takes two input parameters 'a' and 'b', both of type INT
CREATE FUNCTION SafeDiv(a INT, b INT)
-- The function returns a FLOAT value and is deterministic, meaning it will always return the same result for the same inputs
RETURNS FLOAT DETERMINISTIC
BEGIN
    -- The function checks if 'b' is 0, and if so, it returns 0 to avoid division by zero errors.
    -- Otherwise, it returns the result of 'a' divided by 'b'.
    RETURN (IF (b = 0, 0, a / b));
END $$

-- Reset the statement delimiter back to the default ';'
DELIMITER ;
