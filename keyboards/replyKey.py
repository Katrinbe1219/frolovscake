from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def all_cmd():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('🔥 menu')
    b2 = KeyboardButton('💛 Liked')
    b3 = KeyboardButton('🥐 Cart')
    b4 = KeyboardButton('/help')
    b5 = KeyboardButton('👍 order')
    b6 = KeyboardButton('🌼 consultation')
    b7 = KeyboardButton('🥜 My orders')
    kb.add(b1).add(b2).insert(b4).insert(b3).add(b5).insert(b7).insert(b6)
    
    return kb

def make_customer():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    b1= KeyboardButton('yes')
    b2 = KeyboardButton('no')
    kb.add(b1).insert(b2)
    return kb

def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('🔥 menu')
    b2 = KeyboardButton('💛 Liked')
    b3 = KeyboardButton('🥐 Cart')
    b4 = KeyboardButton('/help')
    b5 = KeyboardButton('👍 order')
    b6 = KeyboardButton('🌼 consultation')
    b7 = KeyboardButton('🥜 My orders')
    b8 = KeyboardButton('Рассылка')
    kb.add(b1).add(b2).insert(b4).insert(b3).add(b5).insert(b7).insert(b6).add(b8)
    
    return kb 