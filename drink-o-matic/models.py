from google.appengine.ext import ndb
import itertools
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

    @classmethod
    def all(cls):
        return cls.query().fetch()

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

    def __hash__(self):
        return self.key.id()

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
        """If list of ingredients are all in this recipe, return true
        if only==True, return False unless recipe contains only those ingredients"""
        ingr = [item.name for item, amount in self.ingredients()]
        if only and set(ingr) == set(ingredients):
            return True
        else:
            return all(x in ingr for x in ingredients)

class Ingredient(QueryHelper):
    name = ndb.StringProperty(required=True)
    ingredient_type = ndb.StringProperty(required=True, choices=["liquor", "mixer"])
    unique_fields = ["name"]

    def recipes(self):
        return [ r_i.recipe.get() for r_i in RecipeIngredient.query(RecipeIngredient.ingredient==self.key).fetch() ]

    @classmethod
    def liquors(cls, num=10):
        return cls.query(cls.ingredient_type=="liquor").fetch(num)

    @classmethod
    def mixers(cls, num=10):
        return cls.query(cls.ingredient_type=="mixer").fetch(num)

class IngredientsList(object):
    """User can select lists of ingredients that are owned. Use this class to manipulate those lists"""
    def __init__(self, ingr_list):
        self.ingr_list = ingr_list

    def ingr_combinations(self):
        """Returns all combinations (in the mathematical sense) of the ingredients list"""
        combinations = []
        for element in range(1, len(self.ingr_list)+1):
            combinations.append(itertools.combinations(self.ingr_list, element))
        return list(itertools.chain.from_iterable(combinations))

    def all_recipes(self):
        """get all recipes that correspond to the ingredients"""
        # xxx todo, can we filter this list so dups are removed?
        recipes = set([ recipe for ingr in self.ingr_list for recipe in Ingredient.from_name(ingr).recipes() ])
        combinations = self.ingr_combinations()
        all_recipes = []
        for combo in combinations:
            # filter recipes list by ones that correspond to this combo only
            combo_recipes = [ recipe for recipe in recipes if recipe.has_ingredients(combo, True) ]
            all_recipes.extend(combo_recipes)

        names = [ recipe.name for recipe in all_recipes ]
        # This gives us unique recipes
        return list(set(names))

class RecipeIngredient(ndb.Model):
    """Join model for Recipe and Ingredient"""
    recipe = ndb.KeyProperty(kind=Recipe, required=True)
    ingredient = ndb.KeyProperty(kind=Ingredient, required=True)
    amount = ndb.FloatProperty(required=True)

class Menu(QueryHelper):
    """Menu belogs to User"""
    name = ndb.StringProperty()
    liquor = ndb.KeyProperty(kind=Ingredient, repeated=True)
    mixer = ndb.KeyProperty(kind=Ingredient, repeated=True)
    recipe = ndb.KeyProperty(kind=Recipe, repeated=True)
    unique_fields = []

    @classmethod
    def add_item(cls, menu_name, add_type, item):
        """Add an item (liquor, mixer, or recipe) to a menu"""
        menu = cls.from_name(menu_name)
        if(menu is None):
            menu = Menu(Menu.name=menu_name)

        l = getattr(menu, add_type)
        l.append(item)
        setattr(menu, add_type, l)
        menu.put()

    @classmethod
    def remove_item(cls, menu_name, remove_type, item):
        menu = cls.from_name(menu_name)
        if(menu is None):
            return None
        l = getattr(menu, remove_type).remove(key_to_remove)
        setattr(menu, remove_type, l)

class IngredientInteraction(ndb.Model):
    """Model to keep track of the number of times two
    ingredients listed in a menu are in the same recipe"""
    menu = ndb.KeyProperty(kind=Menu, required=True)
    ingr1 = ndb.KeyProperty(kind=Ingredient, required=True)
    ingr2 = ndb.KeyProperty(kind=Ingredient, required=True)
    interactions = ndb.IntegerProperty(required=True)


class User(QueryHelper):
    """User has many Menus"""
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    menu = ndb.KeyProperty(kind=Menu, repeated=True)
    unique_fields = ["name", "email"]



