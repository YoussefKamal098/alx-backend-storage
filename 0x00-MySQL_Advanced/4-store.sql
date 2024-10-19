-- Set the delimiter to $$ to allow for the definition of multi-statement triggers
DELIMITER $$

-- Drop decrease_items_quantity trigger if it exists
DROP TRIGGER IF EXISTS  decrease_items_quantity;

-- Create a trigger named 'decrease_items_quantity'
CREATE TRIGGER decrease_items_quantity
AFTER INSERT ON orders FOR EACH ROW                    -- Trigger activates after an insert on the 'orders' table for each row
BEGIN
    UPDATE items SET quantity = quantity - NEW.number  -- Update 'items' table, reducing 'quantity' by the number of items in the new order
    WHERE name = NEW.item_name;                        -- Match the item by name from the new order
END $$

-- Reset the delimiter back to the default
DELIMITER ;
