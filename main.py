import os
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')

# Initialize Telegram app
application = Application.builder().token(TOKEN).build()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 হ্যালো! আমি Render.com এ হোস্ট করা একটি টেলিগ্রাম বট!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    await update.message.reply_text(f"📢 আপনি লিখেছেন: {text}")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("echo", echo))

# Webhook handler (Synchronous)
@app.route('/webhook', methods=['POST'])
def webhook():
    json_data = request.get_json()  # await ছাড়াই সরাসরি JSON পড়ুন
    update = Update.de_json(json_data, application.bot)
    
    # Async টাস্ক সিঙ্ক্রোনাসলি রান করান
    application.create_task(application.process_update(update))
    
    return jsonify(success=True), 200

# Health check
@app.route('/')
def health_check():
    return "বট সচল ✅", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
