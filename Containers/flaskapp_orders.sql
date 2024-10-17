-- Table structure for table `orders`

DROP TABLE IF EXISTS orders;

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    burger_name TEXT NOT NULL,
    side_name TEXT NOT NULL,
    comment TEXT,
    order_type TEXT NOT NULL
);

-- Dumping data for table `orders`
INSERT INTO `orders` VALUES 
(1,'CheeseBurger','Cheesy Fries','no tomato','Delivery'),
(2,'CheeseBurger','Large Fries','no tomato','Pickup'),
(3,'CheeseBurger','Cheesy Fries','no tomato','Delivery'),
(4,'CheeseBurger','Large Fries','','Delivery'),
(5,'DoubleBurger','Large Fries','','Delivery'),
...
(28,'CheeseBurger','Large Fries','yes','Pickup');
