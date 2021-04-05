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
bartender.loadBars()


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

    elif callback.data == "prev":
        context = c.getPageInfo().split(":")
        context[1] = str(int(context[1]) - 1)
        c.context = ""
        c.addContext(":".join(context))

    elif callback.data == "change_pages_ignore":
        callback.answer("Листать дальше некуда")
        return

    elif callback.data == "next":
        context = c.getPageInfo().split(":")
        c.context = ""
        context[1] = str(int(context[1]) + 1)
        c.addContext(":".join(context))

    elif callback.data == "update_shoplist":
        bar = bartender.getBar(callback.chat_id)
        context = Context.getContext(callback.message)
        cocktail_id = int(context.getPageInfo().split(":").pop())
        cocktail = bartender.getCocktail(cocktail_id)
        bar.addMissingToShoplist(cocktail)
        answer = "Недостающие ингредиенты добавлены в ваш шоплист"

    elif callback.data == "update_barlist":
        bar = bartender.getBar(callback.chat_id)
        context = Context.getContext(callback.message)
        cocktail_id = int(context.getPageInfo().split(":").pop())
        cocktail = bartender.getCocktail(cocktail_id)
        bar.addMissingToBar(cocktail)
        answer = "Недостающие ингредиенты добавлены в ваш бар"

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
    c.addContext("search:1:" + message.text)

    text = getPageText(c.getPageInfo(), message.chat_id)
    keyboard = getPageKeyboard(c.getPageInfo(), message.chat_id)

    search_results.edit(text, reply_markup = keyboard)

    message.delete()


def getPageText(context, id):
    if context in pages:
        return pages[context]["text"]

    elif context.startswith("search"):
        pages_count = lambda x: x // 7 + (0 if x % 7 == 0 else 1)
        splitted = context.split(":")
        request = splitted.pop()
        page = splitted.pop()
        results_count = len(bartender.search(request))
        text = ""
        if results_count != 0:
            text += "Вот, что мне удалось найти по запросу *" + request + "*"
            if pages_count(results_count) > 1:
                text += "\n`Страница {} из {}`".format(page, pages_count(results_count))
        else:
            text += "К сожалению, по запросу *" + request + "* ничего не удалось найти"

        return text

    elif context.startswith("cocktail"):
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
        pages_count = lambda x: x // 7 + (0 if x % 7 == 0 else 1)
        splitted = context.split(":")
        request = splitted.pop()
        page = int(splitted.pop())
        results = bartender.search(request)
        keyboard = [[{"text": bartender.getCocktail(id).name, "callback_data": "cocktail:" + str(id)}] for id in results[7 * (page - 1) : 7 * page]]
        if pages_count(len(results)) > 1:
            if page == 1:
                page_change_buttons = [{"text": "🚫", "callback_data": "change_pages_ignore"}, {"text": ">>", "callback_data": "next"}]
            elif page == pages_count(len(results)):
                page_change_buttons = [{"text": "<<", "callback_data": "prev"}, {"text": "🚫", "callback_data": "change_pages_ignore"}]
            else:
                page_change_buttons = [{"text": "<<", "callback_data": "prev"}, {"text": ">>", "callback_data": "next"}]
            keyboard += [page_change_buttons]
        keyboard += [[{"text": "Закрыть", "callback_data": "close"}]]

        return keyboard

    elif context.startswith("cocktail"):
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
