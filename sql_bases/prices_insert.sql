INSERT INTO frolovscake.prices(dish_id, price_rub, sales) VALUES (
    (SELECT id FROM frolovscake.menu AS m WHERE m.dish='Blueberry Cake' ),300, 'no'
);
INSERT INTO frolovscake.prices(dish_id, price_rub, sales) VALUES (
    (SELECT id FROM frolovscake.menu AS m WHERE m.dish='Granat Cake' ),375, 'no'
);
INSERT INTO frolovscake.prices(dish_id, price_rub, sales) VALUES (
    (SELECT id FROM frolovscake.menu AS m WHERE m.dish='Chocolate Cake' ),545, 'no'
);
INSERT INTO frolovscake.prices(dish_id, price_rub, sales) VALUES (
    (SELECT id FROM frolovscake.menu AS m WHERE m.dish='Inayan Cake' ),475, 'no'
);