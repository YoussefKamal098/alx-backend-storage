-- Drop ComputeAverageScoreForUser procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Change the statement delimiter to $$ to allow for defining the procedure without interference from semicolons.
DELIMITER $$

-- Create a stored procedure named ComputeAverageScoreForUser that takes a user_id as an input parameter.
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    -- Declare a variable to hold the calculated average score.
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Select the average score from the corrections table for the specified user_id.
    -- The result is stored in the avg_score variable.
    -- The AVG function calculates the average score of all corrections for the given user.
    -- GROUP BY user_id is used to ensure that the average is computed per user, although it's unnecessary
    -- since we're filtering by a specific user_id.
    SELECT AVG(score) INTO avg_score FROM corrections
    WHERE corrections.user_id = user_id GROUP BY user_id;

    -- Update the average_score field in the users table for the specified user_id with the computed average.
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END $$

-- Restore the statement delimiter back to the default semicolon.
DELIMITER ;
