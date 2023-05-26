-- DROP Table frolovscake.cart_product,frolovscake.cart,frolovscake.liked, frolovscake.orders, frolovscake.prices,frolovscake.menu, frolovscake.requests_consult,frolovscake.customers, frolovscake.users;


CREATE TABLE IF NOT EXISTS frolovscake.menu(  
    id int  NOT NULL PRIMARY KEY AUTO_INCREMENT,
    dish VARCHAR(200) NOT NULL,
    dish_img VARCHAR(200),
    dish_category VARCHAR(200),
    dish_description VARCHAR(500) NOT NULL,
    кбжу VARCHAR(100) NOT NULL
);
CREATE TABLE IF NOT EXISTS  frolovscake.prices( 
    id int NOT NULL  PRIMARY KEY AUTO_INCREMENT,
    dish_id INT NOT NULL,
    price_rub INT NOT NULL,
    sales VARCHAR(100),
    FOREIGN KEY (dish_id) REFERENCES frolovscake.menu(id)
);

CREATE TABLE IF NOT EXISTS frolovscake.users( 
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    telegram_id VARCHAR(200) NOT NULL,
    first_user_name VARCHAR(200),
    last_user_name VARCHAR(200)
);
CREATE TABLE IF NOT EXISTS frolovscake.customers( 
    customer_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(100), 
    date_birth DATE,
    add_time DATETIME NOT NULL,
    telegram_id INT NOT NULL,
    phone_num VARCHAR(100), 
    FOREIGN KEY (telegram_id) REFERENCES frolovscake.users(id)
);



CREATE TABLE IF NOT EXISTS frolovscake.cart(
    carts_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_user int not null,
    data_placed DATETIME,

    FOREIGN KEY(id_user) REFERENCES frolovscake.users(id)
);
CREATE TABLE  IF NOT EXISTS frolovscake.orders( 
    orders_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_customer int NOT NULL,
    order_time DATETIME NOT NULL,
    orders_status VARCHAR(100),
    received_time DATETIME,
    receipt INT NOT NULL,
    FOREIGN KEY (id_customer) REFERENCES frolovscake.customers(customer_id)
);

CREATE TABLE IF NOT EXISTS frolovscake.order_products(
    order_id INT NOT NULL ,
    order_product_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    dish_id int not null,
    quantity int not null,
    data_placed DATETIME NOT NULL,
    FOREIGN KEY(order_id) REFERENCES frolovscake.orders(orders_id),
    FOREIGN KEY (dish_id) REFERENCES frolovscake.menu(id)

);

CREATE TABLE IF NOT EXISTS frolovscake.requests_consult( 
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_customer int NOT NULL,
    user_status VARCHAR(100) NOT NULL,
    extra VARCHAR(500),
    FOREIGN KEY (id_customer) REFERENCES frolovscake.customers(customer_id)
);

CREATE TABLE IF NOT EXISTS frolovscake.liked( 
    liked_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    id_user int NOT NULL,
    dish_id INT NOT NULL,

    FOREIGN KEY(id_user) REFERENCES frolovscake.users(id),
    FOREIGN KEY(dish_id) REFERENCES frolovscake.menu(id)
);



CREATE TABLE IF NOT EXISTS frolovscake.cart_product( 
    cart_product_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    cart_id INT NOT NULL,
    dish_id INT NOT NULL,
    quantity INT NOT NULL,
    data_placed DATETIME,

    FOREIGN KEY(cart_id) REFERENCES frolovscake.cart(carts_id),
    FOREIGN KEY(dish_id) REFERENCES frolovscake.menu(id)
);