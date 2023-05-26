import pymysql
import logging
import datetime


logging.basicConfig(filename='D:\\работа\\study tel-bot\\frolov`s cake\\problems\\sql_cntr_probs.log',level=logging.INFO,filemode='w')

async def start_bot():
    try:
        global cur, con
        con = pymysql.connect(
            host='localhost',
            port=3306,
            user='droping',
            password='locomotive39',
            database='frolovscake')
        logging.info('database was succefully connected')
        cur = con.cursor(pymysql.cursors.DictCursor)
        con.commit()
        print('fine')
    except Exception as ex:
        logging.info(f'Something went wrong {ex}')

async def save_user(user_id, first_name, last_name):
    user = cur.execute('SELECT 1 FROM frolovscake.users WHERE telegram_id = "{id}"'.format(id=user_id))
    if not user:
        cur.execute('INSERT INTO frolovscake.users(telegram_id,first_user_name, last_user_name) VALUES(%s,%s,%s)',
                    (user_id, first_name, last_name))
    con.commit()
    
#-----------------------------------------MENU------------------------------------------        
def get_menu_dishes (callback_data):
    cur.execute('SELECT dish from frolovscake.menu WHERE dish_category = "{ctg}"'.format(ctg=callback_data))
    dish_names = cur.fetchall()
    con.commit()
    return dish_names

def get_menu_description(callback_data):
    cur.execute('SELECT dish_description FROM frolovscake.menu WHERE dish_category ="{ctg}"'.format(ctg=callback_data))
    dish_desc = cur.fetchall()
    con.commit()
    return dish_desc

def get_menu_eng_val(callback_data):
    cur.execute('SELECT кбжу FROM frolovscake.menu WHERE dish_category ="{ctg}"'.format(ctg=callback_data))
    dish_en_val = cur.fetchall()
    con.commit()
    return dish_en_val

def get_menu_image_link(callback_data):
    cur.execute('SELECT dish_img FROM frolovscake.menu WHERE dish_category ="{ctg}"'.format(ctg=callback_data))
    dish_image_link = cur.fetchall()
    con.commit()
    return dish_image_link

def get_price(callback_data):
    cur.execute(f"""SELECT price_rub FROM frolovscake.prices AS p INNER JOIN frolovscake.menu AS m 
ON p.dish_id = m.id WHERE m.dish_category = '{callback_data}'""")
    dish_price = cur.fetchall()
    con.commit()
    return dish_price

#--------------------------LIKED-------------------------------------
async def liked_product(user_id,name_product):
    cur.execute(f"""SELECT dish_id FROM frolovscake.liked AS l INNER JOIN frolovscake.menu AS m INNER JOIN frolovscake.users AS u
ON l.id_user = u.id  AND l.dish_id = m.id WHERE m.dish = '{name_product}' AND u.telegram_id='{user_id}'""")
    check = cur.fetchone()
    if not check:
        cur.execute(f"""INSERT INTO frolovscake.liked(id_user, dish_id) VALUES
((SELECT id FROM frolovscake.users WHERE telegram_id = '{user_id}'),
        (SELECT id FROM frolovscake.menu WHERE dish = '{name_product}'))""")
    con.commit()

def get_liked_id(user_id):
    cur.execute(f"""SELECT liked_id FROM frolovscake.liked AS l INNER JOIN frolovscake.users AS u ON
l.id_user = u.id WHERE u.telegram_id = '{user_id}';""")
    product = cur.fetchall()
    con.commit()
    return product
    
def get_liked_product(product_id):
    cur.execute(f"""SELECT dish FROM frolovscake.menu AS m INNER JOIN frolovscake.liked AS l 
ON l.dish_id = m.id WHERE l.liked_id = '{product_id};'""")
    product = cur.fetchone()
    con.commit()
    return product['dish']

def get_product_liked_deleted(user_id,product):
    cur.execute(f"""SELECT liked_id FROM frolovscake.liked AS l INNER JOIN frolovscake.users AS u INNER JOIN frolovscake.menu AS m  ON
l.id_user = u.id  AND m.id = l.dish_id WHERE u.telegram_id = '{user_id}' AND m.dish='{product}'""")
    product = cur.fetchone()
    return product['liked_id']
    
