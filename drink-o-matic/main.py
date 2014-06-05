#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#xaouhbxxskvpejyy

import webapp2
import collections
import itertools
from google.appengine.ext import ndb

class QueryHelper(object):
    @classmethod
    def from_name(cls, name):
        return cls.from_key("name", name)

    @classmethod
    def from_key(cls, key, value):
        try:
            return cls.query(getattr(cls, key)==value).fetch(1)[0]
        except IndexError:
            print "no value at "+value
            return None


class Recipe(ndb.Model, QueryHelper):
    name = ndb.StringProperty(required=True)

    def ingredients(self):
        return [(ingr.ingr.get(), ingr.amt) for
            ingr in RecipeIngredient.query(RecipeIngredient.recipe==self.key).fetch()]

    def has_ingredients(self, ingredients, only=False):
        """docstring for has_ingredients"""
        ingr = self.ingredients()
        print ingr
        print ingredients
        if only and set(ingr) == set(ingredients):
            return True
        else:
            return all(x in ingr for x in ingredients)

class Ingredient(ndb.Model, QueryHelper):
    name = ndb.StringProperty(required=True)
    ingr_type = ndb.StringProperty(required=True, choices=["alcohol", "mixer"])

    def recipes(self):
        return [ r_i.recipe.get() for r_i in RecipeIngredient.query(RecipeIngredient.ingr==self.key).fetch() ]

class IngredientsList(object):
    def __init__(self, ingr_list):
        """docstring for __init__"""
        self.ingr_list = ingr_list

    def ingr_combinations(self):
        combinations = []
        for element in range(1, len(self.ingr_list)+1):
            combinations.append(itertools.combinations(self.ingr_list, element))
        return list(itertools.chain.from_iterable(combinations))

    def all_recipes(self):
        combinations = self.ingr_combinations()
        all_recipes = []
        for combo in combinations:
            # get all recipes for the ingredients and flatten
            _recipes = []
            for ingr in combo:

                r = Ingredient.from_name(ingr).recipes()
                _recipes.append(r)

            #_recipes = [ recipe for ingr in combo for recipe in Ingredient.from_name(ingr).recipes() ]
            _recipes = [ r for rec in _recipes for r in rec ]
            print _recipes
        # then remove any recipes that don't have all ingredients in the combo
            recipes = [ rec for rec in _recipes if rec.has_ingredients(combo) ]
        all_recipes += recipes

        return all_recipes

class RecipeIngredient(ndb.Model):
    recipe = ndb.KeyProperty(kind=Recipe, required=True)
    ingr = ndb.KeyProperty(kind=Ingredient, required=True)
    amt = ndb.FloatProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world! <br>')

        # my_ingr are the ingredients specified by the user
        my_ingr = ["Whiskey", "Vodka", "Orange Juice"]

        # get all the recipes that correspond to these ingredients (some or all)
        # first generate all the ingredient combinations
        ingr_list = IngredientsList(my_ingr)
        combos = ingr_list.ingr_combinations
        ingredients = Ingredient.query(Ingredient.name.IN(my_ingr)).fetch(3)

        # for each subset, get the recipes that correspond

        # get the keys to all the ingredients in my_ingr
        my_ingr_keys = Ingredient.query(Ingredient.name.IN(my_ingr)).fetch(100, keys_only=True)

        # Fetch all the entries from Recipe_Ingredients_Link for the ingredients
        # that the user has using the ingredient keys.
        # Only return the recipe keys.
        my_ril = Recipe_Ingredients_Link.query(Recipe_Ingredients_Link.ingr_key.IN(my_ingr_keys)).fetch(100, projection=Recipe_Ingredients_Link.rec_key)

        # Convert the results to a list of recipe keys (Is there a better way
        # to do this?)
        rec_key_list = [];
        for i in my_ril:
            rec_key_list.append(i.rec_key)

        # Count the frequency of each recipe
        rec_count = collections.Counter(rec_key_list)

        # Check if the frequency of the recipe matches that recipe's number
        # of ingredients.
        mixableRecipes = []
        for key, value in rec_count.iteritems():
            if(value == key.get().ingr_num):
                mixableRecipes.append(key.get().name)

        for mr in mixableRecipes:
            self.response.write(mr)
            self.response.write("<br>")

#        for i in my_ril:
#            self.response.write(i.rec_key.get().name)
#            self.response.write("\n")

##        r1 = Recipe(name="Jack and Coke", ingr_num=2)
##        r1_key = r1.put()
##        r2 = Recipe(name="Screwdriver", ingr_num=2)
##        r2_key = r2.put()
##        i1 = Ingredient(name="Whiskey", ingr_type="alcohol")
##        i1_key = i1.put()
##        i2 = Ingredient(name="Vodka", ingr_type="alcohol")
##        i2_key = i2.put()
##        i3 = Ingredient(name="Cola", ingr_type="mixer")
##        i3_key = i3.put()
##        i4 = Ingredient(name="Orange Juice", ingr_type="mixer")
##        i4_key = i4.put()
##        i5 = Ingredient(name="Rum (White)", ingr_key="alcohol")
##        i5_key = i5.put()
##        ril1 = Recipe_Ingredients_Link(rec_key=r1_key, ingr_key=i1_key, amt=2)
##        ril2 = Recipe_Ingredients_Link(rec_key=r1_key, ingr_key=i3_key, amt=3)
##        ril3 = Recipe_Ingredients_Link(rec_key=r2_key, ingr_key=i2_key, amt=5)
##        ril4 = Recipe_Ingredients_Link(rec_key=r2_key, ingr_key=i4_key, amt=10)
##        ril1.put()
##        ril2.put()
##        ril3.put()
##        ril4.put()





app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
