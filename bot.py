#!/usr/bin/python3
import TelegramAPI
import sys


commands_list = {
                    "start": "Начало работы с чат-ботом и показ справки",
                    "help": "Показ справки",
                    "bar": "Открывает персональный бар",
                    "settings": "Настройки чат-бота"
                }

static = 


bot = TelegramAPI.Bot(token_file = "token.txt")
bot.setCommandsList(commands_list)


@bot.message_handler()
def handler(event):
    if event.text.startswith("/"):
        command_processor(event)
    else:
        search_processor(event)


@bot.callback_handler()
def chandler(event):
    actions = event.data.split(";")

    actions_dict = {}

    for action in actions:
        key, value = action.split(":")
        actions_dict[key.strip()] = value.strip()

    if "page" in actions_dict:
        text = getPageText(actions_dict["page"])
        keyboard = getPageKeyboard(actions_dict["page"])

        result = event.editMessage(text, reply_markup = keyboard)

        event.answer("Выполнено")


def command_processor(event):
    command = event.text[1::]

    text = getPageText(command)
    keyboard = getPageKeyboard(command)

    sended = event.answer(text, reply_markup = keyboard)


def search_processor(event):
    event.answer("Окей, ищу коктейль \"" + event.text + "\"")


def getPageText(page_name):
    if page_name == "bar":
        return "*Бар*\n\nТут срать"

    elif page_name == "my_bar":
        return "Список имеющихся у вас напитков: говно и жопа"

    elif page_name == "shoplist":
        return "Типа шоплист"

    elif page_name == "suggestions":
        return "Ваши предпочтения"

    elif page_name == "wishlist":
        return "Вот что вы хотите попробовать"

    elif page_name in ["help", "start"]:
        return "*Привет, это бот\-бармен*\n\nЧе хотел, я еще не работаю, но можешь написать /bar"

    elif page_name == "settings":
        return "*Настройки ебать*\n\nТоже не работают"

def getPageKeyboard(page_name):
    if page_name == "bar":
        return [[{"text": "Мой бар", "callback_data": "page: my_bar"}, {"text": "Шоплист", "callback_data": "page: shoplist"}],
                [{"text": "Предпочтения", "callback_data": "page: suggestions"}, {"text": "Список желаемого", "callback_data": "page: wishlist"}]]

    elif page_name in ["my_bar", "shoplist", "suggestions", "wishlist"]:
        return [[{"text": "Назад", "callback_data": "page: bar"}]]

    elif page_name in ["start", "help", "settings"]:
        return None


bot.polling()
