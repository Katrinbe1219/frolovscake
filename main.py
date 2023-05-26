from aiogram import Bot, executor , types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types.message import Message
from aiogram.types.input_media import InputMediaPhoto
import os
from re import compile, IGNORECASE

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from filters.filter import IsAdmin

from controllers.controller import check_phone_number
from texts.texts_cmnd import start_cmnd, help_cmd_frst, help_cmd_sec
from texts.menu_cmnd import menu_message, after_product_text, liked_text_before,cart_text_before
from texts.customers import yes_check, book_consult, no_check,send_consult , order_made
from keyboards.inline_keyb import text_send, photo_send,  cart_manipulaton2, change_quantity_cart_kb, help_cmd, menu_cmd,menu_pastry_type, estemate_product, after_menu,after_liked_product,after_cart,make_order, cart_manipulation, estimate_to_cart
from keyboards.replyKey import admin_kb, all_cmd,make_customer
from controllers.sql_controller import start_bot, save_user, liked_product,get_liked_product,send_product_description,get_cart_products_id
from controllers.sql_controller import get_product_liked_deleted, get_liked_id, send_dish_price,send_product_description, send_product_eng_val, send_product_img_link,delete_liked_product
from controllers.sql_controller import get_everything_from_cart, get_price, get_menu_description,get_menu_dishes,get_menu_eng_val,get_menu_image_link, send_product_category
from controllers.sql_controller import check_cart, create_cart,save_to_cart,get_cart_products,delete_cart_product,get_cart_quntity
from controllers.sql_controller import check_customers, fill_customer,request_consulatation ,fill_order,get_product_cart_delete
from controllers.sql_controller import get_every_quantity_cart, get_email_order,get_first_name_order,get_last_name_order, get_phone_order
from controllers.sql_controller import get_users, get_my_orders_id, get_quantity_my_orders, get_product_my_orders,fill_order_products
from controllers.get_data import get_caption, get_photo, liked_caption,cart_caption,order_product, all_order, my_order

email_check = compile(r'^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$', IGNORECASE)

TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)

class Sender(StatesGroup):
    text = State()
    photo = State()
    check = State()

class Client(StatesGroup):
    first_name = State()
    last_name = State()
    email = State()
    phone = State()
    all = State()
    check = State()
    finish = State()

class Consultation(StatesGroup):
    receive_extra = State()

class makeOrder(StatesGroup):
    checking = State()
async def onStartup(_):
    await start_bot()
    print('I was launched')
#------------------BASE---------------------------------------------------------------------
@dp.message_handler(Command('start'))
async def start_command(msg: types.Message):
    await msg.answer(text = start_cmnd, parse_mode='html')

@dp.message_handler(Command('help'))
async def help_command(msg: types.Message):
    await msg.answer(text = help_cmd_frst,parse_mode='html', reply_markup=all_cmd())
    await msg.answer(text = help_cmd_sec,parse_mode='html', reply_markup=help_cmd())
#---------------------------------------------------------------------------------------------------------------------
@dp.message_handler(Text('🔥 menu'))
async def menu_command(msg: types.Message):
    await msg.answer('There are two options:', reply_markup=menu_cmd())

@dp.message_handler(Text('💛 Liked'))
async def get_liked_command(msg: types.Message):
    user_id = msg.from_user.id
    products_id = get_liked_id(user_id)
    await bot.send_message(chat_id=msg.from_user.id , text=liked_text_before, parse_mode='HTML')
    
    for i in range(len(products_id)):
        product = get_liked_product(products_id[i]['liked_id'])
        product_desc = send_product_description(product)
        product_imge_link = send_product_img_link(product)
        product_en_val = send_product_eng_val(product)
        product_topic = send_product_category(product)
        price = send_dish_price(product)
        photo = open(product_imge_link,'rb')
        
        
        await bot.send_photo(chat_id=msg.from_user.id, photo=photo,
                             caption = liked_caption(product,product_desc,product_en_val,product_topic,price),
                             reply_markup=after_liked_product())
        
