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


-- Drop the procedure if it already exists to avoid errors when creating a new one
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Set a custom delimiter to allow for multi-line statements
DELIMITER $$

-- Create the procedure ComputeAverageWeightedScoreForUsers
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare variables
    DECLARE user_id INT;
    DECLARE done INT DEFAULT 0;  -- Variable to signal the end of the cursor
    DECLARE users_cursor CURSOR FOR SELECT id FROM users;  -- Cursor for user IDs
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;  -- Handler for cursor end

    -- Open the cursor
    OPEN users_cursor;

    -- Loop through the users
    users_avg_score_loop: LOOP
        -- Fetch the next user ID
        FETCH users_cursor INTO user_id;  -- Use the declared variable instead of session variable

        -- Check if done
        IF done THEN
            LEAVE users_avg_score_loop;  -- Exit the loop if all users are processed
        END IF;

        -- Call the procedure to compute the average score for the user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;

    -- Close the cursor
    CLOSE users_cursor;
END $$

-- Reset the delimiter back to the default
DELIMITER ;
