import telebot
import yt_dlp

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

# Start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    text = f"""👋 আসসালামু আলাইকুম {name} স্যার!

📥 আপনি এখান থেকে ডাউনলোড করতে পারবেন:
✔ TikTok
✔ Facebook Short Video
✔ YouTube
✔ Instagram

🔗 শুধু ভিডিও লিংক পাঠান

👨‍💻 আমাকে তৈরি করেছে: @JAHIDVAI12
"""
    bot.reply_to(message, text)

# Handle links
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    try:
        bot.reply_to(message, "⏳ ডাউনলোড হচ্ছে...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        video = open(file_name, 'rb')
        bot.send_video(message.chat.id, video)

    except Exception as e:
        bot.reply_to(message, "❌ ডাউনলোড করা যায়নি! অন্য লিংক দিন।")

bot.polling()
