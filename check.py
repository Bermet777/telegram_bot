BOT_TOKEN = "6066026423:AAGClrZrJ1izJVOQW7uWe9a8oPZczbNYBO0"

import os

import telebot

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello!How can I help you?")

bot.infinity_polling()