import aiogram 
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# -----Main menu-----
bt_info =  KeyboardButton('Info 🤖')
bt_how_to_add = KeyboardButton('How to add im chat? 🤝') 
bt_activate = KeyboardButton('Activate ✅')
main_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(bt_info, bt_how_to_add, bt_activate) 