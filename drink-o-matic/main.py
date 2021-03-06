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

import webapp2
import collections
import itertools
from google.appengine.ext import ndb
import logging
import os

import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("get")
        liquors = Ingredient.liquors()
        mixers = Ingredient.mixers()
        template_values = {
            'liquors': liquors,
            'mixers' : mixers,
        }
        template = JINJA_ENVIRONMENT.get_template('/drinkomatic.html')
        self.response.write(template.render(template_values))


class UpdateIngredients(webapp2.RequestHandler):
    def post(self):
        print "post"
        ingr_addrem = self.request.get("change");
        template = JINJA_ENVIRONMENT.get_template('/recipes.html')
        liquors = Ingredient.liquors()
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

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/UpdateIngr', UpdateIngredients),
], debug=True)
