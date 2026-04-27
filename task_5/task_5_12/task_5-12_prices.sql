SELECT product_id, COUNT(*) FROM prices GROUP BY product_id;
SELECT product_id, AVG(price) FROM prices GROUP BY product_id;
SELECT product_id, MAX(price) FROM prices GROUP BY product_id;
SELECT product_id, MIN(price) FROM prices GROUP BY product_id;