import accessify
import requests
import json
import TelegramAPI.message
import TelegramAPI.callback


class Bot:

    max_request_retries_number = 5

    def __init__(self, token = None, token_file = None):
        if token != None:
            self.token = token
        elif token_file != None:
            self.token = self._readToken(token_file)
        else:
            return

        bot_info = self._makeRequest("getMe")

        if bot_info["ok"] == True:
            print("\x1b[1;32mBot sucessfully connected to Telegram API\x1b[0m")
            self.id = bot_info["result"]["id"]
            self.name = bot_info["result"]["first_name"]
            self.username = bot_info["result"]["username"]

        else:
            print("\x1b[1;31mHere raising an exception (incorrect token)\x1b[0m")

        self.event_queue = []
        self.polling_offset = 0

        self.message_handler_func = None
        self.callback_handler_func = None


    @accessify.private
    @staticmethod
    def _readToken(filename):
        with open(filename, "r") as file:
            token = file.read().split("\n")[0]

        return token


    @accessify.private
    def _makeRequest(self, method, **kwargs):
        """Creating request to Telegram API from token and requred method"""

        request_string = "https://api.telegram.org/bot" + self.token + "/" + method + "?"

        for argument in kwargs:
            if kwargs[argument] != None:
                request_string += argument + "=" + str(kwargs[argument]) + "&"

        retries_number = 0

        response = {"ok": False}

        while retries_number < self.max_request_retries_number:

            retries_number += 1

            try:
                response = requests.get(request_string).json()
                break

            except Exception as error:
                print("something gone wrong:", error)
                continue

        return response


    @accessify.private
    def _getUpdates(self):
        updates = self._makeRequest("getUpdates", offset = self.polling_offset, timeout = 1)

        if updates["ok"] and len(updates["result"]) > 0:
            for update in updates["result"]:
                if "message" in update:
                    self.event_queue += [TelegramAPI.message.Message(self, update["message"])]
                elif "callback_query" in update:
                    self.event_queue += [TelegramAPI.callback.Callback(self, update["callback_query"])]
            #self.event_queue += updates["result"]
            self.polling_offset = updates["result"][-1]["update_id"] + 1


    @accessify.private
    def _polling(self):
        while True:
            self._getUpdates()

            while len(self.event_queue) != 0:
                event = self.event_queue.pop(0) # Need to parallel
                if type(event) == TelegramAPI.message.Message:
                    self.message_handler_func(event)
                elif type(event) == TelegramAPI.callback.Callback:
                    self.callback_handler_func(event)


    def polling(self):
        self._polling()


    def setCommandsList(self, commands):
        commands_list = []
        for command, description in commands.items():
            commands_list += [{"command": command, "description": description}]

        return self._makeRequest("setMyCommands", commands = json.dumps(commands_list))



    def sendMessage(self, chat_id, text = None, photo = None, parse_mode = "MarkdownV2",
                    entities = None, disable_web_page_preview = False,
                    disable_notification = False, reply_to_message_id = None,
                    allow_sending_without_reply = True, reply_markup = None):

        if reply_markup != None:
            reply_markup = json.dumps({"inline_keyboard" : reply_markup}, ensure_ascii = False)

        if photo == None:
            result = self._makeRequest("sendMessage", chat_id = chat_id, text = text,
                        parse_mode = parse_mode, entities = entities, disable_web_page_preview = disable_web_page_preview,
                        disable_notification = disable_notification, reply_to_message_id = reply_to_message_id,
                        allow_sending_without_reply = allow_sending_without_reply, reply_markup = reply_markup)
        else:
            result = self._makeRequest("sendPhoto", chat_id = chat_id, photo = photo, caption = text,
                        parse_mode = parse_mode, caption_entities = entities,
                        disable_notification = disable_notification, reply_to_message_id = reply_to_message_id,
                        allow_sending_without_reply = allow_sending_without_reply, reply_markup = reply_markup)

        if result["ok"]:
            result = TelegramAPI.message.Message(self, result["result"])
        return result


    def editMessage(self, chat_id, message_id, text, reply_markup = None):

        if reply_markup != None:
            reply_markup = json.dumps({"inline_keyboard" : reply_markup}, ensure_ascii = False)

        result = self._makeRequest("editMessageText", chat_id = chat_id, message_id = message_id, text = text, reply_markup = reply_markup)

        if result["ok"]:
            result = TelegramAPI.message.Message(self, result["result"])
        return result


    def deleteMessage(self, chat_id, message_id):
        result = self._makeRequest("deleteMessage", chat_id = chat_id, message_id = message_id)
        if result["ok"]:
            result = result["result"]
        return result


    def answerCallbackQuery(self, callback_id, text, show_alert = False):
        result = self._makeRequest("answerCallbackQuery", callback_query_id = callback_id, text = text, show_alert = show_alert)
        if result["ok"]:
            result = result["result"]
        return result


    @staticmethod
    def protectSymbols(text):
        new_text = ""
        for symbol in text:
            if symbol in "*_~-`[]()":
                new_text += "\\"
            new_text += symbol
        return new_text


    def verifyMarkdown(text):
        return True


    def message_handler(self):
        def decorator(message_handler):
            self.message_handler_func = message_handler
            return message_handler

        return decorator


    def callback_handler(self):
        def decorator(callback_handler):
            self.callback_handler_func = callback_handler
            return callback_handler

        return decorator