@dp.message_handler(Text('🥐 Cart'))
async def cart_command(msg: types.Message):
    user_id = msg.from_user.id
    products_id = get_cart_products_id(user_id)
    products = []
    for i in range(len(products_id)):
        products.append(get_cart_products(products_id[i]['cart_product_id']))
    await bot.send_message(chat_id=msg.from_user.id , text=cart_text_before,parse_mode='HTML' )
    total_price = 0
    for i in range(len(products)):
            product = products[i]
            product_desc = send_product_description(product)
            product_imge_link = send_product_img_link(product)
            product_en_val = send_product_eng_val(product)
            product_topic = send_product_category(product)
            quantity = get_cart_quntity(user_id,product)
            price = send_dish_price(product)
            cost = price*quantity
            total_price += cost
            photo = open(product_imge_link,'rb')
            
        
            await bot.send_photo(chat_id=msg.from_user.id, photo=photo,
                             caption = cart_caption(product,product_desc,product_en_val,product_topic, quantity,price),
                             reply_markup=after_cart())
    await bot.send_message(chat_id=msg.from_user.id,
                               text = f'🧩 <b>All in all {total_price} rubles</b> 🧩',parse_mode='html')
    await bot.send_message(chat_id=msg.from_user.id,
                               text = 'Do you want make an order?',reply_markup=make_order())
    
@dp.message_handler(Text('👍 order'))
async def check_customer_base(msg: types.Message):
    check = await check_customers(msg.from_user.id)
    if check == 'Yes':
        await bot.send_message(chat_id=msg.from_user.id, text=yes_check, parse_mode='HTML')
        cart = check_cart(msg.from_user.id)
        
        if cart == 'no check':
            await bot.send_message(chat_id=msg.from_user.id, text='''Your cart is empty▪️
🥐 /menu to choose <em>yummy pastry</em>🥐''', parse_mode='HTML')
        else:
            all_products = get_everything_from_cart(msg.from_user.id)
            all_quantity = get_every_quantity_cart(msg.from_user.id)
            desc = ''
            for i in range(len(all_products)):
                desc += order_product(all_products[i]['dish'], all_quantity[i]['quantity'])

            id = msg.from_user.id

            first_name = get_first_name_order(id)
            last_name = get_last_name_order(id)
            phone = get_phone_order(id)
            email = get_email_order(id)
            await bot.send_message(chat_id = msg.from_user.id, text = all_order(first_name,last_name,email,phone,desc))
            await makeOrder.checking.set()
    
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=no_check, parse_mode='HTML')
        await bot.send_message(chat_id=msg.from_user.id, text='Tell me your first name', parse_mode='HTML')
        await Client.first_name.set()

@dp.message_handler(state = makeOrder.checking)
async def varify_correct_order_info(msg: types.Message, state: FSMContext):
    if msg.text == 'yes' or msg.text == 'Yes':
        await state.finish()
        user_id = msg.from_user.id
        
        products_id = get_cart_products_id(user_id)
        products = []
        for i in range(len(products_id)):
            products.append(get_cart_products(products_id[i]['cart_product_id']))
        
        total_price = 0
        all_quantities = []

        for i in range(len(products)):
            product = products[i]
            quantity = get_cart_quntity(user_id,product)
            all_quantities.append(quantity)

            price = send_dish_price(product)
            cost = price*quantity
            total_price += cost
        order_id = fill_order(user_id,total_price)

        for i in range(len(products)):
            product = products[i]
            quantity = all_quantities[i]
            await fill_order_products(product, quantity,order_id)
        
        await bot.send_message(chat_id = msg.from_user.id, text=order_made, parse_mode='html')
    
    elif msg.text =='no' or msg.text == 'No':
        await bot.send_message(chat_id = msg.from_user.id, text='Let`s change your personal data', parse_mode='html')
        await bot.send_message(chat_id=msg.from_user.id, text='Tell me your first name', parse_mode='HTML')
        await Client.first_name.set()

@dp.message_handler(state=Client.first_name)
async def get_first_name(msg: types.Message, state : FSMContext):
    if msg.text.isalpha():
        async with state.proxy() as data:
            data['first_name'] = msg.text
        await bot.send_message(chat_id=msg.from_user.id, text='What is your last name?')
        await Client.next()
    else:
        await bot.send_message(chat_id=msg.from_user.id, text='Please tell me only your first name')
        
