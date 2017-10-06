#!/usr/bin/python3

from __future__ import print_function
import sys, os, argparse
from PIL import Image

def text_to_bin(text):
    return ' '.join(format(ord(x), '08b') for x in text)

#def numOfBit_to_bin(text_length):

def decrypt(im):
    #get horizontal and vertical size of the image
    #x is vertical, y is horizontal
    x,y = im.size

    #
    y -= 1
    for i in range (0,11):
        x -= 1
        r, b, g = im.getpixel((x, y))
        temp = "{0:08b}".format(r)
        print (temp)
        temp = "{0:08b}".format(b)
        print (temp)
        temp = "{0:08b}".format(g)
        print (temp)
        print (x,y)

    print("{0:032b}".format(120))
    return r

def main():
    im = Image.open("testImage.png")
    width, height = im.size
    print(width, height)
    print(im.format, im.size, im.mode)

    #  foo = text_to_bin("security is fun")
    #  print(foo)

    bottom = decrypt(im)
    print(bottom)

if __name__ == "__main__":
    main()
