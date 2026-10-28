-- Q1. Total Gross Revenue from Delivered Orders

SELECT
    SUM(o.quantity * o.selling_price) AS gross_revenue
FROM order_items AS o
INNER JOIN orders AS p
    ON o.order_id = p.order_id
WHERE p.order_status = 'Delivered';

-- Q2. Total Net Revenue After Discounts

SELECT
    SUM(
        o.quantity * o.selling_price * (1 - o.discount / 100)
    ) AS net_revenue
FROM order_items AS o
INNER JOIN orders AS p
    ON o.order_id = p.order_id
WHERE p.order_status = 'Delivered';

-- Q3. Total Orders, Total Customers and Average Order Value

SELECT
    COUNT(DISTINCT p.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    SUM(
        o.quantity * o.selling_price * (1 - o.discount / 100)
    ) / COUNT(DISTINCT p.order_id) AS average_order_value
FROM orders AS p
INNER JOIN customers AS c
    ON p.customer_id = c.customer_id
INNER JOIN order_items AS o
    ON p.order_id = o.order_id
WHERE p.order_status = 'Delivered';

-- Q4. Revenue by Category

SELECT
    c.category_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS net_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
JOIN categories AS c
    ON p.category_id = c.category_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_name
ORDER BY net_revenue DESC;

-- Q5. Find the Top 5 products based on net revenue.

SELECT
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS net_revenue
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
ORDER BY net_revenue DESC
LIMIT 5;

-- Q6. Find the Top 5 products based on total quantity sold.

SELECT
    p.product_name,
    SUM(oi.quantity) AS total_quantity_sold
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity_sold DESC
LIMIT 5;

-- Q7. Calculate revenue, total cost, and profit for each product.

SELECT
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    SUM(oi.quantity * p.cost_price) AS total_cost,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) - SUM(oi.quantity * p.cost_price) AS profit
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
ORDER BY profit DESC;

-- Q8. Calculate revenue, cost, profit, and profit margin for each category.

SELECT
    c.category_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    SUM(oi.quantity * p.cost_price) AS total_cost,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) - SUM(oi.quantity * p.cost_price) AS profit,
    (
        (
            SUM(
                oi.quantity * oi.selling_price * (1 - oi.discount / 100)
            ) - SUM(oi.quantity * p.cost_price)
        )
        / SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        )
    ) * 100 AS profit_margin
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
JOIN categories AS c
    ON p.category_id = c.category_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_id, c.category_name
ORDER BY profit DESC;

-- Q9. Find the best-selling product in each category based on revenue.

WITH product_revenue AS (
    SELECT
        c.category_name,
        p.product_name,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    JOIN products AS p
        ON oi.product_id = p.product_id
    JOIN categories AS c
        ON p.category_id = c.category_id
    WHERE o.order_status = 'Delivered'
    GROUP BY c.category_name, p.product_id, p.product_name
),
ranked_products AS (
    SELECT
        category_name,
        product_name,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category_name
            ORDER BY revenue DESC
        ) AS product_rank
    FROM product_revenue
)
SELECT
    category_name,
    product_name,
    revenue
FROM ranked_products
WHERE product_rank = 1;

-- Q10. Find each customer's total orders, total revenue,
-- and revenue rank.

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    RANK() OVER (
        ORDER BY SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) DESC
    ) AS revenue_rank
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name;

-- Q11. Find the Top 5 customers based on total revenue.

SELECT
    c.customer_id,
    c.customer_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name
ORDER BY revenue DESC
LIMIT 5;

-- Q12. Find customers who placed more than one delivered order.

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name
HAVING COUNT(DISTINCT o.order_id) > 1;

-- Q13. Calculate the Average Order Value (AOV) for each customer.

SELECT
    c.customer_id,
    c.customer_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) / COUNT(DISTINCT o.order_id) AS customer_aov
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name;

