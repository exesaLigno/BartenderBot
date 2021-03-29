import TelegramAPI.message

class Callback:
    def __init__(self, bot, callback_dict):
        self.bot = bot
        self.chat_id = callback_dict["from"]["id"]
        self.callback_id = callback_dict["id"]
        self.data = callback_dict["data"]
        self.message = TelegramAPI.message.Message(bot, callback_dict["message"])

    def __str__(self):
        return "\x1b[2mButton " + self.data + " pressed in chat " + str(self.chat_id) + " in message " + self.message.text + "\x1b[0m"

    def answerMessage(self, text, reply = False):
        return self.message.answer(text, reply)

    def editMessage(self, text, reply_markup = None):
        return self.message.edit(text, reply_markup = reply_markup)

    def deleteMessage(self):
        return self.message.delete()

    def answer(self, text, show_alert = False):
        return self.bot.answerCallbackQuery(self.callback_id, text, show_alert)
