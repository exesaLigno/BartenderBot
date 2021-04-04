#!/usr/bin/python3
import TelegramAPI
import sys
import json
import time
import threading
import Bartender
from context import Context



commands_list = {
                    "start": "Начало работы с чат-ботом и показ справки",
                    "help": "Показ справки",
                    "bar": "Открывает персональный бар",
                    "settings": "Настройки чат-бота"
                }

with open("static/pages.json") as static_data:
    pages = json.loads(static_data.read())


bot = TelegramAPI.Bot(token_file = "token.txt")
bot.setCommandsList(commands_list)

bartender = Bartender.BarTender()
bartender.setPath("/home/exesa_ligno/Documents/Study/Programming/Mipt/4sem/BartenderBot")
bartender.loadReceipes()


@bot.message_handler()
def handler(message):
    if message.text.startswith("/"):
        command_processor(message)
    else:
        search_processor(message)


@bot.callback_handler()
def callback_handler(callback):

    answer = "Выполнено"

    c = Context.getContext(callback.message)

    if c == None:
        callback.answer("Кажется, произошла внутренняя ошибка, сообщение будет закрыто во избежание глобального пиздеца", show_alert = True)
        callback.message.delete()
        return

    if callback.data == "back":
        c.back()
    elif callback.data == "close":
        c.close()
        callback.message.delete()
        return
    elif callback.data == "update_shoplist":
        bar = bartender.getBar(callback.chat_id)
        context = Context.getContext(callback.message)
        cocktail_id = int(context.getPageInfo().split(":").pop())
        cocktail = bartender.getCocktail(cocktail_id)
        print("Добавляю ингредиенты в шоплист") # Shoplist not implemented in Bar class
        answer = "Недостающие ингредиенты добавлены в ваш шоплист"
    elif callback.data == "update_barlist":
        bar = bartender.getBar(callback.chat_id)
        context = Context.getContext(callback.message)
        cocktail_id = int(context.getPageInfo().split(":").pop())
        cocktail = bartender.getCocktail(cocktail_id)
        for ingredient in cocktail.ingredients:
            if ingredient not in bar.bar_list:
                bar.addIngredient(ingredient)
        answer = "Все ингредиенты добавлены в ваш бар"
    else:
        c.addContext(callback.data)

    text = getPageText(c.getPageInfo(), callback.chat_id)
    keyboard = getPageKeyboard(c.getPageInfo(), callback.chat_id)

    sended = callback.message.edit(text, reply_markup = keyboard)

    callback.answer(answer)

    #print(sended)


def command_processor(message):
    command = message.text[1::]

    text = getPageText(command, message.chat_id)
    keyboard = getPageKeyboard(command, message.chat_id)

    sended = message.answer(text, reply_markup = keyboard)

    c = Context(sended)
    c.addContext(command)

    message.delete()


def search_processor(message):
    search_results = message.answer("Окей, ищу коктейль *" + message.text + "*")

    c = Context(search_results)
    c.addContext("search:" + message.text)

    text = getPageText(c.getPageInfo(), message.chat_id)
    keyboard = getPageKeyboard(c.getPageInfo(), message.chat_id)

    search_results.edit(text, reply_markup = keyboard)

    message.delete()


def getPageText(context, id):
    if context in pages:
        return pages[context]["text"]

    elif context.startswith("search"):
        request = context.split(":").pop()
        if len(bartender.search(request)) != 0:
            return "Вот, что мне удалось найти по запросу *" + request + "*"
        else:
            return "К сожалению, по запросу *" + request + "* ничего не удалось найти"

    elif context.startswith("cocktail"):
        try:
            bar = bartender.getBar(id)
        except Exception as error:
            print(error)
            bartender.createBar(id)
            bar = bartender.getBar(id)

        cocktail_id = int(context.split(":").pop())

        text = "Вот рецепт коктейля *" + bartender.getCocktail(cocktail_id).name + "*\n\nДля приготовления понадобятся:\n"
        missing_count = 0
        for ingredient in bartender.getCocktail(cocktail_id).ingredients:
            if ingredient in bar.bar_list:
                text += "  ▣ "
            else:
                text += "  □ "
                missing_count += 1
            text += "_" + ingredient + "_\n"

        text += "\n"
        text += bartender.getCocktail(cocktail_id).receipe

        if missing_count != 0:
            text += "\n\n`Некоторых ингредиентов для этого коктейля не хватает, но вы можете добавить их в шоплист, нажав соответствующую кнопку ниже`\n"
        else:
            text += "\n\n`У вас есть все необходимое для приготовления этого рецепта!`\n"

        return text

    else:
        return "Чет не работает"


def getPageKeyboard(context, id):
    if context in pages:
        return pages[context]["keyboard"]

    elif context.startswith("search"):
        request = context.split(":").pop()
        keyboard = [[{"text": bartender.getCocktail(id).name, "callback_data": "cocktail:" + str(id)}] for id in bartender.search(request)]
        if len(keyboard) != 0:
            keyboard += [[{"text": "<<", "callback_data": "prev"}, {"text": ">>", "callback_data": "next"}]]
        keyboard += [[{"text": "Закрыть", "callback_data": "close"}]]

        return keyboard

    elif context.startswith("cocktail"):
        try:
            bar = bartender.getBar(id)
        except Exception as error:
            print(error)
            bartender.createBar(id)
            bar = bartender.getBar(id)

        cocktail_id = int(context.split(":").pop())

        missing_count = 0
        for ingredient in bartender.getCocktail(cocktail_id).ingredients:
            if ingredient not in bar.bar_list:
                missing_count += 1

        keyboard = []

        keyboard += [[{"text": "Добавить в избранное", "callback_data": "add_favourites"}]]

        if missing_count != 0:
            keyboard += [[{"text": "Добавить недостающее в шоплист", "callback_data": "update_shoplist"}],
                            [{"text": "У меня есть все ингредиенты", "callback_data": "update_barlist"}]]

        keyboard += [[{"text": "⬅️ К результатам поиска", "callback_data": "back"}]]

        return keyboard

    else:
        return [[{"text": "Закрыть", "callback_data": "close"}]]



if __name__ == "__main__":
    polling_thread = threading.Thread(target = bot.polling, daemon = True)
    polling_thread.start()

    while True:
        pass
