import os
import requests
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7454180235
USERS_FILE = "users.txt"


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

    await update.message.reply_text(f"""
👋 আসসালামু আলাইকুম {username} স্যার!

📥 Download supported:
✔ TikTok
✔ Facebook
✔ Instagram

🔗 শুধু ভিডিও লিংক পাঠান

👨‍💻 তৈরি করেছে: @JAHIDVAI12
""")


# 👥 Users
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not os.path.exists(USERS_FILE):
        count = 0
    else:
        with open(USERS_FILE, "r") as f:
            count = len(f.readlines())

    await update.message.reply_text(f"👥 Total Users: {count}")


# 🎬 Download (API)
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if ("tiktok.com" not in url and
        "facebook.com" not in url and
        "fb.watch" not in url and
        "instagram.com" not in url):
        return

    msg = await update.message.reply_text("⏳ প্রসেস হচ্ছে...")

    try:
        # 🔥 API call
        api = f"https://api.douyin.wtf/api?url={url}"
        res = requests.get(api).json()

        video_url = res.get("data", {}).get("play")

        if not video_url:
            raise Exception("No video")

        await update.message.reply_video(video_url)

    except Exception:
        await msg.edit_text("❌ ভিডিও ডাউনলোড করা যায়নি!")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("✅ Bot Running...")
app.run_polling()
