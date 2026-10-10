INSERT INTO sales (order_id, customer, product, quantity, price,
                   total_amount, order_value_category)
SELECT DISTINCT ON (order_id)
       order_id, customer, product, quantity, price,
       quantity * price,
       CASE WHEN quantity * price >= 500 THEN 'High' ELSE 'Low' END
FROM raw_sales
ORDER BY order_id, loaded_at DESC, raw_id DESC
ON CONFLICT (order_id) DO UPDATE SET
    customer = EXCLUDED.customer,
    product = EXCLUDED.product,
    quantity = EXCLUDED.quantity,
    price = EXCLUDED.price,
    total_amount = EXCLUDED.total_amount,
    order_value_category = EXCLUDED.order_value_category