from aiogram.dispatcher.filters import BoundFilter
from aiogram import  types
import os

class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if str(message.from_user.id) in admins:
            return True
        else:
            return False
# список id админов
admins = os.getenv('ADMIN')
