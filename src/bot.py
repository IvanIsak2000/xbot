from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType, Message
from config import TOKEN
import buttons as bt

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Hi!\nI'm captcha bot for Telegram", reply_markup=bt.main_menu)


@dp.message_handler()
async def echo(message: types.Message):

    if message.text == 'Info 🤖':
        await message.reply("I'm a captcha bot for checking user who are he")

    
    if message.text == 'How to add im chat? 🤝':
        await message.reply("1.Open bot profile\n2.Copy bot `username`\n3.Go to your chat\n4.Add to chat.\n5.Paste bot `username` in search string.\n6.Click add.")



dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
    new_member = message.new_chat_members[0]
    await bot.send_message(message.chat.id, f'Hello! You need to do captcha {new_member.mention}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)