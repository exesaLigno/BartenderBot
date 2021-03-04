import TelegramAPI.api_helper
import accessify
import requests

class Bot:

    max_request_retries_number = 5

    def __init__(self, token):
        self.token = token
        bot_info = api_helper._makeRequest(self.token, "getMe")

        if bot_info["ok"] == True:
            print("\x1b[1;32mBot sucessfully connected to Telegram API\x1b[0m")
            self.id = bot_info["result"]["id"]
            self.name = bot_info["result"]["first_name"]
            self.username = bot_info["result"]["username"]

        else:
            print("\x1b[1;31mHere raising an exception (incorrect token)\x1b[0m")


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


    def sendMessage(self, chat_id, text, parse_mode = "MakrdownV2", entities = None,
                    disable_web_page_preview = False, disable_notification = False,
                    reply_to_message_id = None, allow_sending_without_reply = True,
                    reply_markup = None):
        result = self._makeRequest("sendMessage", chat_id = chat_id, text = text)
        return result
