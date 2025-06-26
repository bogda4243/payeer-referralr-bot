from aiogram import Bot, Dispatcher, executor, types
import logging
import os

API_TOKEN = os.getenv("BOT_TOKEN")
REF_LINK = 'https://payeer.com/?session=38668462'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

ref_users = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    ref = message.get_args()

    if ref and ref != str(user_id):
        if user_id not in ref_users:
            ref_users[user_id] = ref
            try:
                await bot.send_message(ref, f"🎉 У вас новий реферал: @{message.from_user.username or user_id}")
            except:
                pass

    await message.answer(
        f"👋 Привіт, {message.from_user.first_name}!\n"
        f"💸 Заробляй на Payeer разом з нами!\n"
        f"Ось твоє реферальне посилання:\n\n"
        f"{REF_LINK}"
    )

@dp.message_handler(commands=['stats'])
async def show_stats(message: types.Message):
    refs = [k for k, v in ref_users.items() if v == str(message.from_user.id)]
    await message.answer(f"👥 Ваші реферали: {len(refs)}\nID: {refs}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
