import accessify
import json
import string

class Bartender:

    def __init__(self):
        self.receipes_dict = {}
        self.loadReceipes("menu.json")

    def loadReceipes(self, name_file_recipes):
        with open(name_file_recipes, "r") as file_receipes:
            receipes = file_receipes.read()
            self.receipes_dict = json.loads(receipes)

    def dumpReceipes(self, name_file_recipes):
        with open(name_file_recipes, "w") as file_receipes:
            file_receipes.write(json.dumps(self.receipes_dict, indent = 4,
                                            ensure_ascii = False))


    def getCocktailIngredients(self, cocktail_name):
        return self.receipes_dict[cocktail_name]


    def addCocktail(self, cocktail_name, receipe):
        self.receipes_dict[cocktail_name] = receipe
        self.dumpReceipes("menu.json")


    def getShoplist(self, cocktail_names):

        cocktail_names_list = []

        if type(cocktail_names) == str:
            cocktail_names = cocktail_names.lower()
            cocktail_names_list = cocktail_names.split(',')

        elif type(cocktail_names) == list:
            cocktail_names_list = cocktail_names

        else:
            print("Unsupported type")

        for i in range(0, len(cocktail_names_list)):
            cocktail_names_list[i] = cocktail_names_list[i].strip()


        shoplist = []

        for elem in cocktail_names_list:
            shoplist += self.receipes_dict[elem]

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

        for cocktail in self.receipes_dict:
            if self.canDococktail(ingredients_list, self.receipes_dict[cocktail]):
                cocktails_list += [cocktail]


        return cocktails_list