async def delete_liked_product(product_id):
    cur.execute(f""" DELETE FROM frolovscake.liked WHERE frolovscake.liked.liked_id = '{product_id}'""")
    con.commit()
    
#--------------------------------------------------------GETTING SMTH----------------------
def send_product_description(product):
    cur.execute(f'SELECT dish_description FROM frolovscake.menu WHERE dish ="{product}"')
    dish_desc = cur.fetchone()
    con.commit()
    return dish_desc['dish_description']

def send_product_img_link(product):
    cur.execute(f'SELECT dish_img FROM frolovscake.menu WHERE dish ="{product}"')
    dish_image_link = cur.fetchone()
    con.commit()
    return dish_image_link['dish_img']

def send_product_eng_val(product):
    cur.execute(f'SELECT кбжу FROM frolovscake.menu WHERE dish ="{product}"')
    dish_en_val = cur.fetchone()
    con.commit()
    return dish_en_val['кбжу']

def send_product_category(product):
    cur.execute(f'SELECT dish_category FROM frolovscake.menu WHERE dish ="{product}"')
    dish_ctg = cur.fetchone()
    con.commit()
    return dish_ctg['dish_category']

def send_dish_price(product):
    cur.execute(f"""SELECT price_rub FROM frolovscake.prices AS p INNER JOIN frolovscake.menu AS m 
ON p.dish_id = m.id WHERE m.dish = '{product}'""")
    price = cur.fetchone()
    con.commit()
    return price['price_rub']

#--------------------------CART--------------------------------------------
async def create_cart(user_id):
    cur.execute(f"""SELECT data_placed FROM frolovscake.cart AS c INNER JOIN frolovscake.users AS u
ON c.id_user = u.id WHERE u.telegram_id ={user_id}""")
    check = cur.fetchone()
    if not check:
        now = datetime.datetime.now()
        str_now = now.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(f"""INSERT INTO frolovscake.cart (id_user, data_placed) VALUES 
((SELECT id FROM frolovscake.users WHERE frolovscake.users.telegram_id = '{user_id}'),'{str_now}')""")
    con.commit()

async def save_to_cart(user_id, product,quantity):
    cur.execute(f"""SELECT dish_id FROM frolovscake.menu AS m INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.cart_product AS p INNER JOIN frolovscake.users AS u
ON u.id = c.id_user AND p.cart_id = c.carts_id AND p.dish_id = m.id WHERE u.telegram_id = '{user_id}' AND m.dish = '{product}'""")   
    check = cur.fetchone()
    if not check:
        now = datetime.datetime.now()
        str_now = now.strftime('%Y-%m-%d %H:%M:%S')
        cur.execute(f"""INSERT INTO  frolovscake.cart_product(cart_id,data_placed, dish_id, quantity) VALUES
( (SELECT carts_id FROM frolovscake.cart AS c INNER JOIN frolovscake.users AS u ON u.id = c.id_user WHERE u.telegram_id = '{user_id}'),
'{str_now}', (SELECT id FROM frolovscake.menu AS m WHERE m.dish = '{product}'),'{quantity}')""")
        con.commit()
    elif int(check['dish_id']) != int(quantity):
        cur.execute(f"""UPDATE frolovscake.cart_product cr, frolovscake.cart  c, frolovscake.menu  m, frolovscake.users  u 
SET cr.quantity = '{quantity}'
WHERE cr.cart_id = c.carts_id AND c.id_user = u.id AND m.id = cr.dish_id AND u.telegram_id = '{user_id}' AND m.dish = '{product}'
;""")
        con.commit()
def get_cart_products_id(user_id):
    cur.execute(f"""SELECT cart_product_id FROM frolovscake.cart_product AS cr INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.users AS u ON 
cr.cart_id = c.carts_id AND c.id_user = u.id WHERE u.telegram_id = '{user_id}';""")
    info = cur.fetchall()
    return info