@dp.message_handler(state=Client.last_name)
async def get_last_name(msg: types.Message, state: FSMContext):
    if msg.text.isalpha():
        async with state.proxy() as data:
            data['last_name'] = msg.text
        
        await bot.send_message(chat_id=msg.from_user.id, text='Perfect! We need your email to tell you details about our arrangment')
        await Client.email.set()
    else:
        await bot.send_message(chat_id=msg.from_user.id, text='Please tell me only your last name')
        
@dp.message_handler(state = Client.email)
async def get_email(msg: types.Message, state: FSMContext):
    check = email_check.findall(msg.text)
    if check:
        async with state.proxy() as data:
            data['email'] = check[0]
        await bot.send_message(chat_id=msg.from_user.id, text="""What about your phone number? We should be in touch
Example: <em><b>+7</b></em>999999999""", parse_mode='html')
        await Client.phone.set()
    else:
        await bot.send_message(chat_id=msg.from_user.id, text='Please enter only your email')
        
@dp.message_handler(state = Client.phone)
async def get_phone(msg: types.Message, state: FSMContext):
    check = check_phone_number(msg.text)
    if check:
        async with state.proxy() as data:
            data['phone'] = msg.text
        
        await Client.all.set()
        
        async with state.proxy() as data:
            await bot.send_message(chat_id=msg.from_user.id,text=f"""First name: {data['first_name']}
Last name: {data['last_name']}
Email: {data['email']}
Phone Number: {data['phone']}""") 
        
        
        await bot.send_message(chat_id=msg.from_user.id, text='Is everything correct?',reply_markup=make_customer())
        await Client.check.set()
    
    else:
       await bot.send_message(chat_id=msg.from_user.id, text='Please enter only your phone with code region(+7)')

@dp.message_handler(Text('yes'), state = Client.check)
async def change_ratification(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
            await fill_customer(data['first_name'],data['last_name'], data['email'], data['phone'], msg.from_user.id)
    await state.finish()
    await bot.send_message(chat_id=msg.from_user.id,
                               text = '🥐Now you <b>CAN</b> make an <em>/order</em> or book a <em>/consultation</em>🥐',
                               parse_mode='html', reply_markup=all_cmd())

@dp.message_handler(Text('no'), state = Client.check)
async def change_nonratification( msg: types.Message, state: FSMContext):
    await bot.send_message(chat_id=msg.from_user.id, text='Tell me your first name', parse_mode='HTML', reply_markup=all_cmd())
    await Client.first_name.set()

@dp.message_handler(Text('🌼 consultation'))
async def check_customer_base(msg: types.Message):
    check = await check_customers(msg.from_user.id)
    if check == 'Yes':
        await bot.send_message(chat_id=msg.from_user.id, text=yes_check, parse_mode='HTML')
        await bot.send_message(chat_id=msg.from_user.id, text=book_consult, parse_mode='HTML')
        await Consultation.receive_extra.set()
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=no_check, parse_mode='HTML')
        await bot.send_message(chat_id=msg.from_user.id, text='Tell me your first name', parse_mode='HTML')
        await Client.first_name.set()

@dp.message_handler(state= Consultation.receive_extra)
async def consultation_extra(msg: types.Message):
    await request_consulatation(msg.from_user.id , msg.text)
    await bot.send_message(chat_id=msg.from_user.id, text=send_consult, parse_mode='HTML')

@dp.message_handler(Text('🥜 My orders'))
async def look_my_orders(msg: types.Message):
    user_id = msg.from_user.id
    orders_id = get_my_orders_id(user_id)
    
    first_name = get_first_name_order(user_id)
    last_name = get_last_name_order(user_id)
    phone = get_phone_order(user_id)
    email = get_email_order(user_id)
    
    
    if len(orders_id) == 1:
        
        for i in range(len(orders_id)):
           order_id = orders_id[i]['orders_id']
           products = get_product_my_orders(order_id)
           quantities = get_quantity_my_orders(order_id)
           desc = ''
           for y in range(len(products)):
                   product = products[y]['dish']
                   quantity = quantities[y]['quantity']
                   desc += order_product(product, quantity)
        
        await bot.send_message(chat_id = msg.from_user.id, text = my_order(order_id,first_name,last_name,email,phone,desc))
    
    
    elif len(orders_id) > 1:
        
        for i in range(len(orders_id)):
               order_id = orders_id[i]['orders_id']
               products = get_product_my_orders(order_id)
               quantities = get_quantity_my_orders(order_id)
               desc = ''
               
               for y in range(len(products)):
                   product = products[y]['dish']
                   quantity = quantities[y]['quantity']
                   desc += order_product(product, quantity)
               await bot.send_message(chat_id = msg.from_user.id, text = my_order(order_id,first_name,last_name,email,phone,desc))
    
    
