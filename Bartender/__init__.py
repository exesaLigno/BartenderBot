import accessify
import json
import string
import os
from difflib import SequenceMatcher
import Bartender.cocktail
import Bartender.bar
import datetime
import asyncio
import threading

class BarTender:

    def __init__(self):
        self.bars_dict = {}
        self.receipes_list = []

        self.ingredients_list = []

        self.recent_requests = {}

        self.active_threads = []


    def setPath(self, path):
        self.fakeroot_path = path

    @classmethod
    def searchEngine(cls, cocktail_name, request):
        percent = 0

        for word_cocktail in cocktail_name.split():
            for word_request in request.split():
                percent = SequenceMatcher(None, word_cocktail.lower(), word_request.lower()).ratio()
                if percent > 0.6:
                    percent += SequenceMatcher(None, cocktail_name.lower(), request.lower()).ratio()
                    if percent > 0.9:
                        return percent
                else:
                    continue
        return 0

    def getIngredients(self):

        for cocktail in self.receipes_list:
            self.ingredients_list += cocktail.ingredients

        self.ingredients_list = list(set(self.ingredients_list))



    def completeRecentsDict(self, data_dict, request):

        time = datetime.datetime.now()

        if len(self.recent_requests) < 3:
            self.recent_requests[request] = {"timestamp": time, "result": data_dict}
        else:
            latest_request = {"key": None, "latest_request_time": None}
            for key in self.recent_requests:
                if latest_request["latest_request_time"] == None:
                    latest_request["latest_request_time"] = self.recent_requests[key]["timestamp"]
                    latest_request["key"] = key
                elif self.recent_requests[key]["timestamp"] < latest_request["latest_request_time"]:
                    latest_request["latest_request_time"] = self.recent_requests[key]["timestamp"]
                    latest_request["key"] = key

            del self.recent_requests[latest_request["key"]]
            self.recent_requests[request] = {"timestamp": time, "result": data_dict}



    def searchInRecents(self, request):

        if request in self.recent_requests:

            self.recent_requests[request]["timestamp"] = datetime.datetime.now()
            return self.recent_requests[request]["result"]


        return None



    def search(self, request):

        founded_in_recents = self.searchInRecents(request)
        if  founded_in_recents != None:
            return founded_in_recents

        cocktails_list = []
        ingredients_list = []

        for cocktail in self.receipes_list:
            percent = self.searchEngine(cocktail.name, request)
            if percent > 0:
                cocktails_list.append((percent, cocktail.id))
        cocktails_list.sort(reverse = True)
        #cocktails_list.reverse()
        for k in range(0, len(cocktails_list)):
            cocktails_list[k] = cocktails_list[k][1]



        for ingredient in self.ingredients_list:
            percent = self.searchEngine(ingredient, request)
            if percent > 0:
                ingredients_list.append((percent, ingredient))
        ingredients_list.sort(reverse = True)
        #ingredients_list.reverse()
        for k in range(0, len(ingredients_list)):
            ingredients_list[k] = ingredients_list[k][1]

        data_dict = {"cocktails_list": cocktails_list, "ingredients_list": ingredients_list}

        thread = threading.Thread(target = self.completeRecentsDict, args = (data_dict, request,))
        thread.start()

        for th in self.active_threads:
            print("I'm in active_threads")
            if not th.is_alive():
                th.join()
                self.active_threads.remove(th)

        self.active_threads.append(thread)

        return data_dict



    @staticmethod
    def canDoCocktail(ingredients_list, cocktail_ingredients):

        ingredients_counter = 0

        for ingredient in cocktail_ingredients:
            if ingredient in ingredients_list:
                ingredients_counter += 1
            else:
                return False

        if ingredients_counter == len(cocktail_ingredients):
            return True


    def getCocktailsByIngredients(self, ingredients):

        ingredients_list = []
        cocktails_id_list = []

        if type(ingredients) == str:
            ingredients = ingredients.lower()
            ingredients_list = ingredients.split(',')
        elif type(ingredients) == list:
            ingredients_list = ingredients

        else:
            print("Unsupported type")

        for i in range(0, len(ingredients_list)):
            ingredients_list[i] = ingredients_list[i].strip()

        for cocktail in self.receipes_list:
            if self.canDoCocktail(ingredients_list, cocktail.ingredients):
                cocktails_id_list.append(cocktail.id)

        return cocktails_id_list


    def getCocktail(self, id):
        return self.receipes_list[id]



    def loadReceipes(self):
        cocktails_dir_location = self.fakeroot_path + "/static/cocktails/"
        Bartender.cocktail.Cocktail.setCocktailsDirLocation(cocktails_dir_location)
        files = os.listdir(cocktails_dir_location)
        self.receipes_list = [None for k in range(0, len(files))]
        for filename in files:
            id = int(filename.split(".")[0])
            cocktail = Bartender.cocktail.Cocktail(id)
            cocktail.loadCocktail()
            self.receipes_list[id] = cocktail
        self.getIngredients()



    def loadBars(self):
        bars_location = self.fakeroot_path + "/database/bars/"
        Bartender.bar.Bar.setBarsDirLocation(bars_location)
        for filename in os.listdir(bars_location):
            id = int(filename.split(".")[0])
            bar = Bartender.bar.Bar(id)
            bar.loadBar()
            self.bars_dict[id] = bar


    def getBar(self, id):
        if id not in self.bars_dict:
            self.bars_dict[id] = Bartender.bar.Bar(id)

        return self.bars_dict[id]
