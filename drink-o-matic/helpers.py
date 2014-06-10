#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Schuyler
#
# Created:     09/06/2014
# Copyright:   (c) Schuyler 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class StringMatrix():
    mat = ""


def main():
    s ="Hello"
    v = ord(s[2])+1;
    s[2] = chr(v)
    print(s[3])
    print(s)


if __name__ == '__main__':
    main()

