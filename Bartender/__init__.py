import accessify
import json

class Bartender:

    def __init__(self, name_file_recipes):
        self.file_receipes = open(name_file_recipes, "r")
        self.receipes = self.file_receipes.read()
        self.receipes_dict = json.loads(self.receipes)

    def getIngredients(self, coctail_name):
        return self.receipes_dict[coctail_name]

    def addCoctail(self, coctail_name, receipe):
        self.receipes_dict[coctail_name] = receipe


    def getShoplist(self, coctail_names):

        coctail_names_list = []
        if type(coctail_names) == str:
            coctail_names = coctail_names.lower
            coctail_names_list = coctail_names.split(',')

        #разделяю, обрезаю с конца и начала слова пробелы

        shoplist = []
        for elem in coctail_names_list:
            shoplist += self.receipes_dict[elem]

        shoplist_set = set(shoplist)
        shoplist = list(shoplist_set)

        return shoplist


#TODO выдает рецепты по названию коктейлей,
# по списку ингридиентов дает всевозможные коктейли
# по набору коктейлей выдает список ингридиент
