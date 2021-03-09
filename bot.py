#!/usr/bin/python3
import TelegramAPI
import sys


bot = TelegramAPI.Bot(token_file = "token.txt")

def handler(event):
    print(event)
    event.answer("Нет ты " + event.text)


bot.addMessageHandler(handler)
bot.polling()
