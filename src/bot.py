from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message
from config import TOKEN
import buttons as bt
import toml


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

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
#     if message.text == 'Info 🤖':
#         await message.reply("I'm a captcha bot for checking user who are he")

    
#     if message.text == 'How to add im chat? 🤝':
#         await message.reply("1.Open bot profile\n2.Copy bot `username`\n3.Go to your chat\n4.Add to chat.\n5.Paste bot `username` in search string.\n6.Click add.\n7.Change bot role to admin")

#     if message.text == 'Status':
#         await message.reply('Bot is activate ✅')

        

    # async def user_passed_captcha(user):
    #     user_id =(await bot.get_chat_member(message.chat.id,message.reply_to_message.from_user.id))
    #     print(user_id)
# @dp.message_handler(content_types=["new_chat_members"])
# async def handler_new_member(message):
#     user_name = message.new_chat_member.first_name
#     await message.reply(message.chat.id, "Добро пожаловать, {0}!".format(user_name))

@dp.message_handler()
async def get_message(message: Message):
    user_name = message.new_chat_members
    print(user_name)
    # await message.reply(user_name)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