def get_cart_products(product_id):
    cur.execute(f"""SELECT dish FROM frolovscake.menu AS m INNER JOIN frolovscake.cart_product  AS cr ON
cr.dish_id = m.id WHERE cr.cart_product_id = '{product_id}';""")
    product = cur.fetchone()   
    con.commit()
    return product['dish'] 


def get_cart_quntity(user_id,product):
    cur.execute(f"""SELECT quantity FROM frolovscake.cart_product AS cp INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.menu AS m INNER JOIN frolovscake.users AS u 
ON cp.cart_id = c.carts_id AND m.id = cp.dish_id AND c.id_user = u.id WHERE u.telegram_id = '{user_id}' AND m.dish = '{product}';""")
    num = cur.fetchall()
    if len(num) == 1:
        return num[0]['quantity']
    else:
        return None

def get_product_cart_delete(user_id, product):
    cur.execute(f"""SELECT cart_product_id FROM frolovscake.cart_product AS cr INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.users AS u INNER JOIN frolovscake.menu AS m ON 
cr.cart_id = c.carts_id AND c.id_user = u.id AND m.id = cr.dish_id WHERE u.telegram_id = '{user_id}' AND m.dish='{product}';""")
    product = cur.fetchone()
    return product['cart_product_id']
    
async def delete_cart_product(product_id):
    cur.execute(f""" DELETE FROM frolovscake.cart_product WHERE frolovscake.cart_product.cart_product_id = '{product_id}';""")
    con.commit()
    
async def change_quantity_cart(user_id, product,quantity):
    cur.execute(f"""UPDATE frolovscake.cart_product cr, frolovscake.cart  c, frolovscake.menu  m, frolovscake.users  u 
SET cr.quantity = '{quantity}'
WHERE cr.cart_id = c.carts_id AND c.id_user = u.id AND m.id = cr.dish_id AND u.telegram_id = '{user_id}' AND m.dish = '{product}'
;""")
    con.commit()
#--------------------------------------CUSTOMERS------------------------------------------------------------------
async def check_customers(user_id):
    cur.execute(f"""SELECT * FROM frolovscake.customers AS t INNER JOIN frolovscake.users AS u ON u.id = t.telegram_id WHERE u.telegram_id = '{user_id}' """)
    check = cur.fetchone()
    if check is None :
        return ('No')
    return ('Yes')

async def fill_customer(fisrt_name , last_name, email,phone,user_id):
    now = datetime.datetime.now()
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(f"""INSERT INTO frolovscake.customers (first_name, last_name,email, phone_num, telegram_id, add_time) VALUES
( '{fisrt_name}', '{last_name}', '{email}'  ,'{phone}', (SELECT id FROM frolovscake.users AS u WHERE u.telegram_id = '{user_id}'),  '{str_now}')""")
    con.commit()
    
async def request_consulatation(user_id, extra):
    cur.execute(f"""INSERT INTO frolovscake.requests_consult (id_customer, extra, user_status) VALUES 
( (SELECT customer_id FROM frolovscake.customers AS c INNER JOIN frolovscake.users AS u ON u.id = c.telegram_id WHERE u.telegram_id = '{user_id}'), '{extra}','Processing')""")
    con.commit()

#________________________orders----------------------------------------
def check_cart(user_id):
    cur.execute(f"""SELECT cart_product_id FROM frolovscake.cart_product AS cr INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.users AS u 
ON cr.cart_id = c.carts_id AND c.id_user = u.id WHERE u.telegram_id = '{user_id}'""")
    check = cur.fetchone()
    if check:
        return ('check')
    return ('no check')

def get_everything_from_cart(user_id):
    cur.execute(f"""SELECT dish FROM frolovscake.menu AS m INNER JOIN frolovscake.cart_product AS cr INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.users AS u 
ON cr.cart_id = c.carts_id AND c.id_user = u.id  AND cr.dish_id = m.id WHERE u.telegram_id = '{user_id}'""")
    all = cur.fetchall()
    return all

