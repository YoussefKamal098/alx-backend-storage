-- Create the names table

DROP TABLE IF EXISTS names;

CREATE TABLE IF NOT EXISTS names (
  `name` varchar(255) DEFAULT NULL,
  `score` int(11) DEFAULT NULL
);

-- Insert sample data into the names table
INSERT INTO `names` (`name`, `score`) VALUES
('Alice', 85),
('Bob', 75),
('Charlie', 90),
('Diana', 65),
('Eve', 95),
('Frank', 80),
('Martha', 70);