-- Q14. Segment customers based on their total revenue:
-- High Value: ₹50,000 or more
-- Medium Value: ₹20,000 to ₹49,999
-- Low Value: below ₹20,000

SELECT
    c.customer_id,
    c.customer_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    CASE
        WHEN SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) >= 50000
            THEN 'High Value'

        WHEN SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) >= 20000
            THEN 'Medium Value'

        ELSE 'Low Value'
    END AS customer_segment
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name;

-- Q15. Calculate the total net revenue generated on each day
--      from delivered orders.

SELECT
    o.order_date,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS daily_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY o.order_date
ORDER BY o.order_date;

-- Q16. Calculate monthly total orders, unique customers,
--      and total net revenue from delivered orders.

SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;

-- Q17. Calculate the month-over-month (MoM) revenue change percentage.

WITH monthly_revenue AS (
    SELECT
        DATE_FORMAT(o.order_date, '%Y-%m') AS month,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM orders AS o
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
),
revenue_with_previous AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    month,
    revenue,
    previous_month_revenue,
    ROUND(
        (
            (revenue - previous_month_revenue)
            / previous_month_revenue
        ) * 100,
        2
    ) AS mom_revenue_change_percent
FROM revenue_with_previous
ORDER BY month;

-- Q18. Calculate the month-over-month (MoM) order growth percentage.

WITH monthly_orders AS (
    SELECT
        DATE_FORMAT(order_date, '%Y-%m') AS month,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
),
orders_with_previous AS (
    SELECT
        month,
        total_orders,
        LAG(total_orders) OVER (
            ORDER BY month
        ) AS previous_month_orders
    FROM monthly_orders
)
SELECT
    month,
    total_orders,
    previous_month_orders,
    ROUND(
        (
            (total_orders - previous_month_orders)
            / previous_month_orders
        ) * 100,
        2
    ) AS mom_order_growth_percent
FROM orders_with_previous
ORDER BY month;

-- Q19. Find the date that generated the highest net revenue
--      from delivered orders.

SELECT
    o.order_date,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS daily_revenue
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY o.order_date
ORDER BY daily_revenue DESC
LIMIT 1;

-- Q20. Calculate the daily net revenue and running cumulative
--      revenue from delivered orders.

WITH daily_revenue AS (
    SELECT
        o.order_date,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS daily_revenue
    FROM orders AS o
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY o.order_date
)
SELECT
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY order_date
    ) AS cumulative_revenue
FROM daily_revenue
ORDER BY order_date;

-- Q21. Calculate the number of orders and percentage of total orders
--      for each order status.

SELECT
    order_status,
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS order_percentage
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;

-- Q22. Calculate the overall order cancellation rate.

