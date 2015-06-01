#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Schuyler
#
# Created:     31/05/2015
# Copyright:   (c) Schuyler 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from os import listdir
from lxml import html
import json

def main():
    files = listdir('cocktails/')
    listofcocktails = list()
    for f in files:
        with open('cocktails/%s' % f) as data:
            tree = html.fromstring(data.read().replace('\u00a0', " "))
            try:
                cocktail = tree.xpath('//span[@class="info1"]/text()')[0]
            except:
                cocktail = tree.xpath('//span[@class="info1"]/text()')
                print cocktail
            ingredients = tree.xpath('//li/text()')
            ingrlist = list()
            for ing in ingredients:
                try:
                    aok = False
                    for i,c in enumerate(ing):
                        if c.isupper():
                            first = ing[0:i]
                            amount, unit = first.split(' ', 1)
                            ingredient = ing[i:]
                            ingrlist.append({"name" : ingredient, "amount" : amount, "unit" : unit})
                            aok = True
                            break
                    if not aok:
                        raise Exception
                except:
                    pass
##                    print ing
####                    ingrlist.append({"Error" : ing})
##                    ingredient = raw_input("Ingredient? ")
##                    amount = raw_input("Amount? ")
##                    unit = raw_input("Unit? ")
##                    ingrlist.append({"name" : ingredient, "amount" : amount, "unit" : unit})
            instr = "".join(tree.xpath('//div[@class="oc_info"]/text()')).replace('\r\n', '')
            listofcocktails.append({"name" : cocktail, \
                                    "ingredients" : ingrlist,
                                    'instructions': instr})

    with open('summary2.txt', 'w') as f:
        json.dump(listofcocktails, f)
##        for c in listofcocktails:
##            json.dump(c, f)
##            f.write('\n')

if __name__ == '__main__':
    main()
