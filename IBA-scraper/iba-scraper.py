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

import requests
from lxml import html
import urllib2

def main():
    with open('IBA Official Cocktails.html') as addrlist:
        info = addrlist.read()
        tree = html.fromstring(info)

    addrs = tree.xpath('//a[@class="modal"]/@href')

    unknowns = 0

    for a in addrs:
        addr = "http://www.iba-world.com%s" % a
        print addr
        response = urllib2.urlopen(addr)
        page = response.read()
        tree = html.fromstring(page)
        try:
            cocktail = tree.xpath('//span[@class="info1"]/text()')[0].replace("'",'')
            with open('cocktails/%s' % cocktail, 'w')as f:
                f.write(page)
        except:
            with open('cocktails/unknown%s' % str(unknowns), 'w')as f:
                unknowns = unknowns + 1
                f.write(page)
    return

    tree = html.fromstring(page)

    print page

#    cocktail = tree.xpath('//*[@id="official_cocktails"]/div[2]/p[1]/span[1]')
#    ingredients = tree.xpath('//*[@id="official_cocktails"]/div[2]/ul')

    cocktail = tree.xpath('//span[@class="info1"]/text()')
    ingredients = tree.xpath('//li/text()')
    instr = "".join(tree.xpath('//div[@class="oc_info"]/text()')).replace('\r\n', '')
    print cocktail
    print ingredients
    print instr

if __name__ == '__main__':
    main()
