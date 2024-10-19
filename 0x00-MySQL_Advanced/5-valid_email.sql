-- Drop resets_valid_email trigger if it exists
DROP TRIGGER IF EXISTS resets_valid_email;

-- Set the delimiter to $$ to allow for the definition of multi-statement triggers
DELIMITER $$

-- Create a trigger named 'resets_valid_email'
CREATE TRIGGER resets_valid_email
BEFORE UPDATE ON users FOR EACH ROW                     -- Trigger activates before an update on the 'users' table for each row
BEGIN
    IF NEW.email <> OLD.email THEN                      -- Check if the new email is different from the old email
        SET NEW.valid_email = 0;                       -- If different, set 'valid_email' to 0
    END IF;
END $$

-- Reset the delimiter back to the default
DELIMITER ;
