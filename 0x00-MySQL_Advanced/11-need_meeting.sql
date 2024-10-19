-- Drop the view if it already exists
DROP VIEW IF EXISTS need_meeting;

-- Create the view need_meeting
CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80  -- Only include students with a score strictly less than 80
  AND (last_meeting IS NULL  -- Include students with no last meeting
  OR last_meeting < CURDATE() - INTERVAL 1 MONTH);  -- Include students whose last meeting was more than 1 month ago
