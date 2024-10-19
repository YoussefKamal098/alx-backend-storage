-- Query to select the lifespan of metal bands in the glam rock style
SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan  -- Select band name and calculate lifespan; if 'split' is null, use 2022
FROM metal_bands                                       -- From the 'metal_bands' table
WHERE style LIKE "%Glam rock%"                         -- Filter results to include only glam rock style bands
ORDER BY lifespan DESC;   
