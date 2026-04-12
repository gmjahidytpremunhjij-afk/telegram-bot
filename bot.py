import telebot
import yt_dlp
import os

# TOKEN from Railway
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    bot.reply_to(message, f"""👋 আসসালামু আলাইকুম {name} স্যার!

📥 আপনি এখান থেকে ডাউনলোড করতে পারবেন:
✔ TikTok
✔ Facebook Video
✔ YouTube
✔ Instagram

🔗 শুধু ভিডিও লিংক পাঠান
""")

# LINK CHECK FUNCTION
def is_link(message):
    return message.text is not None and message.text.startswith("http")

# ✅ DOWNLOAD HANDLER
@bot.message_handler(func=is_link)
def download_video(message):
    url = message.text

    try:
        bot.reply_to(message, "⏳ ডাউনলোড হচ্ছে...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(id)s.%(ext)s',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_name)

    except Exception as e:
        print(e)

# RUN BOT
bot.infinity_polling()
