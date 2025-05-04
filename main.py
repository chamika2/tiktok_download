import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '7947621759:AAEr203SyS6_e79gnwwaEeZYwRMgscA-S-E'

# Logging
logging.basicConfig(level=logging.INFO)

# Bot init
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Start command
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! Send me a TikTok link and I'll download it without watermark!")

# TikTok link handler
@dp.message_handler()
async def download_tiktok(message: types.Message):
    url = message.text
    if "tiktok.com" not in url:
        await message.reply("Please send a valid TikTok link!")
        return

    await message.reply("Downloading...")

    try:
        # Using ttdownloader.com unofficial API
        api_url = f"https://api.tikmate.app/api/lookup?url={url}"
        r = requests.get(api_url).json()
        video_url = f"https://tikmate.app/download/{r['token']}/{r['id']}.mp4"

        await bot.send_video(chat_id=message.chat.id, video=video_url)
    except Exception as e:
        print(e)
        await message.reply("Failed to download. Please try again later!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)