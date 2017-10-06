#!/usr/bin/python3

from __future__ import print_function
import sys, os, argparse
from PIL import Image

def text_to_bin(text):
    return ' '.join(format(ord(x), '08b') for x in text)

#def numOfBit_to_bin(text_length):

def decrypt(im):
    #get horizontal and vertical size of the image
    #x is vertical(width), y is horizontal(length)
    x,y = im.size

    #use the first 11 pixels on the bottom right to read text length(number of
    #bits)
    numOfBit = [] #store text length in binary

    for i in range (0,11):
        #decrement x to read backward from bottome right to bottom left of image
        x -= 1

        #each pixel has an RGB value in which has 3 sub-value r,b,g
        r, b, g = im.getpixel((x, y-1))

        #each RGB has three sets of 8-bit, retrieve the last digit in each set
        temp = "{0:08b}".format(r)
        numOfBit.append(temp[-1])
        
        temp = "{0:08b}".format(b)
        numOfBit.append(temp[-1])

        temp = "{0:08b}".format(g)
        numOfBit.append(temp[-1])

    #11 pixels store 33 bits, but only 32 bits are used to read the text length
    numOfBit = numOfBit[:-1]

    textLength = int(''.join(numOfBit),2)
    #  length = bin(int(''.join(numOfBit), 2))

    #  print(numOfBit)
    #  print(length)
    print(textLength)

    text = []
    y -= 1
    for i in range (0,int(textLength/3)):
        x -= 1
        r, b, g = im.getpixel((x, y))

        temp = "{0:08b}".format(r)
        text.append(temp[-1])

        temp = "{0:08b}".format(b)
        text.append(temp[-1])

        temp = "{0:08b}".format(g)
        text.append(temp[-1])

        if (x == 0):
            y -= 1
            x -= 1
        
    print(text)
    msg = bin(int(''.join(text), 2))
    print(msg)
    n = int(msg,2)
    message = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    print(message)
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
