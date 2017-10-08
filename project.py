#!/usr/bin/python3

from __future__ import print_function
import sys, os, argparse
from PIL import Image

def text_to_binary(text):
    return ' '.join(format(ord(x), '032b') for x in text)

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

def change_LSB(RGBvalue, bitValue):
    RGBvalue_sequence = list(format(RGBvalue, 'b'))
    RGBvalue_sequence[-1] = bitValue
    RGBvalue_sequence = ''.join(RGBvalue_sequence)
    return RGBvalue_sequence

#this function I got from author Reza Nikoopour(CSUF lecturer)
#it is used to embed a binary in image by changing the LSB of each RGB value in each pixel
def embed_binary_in_image(image_data, binary, index):
    binary = list(binary)
    new_image_data = []
    
    while binary:
        red, green, blue = image_data[index]
        index -= 1

        new_red = change_LSB(red, binary[0])
        red = int(new_red, 2)
        binary.pop(0)
        if not binary:
            new_image_data.append((red, green, blue))
            break
        new_green = change_LSB(green, binary[0])
        green = int(new_green, 2)
        binary.pop(0)
        if not binary:
            new_image_data.append((red, green, blue))
            break
        new_blue = change_LSB(blue, binary[0])
        blue = int(new_blue, 2)
        binary.pop(0)
        new_image_data.append((red, green, blue))
    return (new_image_data, index)

#modify embed_in_image function from  author Reza Nikoopour(CSUF lecturer)
def encrypt(im, text):
    #data stores pixel values in a list. Each element is a group of 3-RGB value
    data = list(im.getdata())

    #get the length of secret text and convert it into numOfBit, then convert
    #that number into binary sequence
    textLength = len(text)
    numOfBit = textLength * 8
    numOfBit = format(numOfBit, '032b')
    
    newData = []
    (modifiedData, index) = embed_binary_in_image(data, numOfBit, -1)
    newData += modifiedData

    text_in_binary = text_to_binary(text)
    (modifiedData, last_pixel) = embed_binary_in_image(data, text_in_binary, -11)
    newData += modifiedData
    newData = data[last_pixel:] + newData

    im.putdata(newData)
    im.save(output_file, 'PNG')
    
def main(image,text, isEncrypt, output):
    im = Image.open(image)
    if isEncrypt:
        new_image = encrypt(im, text)
    else:
        print(decrypt(im))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'stegenography project CPSC353')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("--decrypt", "-d", help = "decryption on an image mode RGB", action = 'store_true', dest = "decryptedImage", default = False)
    group.add_argument("--encrypt", "-e", help = "encryption on an image mode RGB", action = 'store_true', dest = "encryption", default = False)
    parser.add_argument("image", help = "location of the image")
    parser.add_argument("--text", "-t", help = "secret text")
    parser.add_argument("--output", "-o", help = "Name of output file", dest =
    "output",default = None)
    args = parser.parse_args()

    if args.encryption and not args.text and not args.output:
        print("secret text is required")
        sys.exit(0)

    main(args.image, args.output, args.text, args.encryption)

