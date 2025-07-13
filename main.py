# main.py
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')  # Get token from Render environment variables
bot = Bot(token=TOKEN)

# Simple command handlers
def start(update: Update, context):
    update.message.reply_text("Hello! I'm a Render-hosted bot! 🚀\nSend /help for commands.")

def help(update: Update, context):
    update.message.reply_text(
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/echo [text] - Repeat your text"
    )

def echo(update: Update, context):
    if context.args:
        text = ' '.join(context.args)
        update.message.reply_text(f"🔊: {text}")
    else:
        update.message.reply_text("Send text after /echo command")

# Configure dispatcher
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("echo", echo))

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return 'OK', 200

# Health check route (required by Render)
@app.route('/')
def health_check():
    return 'Bot is running!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