def get_every_quantity_cart(user_id):
    cur.execute(f"""SELECT quantity FROM frolovscake.cart_product AS cr INNER JOIN frolovscake.menu AS m  INNER JOIN frolovscake.cart AS c INNER JOIN frolovscake.users AS u 
ON cr.cart_id = c.carts_id AND c.id_user = u.id  AND cr.dish_id = m.id WHERE u.telegram_id = '{user_id}'""")
    all = cur.fetchall()
    return all

def get_first_name_order(user_id):
    cur.execute(f"""SELECT first_name FROM frolovscake.customers AS c  INNER JOIN frolovscake.users AS u 
ON c.telegram_id = u.id WHERE u.telegram_id = '{user_id}'""")
    name = cur.fetchone()
    return name['first_name']

def get_last_name_order(user_id):
    cur.execute(f"""SELECT last_name FROM frolovscake.customers AS c  INNER JOIN frolovscake.users AS u 
ON c.telegram_id = u.id WHERE u.telegram_id = '{user_id}'""")
    name = cur.fetchone()
    return name['last_name']

def get_phone_order(user_id):
    cur.execute(f"""SELECT phone_num FROM frolovscake.customers AS c  INNER JOIN frolovscake.users AS u 
ON c.telegram_id = u.id WHERE u.telegram_id = '{user_id}'""")
    phone = cur.fetchone()
    return phone['phone_num']

def get_email_order(user_id):
    cur.execute(f"""SELECT email FROM frolovscake.customers AS c  INNER JOIN frolovscake.users AS u 
ON c.telegram_id = u.id WHERE u.telegram_id = '{user_id}'""")
    email = cur.fetchone()
    return email['email']

#----------------------------------ORDER___________________--------------------
def fill_order(user_id,suma):
    now = datetime.datetime.now()
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(f"""INSERT INTO frolovscake.orders (id_customer, order_time, orders_status,receipt) VALUES(
    (SELECT customer_id FROM frolovscake.customers AS c INNER JOIN frolovscake.users AS u ON c.telegram_id = u.id WHERE u.telegram_id = '{user_id}'),
    ('{str_now}'),
    ('ОБРАБОТКА'),
    '{suma}'
);""")

    cur.execute(f"""SELECT orders_id FROM frolovscake.orders AS o INNER JOIN frolovscake.customers AS c INNER JOIN frolovscake.users AS u 
ON c.customer_id = o.id_customer AND u.id = c.telegram_id WHERE u.telegram_id = '{user_id}' AND o.order_time = '{str_now}' """)
    check = cur.fetchone()

    con.commit()
    return check['orders_id']

async def fill_order_products(dish, quantity,order_id):
    now = datetime.datetime.now()
    str_now = now.strftime('%Y-%m-%d %H:%M:%S')
    cur.execute(f"""INSERT INTO frolovscake.order_products(order_id,dish_id,quantity, data_placed) VALUES (
'{order_id}', (SELECT id FROM frolovscake.menu WHERE frolovscake.menu.dish= '{dish}'),'{quantity}','{str_now}'
);""")
    con.commit()
       
#----------------------------my orders-----------------------
def get_my_orders_id(user_id):
    cur.execute(f"""SELECT orders_id FROM frolovscake.orders AS o  INNER JOIN frolovscake.customers AS c INNER JOIN frolovscake.users AS u ON
o.id_customer = c.customer_id AND c.telegram_id = u.id WHERE u.telegram_id = '{user_id}';""")
    orders = cur.fetchall()
    con.commit()
    return orders

def get_quantity_my_orders(order_id):

    cur.execute(f"""SELECT quantity FROM frolovscake.order_products AS op WHERE op.order_id = '{order_id}';""")
    quantity = cur.fetchall()
    con.commit()
    return quantity

def get_product_my_orders(order_id):
    cur.execute(f"""SELECT dish FROM frolovscake.menu AS m INNER JOIN frolovscake.order_products AS op 
ON m.id = op.dish_id WHERE op.order_id = '{order_id}';""")
    product = cur.fetchall()
    con.commit()
    return product

#==============================Admin===========
def get_users():
    cur.execute("""SELECT telegram_id FROM frolovscake.users;""")
    users = cur.fetchall()
    return users