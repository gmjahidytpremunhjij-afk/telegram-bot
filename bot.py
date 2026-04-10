import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.username if user.username else user.first_name

    await update.message.reply_text(f"""
👋 আসসালামু আলাইকুম {name}!

✔ TikTok
✔ Facebook
✔ Instagram

🔗 শুধু ভিডিও লিংক দিন
""")


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if ("tiktok.com" not in url and
        "facebook.com" not in url and
        "fb.watch" not in url and
        "instagram.com" not in url):
        return

    msg = await update.message.reply_text("⏳ প্রসেস হচ্ছে...")

    try:
        # 🔥 API 1
        api1 = f"https://api.douyin.wtf/api?url={url}"
        r1 = requests.get(api1).json()
        video = r1.get("data", {}).get("play")

        # 🔁 fallback API 2
        if not video:
            api2 = f"https://tikwm.com/api/?url={url}"
            r2 = requests.get(api2).json()
            video = r2.get("data", {}).get("play")

        if not video:
            raise Exception("fail")

        await update.message.reply_video(video)

    except Exception:
        await msg.edit_text("❌ ভিডিও ডাউনলোড করা যায়নি!")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("✅ Bot Running...")
app.run_polling()
