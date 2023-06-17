from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message
from config import TOKEN
import buttons as bt
import toml
import os 
import secrets
import os.path


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
file_name_for_captcha_users = 'check_list.toml'

def check_list_is_exist()-> None:
    if not os.path.isfile(file_name_for_captcha_users):
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


    new_member = message.new_chat_members[0]
    id_of_new_member = message.new_chat_members[0].id

    all_images_of_captcha = os.listdir('captcha_images')
    random_captcha_image = secrets.choice(all_images_of_captcha)
    captcha_image = open(f'captcha_images/{(random_captcha_image)}','rb') 
    answer = random_captcha_image.split('.')[0]

    user_id_and_captcha_answer = f"'{id_of_new_member}' = '{answer}'"

    with open(file_name_for_captcha_users, "a") as toml_file:
        toml_file.write(user_id_and_captcha_answer)

    await message.answer_photo(captcha_image, caption=f"{new_member.mention}\nPlease complete the captcha by typing /answer  and text on the image.\nTime limit: 10 minutes")

@dp.message_handler(commands=['answer'])
async def new_members_handler(message: Message):


    def answer_is_correct() -> bool:
        users = toml.load(file_name_for_captcha_users)
        user_answer = message.text.split()[1]
        if users['users'][str(message.from_id)] == user_answer:
            return True
        else:
            return False
        
    print(answer_is_correct())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

