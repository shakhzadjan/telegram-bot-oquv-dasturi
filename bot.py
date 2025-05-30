  

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    Message, CallbackQuery
)
from aiogram.filters import CommandStart
import asyncio

# Token va sozlamalar
TOKEN = "7930427840:AAFPLc9KYbftyNX0TuCnMMjsiGsqcTcVzHg"
CHANNELS = ["@kino_news25"]
ADMINS = [2106641907]

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Obuna tekshiruvi
async def check_subs(user_id: int) -> bool:
    for channel in CHANNELS:
        chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if chat_member.status in ["left", "kicked"]:
            return False
    return True

# Global menyular
cafedra_add_kurs = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1-kurs", callback_data="kurs_add1"),
     InlineKeyboardButton(text="2-kurs", callback_data="kurs_add2")],
    [InlineKeyboardButton(text="3-kurs", callback_data="kurs_add3"),
     InlineKeyboardButton(text="4-kurs", callback_data="kurs_add4")]
])

cafedra_add_fanlar = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🖥 Mikroprotsessor va Assimbler dasturlash tili")],
    ],
    resize_keyboard=True
)

cafedra_add_tanlash = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="mustaqil ish"), KeyboardButton(text="amaliy ish")],
        [KeyboardButton(text="orqaga")]
    ],
    resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1-2-amaliy")],
        [KeyboardButton(text="3-4-amaliy")],
        [KeyboardButton(text="5-6-amaliy")],
        [KeyboardButton(text="7-8-amaliy")],
        [KeyboardButton(text="9-10-amaliy")],
        [KeyboardButton(text="11-12-amaliy")],
        [KeyboardButton(text="13-14-15-amaliy")]
    ],
    resize_keyboard=True
)

# /start komandasi
@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    if not await check_subs(user_id):
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
    else:
        kafedra_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Raqamli texnologiyalar va sun'iy intellekt fakulteti", callback_data="kafedra_add")]
        ])
        await message.answer("Xush kelibsiz! Kafedrani tanlang:", reply_markup=kafedra_markup)

# Obuna tekshiruv tugmasi
@dp.callback_query(F.data == "check_subs")
async def check_subs_callback(call: CallbackQuery):
    user_id = call.from_user.id
    if await check_subs(user_id):
        await call.message.edit_text("✅ Rahmat! Siz barcha kanallarga obuna bo‘lgansiz. Botdan foydalanishingiz uchun /start komandasini bosing",)

    else:
        await call.answer("❌ Siz hali ham barcha kanallarga obuna bo‘lmagansiz!", show_alert=True)

# Kafedra tanlandi
@dp.callback_query(F.data == "kafedra_add")
async def kafedra_selected(callback: CallbackQuery):
    await callback.message.answer("Kursingizni tanlang:", reply_markup=cafedra_add_kurs)
    await callback.answer()

# Kurs tanlandi
@dp.callback_query(F.data == "kurs_add2")
async def kurs_2_selected(callback: CallbackQuery):
    await callback.message.answer("Quyidagi fanlardan birini tanlang:", reply_markup=cafedra_add_fanlar)
    await callback.answer()

# Fan tanlandi
@dp.message(F.text == "🖥 Mikroprotsessor va Assimbler dasturlash tili")
async def fan_tanlandi(message: Message):
    await message.answer("Iltimos, ish turini tanlang:", reply_markup=menu)

