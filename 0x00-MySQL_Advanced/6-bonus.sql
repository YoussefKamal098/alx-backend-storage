-- Drop AddBonus procedure if it exists
DROP PROCEDURE IF EXISTS AddBonus;

-- Set the delimiter to $$ to allow for the definition of the stored procedure
DELIMITER $$

-- Create a stored procedure named 'AddBonus'
CREATE PROCEDURE AddBonus (
    IN user_id INT,                               -- Input parameter for user ID
    IN project_name VARCHAR(255),                 -- Input parameter for project name
    IN score INT                                   -- Input parameter for score
)
BEGIN
    DECLARE project_id INT;                           -- Declare a variable for the project ID

    -- Check if the project already exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;                        -- Select the project ID into 'project_id' if the project name matches

    -- If the project does not exist, insert it
    IF project_id IS NULL THEN                         -- If no project ID was found
        INSERT INTO projects (name) VALUES (project_name);  -- Insert a new project with the provided name
        SET project_id = LAST_INSERT_ID();            -- Get the ID of the last inserted project
    END IF;

    -- Insert the correction into the corrections table
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END $$

-- Reset the delimiter back to the default
DELIMITER ;
