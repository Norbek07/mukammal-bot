import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,F #new
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,input_file
from cat import get_cat_image
from wiki import malumot
from filters.admin import IsAdminFilter
from keyboardbutton import main_button,computer_button,computers,computers_info, phones_info, phone_button, phones
from filters.check_sub_channel import IsCheckSubChannels,CHANNELS
from my_sqlite import create_users,add_user,count_users,get_all_user_ids
from aiogram.client.session.aiohttp import AiohttpSession

session = AiohttpSession(proxy='http://proxy.server:3128')
TOKEN = "6441072259:AAFp4xDrtxJfeHn_pVmuSINjHnspFxEMeus"
ADMINS = [1245143580]

dp = Dispatcher()

@dp.message(IsCheckSubChannels())
async def check_sub_channels(message:Message):
    text = "Quidagi kanallarga a'zo bo'ling."
    for channel in CHANNELS:
            result = await bot.get_chat_member(channel,message.from_user.id)
            ChatInviteLink = await bot.create_chat_invite_link(channel)
            text += f"\n<a href='{ChatInviteLink.invite_link}'>kanal</a>"
    await message.answer(text)

@dp.message(CommandStart())
async def command_start_handler(message: Message):
    
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    try:
        add_user(telegram_id,full_name)
        text = f"Salom {full_name}, Xush kelibsiz"
    except:
        text = f"Salom {full_name}, Nima xizmat"
    await message.answer(text)

@dp.message(F.text=="/count",IsAdminFilter(ADMINS))
async def foyda_soni(message:Message):
    try:
        foydalanuvchilar_soni = count_users()[0]
        await message.answer(f"Botimizda {foydalanuvchilar_soni}ta foydalanuvchi mavjud")
    except:
        await message.answer(f"Botimizda foydalanuvchi yo'q")

from aiogram.fsm.state import StatesGroup,State
class Advert(StatesGroup):
    advert = State()

@dp.message(F.text=="/advert",IsAdminFilter(ADMINS))
async def advert_admin(message:Message,state:FSMContext):
    await message.answer("Reklama yuboringiz mumkin...")
    await state.set_state(Advert.advert)
import time

@dp.message(Advert.advert)
async def send_advert(message:Message,state:FSMContext):
    message_id = message.message_id
    from_user = message.from_user.id
    ids = get_all_user_ids()
    # print(ids)
    for id in ids:
        try:
            await bot.copy_message(chat_id=id[0],from_chat_id=from_user,message_id=message_id)
            time.sleep(0.1)
        except:
            pass
    await state.clear()

@dp.message(F.text=="💁🏻‍♂️ About us")
async def about_as_handler(message:Message):
    about = "      🎉 Welcom       \nWe are The Best Company. Mr Norbek"
    photo_link = "https://picjumbo.com/wp-content/uploads/entrepreneur-working-in-the-office-2210x1473.jpg"
    await message.answer_photo(photo=photo_link,caption=about)

@dp.message(F.text=="☎️ Contact admin")
async def about_as_handler(message:Message):
    about = "Admin info: \nTel: +998 (99)0113618 \nAdmin: @norbek_admin" 
    await message.answer(text= about)

@dp.message(F.text == "📍 Location")
async def company_location(message:Message):
    lat = 40.102296
    long = 65.37345
    await message.answer("📍 Norbek company location ")
    await message.reply_location(latitude=lat,longitude=long)


@dp.message(F.text=="💻 Computers")
async def my_computers(message:Message):
    await message.answer("Our computers",reply_markup=computer_button)

@dp.message(F.text.func(lambda computer:computer in computers))
async def computer_info(message:Message):
    info = computers_info.get(message.text)

    photo = info.get("photo")
    price = info.get("price")
    color = info.get("color")

    text = f"{message.text}\nprice: {price}$ \ncolor:{color} and ..."

    await message.answer_photo(photo=photo,caption=text)


@dp.message(F.text=="📱 Phones")
async def my_computers(message:Message):
    await message.answer("Our computers",reply_markup=phone_button)

@dp.message(F.text.func(lambda phone:phone in phones))
async def computer_info(message:Message):
    info = phones_info.get(message.text)

    photo = info.get("photo")
    price = info.get("price")
    color = info.get("color")

    text = f"{message.text}\nprice: {price}$\ncolor:{color} and ..."

    await message.answer_photo(photo=photo,caption=text)


@dp.message(F.text=="🔙 ortga")
async def computer_func(message:Message):
    text = "Asosiy menu"
    await message.answer(text=text, reply_markup=main_button)

@dp.message(Command("cat"))
async def get_cat(message:Message):
    image_content = get_cat_image()
    if image_content:
        await message.answer_document(document=input_file.BufferedInputFile(file=image_content,filename="cat.png"))

@dp.message(F.text)
async def wiki_malumot(message:Message):
    text = message.text
    natija = malumot(text)
    await message.reply(text=natija)

@dp.startup()
async def bot_start():
    await bot.send_message(chat_id=1245143580,text="Botimiz ishga tushdi! ")


@dp.shutdown()
async def bot_stop():
    await bot.send_message(chat_id=1245143580, text="Botimiz to'xtadi! XAYR")

async def main():
    create_users()
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML,session=session)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
