import accessify
import json


class Bar:

    bars_dir_location = None

    def __init__(self, id):
        self.id = id
        self.bar_list = []
        self.shoplist = []
        self.favourites_list = []



    @classmethod
    def setBarsDirLocation(cls, path):
        cls.bars_dir_location = path



    def loadBar(self):
        name_bar_file = str(self.id) + ".json"
        with open(self.bars_dir_location + name_bar_file, "r") as bar_file:
            self.__dict__ = json.loads(bar_file.read())
            self.id = int(self.id)

    def dumpBar(self):
        name_bar_file = str(self.id) + ".json"
        with open(self.bars_dir_location + name_bar_file, "w") as bar_file:
            bar_file.write(json.dumps(self.__dict__, indent = 4, ensure_ascii = False))



    def addIngredientsToBar(self, ingredients):
        self.bar_list += ingredients
        self.dumpBar()

    def addIngredientsToShoplist(self, ingredients):
        self.shoplist += ingredients
        self.dumpBar()

    def addMissingToBar(self, cocktail):
        for ingredient in cocktail.ingredients:
            if ingredient not in self.bar_list:
                self.bar_list.append(ingredient)
                if ingredient in self.shoplist:
                    self.shoplist.remove(ingredient)
        self.dumpBar()

    def addMissingToShoplist(self, cocktail):
        for ingredient in cocktail.ingredients:
            if ingredient not in self.shoplist and ingredient not in self.bar_list:
                self.shoplist.append(ingredient)
        self.dumpBar()

    def eraseShoplist(self):
        self.shoplist = []
        self.dumpBar()

    def moveShoplistToBar(self):
        self.bar_list += self.shoplist
        self.shoplist = []
        self.dumpBar()