#---------------------------------CALLBACK------------------------------------------------------------ 
        
@dp.callback_query_handler()
async def callback_command(callback: types.CallbackQuery, state:FSMContext):
    if callback.data == 'menu_pdf':#-------------------------------------menu pdf-------------------
        await bot.send_message(chat_id=callback.from_user.id, text = 'Here you are')
        await bot.send_message(chat_id=callback.from_user.id, text='There would be your pdf file')
    elif callback.data == 'menu_in_chat':#-------------------------------------------menu in chat--------
        await bot.send_message(chat_id=callback.from_user.id, text = menu_message,
                               reply_markup=menu_pastry_type(), parse_mode='HTML')
    elif callback.data == 'cake' or callback.data == 'muffins': #------------------------ cake or muffins-------
        topic = callback.data
        dishes = get_menu_dishes(topic)
        desc = get_menu_description(topic)
        en_val = get_menu_eng_val(topic)
        img_link = get_menu_image_link(topic)
        price = get_price(topic)
        for i in range(len(dishes)):
            
            link = get_photo(img_link,i)
            photo = open(link, 'rb')
            await bot.send_photo(chat_id=callback.from_user.id, photo=photo,
                                 caption = get_caption(dishes,topic,desc,en_val,i,price),
                                 reply_markup=estemate_product())
            
        await bot.send_message(chat_id = callback.from_user.id, text=after_product_text, 
                               reply_markup=after_menu(), parse_mode='HTML')
    elif callback.data == 'liked':#-------------------------------------------------liked----------------
        product =  callback.message['caption'].split(':')[0][2::]
        telegram_id = callback.message['chat']['id']
        first_name = callback.message['chat']['first_name'] 
        last_name = callback.message['chat']['last_name']
        await save_user(telegram_id,first_name, last_name)
        await create_cart(telegram_id)
        
        await liked_product(telegram_id, product)
        await callback.answer( 
                               text='Successfully added to "💛Liked"')
    elif callback.data == 'del_liked_product':#---------------------------------------------------del_liked_product---
        product =  callback.message['caption'].split(':')[0][2::]
        telegram_id = callback.message['chat']['id']
        product_id = get_product_liked_deleted(telegram_id, product)
        await delete_liked_product(product_id)
        await callback.answer(text='Successfully deleted🍾')
        await callback.message.delete()
    
    
    elif callback.data == 'go_to_liked': #--------------------------go to liked---------------
        user_id = callback.from_user.id
        products_id = get_liked_id(user_id)
        await bot.send_message(chat_id=callback.from_user.id , text=liked_text_before, parse_mode='HTML')
        
        for i in range(len(products_id)):
            product = get_liked_product(products_id[i]['liked_id'])
            product_desc = send_product_description(product)
            product_imge_link = send_product_img_link(product)
            product_en_val = send_product_eng_val(product)
            product_topic = send_product_category(product)
            price = send_dish_price(product)
            photo = open(product_imge_link,'rb')
            
        
            await bot.send_photo(chat_id=callback.from_user.id, photo=photo,
                             caption = liked_caption(product,product_desc,product_en_val,product_topic,price),
                             reply_markup=after_liked_product())
    
    elif callback.data == 'buy':#-----------------------------------------------------------Save to Cart/buy----
        await callback.message.edit_reply_markup(reply_markup=estimate_to_cart())
    
    elif callback.data == 'change_quantity':
        user_id = callback.from_user.id
        product =  callback.message['caption'].split(':')[0][2::]
        quantity = int(callback['message']['caption'].split(':')[2].split('🧩')[0])
        await callback.message.edit_reply_markup(reply_markup=cart_manipulation(quantity))
    
    elif callback.data == 'less_cart':
        quantity = int(callback['message']['reply_markup']['inline_keyboard'][0][1]['text'])
        quantity -= 1
        if quantity > 0:
           cake = callback['message']['caption'].split(':')[0][2::]
           default_price = send_dish_price(cake)
           total_price = int(default_price) * quantity
           await callback.message.edit_reply_markup(reply_markup=cart_manipulaton2(quantity,total_price))
        
        else:
            product =  callback.message['caption'].split(':')[0][2::]
            telegram_id = callback.message['chat']['id']
            product_id = get_product_cart_delete(telegram_id,product)
            await delete_cart_product(product_id)
            await callback.answer(text='Successfully deleted🍾')
            await callback.message.delete() 
          
    elif callback.data =='more':
        quantity = int(callback['message']['reply_markup']['inline_keyboard'][0][1]['text'])
        quantity += 1
        
        cake = callback['message']['caption'].split(':')[0][2::]
        default_price = send_dish_price(cake)
        total_price =  int(default_price)*quantity
        await callback.message.edit_reply_markup(reply_markup=change_quantity_cart_kb(quantity,total_price))
    
    elif callback.data =='less':
        quantity = int(callback['message']['reply_markup']['inline_keyboard'][0][1]['text'])
        quantity -= 1
        if quantity > 0:
           cake = callback['message']['caption'].split(':')[0][2::]
           default_price = send_dish_price(cake)
           total_price = int(default_price) * quantity
           await callback.message.edit_reply_markup(reply_markup=change_quantity_cart_kb(quantity,total_price))
        
        else:
            await callback.message.edit_reply_markup(reply_markup=estemate_product())
    
    elif callback.data == 'add_to_cart':
        quantity = int(callback['message']['reply_markup']['inline_keyboard'][0][1]['text'])
        product = callback['message']['caption'].split(':')[0][2::]
        await save_to_cart(callback.from_user.id, product,quantity)
        await callback.answer(text='Successfully added to cart🥐')
    
    elif callback.data == 'go_to_buy':
        user_id = callback.from_user.id
        products_id = get_cart_products_id(user_id)
        products = []
        for i in range(len(products_id)):
            products.append(get_cart_products(products_id[i]['cart_product_id']))
        await bot.send_message(chat_id=callback.from_user.id , text=cart_text_before,parse_mode='HTML' )
        total_price = 0
        for i in range(len(products)):
            product = products[i]
            product_desc = send_product_description(product)
            product_imge_link = send_product_img_link(product)
            product_en_val = send_product_eng_val(product)
            product_topic = send_product_category(product)
            price = send_dish_price(product)
            quantity = get_cart_quntity(user_id,product)
            cost = price*quantity
            total_price += cost
            photo = open(product_imge_link,'rb')

            await bot.send_photo(chat_id=callback.from_user.id, photo=photo,
                             caption = cart_caption(product,product_desc,product_en_val,product_topic, quantity,price),
                             reply_markup=after_cart())
        await bot.send_message(chat_id=callback.from_user.id,
                               text = f'🧩 <b>All in all {total_price} rubles</b> 🧩',parse_mode='html')
        await bot.send_message(chat_id=callback.from_user.id,
                               text = 'Do you want make an order?',reply_markup=make_order())
    
    elif callback.data == 'delete_cart':
        product =  callback.message['caption'].split(':')[0][2::]
        telegram_id = callback.message['chat']['id']
        product_id = get_product_cart_delete(telegram_id,product)
        await delete_cart_product(product_id)
        await callback.answer(text='Successfully deleted🍾')
        await callback.message.delete()
    
    elif callback.data == 'yes_customer':
        await bot.send_message(chat_id=callback.from_user.id,
                               text = '🥐Now you <b>CAN</b> make an <em>/order</em> or book a <em>/consultation</em>🥐',
                               parse_mode='html')
    
    elif callback.data == 'no_customer':
        
        await bot.send_message(chat_id=callback.from_user.id, text='Tell me your first name', parse_mode='HTML')
        await Client.first_name.set()


    elif callback.data == 'make_order':
        check = await check_customers(callback.from_user.id)
        if check == 'Yes':
            await bot.send_message(chat_id=callback.from_user.id, text=yes_check, parse_mode='HTML')
            cart = check_cart(callback.from_user.id)
        
            if cart == 'no check':
                await bot.send_message(chat_id=callback.from_user.id, text='''Your cart is empty▪️
🥐 /menu to choose <em>yummy pastry</em>🥐''', parse_mode='HTML')
            else:
                all_products = get_everything_from_cart(callback.from_user.id)
                all_quantity = get_every_quantity_cart(callback.from_user.id)
                desc = ''
                for i in range(len(all_products)):
                    desc += order_product(all_products[i]['dish'], all_quantity[i]['quantity'])

                id = callback.from_user.id

                first_name = get_first_name_order(id)
                last_name = get_last_name_order(id)
                phone = get_phone_order(id)
                email = get_email_order(id)
                await bot.send_message(chat_id = callback.from_user.id, text = all_order(first_name,last_name,email,phone,desc))
                await makeOrder.checking.set()
    
        else:
            await bot.send_message(chat_id=callback.from_user.id, text=no_check, parse_mode='HTML')
            await bot.send_message(chat_id=callback.from_user.id, text='Tell me your first name', parse_mode='HTML')
            await Client.first_name.set()