# Adminlar uchun fayl ID olish
@dp.message(F.video | F.photo | F.document | F.audio | F.voice)
async def get_file_id(message: Message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        if message.video:
            await message.answer(f"📹 Video File ID: `{message.video.file_id}`", parse_mode="Markdown")
        elif message.photo:
            await message.answer(f"🖼 Photo File ID: `{message.photo[-1].file_id}`", parse_mode="Markdown")
        elif message.document:
            if message.document.file_name.endswith('.docx'):
                await message.answer(f"📄 DOCX File ID: `{message.document.file_id}`", parse_mode="Markdown")
            else:
                await message.answer("🚫 Faqat .docx formatdagi fayllar qabul qilinadi.")
        elif message.audio:
            await message.answer(f"🎵 Audio File ID: `{message.audio.file_id}`", parse_mode="Markdown")
        elif message.voice:
            await message.answer(f"🎙 Voice File ID: `{message.voice.file_id}`", parse_mode="Markdown")
    else:
        await message.answer("🚫 Ushbu buyruq faqat adminlar uchun mavjud!")

# 1-2-amaliy ish
@dp.message(F.text == "1-2-amaliy")
async def send_video_and_doc(message: Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIBxWg5b6i83b3n3isWNRy3Gi5t3jwwAALxcQACGvnISWXtlUNHoLvJNgQ"
        docx_id = "BQACAgIAAxkBAAIBx2g5b8hEX00U1njrcxW5IZsImMsgAALycQACGvnISfFePfCY8tDjNgQ"
        await message.answer_video(video_id, caption="🎬 1-2-amaliy ish")
        await message.answer_document(docx_id, caption="📄 1-2-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)









# "3-4-amaliy ish" tugmasi bosilganda video + DOCX yuborish
@dp.message(F.text == "3-4-amaliy")
async def send_video_and_doc(message: types.Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIByWg5cONSLi6R-X61KoVgFzJYj345AAIGcgACGvnISVFTkY1dNKVnNgQ"
        docx_id = "BQACAgIAAxkBAAIBy2g5cPAOTV638xiUBiEZxd5vg-ESAAIHcgACGvnISbVhY7bAuMJsNgQ"  # <-- DOCX faylingiz file_id
        await message.answer_video(video_id, caption="🎬 3-4-amaliy ish")
        await message.answer_document(docx_id, caption="📄 3-4-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)



# "5-6-amaliy ish" tugmasi bosilganda video + DOCX yuborish
@dp.message(F.text == "5-6-amaliy")
async def send_video_and_doc(message: types.Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIBzWg5cVz72s3osExmXwu5pi8RgiKcAAILcgACGvnISS-zTnacHJZmNgQ"
        docx_id = "BQACAgIAAxkBAAIBz2g5cWtOfm3X5FH8NLtD6SkAAabchAACDnIAAhr5yElMUTTB2gABeZA2BA"  # <-- DOCX faylingiz file_id
        await message.answer_video(video_id, caption="🎬 5-6-amaliy ish")
        await message.answer_document(docx_id, caption="📄 5-6-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)





# "7-8-amaliy ish" tugmasi bosilganda video + DOCX yuborish
@dp.message(F.text == "7-8-amaliy")
async def send_video_and_doc(message: types.Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIB0Wg5cZc1mxBbruivu8fYCgzqf8BNAAJQdwACTP7ISXkHKUNUNXEmNgQ"
        docx_id = "BQACAgIAAxkBAAIB02g5caZ7zlvg4gABcKfUN2VW52TgSgACFXIAAhr5yEnlKLZ9UhksGDYE"  # <-- DOCX faylingiz file_id
        await message.answer_video(video_id, caption="🎬 7-8-amaliy ish")
        await message.answer_document(docx_id, caption="📄 7-8-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)





# "9-10-amaliy ish" tugmasi bosilganda video + DOCX yuborish
@dp.message(F.text == "9-10-amaliy")
async def send_video_and_doc(message: types.Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIB1Wg5ccO62CZuhbAuXzi-yRdfFRnVAAIZcgACGvnISaxOcVpX4nZPNgQ"
        docx_id = "BQACAgIAAxkBAAIB12g5cdXMgMlXPg67s2txbpCnPOVWAAIccgACGvnISdSogwovr9zBNgQ"  # <-- DOCX faylingiz file_id
        await message.answer_video(video_id, caption="🎬 9-10-amaliy ish")
        await message.answer_document(docx_id, caption="📄 9-10-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)



# "11-12-amaliy ish" tugmasi bosilganda video + DOCX yuborish
@dp.message(F.text == "11-12-amaliy")
async def send_video_and_doc(message: types.Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIB2Wg5cimoOj62d7bdZgKl-nBkRsdDAAIkcgACGvnISXdj-8FhuGDVNgQ"
        docx_id = "BQACAgIAAxkBAAIB22g5cjcbNCrvrPdX-18LJmcXl7kzAAIocgACGvnISYnTPGA7PHJtNgQ"  # <-- DOCX faylingiz file_id
        await message.answer_video(video_id, caption="🎬 11-12-amaliy ish")
        await message.answer_document(docx_id, caption="📄 11-12-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)




# "13-14-15-amaliy ish" tugmasi bosilganda video + DOCX yuborish
@dp.message(F.text == "13-14-15-amaliy")
async def send_video_and_doc(message: types.Message):
    user_id = message.from_user.id
    if await check_subs(user_id):
        video_id = "BAACAgIAAxkBAAIB3Wg5cveJBT3VrPhW5AT6fuj66IoaAAJmdwACTP7ISYbD2gtlOsk0NgQ"
        docx_id = "BQACAgIAAxkBAAIB32g5cwSV6Tw8a7qrPWyYWm3uqE86AAI4cgACGvnISUsJ_lJJcYYvNgQ"  # <-- DOCX faylingiz file_id
        await message.answer_video(video_id, caption="🎬 13-14-15-amaliy ish")
        await message.answer_document(docx_id, caption="📄 13-14-15-amaliy ish")
    else:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🔗 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS
            ] + [[InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")]]
        )
        await message.answer("🚫 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)






# Botni ishga tushurish
async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
