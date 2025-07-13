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

# Webhook handler (Fully synchronous)
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        json_data = request.get_json()  # No await here
        update = Update.de_json(json_data, application.bot)
        
        # Run async code synchronously
        application.run_until_complete(
            application.process_update(update)
        )
        
        return jsonify(success=True), 200
    except Exception as e:
        print(f"Error processing update: {e}")
        return jsonify(error=str(e)), 500

# Health check
@app.route('/')
def home():
    return "বট সচল ✅", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