SELECT
    COUNT(CASE WHEN order_status = 'Cancelled' THEN 1 END) AS cancelled_orders,
    COUNT(*) AS total_orders,
    ROUND(
        COUNT(CASE WHEN order_status = 'Cancelled' THEN 1 END)
        * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_percent
FROM orders;

-- Q23. Find the customers who have placed the most cancelled orders.

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(*) AS cancelled_orders
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'Cancelled'
GROUP BY c.customer_id, c.customer_name
ORDER BY cancelled_orders DESC;

-- Q24. Calculate total orders, total revenue, and Average Order Value
--      for each payment method using successful payments.

SELECT
    p.payment_method,
    COUNT(DISTINCT p.order_id) AS total_orders,
    SUM(p.amount) AS total_revenue,
    SUM(p.amount) / COUNT(DISTINCT p.order_id) AS average_order_value
FROM payments AS p
WHERE p.payment_status = 'Successful'
GROUP BY p.payment_method
ORDER BY total_revenue DESC;

-- Q25. Calculate the payment success rate for each payment method.

SELECT
    payment_method,
    COUNT(*) AS total_payment_attempts,
    COUNT(
        CASE
            WHEN payment_status = 'Successful' THEN 1
        END
    ) AS successful_payments,
    ROUND(
        COUNT(
            CASE
                WHEN payment_status = 'Successful' THEN 1
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS success_rate_percent
FROM payments
GROUP BY payment_method
ORDER BY success_rate_percent DESC;

-- Q26. Calculate the average delivery time in days
--      for successfully delivered orders.

SELECT
    ROUND(
        AVG(DATEDIFF(delivered_date, shipped_date)),
        2
    ) AS average_delivery_days
FROM deliveries
WHERE delivery_status = 'Delivered';

-- Q27. Calculate the delivery time for each order
--      and display its delivery status.

SELECT
    d.order_id,
    d.shipped_date,
    d.delivered_date,
    d.delivery_status,
    CASE
        WHEN d.delivered_date IS NOT NULL
        THEN DATEDIFF(d.delivered_date, d.shipped_date)
        ELSE NULL
    END AS delivery_days
FROM deliveries AS d
ORDER BY d.order_id;

-- Q28. Find the Top 5 slowest delivered orders
--      based on delivery time in days.

SELECT
    d.order_id,
    d.shipped_date,
    d.delivered_date,
    DATEDIFF(d.delivered_date, d.shipped_date) AS delivery_days
FROM deliveries AS d
WHERE d.delivery_status = 'Delivered'
ORDER BY delivery_days DESC
LIMIT 5;

-- Q29. Calculate the number of orders for each delivery status.

SELECT
    delivery_status,
    COUNT(*) AS total_orders
FROM deliveries
GROUP BY delivery_status
ORDER BY total_orders DESC;

-- Q30. Calculate the average rating for each product.

SELECT
    p.product_id,
    p.product_name,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM reviews AS r
JOIN products AS p
    ON r.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY average_rating DESC;

-- Q31. Find the Top 5 products with the highest average rating.

SELECT
    p.product_id,
    p.product_name,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM reviews AS r
JOIN products AS p
    ON r.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY average_rating DESC
LIMIT 5;

-- Q32. Calculate the average product rating for each category.

SELECT
    c.category_name,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM reviews AS r
JOIN products AS p
    ON r.product_id = p.product_id
JOIN categories AS c
    ON p.category_id = c.category_id
GROUP BY c.category_id, c.category_name
ORDER BY average_rating DESC;

-- Q33. Find products with an average rating below 3.5.

SELECT
    p.product_id,
    p.product_name,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM reviews AS r
JOIN products AS p
    ON r.product_id = p.product_id
GROUP BY p.product_id, p.product_name
HAVING AVG(r.rating) < 3.5
ORDER BY average_rating ASC;

-- Q34. Compare each product's net revenue with its average rating
--      to identify the relationship between sales performance
--      and customer satisfaction.

SELECT
    p.product_id,
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM products AS p
JOIN order_items AS oi
    ON p.product_id = oi.product_id
JOIN orders AS o
    ON oi.order_id = o.order_id
LEFT JOIN reviews AS r
    ON p.product_id = r.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC;

-- Q35. Find the top-performing product in each category
--      based on net revenue using a window function.

WITH product_revenue AS (
    SELECT
        c.category_name,
        p.product_id,
        p.product_name,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    JOIN products AS p
        ON oi.product_id = p.product_id
    JOIN categories AS c
        ON p.category_id = c.category_id
    WHERE o.order_status = 'Delivered'
    GROUP BY
        c.category_name,
        p.product_id,
        p.product_name
),
ranked_products AS (
    SELECT
        category_name,
        product_id,
        product_name,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category_name
            ORDER BY revenue DESC
        ) AS product_rank
    FROM product_revenue
)
SELECT
    category_name,
    product_id,
    product_name,
    revenue
FROM ranked_products
WHERE product_rank = 1
ORDER BY category_name;

-- Q36. Find the second-highest revenue-generating product
--      based on net revenue.

WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    JOIN products AS p
        ON oi.product_id = p.product_id
    WHERE o.order_status = 'Delivered'
    GROUP BY p.product_id, p.product_name
),
ranked_products AS (
    SELECT
        product_id,
        product_name,
        revenue,
        DENSE_RANK() OVER (
            ORDER BY revenue DESC
        ) AS revenue_rank
    FROM product_revenue
)
SELECT
    product_id,
    product_name,
    revenue
FROM ranked_products
WHERE revenue_rank = 2;

-- Q37. Find the first delivered order date for each customer.

SELECT
    c.customer_id,
    c.customer_name,
    MIN(o.order_date) AS first_delivered_order_date
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name
ORDER BY first_delivered_order_date;

-- Q38. Find the latest delivered order date for each customer.

SELECT
    c.customer_id,
    c.customer_name,
    MAX(o.order_date) AS latest_delivered_order_date
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name
ORDER BY latest_delivered_order_date DESC;

-- Q39. Calculate the number of days between consecutive delivered
--      orders for each customer.

WITH customer_orders AS (
    SELECT
        o.customer_id,
        o.order_id,
        o.order_date,
        LAG(o.order_date) OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date
        ) AS previous_order_date
    FROM orders AS o
    WHERE o.order_status = 'Delivered'
)
SELECT
    customer_id,
    order_id,
    order_date,
    previous_order_date,
    DATEDIFF(
        order_date,
        previous_order_date
    ) AS days_since_previous_order
