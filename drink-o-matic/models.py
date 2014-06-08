from google.appengine.ext import ndb

class QueryHelper(ndb.Model):
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
        
    def validate_unique(self):
        for k in self.unique_fields:
            # self.__class__.k is the class attribute that holds the Property
            # self.k is the property value itself
            if self.query(getattr(self.__class__, k)==getattr(self, k)).count() > 0:
                return False
            else:
                next
        return True
     
    def put(self, *args, **kwargs):
        if self.validate_unique():
            super(QueryHelper, self).put(*args, **kwargs)
        else:
            raise ndb.InvalidPropertyError()
             
    def __eq__(self, other):
        return self.name == other.name

# Recipe has many ingredients through the RecipeIngredient class
class Recipe(QueryHelper, ndb.Model):
    name = ndb.StringProperty(required=True)
    unique_fields = ["name"]
    
    @classmethod
    def create(cls, **kwargs):
        recipe = cls(**kwargs).put()
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

class Ingredient(QueryHelper):
    name = ndb.StringProperty(required=True)
    ingredient_type = ndb.StringProperty(required=True, choices=["alcohol", "mixer"])
    unique_fields = ["name"]

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