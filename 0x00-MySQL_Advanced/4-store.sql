-- Trigger that decreases items after an order is made

CREATE TRIGGER after_adding_order
AFTER INSERT ON oders
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
