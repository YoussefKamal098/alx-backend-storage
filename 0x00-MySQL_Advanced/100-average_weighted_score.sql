-- Drop the procedure if it already exists to avoid errors when creating a new one
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Set a custom delimiter to allow for multi-line statements
DELIMITER $$

-- Create a stored procedure named ComputeAverageWeightedScoreForUser
-- It takes one parameter: user_id of type INT
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN

    -- Declare a variable to store the average score, initialized to 0
    DECLARE avg_score INT DEFAULT 0;

    -- Calculate the average weighted score for the specified user
    -- The calculation is done by summing the product of scores and weights
    -- and dividing it by the total weights
    -- The result is stored in the avg_score variable
    SELECT SUM(score * weight) / SUM(weight) INTO avg_score
    FROM projects
    JOIN corrections ON id = project_id
    WHERE corrections.user_id = user_id
    GROUP BY corrections.user_id;

    -- Update the users table to set the average_score for the specified user
    UPDATE users SET average_score = avg_score WHERE id = user_id;

END $$

-- Reset the delimiter back to the default
DELIMITER ;
