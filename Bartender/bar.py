import accessify
import json

import sqlite3
DB_PATH = "/home/ouvt02/proga/BartenderBot/database/db_bars.s3db"


class Bar:

    def __init__(self, id):
        self.id = id
        self.bar_list = []
        self.shoplist = []
        self.favourites_list = []


    @classmethod
    def createDataBase(cls):
         with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS bar(id INTEGER, bar_list STRING, shoplist STRING, favourites_list STRING)")
            conn.commit()

    def loadBar(self):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT bar_list, shoplist, favourites_list FROM bar WHERE id = {self.id}")
            if (len(cur.fetchall()) == 0):
                return
            cur.execute(f"SELECT bar_list, shoplist, favourites_list FROM bar WHERE id = {self.id}")
            bar_list, shoplist, favourites_list = map(str, cur.fetchone())

            bar_list = bar_list.split(",")
            shoplist = shoplist.split(",")
            favourites_list = list(map(int, (favourites_list.split(","))))

            tmp_dict = {"id" : self.id, "bar_list" : bar_list, "shoplist" : shoplist, "favourites_list" : favourites_list}

            object_correct = True

            bar_fields = {"id" : 0, "bar_list" : [], "shoplist" : [], "favourites_list" : []}
            for field in bar_fields:
                if field not in tmp_dict:
                    tmp_dict[field] = bar_fields[field]
                    object_correct = False

            self.__dict__ = tmp_dict
            self.id = int(self.id)

            if not object_correct:
                self.dumpBar()


    def dumpBar(self):
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            bar_list = ",".join(self.bar_list)
            shoplist = ",".join(self.shoplist)
            favourites_list = ",".join(list(map(str, self.favourites_list)))

            cur.execute(f"SELECT bar_list, shoplist, favourites_list FROM bar WHERE id = {self.id}")
            if (len(cur.fetchall()) != 0):
                cur.execute(f"UPDATE bar SET id = '{self.id}', bar_list = '{bar_list}', shoplist = '{shoplist}', favourites_list = '{str(favourites_list)}' WHERE id = '{self.id}'")
            else:
                cur.execute(f"INSERT INTO bar VALUES ('{self.id}', '{bar_list}', '{shoplist}', '{favourites_list}')")
            conn.commit()



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