SELECT 
name AS название товара, 
price AS цену
FROM products AS p
JOIN prices  AS pr  ON p.id = pr.id;