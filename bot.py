import os
import yt_dlp
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔑 ENV থেকে token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 👑 তোমার Admin ID
ADMIN_ID = 7454180235

# 📁 user file
USERS_FILE = "users.txt"

# 👉 user save function
def save_user(user_id):
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()

    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(str(user_id) + "\n")


# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # user save
    save_user(user.id)

    username = user.username if user.username else user.first_name

    text = f"""
👋 আসসালামু আলাইকুম {username} স্যার!

📥 আপনি এখান থেকে ডাউনলোড করতে পারবেন:
✔ TikTok
✔ Facebook Short Video

🔗 শুধু ভিডিও লিংক পাঠান

👨‍💻 আমাকে তৈরি করেছে: @JAHIDVAI12
"""
    await update.message.reply_text(text)


# 👥 Users count (admin only)
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.readlines())

    await update.message.reply_text(f"👥 Total Users: {count}")


# 🎬 Video Download
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    msg = await update.message.reply_text("⏳ ডাউনলোড হচ্ছে...")

    unique_id = str(uuid.uuid4())
    filename = f"video_{unique_id}.mp4"

    ydl_opts = {
        'outtmpl': filename,
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, 'rb') as f:
            await update.message.reply_video(f)

        os.remove(filename)

    except Exception:
        await msg.edit_text("❌ ভিডিও ডাউনলোড করা যায়নি!")


# 🚀 App Setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("✅ Bot Running...")
app.run_polling()