FROM customer_orders
ORDER BY customer_id, order_date;

-- Q40. Find customers who placed a delivered order in one month
--      and returned to place another delivered order in the following month.

WITH customer_months AS (
    SELECT DISTINCT
        customer_id,
        DATE_FORMAT(order_date, '%Y-%m') AS order_month
    FROM orders
    WHERE order_status = 'Delivered'
),
customer_with_next_month AS (
    SELECT
        customer_id,
        order_month,
        LEAD(order_month) OVER (
            PARTITION BY customer_id
            ORDER BY order_month
        ) AS next_order_month
    FROM customer_months
)
SELECT
    customer_id,
    order_month,
    next_order_month
FROM customer_with_next_month
WHERE next_order_month =
      DATE_FORMAT(
          DATE_ADD(
              STR_TO_DATE(
                  CONCAT(order_month, '-01'),
                  '%Y-%m-%d'
              ),
              INTERVAL 1 MONTH
          ),
          '%Y-%m'
      )
ORDER BY customer_id, order_month;

-- Q41. Find customers who have never cancelled an order.

SELECT
    c.customer_id,
    c.customer_name
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(
    CASE
        WHEN o.order_status = 'Cancelled' THEN 1
        ELSE 0
    END
) = 0
ORDER BY c.customer_id;

-- Q42. Find products that have never been purchased
--      in a delivered order.

SELECT
    p.product_id,
    p.product_name
FROM products AS p
LEFT JOIN order_items AS oi
    ON p.product_id = oi.product_id
LEFT JOIN orders AS o
    ON oi.order_id = o.order_id
    AND o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
HAVING COUNT(o.order_id) = 0
ORDER BY p.product_id;

-- Q43. Calculate each category's percentage contribution
--      to total delivered net revenue.

WITH category_revenue AS (
    SELECT
        c.category_name,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    JOIN products AS p
        ON oi.product_id = p.product_id
    JOIN categories AS c
        ON p.category_id = c.category_id
    WHERE o.order_status = 'Delivered'
    GROUP BY c.category_id, c.category_name
)
SELECT
    category_name,
    revenue,
    ROUND(
        revenue * 100.0 / SUM(revenue) OVER (),
        2
    ) AS revenue_contribution_percent
FROM category_revenue
ORDER BY revenue DESC;

-- Q44. Calculate cumulative revenue and cumulative revenue percentage
--      for products ordered by revenue, to identify products
--      contributing approximately to the first 80% of revenue.

