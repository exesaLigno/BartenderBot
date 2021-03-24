#!/usr/bin/python3
import TelegramAPI
import sys


bot = TelegramAPI.Bot(token_file = "token.txt")


@bot.message_handler()
def handler(event):
    print(event)
    event.answer("Нет ты " + event.text.lower())

@bot.callback_handler()
def chandler(event):
    print(event)
    event.answerMessage("ну нажал и нажал, че бухтеть")
    event.answer("ебать прикол", show_alert = True)


bot.polling()
