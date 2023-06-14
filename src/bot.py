from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message
from config import TOKEN
import buttons as bt


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hi!\nI'm captcha bot for Telegram", reply_markup=bt.main_menu)

@dp.message_handler(commands=['role'])
async def echo(message: types.Message):
    

    async def is_admin(currency_user_id,currency_chat_id):
        admins = await bot.get_chat_administrators(currency_chat_id)

        for admin in admins:
            if admin.user.id ==  currency_user_id:
                return True
            
        
    if await is_admin(message.from_id,message.chat.id):
        await message.reply('You are an admin 👮‍♂️')

    else:
        await message.reply('You are a member 🧑‍🌾')
                



@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Info 🤖':
        await message.reply("I'm a captcha bot for checking user who are he")

    
    if message.text == 'How to add im chat? 🤝':
        await message.reply("1.Open bot profile\n2.Copy bot `username`\n3.Go to your chat\n4.Add to chat.\n5.Paste bot `username` in search string.\n6.Click add.")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)