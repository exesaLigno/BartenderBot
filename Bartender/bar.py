import accessify
import json
class Bar:

    def __init__(self, id, path):
        self.id = id
        self.bar_list = []
        self.fakeroot_path = path
        self.dumpBar()


    def loadBar(self):
        name_bar_file = str(self.id) + ".json"
        bar_dict = {}
        with open(self.fakeroot_path + "/database/bars/" + name_bar_file, "r") as bar_file:
            bar = bar_file.read()
            bar_dict = json.loads(bar)
        self.bar_list = bar_dict["Ingredients"]

    def addIngredient(self, ingredient):
        self.bar_list += [ingredient]
        self.dumpBar()

    def dumpBar(self):
        with open(self.fakeroot_path + "/database/bars/" + str(self.id) +
                    ".json", "w") as bar_file:
            bar_file.write(json.dumps({"id": str(self.id), "Ingredients": self.bar_list},
                                        indent = 4, ensure_ascii = False))
