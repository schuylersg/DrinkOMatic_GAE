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


from models import *



class MainHandler(webapp2.RequestHandler):
    def get(self):
##        ing = Ingredient(name="Tequila", ingredient_type="alcohol")
##        ing.put();


        ingredients = Ingredient.query().fetch(10);
        template_values = {
            'ingredients': ingredients,
        }
        template = JINJA_ENVIRONMENT.get_template('/drinkomatic.html')
        self.response.write(ingredients)
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

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
