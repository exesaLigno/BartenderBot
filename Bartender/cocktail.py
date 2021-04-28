import json

class Cocktail:

    def __init__(self, id):
        self.id = id

    @classmethod
    def setCocktailsDirLocation(cls, path):
        cls.cocktails_dir_location = path

    def loadCocktail(self):
        name_cocktail_file = str(self.id) + ".json"
        with open(self.cocktails_dir_location + name_cocktail_file, "r") as cocktail_file:
            self.__dict__ = json.loads(cocktail_file.read())
            self.id = int(self.id)

    def dumpCocktail(self):
        name_cocktail_file = str(self.id) + ".json"
        with open(self.cocktails_dir_location + name_cocktail_file, "w") as cocktail_file:
            cocktail_file.write(json.dumps(self.__dict__, indent = 4, ensure_ascii = False))
