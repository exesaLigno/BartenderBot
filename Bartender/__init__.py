import accessify
import json
import string
import os
from difflib import SequenceMatcher
import Bartender.cocktail
import Bartender.bar

class BarTender:

    def __init__(self):
        self.bars_dict = {}


    def setPath(self, path):
        self.fakeroot_path = path

    def loadReceipes(self):
        self.receipes_list = []
        for filename in sorted(os.listdir(self.fakeroot_path + "/static/cocktails/")):
            self.receipes_list.append(Bartender.cocktail.Cocktail(self.fakeroot_path + "/static/cocktails/" + filename))


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
                cocktails_list += [(percent, cocktail.id)]

        cocktails_list.sort()
        cocktails_list.reverse()

        for k in range(0, len(cocktails_list)):
            cocktails_list[k] = cocktails_list[k][1]

        return cocktails_list


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
            if self.canDococktail(ingredients_list, cocktail.Ingredients):
                cocktails_id_list += [cocktail.id]

        return cocktails_id_list


    def getCocktail(self, id):
        for cocktail in self.receipes_list:

            if cocktail.id == id:
                return cocktail

        return None



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
