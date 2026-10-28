USE shopsphere;

INSERT INTO customers
(customer_id, customer_name, gender, age, city, state, signup_date)
VALUES
('C001', 'Sandeep', 'Male', 25, 'Hyderabad', 'Telangana', '2025-06-15'),
('C002', 'Rahul', 'Male', 28, 'Chennai', 'Tamil Nadu', '2025-07-20'),
('C003', 'Priya', 'Female', 24, 'Bangalore', 'Karnataka', '2025-08-10'),
('C004', 'Arjun', 'Male', 31, 'Mumbai', 'Maharashtra', '2025-09-05'),
('C005', 'Ananya', 'Female', 27, 'Pune', 'Maharashtra', '2025-10-12'),
('C006', 'Vikram', 'Male', 29, 'Delhi', 'Delhi', '2025-11-18'),
('C007', 'Sneha', 'Female', 23, 'Kochi', 'Kerala', '2025-12-01'),
('C008', 'Kiran', 'Male', 26, 'Visakhapatnam', 'Andhra Pradesh', '2026-01-14'),
('C009', 'Meena', 'Female', 30, 'Hyderabad', 'Telangana', '2026-02-20'),
('C010', 'Rohit', 'Male', 33, 'Bangalore', 'Karnataka', '2026-03-11');

INSERT INTO categories
(category_id, category_name)
VALUES
('CAT01', 'Electronics'),
('CAT02', 'Fashion'),
('CAT03', 'Home & Kitchen'),
('CAT04', 'Beauty'),
('CAT05', 'Sports');

INSERT INTO products
(product_id, product_name, category_id, brand, cost_price, selling_price)
VALUES
('P001', 'iPhone 15', 'CAT01', 'Apple', 52000, 60000),
('P002', 'Galaxy S24', 'CAT01', 'Samsung', 55000, 65000),
('P003', 'Running Shoes', 'CAT05', 'Nike', 2500, 4000),
('P004', 'T-Shirt', 'CAT02', 'Puma', 700, 1200),
('P005', 'Laptop', 'CAT01', 'Dell', 55000, 70000),
('P006', 'Headphones', 'CAT01', 'Sony', 1800, 2500),
('P007', 'Mixer Grinder', 'CAT03', 'Philips', 3000, 4500),
('P008', 'Face Wash', 'CAT04', 'Minimalist', 250, 399),
('P009', 'Yoga Mat', 'CAT05', 'Boldfit', 500, 899),
('P010', 'Jeans', 'CAT02', 'Levis', 1500, 2500);

INSERT INTO orders
(order_id, customer_id, order_date, order_status, payment_method)
VALUES
('O1001', 'C001', '2026-08-01', 'Delivered', 'UPI'),
('O1002', 'C002', '2026-08-02', 'Delivered', 'Card'),
('O1003', 'C001', '2026-08-03', 'Cancelled', 'UPI'),
('O1004', 'C003', '2026-08-05', 'Delivered', 'UPI'),
('O1005', 'C004', '2026-08-07', 'Delivered', 'Cash'),
('O1006', 'C005', '2026-08-10', 'Delivered', 'Card'),
('O1007', 'C006', '2026-08-12', 'Cancelled', 'UPI'),
('O1008', 'C007', '2026-08-15', 'Delivered', 'UPI'),
('O1009', 'C008', '2026-08-18', 'Delivered', 'Card'),
('O1010', 'C009', '2026-08-20', 'Delivered', 'UPI'),
('O1011', 'C001', '2026-08-22', 'Delivered', 'Card'),
('O1012', 'C010', '2026-08-25', 'Delivered', 'UPI');

INSERT INTO order_items
(order_id, product_id, quantity, selling_price, discount)
VALUES
('O1001', 'P001', 1, 60000, 0),
('O1001', 'P003', 2, 4000, 10),
('O1002', 'P004', 3, 1200, 5),
('O1003', 'P002', 1, 65000, 0),
('O1004', 'P004', 2, 1200, 0),
('O1005', 'P006', 2, 2500, 5),
('O1006', 'P005', 1, 70000, 10),
('O1007', 'P007', 1, 4500, 0),
('O1008', 'P009', 2, 899, 0),
('O1009', 'P002', 1, 65000, 5),
('O1010', 'P008', 2, 399, 0),
('O1011', 'P001', 1, 60000, 5),
('O1011', 'P010', 1, 2500, 0),
('O1012', 'P003', 1, 4000, 0);

INSERT INTO payments
(payment_id, order_id, payment_date, payment_method, amount, payment_status)
VALUES
('PAY001', 'O1001', '2026-08-01', 'UPI', 67200, 'Successful'),
('PAY002', 'O1002', '2026-08-02', 'Card', 3420, 'Successful'),
('PAY003', 'O1003', '2026-08-03', 'UPI', 0, 'Failed'),
('PAY004', 'O1004', '2026-08-05', 'UPI', 2400, 'Successful'),
('PAY005', 'O1005', '2026-08-07', 'Cash', 4750, 'Successful'),
('PAY006', 'O1006', '2026-08-10', 'Card', 63000, 'Successful'),
('PAY007', 'O1007', '2026-08-12', 'UPI', 0, 'Failed'),
('PAY008', 'O1008', '2026-08-15', 'UPI', 1798, 'Successful'),
('PAY009', 'O1009', '2026-08-18', 'Card', 61750, 'Successful'),
('PAY010', 'O1010', '2026-08-20', 'UPI', 798, 'Successful'),
('PAY011', 'O1011', '2026-08-22', 'Card', 59500, 'Successful'),
('PAY012', 'O1012', '2026-08-25', 'UPI', 4000, 'Successful');

INSERT INTO deliveries
(delivery_id, order_id, shipped_date, delivered_date, delivery_status)
VALUES
('D001', 'O1001', '2026-08-02', '2026-08-05', 'Delivered'),
('D002', 'O1002', '2026-08-03', '2026-08-06', 'Delivered'),
('D003', 'O1004', '2026-08-06', '2026-08-09', 'Delivered'),
('D004', 'O1005', '2026-08-08', '2026-08-12', 'Delivered'),
('D005', 'O1006', '2026-08-11', '2026-08-16', 'Delivered'),
('D006', 'O1008', '2026-08-16', '2026-08-19', 'Delivered'),
('D007', 'O1009', '2026-08-19', '2026-08-23', 'Delivered'),
('D008', 'O1010', '2026-08-21', '2026-08-24', 'Delivered'),
('D009', 'O1011', '2026-08-23', '2026-08-27', 'Delivered'),
('D010', 'O1012', '2026-08-26', NULL, 'In Transit');

INSERT INTO reviews
(review_id, order_id, customer_id, product_id, rating, review_date)
VALUES
('R001', 'O1001', 'C001', 'P001', 5, '2026-08-06'),
('R002', 'O1001', 'C001', 'P003', 4, '2026-08-06'),
('R003', 'O1002', 'C002', 'P004', 3, '2026-08-07'),
('R004', 'O1004', 'C003', 'P004', 4, '2026-08-10'),
('R005', 'O1005', 'C004', 'P006', 2, '2026-08-13'),
('R006', 'O1006', 'C005', 'P005', 5, '2026-08-17'),
('R007', 'O1008', 'C007', 'P009', 4, '2026-08-20'),
('R008', 'O1009', 'C008', 'P002', 5, '2026-08-24'),
('R009', 'O1010', 'C009', 'P008', 3, '2026-08-25'),
('R010', 'O1011', 'C001', 'P001', 4, '2026-08-28');

