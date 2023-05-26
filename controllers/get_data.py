
def get_caption(dishes,topic, desc, en_val,dish_num: int, prices):
    dish = dishes[dish_num]['dish']
    description = desc[dish_num]['dish_description']
    energy_value = en_val[dish_num]['кбжу']
    price = prices[dish_num]['price_rub']
    if topic == 'cake':
        message = f"""🎂 {dish}:

{description}

📌 {energy_value}

🧩 {price} rubles"""
        return message
    else:
        message = f"""🎂 {dish}

{description}

📌 {energy_value}

🧩 {price} rubles"""
        
        return message  

def get_photo(img_link, num:int):
    return img_link[num]['dish_img']

def liked_caption(dish, desc,en_val, topic,price):
    if topic == 'cake':
        message = f"""🎂 {dish}:

{desc}

📌 {en_val}

🧩 {price} rubles"""
        return message
    else:
        message = f"""🎂 {dish}

{desc}

📌 {en_val}

🧩 {price} rubles"""
        return message 

def cart_caption(dish, desc,en_val, topic, quantity,prices):
    price = quantity*prices
    if topic == 'cake':
        message = f"""🎂 {dish}:

{desc}

📌 {en_val}

🥠 Quantity: {quantity}

🧩 {price} rubles"""
        return message
    else:
        message = f"""🎂 {dish}

{desc}

📌 {en_val}

🥠 Quantity: {quantity}

🧩 {price} rubles"""
        return message 

def order_product(product, quantity ):
    if product.find('Cake'):
        text = f"""🎂{product}: {quantity} pcs\n"""
        return text

def all_order(first_name, last_name,email,phone, desc):
    text = f"""First name: {first_name}
Last name: {last_name}
Phone: {phone}
Email: {email}

Order:

{desc}

Everything is right?"""
    return text

def my_order(num , first_name, last_name,email,phone, desc):
    text = f""" Order: #00{num}64{num}19
First name: {first_name}
Last name: {last_name}
Phone: {phone}
Email: {email}

Order:

{desc}"""
    return text
    
    
    
    
    