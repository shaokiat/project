#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
import pickle
import datetime

# TODO:
#  + upgrade to database (sqlite for the start)
#  + stats per category, month, user (sql-like syntax?)
#  + allow for multiple users as payers
#  ? check for user expenses < 0


# Data model classes, to be replaced by the database
class Category:
	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Category {}>'.format(self.name)

class Expense:
	def __init__(self, user_id, amount):
		self.amount = amount
		self.datetime = datetime.datetime.now()
		self.user_id = user_id

	def __repr__(self):
		return '<Expense: {}: {} ({})>'.format(self.user_id, self.amount, self.datetime)

def update_expenses(bot, update, args):
	'''Allows to add a new expense. Expenses can also have a negative amount.'''
	global expenses, users
	logger.info('Update expenses command, args={}'.format(args))
	chat_id = update.message.chat_id
	user = update.message.from_user

	if len(args) < 1:
		bot.sendMessage(chat_id=chat_id, text='/spent <amount> [<amount2>] [...]')
		return

	try:
		amount = sum([float(a) for a in args])
	except ValueError:
		error_handler(bot, update, 'ValueError')
		return

	if user.id not in users:
		bot.sendMessage(chat_id=chat_id, text='Hello {}, initialized your expenses with 0.'.format(user.first_name))
		users[user.id] = user
		expenses[user.id] = []

	expenses[user.id].append(Expense(user.id, amount))

	if amount > 0:
		text = 'Added {:.2f} to your expenses.'
	else:
		text = 'Subtracted {:.2f} from your expenses.'
	bot.sendMessage(chat_id=chat_id, text=text.format(amount))

def backlog(bot, update, args):
	'''Backlog of the last n expenses.'''
	global expenses, users
	logger.info('Backlog command, args={}'.format(args))

	if len(args) > 1:
		bot.sendMessage(chat_id=chat_id, text='/log [<number_of_expenses>]')
		return

	if len(args) == 1:
		try:
			number_of_expenses = int(args[0])
		except ValueError:
			error_handler(bot, update, 'ValueError')
	else:
		number_of_expenses = 5

	# TODO:
	#  - sort all expenses by date
	#  - return last number_of_expenses

	bot.sendMessage(chat_id=update.message.chat_id, text='Not yet implemented, sorry')

def stats(bot, update):
	'''Gives a summed and per-user overview of the expenses.'''
	global expenses, users
	logger.info('Stats command')

	message = ''
	overall_sum = 0
	for user_id, user_expenses in expenses.items():
		user_sum = sum([e.amount for e in user_expenses])
		overall_sum += user_sum
		message += '{}: {:.2f}\n'.format(users[user_id].first_name, user_sum)

	message = 'Summed expenses: {:.2f}\n'.format(overall_sum) + message
	bot.sendMessage(chat_id=update.message.chat_id, text=message)

def list_categories(bot, update):
	'''Lists the currently available categories.'''
	global categories
	logger.info('List categories command')

	message = 'Categories: ' + ', '.join([c.name for c in categories])

	bot.sendMessage(chat_id=update.message.chat_id, text=message)

def add_category(bot, update, args):
	'''Add new category/categories to available categories.'''
	global categories
	logger.info('Add category command')

	if len(args) < 1:
		bot.sendMessage(chat_id=chat_id, text='/add_category <category_name> [<category2_name>] [...]')
		return

	category_names = [c.name for c in categories]
	added = []
	not_added = []
	for category_name in args:
		if category_name not in category_names:
			categories.append(Category(category_name))
			added.append(category_name)
		else:
			not_added.append(category_name)

	message = ''
	if added:
		message += 'Added categories: {}'.format(', '.join(added))

	if not_added:
		message += '\nAlready existing: {}'.format(', '.join(not_added))

	bot.sendMessage(chat_id=update.message.chat_id, text=message)

def error_handler(bot, update, error):
	bot.sendMessage('Syntax error or sth')
	logger.warn('Update "{}" caused error "{}"'.format(update, error))

def dump_to_file(expenses, users):
	pickle.dump(expenses, open('expenses.p', 'wb'))
	pickle.dump(users, open('users.p', 'wb'))
	logger.info('Dumped expenses and users to file.')

def main():
	global expenses, users, categories
	try:
		expenses = pickle.load(open('expenses.p', 'rb')) # user_id:expenses
	except FileNotFoundError:
		logger.warn('Expenses file not found! Starting with empty one.')
		expenses = {}

	try:
		users = pickle.load(open('users.p', 'rb')) # user_id:user
	except FileNotFoundError:
		logger.warn('Users file not found! Starting with empty one.')
		users = {}

	categories = [Category('grocery'), Category('car'), Category('hobby')]

	with open('token.ini', 'r') as file:
		BOT_TOKEN = file.read()

	# Create the bot
	updater = Updater(token=BOT_TOKEN, use_context=True)

	updater.dispatcher.add_handler(CommandHandler('spent', update_expenses, pass_args=True))
	updater.dispatcher.add_handler(CommandHandler('stats', stats))
	updater.dispatcher.add_handler(CommandHandler('log', backlog, pass_args=True))
	updater.dispatcher.add_handler(CommandHandler('categories', list_categories))
	updater.dispatcher.add_handler(CommandHandler('add_category', add_category, pass_args=True))
	updater.dispatcher.add_error_handler(error_handler)

	updater.start_polling()
	logger.info('Updater started polling...')
	updater.idle()

	dump_to_file(expenses, users)

if __name__ == '__main__':
	main()