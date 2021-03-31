import accessify
import json
import string
import os
from difflib import SequenceMatcher
import Bartender.cocktail
import Bartender.bar

class BarTender:

    latest_id = 0;

    def __init__(self):
        self.bar_dict = {}


    def setPath(self, path):
        self.fakeroot_path = path

    def loadReceipes(self):
        self.latest_id = 0
        self.receipes_list = []
        for filename in os.listdir(self.fakeroot_path + "/static/cocktails/"):
            self.receipes_list.append(Bartender.cocktail.Cocktail(self.fakeroot_path + "/static/cocktails/" + filename))
            self.latest_id += 1


    def dumpReceipes(self):
        for cocktail in self.receipes_list:
            with open(self.fakeroot_path + "/static/cocktails/" + str(cocktail.id) +
                        ".json", "w") as file_receipe:
                self.latest_id += 1
                file_receipe.write(json.dumps(cocktail.__dict__, indent = 4,
                                                ensure_ascii = False))


    def getCocktailIngredients(self, cocktail_name):
        for cocktail in self.receipes_list:
            if cocktail.name == cocktail_name:
                return cocktail.Ingredients
        return None


    @classmethod
    def searchEngine(cls, cocktail_name, asked_coctail_name):
        percent = 1/2*(SequenceMatcher(None, cocktail_name, asked_coctail_name).ratio() +
            SequenceMatcher(None, cocktail_name, asked_coctail_name).ratio())
        if  percent > 0.5:
            return percent
        return 0

    def search(self, asked_coctail_name):
        cocktails_list = []
        for cocktail in self.receipes_list:
            percent = self.searchEngine(cocktail.name, asked_coctail_name)
            if percent > 0:
                cocktails_list += [(percent, cocktail.name)]

        cocktails_list.sort()
        cocktails_list.reverse()

        for k in range(0, len(cocktails_list)):
            cocktails_list[k] = cocktails_list[k][1]

        return cocktails_list

    @classmethod
    def getElemClassCocktail(cls, cocktail_dict):

        cocktail = Bartender.cocktail.Cocktail()
        cocktail.__dict__ = cocktail_dict

        return cocktail


    def addCocktail(self, cocktail_name, ingredients, receipe = "null", sweetness = "null",
                    strength = "null", prettiness = "null", estime = "null"):

        self.loadReceipes()
        self.latest_id += 1
        ingredients_list = []
        if type(ingredients) == str:
            ingredients = ingredients.lower()
            ingredients_list = ingredients.split(',')

        elif type(ingredients) == list:
            ingredients_list = ingredients

        else:
            print("Unsupported type")

        self.receipes_list += [self.getElemClassCocktail({"id": self.latest_id, "name": cocktail_name, "Ingredients": ingredients_list,
                                "Receipe": receipe, "Sweetness": sweetness, "Strength": strength,
                                "Prettiness": prettiness, "Estime": estime})]


        self.dumpReceipes()


    def getShoplist(self, cocktail_names):

        cocktail_names_list = []

        if type(cocktail_names) == str:
            cocktail_names_list = cocktail_names.split(',')

        elif type(cocktail_names) == list:
            cocktail_names_list = cocktail_names

        else:
            print("Unsupported type")

        for i in range(0, len(cocktail_names_list)):
            cocktail_names_list[i] = cocktail_names_list[i].strip()

        shoplist = []

        for elem in cocktail_names_list:
            for cocktail in self.receipes_list:
                if elem == cocktail.name:
                    shoplist += cocktail.Ingredients

        shoplist_set = set(shoplist)
        shoplist = list(shoplist_set)

        return shoplist

    @staticmethod
    def canDococktail(ingredients_list, cocktail_ingredients):

        ingredients_counter = 0

        for ingredient in cocktail_ingredients:
            if ingredient in ingredients_list:
                ingredients_counter += 1
            else:
                return False

        if ingredients_counter == len(cocktail_ingredients):
            return True

    def getCocktails(self, ingredients):

        ingredients_list = []
        cocktails_list = []

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
            if self.canDococktail(ingredients_list, cocktail.Ingredients):
                cocktails_list += [cocktail.name]

        return cocktails_list



    def createBar(self, id):
        new_bar = Bartender.bar.Bar(id, self.fakeroot_path)
        self.bar_dict[id] = new_bar


    def getBar(self, id):
        return self.bar_dict[id]

    def addIngrToBar(self, id, ingredient):
        self.bar_dict[id].addIngredient(ingredient)
