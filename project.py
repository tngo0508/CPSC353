#!/usr/bin/python3

from __future__ import print_function
import sys, os, argparse
from PIL import Image

def text_to_binary(text):
    #  return ' '.join(format(ord(x), '08b') for x in text)
    binary = bin(int.from_bytes(text.encode(), 'big'))
    return binary

def binary_to_text(binary):
    n = int(binary,2)
    text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return text

def decrypt(im):
    #get horizontal and vertical size of the image
    #x is horizontal, y is vertical
    x,y = im.size

    #use the first 11 pixels on the bottom right to read text length(number of
    #bits)
    numOfBit = [] #store text length in binary
    y -=1
    for i in range (0,11):
        #decrement x to read backward from bottome right to bottom left of image
        x -= 1

        #each pixel has an RGB value in which has 3 sub-value r,b,g
        r, b, g = im.getpixel((x, y))

        #each RGB has three sets of 8-bit, retrieve the least significant
        #bit(LSB) in each set and add them in numOfBit to establish a sequence of binary
        temp = "{0:08b}".format(r)
        numOfBit.append(temp[-1])
        
        temp = "{0:08b}".format(b)
        numOfBit.append(temp[-1])

        temp = "{0:08b}".format(g)
        numOfBit.append(temp[-1])

    #11 pixels store 33 LSB, but only 32 LSB are used to read the text length
    numOfBit = numOfBit[:-1]

    #convert binary to text length in number of LSB
    #numOfBit is just a array containing elements that represent for a binary
    #sequence, it is NOT a real binary
    textLength = int(''.join(numOfBit),2)
    print("The text length:", textLength)
    print("The text length in bit:", bin(int(''.join(numOfBit),2))[2:].zfill(32))

    text = []
    #each pixel has 3 LSB, textLength/3 will give the number of pixel
    #containing the data
    for i in range (0,int(textLength/3)):
        x -= 1
        r, b, g = im.getpixel((x, y))

        temp = "{0:08b}".format(r)
        text.append(temp[-1])

        temp = "{0:08b}".format(b)
        text.append(temp[-1])

        temp = "{0:08b}".format(g)
        text.append(temp[-1])

        #if horizontal value becomes 0, program has reached the end of
        #bottom left. Need to reset the values of horizontal and vertical
        #to read the line above the current line and from right to left
        if (x == 0):
            y -= 1
            x -= 1
        
    #convert sequence of LSB into a real binary
    msg = bin(int(''.join(text), 2))
    print("The binary sequence of secret text:",
            bin(int(''.join(text),2))[2:].zfill(32)) 
    message = binary_to_text(msg)
    return message

def main(image):
    im = Image.open(image)
    print(decrypt(im))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'stegenography project CPSC353')

    #make sure that only one of the arguments in the mutually exclusive group was present on the command line
    #a required argument, to indicate that at least one of the mutually exclusive arguments is required
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--decrypt", "-d", help = "decryption on an image mode RGB", action = 'store_true', dest = "decryptedImage")
    parser.add_argument("image", help = "location of the image")
    args = parser.parse_args()

    main(args.image)
