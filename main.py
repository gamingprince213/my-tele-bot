import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
bot = Bot(token=TOKEN)

# Create Application
application = Application.builder().token(TOKEN).build()

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm a Render-hosted bot! 🚀")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    await update.message.reply_text(f"🔊: {text}")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("echo", echo))

# Webhook endpoint
@app.post('/webhook')
async def webhook():
    await application.update_queue.put(
        Update.de_json(data=request.json, bot=bot)
    return '', 200

# Health check
@app.get('/')
def health_check():
    return 'Bot is running!', 200

if __name__ == '__main__':
    application.initialize()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
