class Bar:

    def __init__(self, ingredients):
        self.ingredients_list = []

        if type(ingredients) == str:
            ingredients = ingredients.lower()
            self.ingredients_list = ingredients.split(',')

        elif type(ingredients) == list:
            self.ingredients_list = ingredients

        else:
            print("Unsupported type")

            
