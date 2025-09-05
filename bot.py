import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào! Gửi /ip <địa chỉ IP> để tra cứu IP hoặc /track <link> để kiểm tra link.")

async def check_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập IP. Ví dụ: /ip 8.8.8.8")
        return

    ip = context.args[0]
    response = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719").json()

    if response["status"] == "success":
        message = (
            f"🌍 IP: {response['query']}\n"
            f"🌐 Quốc gia: {response['country']} - {response['regionName']}\n"
            f"🏙 Thành phố: {response['city']}\n"
            f"📡 ISP: {response['isp']}\n"
            f"🛰 Org: {response['org']}\n"
            f"📍 Vĩ độ: {response['lat']}, Kinh độ: {response['lon']}"
        )
    else:
        message = "Không thể tra cứu IP này."

    await update.message.reply_text(message)

async def track_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập link. Ví dụ: /track https://example.com")
        return

    url = context.args[0]
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        message = f"🔗 Link gốc: {url}\n"
        message += f"🚀 Redirect đến: {r.url}\n"
        message += f"📄 Content-Type: {r.headers.get('Content-Type')}\n"
        message += f"🔍 Server: {r.headers.get('Server')}\n"
    except Exception as e:
        message = f"❌ Không thể kiểm tra link: {e}"

    await update.message.reply_text(message)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ip", check_ip))
    app.add_handler(CommandHandler("track", track_link))

    print("Bot is running...")
    app.run_polling()
