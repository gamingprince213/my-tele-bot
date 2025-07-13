import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask অ্যাপ
app = Flask(__name__)

# টেলিগ্রাম টোকেন আনুন
TOKEN = os.environ.get('TOKEN')

# অ্যাসিঙ্ক্রোনাস ইভেন্ট লুপ তৈরি করুন
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# টেলিগ্রাম অ্যাপ্লিকেশন তৈরি করুন
application = Application.builder().token(TOKEN).build()

# 📌 Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 হ্যালো! আমি Render.com এ হোস্ট করা একটি টেলিগ্রাম বট!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    await update.message.reply_text(f"📢 আপনি লিখেছেন: {text}")

# হ্যান্ডলার রেজিস্টার করুন
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("echo", echo))

# 📌 Webhook রাউট
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json()
        update = Update.de_json(json_data, application.bot)
        loop.create_task(application.process_update(update))  # ✅ Non-blocking async task
        return jsonify(success=True), 200
    except Exception as e:
        app.logger.error(f"Error processing update: {str(e)}")
        return jsonify(error=str(e)), 500

# ✅ Health check route
@app.route('/')
def home():
    return "বট সচল ✅", 200

# 📌 অ্যাপ চালু করুন
if __name__ == '__main__':
    async def run_bot():
        await application.initialize()
        await application.start()
        print("✅ Bot initialized and started!")

    loop.run_until_complete(run_bot())

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
