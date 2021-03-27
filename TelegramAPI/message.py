class Message:
    def __init__(self, bot, message_dict):
        self.bot = bot
        self.chat_id = message_dict["chat"]["id"]
        self.message_id = message_dict["message_id"]
        self.text = message_dict["text"]

    def __str__(self):
        return "\x1b[2mMessage " + str(self.message_id) + " from chat " + str(self.chat_id) + ":\x1b[0;1m " + self.text + "\x1b[0m"

    def answer(self, text, reply_markup = None, reply = False):
        if reply:
            result = self.bot.sendMessage(self.chat_id, text = text, reply_markup = reply_markup, reply_to_message_id = self.message_id)
        else:
            result = self.bot.sendMessage(self.chat_id, text = text, reply_markup = reply_markup)
        return result

    def edit(self, text, reply_markup = None):
        result = self.bot.editMessage(self.chat_id, self.message_id, text = text, reply_markup = reply_markup)
        return result

    def delete(self):
        result = self.bot.deleteMessage(self.chat_id, self.message_id)
        return result
