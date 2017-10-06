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

    #use the first 11 pixels on the bottom right to read text length(number of
    #bits)
    numOfBit = []
    #textLength = int
    for i in range (0,11):
        x -= 1
        r, b, g = im.getpixel((x, y-1))
        temp = "{0:08b}".format(r)
        numOfBit.append(temp[-1])
        #print (temp)
        temp = "{0:08b}".format(b)
        numOfBit.append(temp[-1])
        #print (temp)
        temp = "{0:08b}".format(g)
        numOfBit.append(temp[-1])
        #print (temp)
        #print (x,y)

    numOfBit = numOfBit[:-1]
    textLength = int((int(''.join(numOfBit),2)) / 8)
    length = bin(int(''.join(numOfBit), 2))

    print(numOfBit)
    print(length)
    print(textLength)
    return r

def main():
    im = Image.open("testImage.png")
    width, height = im.size
    print(width, height)
    print(im.format, im.size, im.mode)

    #  foo = text_to_bin("security is fun")
    #  print(foo)
    print(len("security is fun")*8)
    print("{0:032b}".format(120))

    bottom = decrypt(im)
    #print(bottom)

if __name__ == "__main__":
    main()
