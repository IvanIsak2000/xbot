import os
import secrets
import os.path
from dataclasses import dataclass
import logging
from datetime import timedelta

import toml
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message

import buttons as bt
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users_verification_file = 'check_list.toml'
folder_of_all_captchas = 'captcha_images'
name_of_white_list_file = 'white_list.toml'
default_data = "title = ''\n"
allowed_time = 60  # in seconds
message_to_pass_captcha = f'\nPlease complete the captcha by typing /answer and text on the image.\nTime limit: {allowed_time} seconds'

logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s")


def create_default_file(filename) -> None:
    with open(filename, 'w') as new_file:
        new_file.write(default_data)


def write_in_check_list(
        filename: str,
        user_id: int,
        correct_answer: str,
        message_id: str) -> None:
    if not os.path.isfile(filename):
        create_default_file(filename)
    with open(filename, 'a') as file:
        file.write(
            f"[{user_id}]\ncorrect_answer = '{correct_answer}'\nbot_message_id = '{message_id}'")


def write_in_white_list(filename: str, user_id: int, name: str) -> None:
    if not os.path.isfile(filename):
        create_default_file(filename)
    with open(filename, 'a') as file:
        file.write(f"'{user_id}' = '{name}'")


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    if message.chat.type == "private":
        await message.reply('Hi 👋', reply_markup=bt.main_menu)

@dp.message_handler()
async def echo(message: types.Message):

    if message.chat.type == "private":
        if message.text == 'Info 🤖':
            await message.reply("Hi 👋 \nI'm chat bot for checking if the user is really human")

        if message.text == 'How to add im chat? 🤝':
            await message.reply(f'1. Copy: <code>@{(await bot.get_me()).username}</code>\n2. Open your chat\n3. Add me\n4. Set my role as administrator\n5. Add all rules\n6. You can check status: <code>/status</code>', parse_mode='html')

        if message.text == 'Gihub 💻':
            await message.reply('https://github.com/IvanIsak2000/xbot')



@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def get_new_member_and_send_captcha(message: Message) -> None:

    if not message.new_chat_members[0].is_bot:

        @dataclass
        class Captcha:
            image: str
            answer: str

        @dataclass
        class NewUser:
            id: str
            mention: str

        async def get_random_captcha() -> str:
            '''
            Открывает заранее подготовленную папку с изображениями капч
            Возвраащет рандомное изображение
            пример: '12345.jpg', где название файла - это сам ответ
            '''
            all_captchas = os.listdir(folder_of_all_captchas)
            random_captcha = secrets.choice(all_captchas)
            return random_captcha

        async def send_captcha_and_return_message_id(image, mention) -> int:
            '''
            Получает название файла из папки капч и отправляет его новому пользователю
            Возвращает id отправленной ботом капчи
            '''
            captcha_image = open(f'{folder_of_all_captchas}/{image}', 'rb')
            bot_message = await message.answer_photo(
                captcha_image,
                caption=f"{mention} {message_to_pass_captcha}")
            return bot_message['message_id']

        captcha = await get_random_captcha()  # 123456.jpg
        answer = captcha.split('.')[0]  # 123456

        captcha = Captcha(image=captcha, answer=answer)
        user = NewUser(
            id=message.new_chat_members[0].id,
            mention=message.new_chat_members[0].mention)

        message_id = await send_captcha_and_return_message_id(captcha.image, user.mention)
        write_in_check_list(
            users_verification_file,
            user.id,
            captcha.answer,
            message_id)


@dp.message_handler(commands=['answer'])
async def check_user_answer(message: Message):

    @dataclass
    class User_performing_captcha:
        id: str
        name: str
        answer: str
        answer_id: int

    try:
        user_answer = message.text.split()[1]
        user = User_performing_captcha(
            id=message.from_id,
            name=message.from_user.full_name,
            answer=user_answer,
            answer_id=message.message_id)

    except IndexError:
        await message.reply('You need write message as: \n/answer <captcha code>')

    async def answer_is_correct(id, answer) -> bool:
        users = toml.load(users_verification_file)
        return users[str(id)]['correct_answer'] == answer

    async def get_captcha_id(user_id: int) -> int:
        '''
        Если пользователь ввёл правильный ответ на капчу, то эта функция вернут id сообщения капчи, чтобы его можно было удалить
        '''
        users = toml.load(users_verification_file)
        return users[str(user_id)]['bot_message_id']

    async def delete_messages(captcha_message_id, user_message_id) -> None:
        '''
        Удаляет саму капчу и правильный ответ пользователя
        '''
        await bot.delete_message(message.chat.id, captcha_message_id)
        await bot.delete_message(message.chat.id, user_message_id)

    if await answer_is_correct(user.id, user.answer):
        captcha_id = await get_captcha_id(user.id)
        await delete_messages(captcha_id, user.answer_id)

        write_in_white_list(name_of_white_list_file,
                            user.id,
                            user.name)


@dp.message_handler(commands=['Status','status'])
async def check_bot_status(message: Message):

    async def get_user_status(chat_id, user_id) -> str:
        return (await bot.get_chat_member(chat_id, user_id)).status  

    async def is_admin(user_status) -> bool:
        return user_status == 'administrator' or  user_status == 'creator'
    
    user_status = await get_user_status(message.chat.id, message.from_id)

    if await is_admin(user_status):
        await message.reply('Bot is activate ✅')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