WITH product_revenue AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM order_items AS oi
    JOIN orders AS o
        ON oi.order_id = o.order_id
    JOIN products AS p
        ON oi.product_id = p.product_id
    WHERE o.order_status = 'Delivered'
    GROUP BY p.product_id, p.product_name
),
revenue_analysis AS (
    SELECT
        product_id,
        product_name,
        revenue,
        SUM(revenue) OVER (
            ORDER BY revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue,
        SUM(revenue) OVER () AS total_revenue
    FROM product_revenue
)
SELECT
    product_id,
    product_name,
    revenue,
    cumulative_revenue,
    ROUND(
        cumulative_revenue * 100.0 / total_revenue,
        2
    ) AS cumulative_revenue_percent
FROM revenue_analysis
ORDER BY revenue DESC;

-- Q45. Rank customers by delivered net revenue within each city.

WITH customer_revenue AS (
    SELECT
        c.customer_id,
        c.customer_name,
        c.city,
        SUM(
            oi.quantity * oi.selling_price * (1 - oi.discount / 100)
        ) AS revenue
    FROM customers AS c
    JOIN orders AS o
        ON c.customer_id = o.customer_id
    JOIN order_items AS oi
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'Delivered'
    GROUP BY
        c.customer_id,
        c.customer_name,
        c.city
)
SELECT
    customer_id,
    customer_name,
    city,
    revenue,
    RANK() OVER (
        PARTITION BY city
        ORDER BY revenue DESC
    ) AS city_revenue_rank
FROM customer_revenue
ORDER BY city, city_revenue_rank;

-- Q46. Identify the category generating the highest
--      delivered net revenue.

SELECT
    c.category_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue
FROM categories AS c
JOIN products AS p
    ON c.category_id = p.category_id
JOIN order_items AS oi
    ON p.product_id = oi.product_id
JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.category_id, c.category_name
ORDER BY revenue DESC
LIMIT 1;

-- Q47. Find products generating high revenue but having
--      a relatively low profit margin.
--      Here, high revenue means at least ₹20,000
--      and low profit margin means below 20%.

SELECT
    p.product_id,
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    SUM(oi.quantity * p.cost_price) AS total_cost,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) - SUM(oi.quantity * p.cost_price) AS profit,
    ROUND(
        (
            (
                SUM(
                    oi.quantity * oi.selling_price
                    * (1 - oi.discount / 100)
                ) - SUM(oi.quantity * p.cost_price)
            )
            /
            SUM(
                oi.quantity * oi.selling_price
                * (1 - oi.discount / 100)
            )
        ) * 100,
        2
    ) AS profit_margin_percent
FROM products AS p
JOIN order_items AS oi
    ON p.product_id = oi.product_id
JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
HAVING revenue >= 20000
   AND profit_margin_percent < 20
ORDER BY revenue DESC;

-- Q48. Identify the most valuable customers based on
--      delivered net revenue.
--      Display their orders, revenue, and average order value.

