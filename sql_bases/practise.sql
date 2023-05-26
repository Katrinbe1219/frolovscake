-- SELECT dish FROM frolovscake.menu AS m INNER JOIN frolovscake.liked AS l INNER JOIN frolovscake.users AS u
-- ON u.id = l.id_user and l.dish_id = m.id WHERE u.telegram_id = 1063515997;

-- SELECT dish_id FROM frolovscake.liked AS l INNER JOIN frolovscake.menu AS m INNER JOIN frolovscake.users AS u
-- ON l.id_user = u.id  AND l.dish_id = m.id WHERE m.dish = 'Chocolate Cake';

--  DELETE FROM frolovscake.liked WHERE dish_id IN (
--     SELECT * FROM(
--      SELECT dish_id FROM frolovscake.liked AS l INNER JOIN frolovscake.menu AS m INNER JOIN frolovscake.users AS u 
-- ON l.id_user = u.id AND l.dish_id = m.id WHERE m.dish = 'Chocolate Cake' AND u.telegram_id = 1063515997) AS d
-- );
-- INSERT INTO frolovscake.cart (id_user) VALUES 

-- ((SELECT id FROM frolovscake.users WHERE frolovscake.users.telegram_id = 1063515997));

-- SELECT dish_id FROM frolovscake.menu AS m INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.cart_product AS p INNER JOIN frolovscake.users AS u
-- ON u.id = c.id_user AND p.cart_id = c.id AND p.dish_id = m.id WHERE u.telegram_id = '1063515997' AND m.dish = 'Chocolate Cake';

-- INSERT INTO  frolovscake.cart_product(cart_id,data_placed, dish_id, quantity) VALUES
-- ( (SELECT carts_id FROM frolovscake.cart AS c INNER JOIN frolovscake.users AS u ON u.id = c.id_user WHERE u.telegram_id = 1063515997),
-- '2023-05-14 10:37:23', (SELECT id FROM frolovscake.menu AS m WHERE m.dish = 'Granat Cake'),1)

-- SELECT quantity FROM frolovscake.cart_product AS cp INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.menu AS m INNER JOIN frolovscake.users AS u 
-- ON cp.cart_id = c.carts_id AND m.id = cp.dish_id AND c.id_user = u.id WHERE u.telegram_id = 1063515997 AND m.dish = 'Blueberry Cake';


-- UPDATE frolovscake.cart_product cr, frolovscake.cart  c, frolovscake.menu  m, frolovscake.users  u 
-- SET cr.quantity = 2
-- WHERE cr.cart_id = c.carts_id AND c.id_user = u.id AND m.id = cr.dish_id AND u.telegram_id = 1063515997 AND m.dish = 'Granat Cake'
-- ;

-- SELECT dish FROM frolovscake.menu AS m INNER JOIN frolovscake.cart_product AS cr  INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.orders AS o ON
-- o.cart_id = c.carts_id AND c.carts_id = cr.cart_id AND cr.dish_id = m.id WHERE o.order_id = 3;

-- SELECT orders_id FROM frolovscake.orders AS o INNER JOIN frolovscake.customers AS c INNER JOIN frolovscake.users AS u 
-- ON c.customer_id = o.id_customer AND u.id = c.telegram_id WHERE u.telegram_id = 1063515997 AND o.order_time = '2023-05-22 16:49:46'

SELECT telegram_id FROM frolovscake.users;