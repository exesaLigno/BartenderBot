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

        self.ingredients_list = []


    def setPath(self, path):
        self.fakeroot_path = path

    @classmethod
    def searchEngine(cls, cocktail_name, asked_coctail_name):
        percent = 0

        for word in cocktail_name.split(" "):
            percent = SequenceMatcher(None, word.lower(), asked_coctail_name.lower()).ratio()
            if percent > 0.6:
                percent += SequenceMatcher(None, cocktail_name.lower(), asked_coctail_name.lower()).ratio()
                if percent > 0.9:
                    return percent
            else:
                continue
        return 0

    def getIngredients(self):

        for cocktail in self.receipes_list:
            self.ingredients_list += cocktail.ingredients

        self.ingredients_list = list(set(self.ingredients_list))

    def search(self, asked_coctail_name):

        cocktails_list = []
        ingredients_list = []


        for cocktail in self.receipes_list:
            percent = self.searchEngine(cocktail.name, asked_coctail_name)
            if percent > 0:
                cocktails_list += [(percent, cocktail.id)]
        cocktails_list.sort()
        cocktails_list.reverse()
        for k in range(0, len(cocktails_list)):
            cocktails_list[k] = cocktails_list[k][1]



        for ingredient in self.ingredients_list:
            percent = self.searchEngine(ingredient, asked_coctail_name)
            if percent > 0:
                ingredients_list += [(percent, ingredient)]
        ingredients_list.sort()
        ingredients_list.reverse()
        for k in range(0, len(ingredients_list)):
            ingredients_list[k] = ingredients_list[k][1]

        data_dict = {"cocktails_list": cocktails_list, "ingredients_list": ingredients_list}

        return data_dict


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
