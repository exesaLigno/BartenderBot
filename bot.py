#!/usr/bin/python3
import TelegramAPI
import sys
import json
import time
import threading
import Bartender



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
bartender.setPath("/home/exesa_ligno/Documents/Study/Programming/Mipt/4sem/BartenderBot/")
bartender.loadReceipes()


@bot.message_handler()
def handler(event):
    if event.text.startswith("/"):
        command_processor(event)
    else:
        search_processor(event)


def parse_commands(commands):
    new_commands = []

    for action in commands.split(";"):
        cmd = action.split(":")
        if len(cmd) == 1:
            cmd = {"command": cmd[0].strip()}
        elif len(cmd) == 2:
            cmd = {"command": cmd[0].strip(), "data": cmd[1].split(",")}
            for i in range(0, len(cmd["data"])):
                cmd["data"][i] = cmd["data"][i].strip()
                try:
                    cmd["data"][i] = int(cmd["data"][i])
                except Exception:
                    pass

        new_commands.append(cmd)

    print(new_commands)
    return new_commands


@bot.callback_handler()
def callback_handler(event):
    commands_list = parse_commands(event.data)

    for command in commands_list:

        if command["command"] == "close":
            event.deleteMessage()
            event.answer("Вкладка закрыта")

        elif command["command"] == "set_page":
            text = getPageText(command["data"][0], command["data"][1::])
            keyboard = getPageKeyboard(command["data"][0], command["data"][1::])
            print(text)
            print(event.editMessage(text, reply_markup = keyboard))
            event.answer("Выполнено")

        else:
            print("Получена неподдерживаемая комманда", command)
            event.answer("Кажется, эта кнопка не работает")


def command_processor(event):
    command = event.text[1::]

    text = getPageText(command)
    keyboard = getPageKeyboard(command)

    sended = event.answer(text, reply_markup = keyboard)

    event.delete()


def search_processor(event):
    search_results = event.answer("Окей, ищу коктейль *" + event.text + "*")

    text = getPageText("search", [event.text])
    keyboard = getPageKeyboard("search", [event.text])

    search_results.edit(text, reply_markup = keyboard)

    event.delete()


def getPageText(page_name, args = None):
    if page_name in pages:
        return pages[page_name]["text"]

    elif page_name == "search":
        if len(bartender.search(args[0])) != 0:
            return "Вот, что мне удалось найти по запросу *" + args[0] + "*"
        else:
            return "К сожалению, по запросу *" + args[0] + "* ничего не удалось найти"

    elif page_name == "cocktail":
        text = "Вот рецепт коктейля *" + bartender.getCocktail(args[0]).name + "*\n\nДля приготовления понадобятся:\n"
        for ingredient in bartender.getCocktail(args[0]).ingredients:
            text += "  \- _" + ingredient + "_\n"
        text += "\n"
        text += bartender.getCocktail(args[0]).receipe
        return text

    else:
        return "Данная страница еще не работает"

def getPageKeyboard(page_name, args = None):
    if page_name in pages:
        return pages[page_name]["keyboard"]

    elif page_name == "search":
        keyboard = [[{"text": bartender.getCocktail(id).name, "callback_data": "set_page: cocktail, " + str(id) + ", search, " + args[0]}] for id in bartender.search(args[0])]
        if len(keyboard) != 0:
            keyboard += [[{"text": "<<", "callback_data": "prev"}, {"text": ">>", "callback_data": "next"}]]
        keyboard += [[{"text": "Закрыть", "callback_data": "close"}]]

        return keyboard


    elif page_name == "cocktail":
        return [[{"text": "Добавить в избранное", "callback_data": "add_priority"}],
                [{"text": "Добавить недостающее в шоплист", "callback_data": "add_shoplist"}],
                [{"text": "Назад", "callback_data": "set_page: " + args[1] + ", " + args[2]}],
                [{"text": "Закрыть", "callback_data": "close"}]]

    else:
        return [[{"text": "Закрыть", "callback_data": "close"}]]


if __name__ == "__main__":
    polling_thread = threading.Thread(target = bot.polling, daemon = True)
    polling_thread.start()

    while True:
        pass
