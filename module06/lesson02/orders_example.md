```
-- Table: Users
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Table: Orders
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id),
    order_date DATE NOT NULL
);

-- Table: Products
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Table: OrderItems (Many-to-many relationship between Orders and Products)
CREATE TABLE OrderItems (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES Orders(order_id),
    product_id INT REFERENCES Products(product_id),
    quantity INT NOT NULL
);


-- Insert data into Users table
INSERT INTO Users (username, email) VALUES
('john_doe', 'john@example.com'),
('jane_doe', 'jane@example.com'),
('bob_smith', 'bob@example.com');

-- Insert data into Products table
INSERT INTO Products (product_name, price) VALUES
('Laptop', 1000.00),
('Mouse', 25.00),
('Keyboard', 45.00),
('Monitor', 200.00);

-- Insert data into Orders table
INSERT INTO Orders (user_id, order_date) VALUES
(1, '2024-09-19'),
(2, '2024-09-18'),
(1, '2024-09-17');

-- Insert data into OrderItems table
INSERT INTO OrderItems (order_id, product_id, quantity) VALUES
(1, 1, 1), -- John ordered 1 Laptop
(1, 2, 2), -- John ordered 2 Mice
(2, 3, 1), -- Jane ordered 1 Keyboard
(3, 4, 2); -- John ordered 2 Monitors


-- Get all orders with user info
SELECT u.username, o.order_date, p.product_name, oi.quantity
FROM Users u
JOIN Orders o ON u.user_id = o.user_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id;


-- Get all users and their orders, even if they haven't placed any orders
SELECT u.username, o.order_date, p.product_name, oi.quantity
FROM Users u
LEFT JOIN Orders o ON u.user_id = o.user_id
LEFT JOIN OrderItems oi ON o.order_id = oi.order_id
LEFT JOIN Products p ON oi.product_id = p.product_id;

-- Get all products and the users who ordered them, even if no one has ordered a product
SELECT p.product_name, u.username, o.order_date, oi.quantity
FROM Products p
RIGHT JOIN OrderItems oi ON p.product_id = oi.product_id
RIGHT JOIN Orders o ON oi.order_id = o.order_id
RIGHT JOIN Users u ON o.user_id = u.user_id;


-- Get all users and products with orders if they exist
SELECT u.username, p.product_name, o.order_date, oi.quantity
FROM Users u
FULL OUTER JOIN Orders o ON u.user_id = o.user_id
FULL OUTER JOIN OrderItems oi ON o.order_id = oi.order_id
FULL OUTER JOIN Products p ON oi.product_id = p.product_id;

-- Get users who ordered 'Laptop'
SELECT u.username
FROM Users u
JOIN Orders o ON u.user_id = o.user_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
WHERE p.product_name = 'Laptop';


-- Get the highest spending user
SELECT u.username, SUM(p.price * oi.quantity) AS total_spent
FROM Users u
JOIN Orders o ON u.user_id = o.user_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY u.username
ORDER BY total_spent DESC
LIMIT 1;

```