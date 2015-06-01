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
import json

def main():
    with open('summary.txt') as f1:
        with open('summary2.txt') as finstr:
            data = json.load(f1)
            inst = json.load(finstr)

    print type(data)
    print len(data)

    for j, ct in enumerate(data):
        print j, ct
        for i in inst:
            if ct["name"] == i["name"]:
                ct["instructions"] = i["instructions"]

    with open('summary3.txt', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    main()
