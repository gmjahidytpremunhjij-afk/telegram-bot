import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# 🔑 ENV TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

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

📥 Download supported:
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


# 🎬 Download function
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    # ❌ hi / hello ignore (no reply)
    if not any(x in url for x in ["tiktok.com", "facebook.com", "fb.watch", "instagram.com"]):
        return

    msg = await update.message.reply_text("⏳ প্রসেস হচ্ছে...")

    try:
        api_url = f"https://api.fastsaver.io/fetch?url={url}"

        headers = {
            "x-api-key": API_KEY
        }

        res = requests.get(api_url, headers=headers)
        data = res.json()

        if not data.get("ok"):
            await msg.edit_text("❌ ভিডিও পাওয়া যায়নি!")
            return

        video_url = data["download_url"]

        await update.message.reply_video(video_url)

    except Exception:
        await msg.edit_text("❌ ডাউনলোড failed!")


# 🚀 App
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("✅ Bot Running...")
app.run_polling()
