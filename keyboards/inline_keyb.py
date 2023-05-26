from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def help_cmd():
    kb = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('/HEEEEELP', callback_data='call to manager')
    kb.add(b1)
    return kb

def menu_cmd():
    kb = InlineKeyboardMarkup()
    b1 =InlineKeyboardButton('📱PDF file', callback_data='menu_pdf')
    b2 =  InlineKeyboardButton('📑In chat', callback_data='menu_in_chat')
    kb.add(b1).insert(b2)
    return kb

def menu_pastry_type():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('🥧Cake', callback_data='cake')
    kb.add(b1)
    return kb

def estemate_product():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('💛Liked', callback_data='liked')
    b2 = InlineKeyboardButton(f'🥐To cart', callback_data='buy')
    kb.add(b1).insert(b2)
    return kb

def estimate_to_cart():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('-', callback_data='less')
    b2 = InlineKeyboardButton('1', callback_data='quantity')
    b3 = InlineKeyboardButton('+', callback_data='more')
    b4 = InlineKeyboardButton('🥐To cart', callback_data='add_to_cart')
    kb.add(b1).insert(b2).insert(b3).add(b4)
    return kb

def change_quantity_cart_kb(quantity,price):
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('-', callback_data='less')
    b2 = InlineKeyboardButton(f'{quantity}', callback_data='quantity')
    b3 = InlineKeyboardButton('+', callback_data='more')
    b4 = InlineKeyboardButton(f'🥐To cart {price} rub', callback_data='add_to_cart')
    kb.add(b1).insert(b2).insert(b3).add(b4)
    return kb

def cart_manipulation(quntity):
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('-', callback_data='less_cart')
    b2 = InlineKeyboardButton(f'{quntity}', callback_data='quantity')
    b3 = InlineKeyboardButton('+', callback_data='more')
    b4 = InlineKeyboardButton('🥐Save', callback_data='add_to_cart')
    kb.add(b1).insert(b2).insert(b3).add(b4)
    return kb

def cart_manipulaton2(quntity, price):
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('-', callback_data='less_cart')
    b2 = InlineKeyboardButton(f'{quntity}', callback_data='quantity')
    b3 = InlineKeyboardButton('+', callback_data='more')
    b4 = InlineKeyboardButton(f'🥐To cart {price} rub', callback_data='add_to_cart')
    kb.add(b1).insert(b2).insert(b3).add(b4)
    return kb

def after_menu():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('💛Go to Liked', callback_data='go_to_liked')
    b2 = InlineKeyboardButton('🥐Go to Cart', callback_data='go_to_buy')
    kb.add(b1).insert(b2)
    return kb

def after_liked_product():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('🥚To oven', callback_data='del_liked_product')
    b2 = InlineKeyboardButton('🥐Add to cart', callback_data='buy')
    kb.add(b1).insert(b2)
    return kb

def after_cart():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('🥄crave', callback_data='change_quantity')
    b2 = InlineKeyboardButton('🍾bye', callback_data='delete_cart')
    kb.add(b1).insert(b2)
    return kb

def make_order():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('🥮ORDER', callback_data='make_order')
    kb.add(b1)
    return kb

def make_customer():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('yes', callback_data='yes_customer')
    b2 = InlineKeyboardButton('🍾no', callback_data='no_customer')
    kb.add(b1).insert(b2)
    return kb

def admin_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    b1= InlineKeyboardButton('рассылка', callback_data='рассылка')
    kb.add(b1)
    return kb

def text_send():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('yes', callback_data='yes_text')
    b2 = InlineKeyboardButton('no', callback_data='no')
    kb.add(b1).insert(b2)
    return kb

def photo_send():
    kb = InlineKeyboardMarkup()
    b1= InlineKeyboardButton('yes', callback_data='yes_photo')
    b2 = InlineKeyboardButton('no', callback_data='no')
    kb.add(b1).insert(b2)
    return kb
