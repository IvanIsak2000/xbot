from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message
from config import TOKEN
import buttons as bt
import toml
import os 
import secrets
import os.path
from dataclasses import dataclass


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
users_verification_file = 'check_list.toml'
folder_of_all_captcha_images = 'captcha_images'

def check_list_is_exist()-> None:
    if not os.path.isfile(users_verification_file):
        create_check_list()

def create_check_list()-> None:
    default_data = """
title = 'this is a file to store the correct answer for each new member'
[users]
    
"""
    with open ('check_list.toml','w') as file:
        file.write(default_data)

# @dp.message_handler(commands=['start', 'help'])
# async def welcome(message: types.Message):
#     await message.reply("Hi!\nI'm captcha bot for Telegram", reply_markup=bt.main_menu)

# @dp.message_handler(commands=['role'])
# async def echo(message: types.Message):

#     user_status = (await bot.get_chat_member(message.chat.id,message.reply_to_message.from_user.id)).status
    
#     async def is_admin(user_status):
#         return user_status ==  'administrator' or 'creator'

        
#     if await is_admin(user_status):
#         await message.reply(f'He are an admin 👮‍♂️: {user_status}' )


#     else:
#         await message.reply(f'He are member 🧑‍🌾: {user_status}')


# @dp.message_handler(commands=['myrole'])
# async def echo(message: types.Message):

#     async def user_passed_captcha():
#         db = toml.load('users.toml')
#         for user in db['users_successful_passed_captcha']:
#             if str(message.from_id) == user:
#                 return True
#             else:
#                 return False

#         # db['users_successful_passed_captcha'][message.from_id] = message.from_user.username

#     if not await user_passed_captcha():
#         await message.reply('Пройдите капчу!')

#     await message.reply(f'You are: {(await bot.get_chat_member(message.chat.id,message.from_user.id)).status}')
          

# @dp.message_handler()
# async def echo(message: types.Message):

    # # images = files = [os.path.splitext(filename)[0] for filename in os.listdir('captcha_images')]
    # images = os.listdir('captcha_images')
    # captcha_image = secrets.choice(images)
    # answer = captcha_image.split('.')[0]
    # await message.reply(answer)
    # captcha_image = open(f'captcha_images/{(captcha_image)}','rb') 

    # await message.answer_photo(captcha_image, caption="Please complete the captcha by typing `/answer ` and text on the image.\nTime limit: 10 minut")
    # print(message.text)

    # if message.text == 'Info 🤖':
    #     await message.reply("I'm a captcha bot for checking user who are he")

    
    # if message.text == 'How to add im chat? 🤝':
    #     await message.reply("1.Open bot profile\n2.Copy bot `username`\n3.Go to your chat\n4.Add to chat.\n5.Paste bot `username` in search string.\n6.Click add.\n7.Change bot role to admin")

    # if message.text == 'Status':
    #     await message.reply('Bot is activate ✅')



    # async def user_passed_captcha(user):
    #     user_id =(await bot.get_chat_member(message.chat.id,message.reply_to_message.from_user.id))
    #     print(user_id)
# @dp.message_handler(content_types=["new_chat_members"])
# async def handler_new_member(message):
#     user_name = message.new_chat_member.first_name
#     await message.reply(message.chat.id, "Добро пожаловать, {0}!".format(user_name))

@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: Message):
    check_list_is_exist()

    @dataclass
    class Captcha:
        captcha: str
        answer: str

    @dataclass
    class NewUser:
        id: str
        mention: str

    async def get_random_captcha ()-> str:
        all_images_of_captcha = os.listdir(folder_of_all_captcha_images)
        random_captcha_image = secrets.choice(all_images_of_captcha)
        return random_captcha_image
    
    async def get_captcha_answer(random_captcha) -> str:
        return  random_captcha.split('.')[0]
        
    async def send_captcha(captcha: Captcha, new_user: NewUser)-> None:
        captcha_image = open(f'{folder_of_all_captcha_images}/{(captcha.captcha)}','rb') 
        await message.answer_photo(captcha_image, caption=f"{new_user.mention}\nPlease complete the captcha by typing /answer  and text on the image.\nTime limit: 10 minutes")

    async def write_id_with_correct_answer(captcha:Captcha, new_user:NewUser )-> None:
        user_id_and_captcha_answer = f"'{new_user.id}' = '{captcha.answer}'"
        with open(users_verification_file, "a") as toml_file:
            toml_file.write(user_id_and_captcha_answer)


    captcha = await get_random_captcha()
    answer = await get_captcha_answer(captcha)

    captcha_data = Captcha(captcha=captcha, answer=answer)
    user_data = NewUser(id=message.new_chat_members[0].id,mention=message.new_chat_members[0].mention)

    await send_captcha(captcha_data, user_data)
    await write_id_with_correct_answer(captcha_data, user_data)

@dp.message_handler(commands=['answer'])
async def new_members_handler(message: Message):
    
    @dataclass
    class User_performing_captcha:
        id : str
        answer : str

    async def answer_is_correct(user: User_performing_captcha) -> bool:
        users = toml.load(users_verification_file)
        return users['users'][str(user.id)] == str(user.answer)
    
    try:
        print(await answer_is_correct(User_performing_captcha(id=message.from_id, answer=message.text.split()[1])))
    except IndexError:
        await message.reply('You need write message as: \n/answer <captcha code>')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)