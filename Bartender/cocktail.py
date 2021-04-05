import json

class Cocktail:

    def __init__(self, file_name = None):
        if file_name == None:
            pass
        else:
            self.cocktail_file_name = file_name
            self.__dict__ = self.loadReceipe()

    def loadReceipe(self):
        cocktail_dict = {}
        with open(self.cocktail_file_name, "r") as cocktail_file:
            cocktail = cocktail_file.read()
            cocktail_dict = json.loads(cocktail)
        return cocktail_dict
