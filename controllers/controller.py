import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

def check_phone_number(number):
    try:
        check = carrier._is_mobile(number_type(phonenumbers.parse(number)))
    except  phonenumbers.phonenumberutil.NumberParseException as err:
        check = None
    print(check)
    return check
