-- Drop the procedure if it already exists to avoid errors when creating a new one
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Set a custom delimiter to allow for multi-line statements
DELIMITER $$

-- Create a stored procedure named ComputeAverageWeightedScoreForUser
-- It takes one parameter: user_id of type INT
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN

    -- Declare a variable to store the average score, initialized to 0
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Check if the user exists before calculating the average score
    IF EXISTS (SELECT name FROM users WHERE id = user_id) THEN

        -- Calculate the average weighted score for the specified user
        -- The calculation is done by summing the product of scores and weights
        -- and dividing it by the total weights. If no scores exist, avg_score will be NULL.
        SELECT IFNULL(SUM(score * weight) / NULLIF(SUM(weight), 0), 0) INTO avg_score
        FROM projects JOIN corrections ON id = project_id
        WHERE corrections.user_id = user_id;

        -- Update the users table to set the average_score for the specified user
        UPDATE users SET average_score = avg_score WHERE id = user_id;

    ELSE
        -- Optionally, handle the case where the user does not exist
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User does not exist';
    END IF;

END $$

-- Reset the delimiter back to the default
DELIMITER ;

---------------------------------------- ALTERNATIVE APPROACH ------------------------------------------------

-- Set a custom delimiter to allow for multi-line statements
DELIMITER $$

-- Drop the procedure if it already exists to avoid errors when creating a new one
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Create the procedure ComputeAverageWeightedScoreForUser
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    -- Update the average_score in the users table for the specified user
    UPDATE users
    SET average_score = (
        -- Calculate the average weighted score
        SELECT SUM(corrections.score * projects.weight) / SUM(projects.weight)
        FROM corrections
        INNER JOIN projects ON projects.id = corrections.project_id
        WHERE corrections.user_id = user_id
    )
    WHERE users.id = user_id; -- Ensure we only update the specified user
END $$

-- Reset the delimiter back to the default
DELIMITER ;
