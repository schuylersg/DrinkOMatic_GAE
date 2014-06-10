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

from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        liquors = Ingredient.liquors()
        mixers = Ingredient.mixers()
        template_values = {
            'liquors': liquors,
            'mixers' : mixers,
        }
        template = JINJA_ENVIRONMENT.get_template('/drinkomatic.html')
        #self.response.write(ingredients)
        self.response.write(template.render(template_values))

class UpdateIngredients(webapp2.RequestHandler):
    def post(self):
        menu_name = self.request.get("menuname")
        ingr_name = self.request.get("ingr")
        ingr_addrem = self.request.get("change")

        ingr_key = Ingredient.query(Ingredient.name==ingr_name).fetch(keys_only=True)[0]
        #ingr = ingr_key.get();

        menu_key = 0;

        if(ingr_addrem == "Add"):
            Menu.add_item(menu_name, ingr_key.get().ingredient_type, ingr_key)
        elif(ingr_addrem == "Rem"):
            Menu.remove_item(menu_name, ingr.get().ingredient_type, ingr)


        template = JINJA_ENVIRONMENT.get_template('/recipes.html')

        menu = Menu.from_name(menu_name)
        print menu.name;
        liquors = ndb.get_multi([ndb.Key(Ingredient, k) for k in menu.liquor])
        mixers = Ingredient.mixers()
        r1 = Recipe(name="Gin and Tonic")
        r2 = Recipe(name="Jack and Coke")
        r = [r1, r2]
        template_values = {
            'liquors': liquors,
            'mixers' : mixers,
            'recipes': r,
        }

        self.response.write(template.render(template_values))
        #self.response.write("Hello")
##        if(ingr_addrem ==  "Add"):
##            self.response.write(template.render(template_values))
##        else:
##            self.response.write("Removed data")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/UpdateIngr', UpdateIngredients),
], debug=True)


##        ing = Ingredient(name="Tequila", ingredient_type="liquor")
##        ing.put();
##        ing = Ingredient(name="Whiskey", ingredient_type="liquor")
##        ing.put();
##        ing = Ingredient(name="Rum", ingredient_type="liquor")
##        ing.put();
##        ing = Ingredient(name="Vodka", ingredient_type="liquor")
##        ing.put();
##        ing = Ingredient(name="Gin", ingredient_type="liquor")
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
