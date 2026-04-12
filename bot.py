import telebot
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 আসসালামু আলাইকুম!\n\n🔗 শুধু ভিডিও লিংক পাঠান")

# ✅ শুধু link detect করবে
def is_link(message):
    return message.text and message.text.startswith("http")

# DOWNLOAD
@bot.message_handler(func=is_link)
def download_video(message):
    url = message.text

    try:
        bot.reply_to(message, "⏳ ডাউনলোড হচ্ছে...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(id)s.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        with open(file_name, 'rb') as f:
            bot.send_video(message.chat.id, f)

        os.remove(file_name)

    except Exception as e:
        print(e)

bot.infinity_polling()