#_________---------------------------ADMIN SIDE---------------------------------
@dp.message_handler(IsAdmin(), Command('admin'))
async def check_admin(msg: types.Message):
    await bot.send_message(chat_id=msg.from_user.id, text='Admin, welcome',reply_markup= admin_kb()) 

@dp.message_handler(IsAdmin(), Text('Рассылка')) 
async def send_everybody(msg: types.Message):
    await bot.send_message(chat_id = msg.from_user.id, text='Write text')
    await Sender.text.set()
    
@dp.message_handler(IsAdmin(), state = Sender.text)
async def get_sending_text(msg: types.Message, state: FSMContext):
    if msg.text == 'Stop' or msg.text == 'stop':
        await state.finish()
        await bot.send_message(chat_id=msg.from_user.id, text='Cancled')
    else:
        async with state.proxy() as data:
            data['text'] = msg.text
        
        await bot.send_message(chat_id=msg.from_user.id, text='Send a pic')
        await Sender.photo.set()


    
   
        

@dp.message_handler(IsAdmin(), state = Sender.photo, content_types=['text'])
async def get_sending_photo_text(msg: types.Message, state: FSMContext):

    if msg.text == 'Stop' or msg.text == 'stop':
        await state.finish()
        await bot.send_message(chat_id=msg.from_user.id, text='Cancled')
    elif msg.text == 'no' or msg.text =='No':
        await bot.send_message(chat_id=msg.from_user.id, text='Check')
        data = await state.get_data()
        text = data.get('text')
        await bot.send_message(chat_id=msg.from_user.id, text=text,parse_mode='html')
        await bot.send_message(chat_id=msg.from_user.id, text='Send?')
        await Sender.check.set()

