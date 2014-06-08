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

import os
import urllib

import webapp2
import collections
import itertools
from google.appengine.ext import ndb

import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class QueryHelper(object):
    @classmethod
    def from_name(cls, name):
        return cls.from_field("name", name)

    @classmethod
    def from_field(cls, key, value):
        try:
            return cls.query(getattr(cls, key)==value).fetch(1)[0]
        except IndexError:
            print "no value at "+value
            return None

    def __eq__(self, other):
        return self.name == other.name

# Recipe has many ingredients through the RecipeIngredient class
class Recipe(ndb.Model, QueryHelper):
    name = ndb.StringProperty(required=True)

    @classmethod
    def create(cls, **kwargs):
        recipe = cls(name=kwargs["name"]).put()
        # Now create association from ingredients
        try:
            for ingredient_amount in kwargs["ingredients"]:
                ingredient, amount = ingredient_amount
                RecipeIngredient(recipe=recipe, ingredient=ingredient.key, amount=amount).put()
        except:
            print "Exception: %s not created" % kwargs["name"]
            recipe.delete()

    def ingredients(self):
        return [(ingr.ingredient.get(), ingr.amount) for
            ingr in RecipeIngredient.query(RecipeIngredient.recipe==self.key).fetch()]

    def has_ingredients(self, ingredients, only=False):
        """docstring for has_ingredients"""
        ingr = [item.name for item, amount in self.ingredients()]
        if only and set(ingr) == set(ingredients):
            return True
        else:
            return all(x in ingr for x in ingredients)

class Ingredient(ndb.Model, QueryHelper):

    name = ndb.StringProperty(required=True)
    ingredient_type = ndb.StringProperty(required=True, choices=["alcohol", "mixer"])

    def recipes(self):
        return [ r_i.recipe.get() for r_i in RecipeIngredient.query(RecipeIngredient.ingredient==self.key).fetch() ]

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
        # get all recipes that correspond to the ingredients
        recipes = [ recipe for ingr in self.ingr_list for recipe in Ingredient.from_name(ingr).recipes() ]

        combinations = self.ingr_combinations()
        all_recipes = []
        for combo in combinations:
            # filter recipes list by ones that correspond to this combo only
            combo_recipes = [ recipe for recipe in recipes if recipe.has_ingredients(combo, True) ]
            all_recipes.extend(combo_recipes)

        names = [ recipe.name for recipe in all_recipes ]
        return list(set(names))

class RecipeIngredient(ndb.Model):
    recipe = ndb.KeyProperty(kind=Recipe, required=True)
    ingredient = ndb.KeyProperty(kind=Ingredient, required=True)
    amount = ndb.FloatProperty(required=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        liquors = Ingredient.query(Ingredient.ingredient_type =="alcohol").fetch();
        mixers = Ingredient.query(Ingredient.ingredient_type =="mixer").fetch();
        template_values = {
            'liquors': liquors,
            'mixers' : mixers,
        }
        template = JINJA_ENVIRONMENT.get_template('/drinkomatic.html')
        #self.response.write(ingredients)
        self.response.write(template.render(template_values))


##        # my_ingr are the ingredients specified by the user
##        my_ingr = ["whiskey", "vodka", "oj"]
##
##        # get all the recipes that correspond to these ingredients (some or all)
##        ingr_list = IngredientsList(my_ingr)
##        mixable_recipes = ingr_list.all_recipes()

##
##        for mr in mixable_recipes:
##            self.response.write(mr)
##            self.response.write("<br>")
##



class UpdateIngredients(webapp2.RequestHandler):
    def post(self):
        ingr_addrem = self.request.get("change");
        template = JINJA_ENVIRONMENT.get_template('/recipes.html')
        r1 = Recipe(name="Gin and Tonic")
        r2 = Recipe(name="Jack and Coke")
        r = [r1, r2]
        template_values = {'recipes': r,}
        #self.response.write("Hello")
        if(ingr_addrem ==  "Add"):
            self.response.write(template.render(template_values))
        else:
            self.response.write("Removed data")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/UpdateIngr', UpdateIngredients),
], debug=True)


##        ing = Ingredient(name="Tequila", ingredient_type="alcohol")
##        ing.put();
##        ing = Ingredient(name="Whiskey", ingredient_type="alcohol")
##        ing.put();
##        ing = Ingredient(name="Rum", ingredient_type="alcohol")
##        ing.put();
##        ing = Ingredient(name="Vodka", ingredient_type="alcohol")
##        ing.put();
##        ing = Ingredient(name="Gin", ingredient_type="alcohol")
##        ing.put();
##        ing = Ingredient(name="Orage Juice", ingredient_type="mixer")
##        ing.put();
##        ing = Ingredient(name="Coke", ingredient_type="mixer")
##        ing.put();
##        ing = Ingredient(name="Lemon Juice", ingredient_type="mixer")
##        ing.put();
##        ing = Ingredient(name="Simple Syrup", ingredient_type="mixer")
##        ing.put();
##        ing = Ingredient(name="Lime Juice", ingredient_type="mixer")
##        ing.put();