SELECT
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS total_revenue,
    ROUND(
        SUM(
            oi.quantity * oi.selling_price
            * (1 - oi.discount / 100)
        ) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
LIMIT 5;

-- Q49. Calculate the total delivered net revenue generated
--      by each customer city.

SELECT
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_items AS oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'Delivered'
GROUP BY c.city
ORDER BY revenue DESC;

-- Q50. Identify the payment method generating the highest
--      successful payment revenue.

SELECT
    payment_method,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(amount) AS total_revenue,
    ROUND(
        SUM(amount) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM payments
WHERE payment_status = 'Successful'
GROUP BY payment_method
ORDER BY total_revenue DESC
LIMIT 1;

-- Q51. Calculate the cancellation rate for each city
--      based on total orders placed by customers in that city.

SELECT
    c.city,
    COUNT(*) AS total_orders,
    SUM(
        CASE
            WHEN o.order_status = 'Cancelled' THEN 1
            ELSE 0
        END
    ) AS cancelled_orders,
    ROUND(
        SUM(
            CASE
                WHEN o.order_status = 'Cancelled' THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_percent
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.city
ORDER BY cancellation_rate_percent DESC;

-- Q52. Compare average delivery time with average customer rating
--      to identify whether slower deliveries are associated
--      with lower ratings.

SELECT
    ROUND(
        AVG(DATEDIFF(d.delivered_date, d.shipped_date)),
        2
    ) AS average_delivery_days,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(DISTINCT d.order_id) AS reviewed_delivered_orders
FROM deliveries AS d
JOIN reviews AS r
    ON d.order_id = r.order_id
WHERE d.delivery_status = 'Delivered'
  AND d.delivered_date IS NOT NULL;

-- Q53. Identify products that should be considered for promotion
--      based on strong delivered quantity and good customer ratings.
--      Promotion criteria:
--      at least 2 units sold and average rating >= 4.

SELECT
    p.product_id,
    p.product_name,
    SUM(oi.quantity) AS quantity_sold,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM products AS p
JOIN order_items AS oi
    ON p.product_id = oi.product_id
JOIN orders AS o
    ON oi.order_id = o.order_id
LEFT JOIN reviews AS r
    ON p.product_id = r.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
HAVING quantity_sold >= 2
   AND average_rating >= 4
ORDER BY revenue DESC;

-- Q54. Identify products that may need pricing or discount
--      optimization based on low profit margin or low customer rating.
--      A product is flagged when:
--      profit margin < 20% OR average rating < 3.5.

SELECT
    p.product_id,
    p.product_name,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) AS revenue,
    SUM(oi.quantity * p.cost_price) AS total_cost,
    SUM(
        oi.quantity * oi.selling_price * (1 - oi.discount / 100)
    ) - SUM(oi.quantity * p.cost_price) AS profit,
    ROUND(
        (
            (
                SUM(
                    oi.quantity * oi.selling_price
                    * (1 - oi.discount / 100)
                ) - SUM(oi.quantity * p.cost_price)
            )
            /
            SUM(
                oi.quantity * oi.selling_price
                * (1 - oi.discount / 100)
            )
        ) * 100,
        2
    ) AS profit_margin_percent,
    ROUND(AVG(r.rating), 2) AS average_rating
FROM products AS p
JOIN order_items AS oi
    ON p.product_id = oi.product_id
JOIN orders AS o
    ON oi.order_id = o.order_id
LEFT JOIN reviews AS r
    ON p.product_id = r.product_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id, p.product_name
HAVING profit_margin_percent < 20
    OR average_rating < 3.5
ORDER BY profit_margin_percent ASC;

-- Q55. Generate the major business KPIs required to summarize
--      the top business insights from the ShopSphere dataset.

SELECT
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    COUNT(DISTINCT o.customer_id) AS unique_customers,
    ROUND(
        SUM(
            oi.quantity * oi.selling_price
            * (1 - oi.discount / 100)
        ),
        2
    ) AS total_net_revenue,
    ROUND(
        SUM(
            oi.quantity * oi.selling_price
            * (1 - oi.discount / 100)
        )
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value,
    ROUND(
        SUM(oi.quantity * p.cost_price),
        2
    ) AS total_cost,
    ROUND(
        SUM(
            oi.quantity * oi.selling_price
            * (1 - oi.discount / 100)
        )
        - SUM(oi.quantity * p.cost_price),
        2
    ) AS total_profit,
    ROUND(
        (
            (
                SUM(
                    oi.quantity * oi.selling_price
                    * (1 - oi.discount / 100)
                )
                - SUM(oi.quantity * p.cost_price)
            )
            /
            SUM(
                oi.quantity * oi.selling_price
                * (1 - oi.discount / 100)
            )
        ) * 100,
        2
    ) AS overall_profit_margin
FROM orders AS o
JOIN order_items AS oi
    ON o.order_id = oi.order_id
JOIN products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Delivered';
    