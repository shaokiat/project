from telegram.ext import CommandHandler, Updater
from telegram import ChatAction, ParseMode
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

# Load persistent state
# if os.path.isfile('data.txt'):
#     with open('data.txt', 'r') as file:
#         counter_dict = json.load(file)
# else:
#     counter_dict = {}

# Add /start handler
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Hello {update.effective_message.chat.first_name}! Type /help to see all functions available.'
    )
    
def helpme(update, context):
  context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'/hello \n /hi'
    )

def exit(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'SUCKYSUCKY! BYEBYE'
    )
    
    
def lend(update, context, amount, friend):
  if friend not in friends:
    friends[friend] = -amount
  else:
    friends[friend] -= amount
  context.bot.send_message(
  	chat_id=update.effective_chat.id,
    	text=f'{update.effective_message.chat.first_name} lend {friend} {amount}!'
  )

def borrow(update, context, amount, friend):
  if friend not in friends:
    friends[friend] = amount
  else:
    friends[friend] += amount
  context.bot.send_message(
  	chat_id=update.effective_chat.id,
    	text=f'{friend} lend {update.effective_message.chat.first_name} {amount}!'
  )

def balance(update, context):
  context.bot.send_message(
  	chat_id=update.effective_chat.id,
    text=f'Constructing table....'
  )
  
  context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
  
  for friend in friends:
    if friends[friend] > 0:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{friend} owes you {friends[friend]}'
      )
    elif friends[friend] < 0:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'You owe {friend} {friends[friend]}'
      )
    else:
      context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{friend} and your debt has been cleared!'
      )
      del friends.friend


# Add /quote handler
def quote(update, context):
    # Update /quote count
    user_key = str(update.effective_chat.id)
    count = counter_dict.get(user_key, 0) + 1
    counter_dict[user_key] = count

    # Send thinking message
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hmm...let me think...BOUT U STFU!!!!'
    )

    # Send typing status
    context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    # Generate image url
    img_url = f'https://picsum.photos/seed/{datetime.now()}/500'

    # Fetch quote
    response = requests.get('https://quotable.dev/random')
    if response.status_code != 200:
        # Document not found
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Hmm, got nothing on me at the moment. Try again later.'
        )
        return
    random_quote = response.json()
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=img_url,
        caption=f'{random_quote["content"]}\n- _{random_quote["author"]}_\n\nYou have called /quote {count} time(s)!',
        parse_mode=ParseMode.MARKDOWN
    )

updater.dispatcher.add_handler(
    CommandHandler('start', start)
)

updater.dispatcher.add_handler(
    CommandHandler('quote', quote)
)

updater.dispatcher.add_handler(
    CommandHandler('help', helpme)
)

updater.dispatcher.add_handler(
    CommandHandler('exit', exit)
)

updater.dispatcher.add_handler(
    CommandHandler('Lend', lend)
)
  
updater.dispatcher.add_handler(
    CommandHandler('Borrow', borrow)
)
updater.dispatcher.add_handler(
    CallbackQueryHandler(button))


# Start the bot
updater.start_polling()
print('Bot started!')

# Wait for the bot to stop
updater.idle()

# Dump persistent state
with open('data.txt', 'w') as file:
    json.dump(counter_dict, file)

print('Bot stopped!')