#!/usr/bin/python3
import TelegramAPI
import sys
import json
import time



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

        new_commands.append(cmd)

    return new_commands


@bot.callback_handler()
def callback_handler(event):
    commands_list = parse_commands(event.data)

    for command in commands_list:

        if command["command"] == "close":
            event.deleteMessage()
            event.answer("Вкладка закрыта")

        elif command["command"] == "set_page":
            text = getPageText(command["data"][0])
            keyboard = getPageKeyboard(command["data"][0])

            event.editMessage(text, reply_markup = keyboard)
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
    time.sleep(10)   # Типа ищется коктейль в базе

    keyboard = [[{"text": "Маргарита", "callback_data": "set_page: cocktail, 1, search, fuck any"}],
                [{"text": "Белый Русский", "callback_data": "set_page: cocktail, 2, search, fuck any"}],
                [{"text": "Куба Либре", "callback_data": "set_page: cocktail, 3, search, fuck any"}],
                [{"text": "Ром-Кола", "callback_data": "set_page: cocktail, 4, search, fuck any"}],
                [{"text": "Виски-Кола", "callback_data": "set_page: cocktail, 5, search, fuck any"}],
                [{"text": "Зеленая Фея", "callback_data": "set_page: cocktail, 6, search, fuck any"}],
                [{"text": "Керш", "callback_data": "set_page: cocktail, 7, search, fuck any"}],
                [{"text": "<<", "callback_data": "prev"}, {"text": ">>", "callback_data": "next"}]]

    search_results.edit("Вот список всего, что мы смогли найти по запросу *" + event.text + "*\n`Страница 1/2`", reply_markup = keyboard)

    event.delete()


def getPageText(page_name, *args):
    if page_name in pages:
        return pages[page_name]["text"]

    elif page_name == "cocktail":
        return "Типа коктейль короче"

    else:
        return "Данная страница еще не работает"

def getPageKeyboard(page_name, *args):
    if page_name in pages:
        return pages[page_name]["keyboard"]

    else:
        return [[{"text": "Закрыть", "callback_data": "close"}]]


if __name__ == "__main__":
    bot.polling()
