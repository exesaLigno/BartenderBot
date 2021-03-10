#!/usr/bin/python3
import TelegramAPI
import sys


bot = TelegramAPI.Bot(token_file = "token.txt")


@bot.handler()
def handler(event):
    print(event)
    event.answer("Нет ты " + event.text.lower())


bot.polling()
