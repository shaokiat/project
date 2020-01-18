from telegram.ext import CommandHandler, Updater
from telegram import ChatAction, ParseMode, Sticker, StickerSet
from datetime import datetime
import json
import os
import requests
import logging

# Initialise logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load bot token
with open('token.ini', 'r') as file:
    BOT_TOKEN = file.read()

# Create the bot
updater = Updater(token=BOT_TOKEN, use_context=True)

def start(update, context):
    print(update.message.text.partition(' ')[2])
    # print(update.message.text.partition(' ')[3])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello. This is start message.'
    )

with open('AnimatedSticker.tgs', 'rb') as file:
    f = file.read()

def sticker(update, context):
    with open('AnimatedSticker.tgs', 'rb') as f:
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=f, timeout=50).sticker

updater.dispatcher.add_handler(
    CommandHandler('start', start)
)

updater.dispatcher.add_handler(
    CommandHandler('send', sticker)
)

# Start the bot
updater.start_polling()
print('Bot started!')

# Wait for the bot to stop
updater.idle()


print('Bot stopped!')

