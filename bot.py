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
bartender.setPath("/home/exesa_ligno/Documents/Study/Programming/Mipt/4sem/BartenderBot")
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
            text = getPageText(event.chat_id, command["data"][0], command["data"][1::])
            keyboard = getPageKeyboard(event.chat_id, command["data"][0], command["data"][1::])
            print(text)
            print(event.editMessage(text, reply_markup = keyboard))
            event.answer("Выполнено")

        else:
            print("Получена неподдерживаемая комманда", command)
            event.answer("Кажется, эта кнопка не работает")


def command_processor(event):
    command = event.text[1::]

    text = getPageText(event.chat_id, command)
    keyboard = getPageKeyboard(event.chat_id, command)

    sended = event.answer(text, reply_markup = keyboard)

    event.delete()


def search_processor(event):
    search_results = event.answer("Окей, ищу коктейль *" + event.text + "*")

    text = getPageText(event.chat_id, "search", [event.text])
    keyboard = getPageKeyboard(event.chat_id, "search", [event.text])

    search_results.edit(text, reply_markup = keyboard)

    event.delete()


def getPageText(user_id, page_name, args = None):
    if page_name in pages:
        return pages[page_name]["text"]

    elif page_name == "search":
        if len(bartender.search(args[0])) != 0:
            return "Вот, что мне удалось найти по запросу *" + args[0] + "*"
        else:
            return "К сожалению, по запросу *" + args[0] + "* ничего не удалось найти"

    elif page_name == "cocktail":
        try:
            bar = bartender.getBar(user_id)
        except Exception as error:
            print(error)
            bartender.createBar(user_id)
            bar = bartender.getBar(user_id)

        text = "Вот рецепт коктейля *" + bartender.getCocktail(args[0]).name + "*\n\nДля приготовления понадобятся:\n"
        missing_count = 0
        for ingredient in bartender.getCocktail(args[0]).ingredients:
            if ingredient in bar.bar_list or ingredient in ["Лёд", "Виски", "Кола", "Текила"]:  # Hard comparing added just for demonstration
                text += "  ☒ "
            else:
                text += "  ☐ "
                missing_count += 1
            text += "_" + ingredient + "_\n"

        text += "\n"
        text += bartender.getCocktail(args[0]).receipe

        if missing_count != 0:
            text += "\n\n`Некоторых ингредиентов для этого коктейля не хватает, но вы можете добавить их в шоплист, нажав соответствующую кнопку ниже`\n"
        else:
            text += "\n\n`У вас есть все необходимое для приготовления этого рецепта!`\n"

        return text

    else:
        return "Данная страница еще не работает"

def getPageKeyboard(user_id, page_name, args = None):
    if page_name in pages:
        return pages[page_name]["keyboard"]

    elif page_name == "search":
        keyboard = [[{"text": bartender.getCocktail(id).name, "callback_data": "set_page: cocktail, " + str(id) + ", search, " + args[0]}] for id in bartender.search(args[0])]
        if len(keyboard) != 0:
            keyboard += [[{"text": "<<", "callback_data": "prev"}, {"text": ">>", "callback_data": "next"}]]
        keyboard += [[{"text": "Закрыть", "callback_data": "close"}]]

        return keyboard


    elif page_name == "cocktail":
        try:
            bar = bartender.getBar(user_id)
        except Exception as error:
            print(error)
            bartender.createBar(user_id)
            bar = bartender.getBar(user_id)

        missing_ingredients = []
        for ingredient in bartender.getCocktail(args[0]).ingredients:
            if ingredient not in bar.bar_list and ingredient not in ["Лёд", "Виски", "Кола", "Текила"]:  # Hard comparing added just for demonstration
                missing_ingredients += [ingredient]

        keyboard = []

        keyboard += [[{"text": "Добавить в избранное", "callback_data": "add_priority"}]]

        if len(missing_ingredients) != 0:
            print(missing_ingredients)
            adding_ingredients = ", ".join(missing_ingredients)
            adding_ingredients = "test, test, test, test, test, test, test, test, test, test"
            print(adding_ingredients)
            keyboard += [[{"text": "Добавить недостающее в шоплист", "callback_data": "add_shoplist: " + adding_ingredients}]]

        keyboard += [[{"text": "Назад", "callback_data": "set_page: " + args[1] + ", " + args[2]}]]
        keyboard += [[{"text": "Закрыть", "callback_data": "close"}]]

        return keyboard

    else:
        return [[{"text": "Закрыть", "callback_data": "close"}]]


if __name__ == "__main__":
    polling_thread = threading.Thread(target = bot.polling, daemon = True)
    polling_thread.start()

    while True:
        pass
