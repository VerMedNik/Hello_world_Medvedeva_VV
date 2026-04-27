UPDATE price WHERE price > 1000 SET price = price * 1.1;
UPDATE price WHERE price < 10000 AND product_id ≤ 5 SET price = price * 1.05;