@dp.message_handler(IsAdmin(), state = Sender.photo, content_types=['photo'])
async def get_sending_photo(msg: types.Message, state: FSMContext):   
        photo_file_id = msg.photo[-1].file_id
        await state.update_data(photo=photo_file_id)
        data = await state.get_data()
        text = data.get('text')
        photo = data.get('photo')
        
        await bot.send_photo(chat_id=msg.from_user.id, photo=photo, caption=text, parse_mode='html')
        await bot.send_message(chat_id=msg.from_user.id, text='Send?')
        await Sender.check.set()
        
@dp.message_handler(IsAdmin(), state = Sender.check)
async def get_sending_photo(msg: types.Message, state: FSMContext):  
    if msg.text == 'Yes' or msg.text == 'yes' or msg.text == 'Да' or msg.text == 'да':
        users = get_users()
        data = await state.get_data()
        text = data.get('text')
        photo = data.get('photo')
        
        if photo == None:
            for i in range(len(users)):
                user = users[i]['telegram_id']
                await bot.send_message(chat_id=user, text = text, parse_mode='html')
                await state.finish()
                await bot.send_message(chat_id=msg.from_user.id, text='Done')
        else:
            for i in range(len(users)):
                user = users[i]['telegram_id']
                await bot.send_photo(chat_id=user, caption = text, parse_mode='html', photo=photo)
                await state.finish()
                await bot.send_message(chat_id=msg.from_user.id, text='Done')
        
        
        
    
    elif msg.text =='No' or msg.text =='no' or msg.text =='да' or msg.text =='Да':
        await state.finish()
        await bot.send_message(chat_id=msg.from_user.id, text='Canceled')
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True ,on_startup=onStartup)
