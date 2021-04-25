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
        self.receipes_list = []


    def setPath(self, path):
        self.fakeroot_path = path


    @classmethod
    def searchEngine(cls, cocktail_name, asked_coctail_name):
        percent = 1/2*(SequenceMatcher(None, cocktail_name, asked_coctail_name).ratio() +
            SequenceMatcher(None, cocktail_name, asked_coctail_name).ratio())
        if  percent > 0.5:
            return percent
        return 0


    def search(self, asked_coctail_name):
        receipes_list = []
        for cocktail in self.receipes_list:
            percent = self.searchEngine(cocktail.name, asked_coctail_name)
            if percent > 0:
                receipes_list += [(percent, cocktail.id)]

        receipes_list.sort()
        receipes_list.reverse()

        for k in range(0, len(receipes_list)):
            receipes_list[k] = receipes_list[k][1]

        return receipes_list


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
