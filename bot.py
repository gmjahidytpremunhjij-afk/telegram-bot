import os
import yt_dlp
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔑 ENV token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 👑 Admin ID
ADMIN_ID = 7454180235

# 📁 user file
USERS_FILE = "users.txt"


# 👉 user save
def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")


# ✅ Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)

    username = user.username if user.username else user.first_name

    text = f"""
👋 আসসালামু আলাইকুম {username} স্যার!

📥 আপনি এখান থেকে ডাউনলোড করতে পারবেন:
✔ TikTok
✔ Facebook
✔ Instagram

🔗 শুধু ভিডিও লিংক পাঠান

👨‍💻 তৈরি করেছে: @JAHIDVAI12
"""
    await update.message.reply_text(text)


# 👥 User count (admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.readlines())

    await update.message.reply_text(f"👥 Total Users: {count}")


# 🎬 Download function (FINAL CLEAN)
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip().lower()

    # ✅ Only allow valid links
    if not any(x in url for x in ["tiktok.com", "facebook.com", "fb.watch", "instagram.com"]):
        return  # ❌ ignore hi/hello বা random text

    msg = await update.message.reply_text("⏳ প্রসেস হচ্ছে...")

    unique_id = str(uuid.uuid4())
    filename = f"video_{unique_id}.%(ext)s"

    ydl_opts = {
        'outtmpl': filename,
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    try:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)
        except Exception:
            # 🔥 fallback
            ydl_opts['format'] = 'best'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)

        if not file_name.endswith(".mp4"):
            file_name = file_name.rsplit(".", 1)[0] + ".mp4"

        with open(file_name, 'rb') as f:
            await update.message.reply_video(f)

        os.remove(file_name)

    except Exception:
        await msg.edit_text("❌ ভিডিও ডাউনলোড করা যায়নি!")


# 🚀 App
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("✅ Bot Running...")
app.run_polling()
