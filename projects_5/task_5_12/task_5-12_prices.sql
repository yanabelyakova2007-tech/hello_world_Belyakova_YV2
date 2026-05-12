SELECT product_id, COUNT(*) FROM prices GROUP BY product_id;
SELECT product_id, AVG(price) AS avg_price FROM prices GROUP BY product_id;
SELECT product_id, MIN(price) AS min_price FROM prices GROUP BY product_id;
SELECT product_id, MAX(price) AS max_price FROM prices GROUP BY product_id;