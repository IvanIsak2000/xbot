from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message
import buttons as bt
import toml
import os 
import secrets
import os.path
from dataclasses import dataclass
import logging

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users_verification_file = 'check_list.toml'
folder_of_all_captchas = 'captcha_images'
name_of_white_list_file = 'white_list.toml'
default_data = "title = ''\n[users]"

logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s")

def create_default_file_and_write_data_if_not_exist(func):
    def wrapper(filename, first_data, second_data):
        if not os.path.isfile(filename):
            with open(filename,'w') as new_file:
                default_data = "title = ''\n[users]"
                new_file.write(default_data)
            with open(filename,'a') as file:
                file.write(f"\n'{first_data}'='{second_data}'")
    return wrapper

@create_default_file_and_write_data_if_not_exist
def write_in_file(filename, first_data, second_data):
    with open(filename,'a') as file:
        file.write(f"\n'{first_data}'='{second_data}'")

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def get_new_member_and_send_captcha(message: Message):

    @dataclass
    class Captcha:
        image: str
        answer: str

    @dataclass
    class NewUser:
        id: str
        mention: str
        
    async def get_random_captcha ()-> str:
        all_captchas = os.listdir(folder_of_all_captchas)
        random_captcha = secrets.choice(all_captchas)
        return random_captcha
        
    async def send_captcha(image, mention)-> None:
        captcha_image = open(f'{folder_of_all_captchas}/{image}','rb') 
        await message.answer_photo(captcha_image, caption=f"{mention}\nPlease complete the captcha by typing /answer and text on the image.\nTime limit: 10 minutes")

    captcha = await get_random_captcha()
    answer = captcha.split('.')[0]

    captcha = Captcha(image=captcha, answer=answer)
    user = NewUser(
    id=message.new_chat_members[0].id,
    mention=message.new_chat_members[0].mention)

    write_in_file(users_verification_file, user.id, captcha.answer)
    await send_captcha(captcha.image, user.mention)
    
@dp.message_handler(commands=['answer'])
async def new_members_handler(message: Message):
    
    @dataclass
    class User_performing_captcha:
        id: str
        answer: str
        name: str

    async def answer_is_correct(user: User_performing_captcha) -> bool:
        users = toml.load(users_verification_file)
        return users['users'][str(user.id)] == str(user.answer)

    try:
        user_answer = message.text.split()[1]
    except IndexError:
        await message.reply('You need write message as: \n/answer <captcha code>')

    user = User_performing_captcha(id=message.from_id, answer=user_answer, name=message.from_user.full_name) 

    if await answer_is_correct(user.id, user.answer):
        write_in_file(name_of_white_list_file, user.id, user.name)
        await message.reply('Successful!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)