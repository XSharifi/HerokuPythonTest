import os
from flask import Flask, request, redirect
from flask_bcrypt import Bcrypt
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Dispatcher,CommandHandler, MessageHandler, Filters
from queue import Queue
from threading import Thread
TOKEN = '765185530:AAGaBUP8CiLfzPhpfni2NcUfpUnPodm7oAg'
bot = Bot(TOKEN)
update_queue = Queue()

dp = Dispatcher(bot, update_queue)

# Initialize application
app = Flask(__name__, static_folder=None)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Edit here below
def start(bot, update, args):
    telegram_user = update.message.from_user

    bot.sendMessage(update.message.chat_id, text="Hello!")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Help!")

def main():
    dp.add_handler(CommandHandler('start', start, pass_args=True))
    dp.add_handler(CommandHandler("help", help))
    
    thread = Thread(target=dp.start, name='dp')
    thread.start()

main()

@app.route('/'+TOKEN, methods=['GET', 'POST'])
def webhook():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = Update.de_json(request.get_json(force=True), bot)

        dp.process_update(update)
        update_queue.put(update)
        return "OK"

@app.route('/', methods=['GET', 'POST'])
def index():
    bot.sendMessage(update.message.chat_id, text="Index")

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.set_webhook("https://python20.herokuapp.com/"+TOKEN)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"