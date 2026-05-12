SELECT
    p.name AS "название товара",
    pr.price AS "цена"
FROM products AS p
JOIN prices AS pr ON p.id = pr.id;  