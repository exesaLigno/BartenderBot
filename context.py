import TelegramAPI

class Context:

    database = {}

    def __init__(self, message):
        self.chat_id = message.chat_id
        self.message_id = message.message_id
        self.context = ""
        if self.chat_id not in self.database:
            self.database[self.chat_id] = []
        self.database[self.chat_id].append(self)

    @classmethod
    def getContext(cls, message):
        if message.chat_id in cls.database:
            for message_context in cls.database[message.chat_id]:
                if message_context.message_id == message.message_id:
                    return message_context

        return None

    def back(self):
        context = self.context.split("/")
        context.pop()
        if (len(context) == 1):
            return
        self.context = "/".join(context)

    def close(self):
        self.database[self.chat_id].remove(self)

    def getPageInfo(self):
        context = self.context.split("/")
        return context.pop()

    def addContext(self, context):
        self.context += "/" + context

    def replaceContext(self, new_context):
        context = self.context.split("/")
        context.pop()
        context.append(new_context)
        self.context = "/".join(context)
