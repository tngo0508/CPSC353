#!/usr/bin/python3

from __future__ import print_function
import sys, os, argparse
import pdb
from PIL import Image

def text_to_binary(text):
    return ''.join(format(ord(x), '08b') for x in text)

def binary_to_text(binary):
    n = int(binary,2)
    text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return text

def decode(im):
    #get horizontal and vertical size of the image
    #x is horizontal, y is vertical
    x,y = im.size
    
    #use the first 11 pixels on the bottom right to read text length(number of
    #bits)
    numOfBit = [] #store text length in binary
    y -=1
    for i in range (11):
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
    print("The text length in bit:", textLength)
    print("The text length in binary:", bin(int(''.join(numOfBit),2))[2:].zfill(32))

    #knew the length of secret text, use it to find the sequence binary of the secret text
    #after that, use the function binary_to_text to decode it into message
    text = []
    while (len(text) < textLength):
        x -= 1
        r, b, g = im.getpixel((x, y))

        temp = "{0:08b}".format(r)
        text.append(temp[-1])
        if (len(text) == textLength):
            break

        temp = "{0:08b}".format(b)
        text.append(temp[-1])
        if (len(text) == textLength):
            break
        
        temp = "{0:08b}".format(g)
        text.append(temp[-1])
        if (len(text) == textLength):
            break

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

def change_LSB(RGB_elem, binary):
    temp = list('{0:08b}'.format(RGB_elem))
    binary = list(binary)
    temp[-1] = binary[0]
    temp  = ''.join(temp)
    RGB_elem = int(temp,2) 
    return RGB_elem

def encode(im, text):
    imageData = list(im.getdata())
    newImageData = []
    text_in_binary = text_to_binary(text) 
    textLength = len(text_in_binary)
    
    #hide textLength as binary inside 11 pixels of the image
    textLength = format(textLength, '032b')
    print(textLength)

    pixels = im.load() #create a pixel map
    x,y = im.size
    y -=1
    while textLength:
        x -= 1

        r, b, g = im.getpixel((x, y))
        
        if textLength:
            r = change_LSB(r, textLength)
            textLength = textLength[1:]
             
            if not textLength:
                newImageData.append((r, b, g))
                break
            
            b = change_LSB(b, textLength)
            textLength = textLength[1:]
            if not textLength:
                newImageData.append((r, b, g))
                break

            g = change_LSB(g, textLength)
            textLength = textLength[1:]
            if not textLength:
                newImageData.append((r, b, g))
                break

        newImageData.append((r, b, g))
    
    print(newImageData)

    numOfBit = []
    #testing
    for i in range(10, 0, -1):
        #  print(i)
        #decrement x to read backward from bottome right to bottom left of image

        #each pixel has an RGB value in which has 3 sub-value r,b,g
        r, b, g = newImageData[-i]
        print(newImageData[-i])

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
    
    print("The text length in binary:", bin(int(''.join(numOfBit),2))[2:].zfill(32))

    
#  def main(image, output, text, isEncode):
def main(image, text, isEncode):
    im = Image.open(image)
    if isEncode:
        encode(im, text)
    else:
        print(decode(im))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'stegenography project CPSC353')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--decode", "-d", help = "decode on an image mode RGB", action = 'store_true', dest = "decode", default = False)
    group.add_argument("--encode", "-e", help = "encode on an image mode RGB", action = 'store_true', dest = "encode", default = False)
    parser.add_argument("image", help = "location of the image")
    parser.add_argument("--text", "-t", action='store',help = "secret text")
    #  parser.add_argument("--output", "-o", help = "Name of output file", dest = "output",default = None)
    args = parser.parse_args()

    if args.encode and not args.text and not args.output:
        print("secret text is required")
        sys.exit(0)

    #  main(args.image, args.output, args.text, args.encode)
    main(args.image, args.text, args.encode)
    

