import telebot
import yt_dlp
import os

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# START MESSAGE
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    text = f"""👋 আসসালামু আলাইকুম {name} স্যার!

📥 আপনি এখান থেকে ডাউনলোড করতে পারবেন:
✔ TikTok
✔ Facebook Video
✔ YouTube
✔ Instagram

🔗 শুধু ভিডিও লিংক পাঠান

👨‍💻 আমাকে তৈরি করেছে: @JAHIDVAI12
"""
    bot.reply_to(message, text)

# DOWNLOAD FUNCTION
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    try:
        msg = bot.reply_to(message, "⏳ ডাউনলোড হচ্ছে...")

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': '%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        # SEND VIDEO
        with open(file_name, 'rb') as video:
            bot.send_video(message.chat.id, video)

        # DELETE FILE AFTER SEND
        os.remove(file_name)

    except Exception as e:
        bot.reply_to(message, f"❌ ডাউনলোড করা যায়নি!\n{str(e)}")

bot.infinity_polling()
