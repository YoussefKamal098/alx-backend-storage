-- Query to select the origin of metal bands and the total number of fans for each origin
SELECT origin, SUM(fans) as nb_fans                  -- Select the origin and sum of fans, aliasing it as 'nb_fans'
FROM metal_bands                                     -- From the 'metal_bands' table
GROUP BY origin                                       -- Group results by origin
ORDER BY nb_fans DESC; 
