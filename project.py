#!/usr/bin/env python3
from __future__ import print_function
from PIL import Image
import sys
import os
import argparse

def text_to_binary(text):
    """Convert a string text into sequence of binary by using ASCII key number.
    First, convert each character in string into ASCII key number. Then, format
    the integer ASCII key number into 8-bit representing for each character.
    Finally, join them together to form a sequence of binary

    Args:
        text: a string of character

    Returns:
        A string of number 1 and 0 as sequence of binary
    """

    return ''.join(format(ord(x), '08b') for x in text)

def binary_to_text(binary):
    """Convert a sequence of binary back to text. First, change binary to an
    integer. Then, use to_bytes() and decode() to change data again into bytes
    and ASCII key character respectively.

    Args:
        binary: a string of number 1 and 0 as sequence of binary

    Returns:
        A string of character in human-readable mode
    """

    n = int(binary,2)
    text = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
    return text

def decode(im):
    """Decode the hidden secret text inside an image

    Retrieves the textLength using the bottom right 11 pixels. Then, use the
    textLength to extract the text from image after those 11 pixels.

    Args:
        im: an image stores the textLength and secret message/text

    Returns:    
        A string contains the content of secret text
    """

    """Get horizontal and vertical size of the image
    x is horizontal, y is vertical"""
    x,y = im.size

    """Used to reset x and y"""
    w,l = im.size

    """Use the first 11 pixels on the bottom right to read text length(number of bits)"""
    """Store text length in binary"""
    num_of_bit = []
    y -=1
    for i in range (11):
        """Decrement x to read backward from bottome right to bottom left of image"""
        x -= 1

        """Each pixel has an RGB value in which has 3 sub-value r,b,g"""
        r, b, g = im.getpixel((x, y))

        """Each RGB has three sets of 8-bit, retrieve the least significant 
        bit(LSB) in each set and add them in numOfBit to establish a sequence of binary"""
        temp = '{0:08b}'.format(r)
        num_of_bit.append(temp[-1])

        temp = '{0:08b}'.format(b)
        num_of_bit.append(temp[-1])

        temp = '{0:08b}'.format(g)
        num_of_bit.append(temp[-1])

    """11 pixels store 33 LSB, but only 32 LSB are used to read the text length"""
    num_of_bit = num_of_bit[:-1]

    """Convert binary to text length in number of LSB numOfBit is just a array 
    containing elements that represent for a binary sequence, it is NOT a real binary"""
    text_length = int(''.join(num_of_bit),2)
    print('The text length in bit:', text_length)
    print('The text length in binary:', bin(int(''.join(num_of_bit),2))[2:].zfill(32))

    """Once knew the length of secret text, use it to find the sequence binary of the secret text.
    After that, use the function binary_to_text to decode it into message"""
    text = []
    while (len(text) < text_length):
        x -= 1
        r, b, g = im.getpixel((x, y))

        temp = '{0:08b}'.format(r)
        text.append(temp[-1])
        if (len(text) == text_length):
            break

        temp = '{0:08b}'.format(b)
        text.append(temp[-1])
        if (len(text) == text_length):
            break

        temp = '{0:08b}'.format(g)
        text.append(temp[-1])
        if (len(text) == text_length):
            break

        """If horizontal value becomes 0, program has reached the end of bottom
        left. Need to reset the values of horizontal and vertical to read the
        line above the current line and from right to left"""
        if (x == 0):
            y = y - 1
            x = w

    """Convert sequence of LSB into a real binary"""
    msg = bin(int(''.join(text), 2))
    message = binary_to_text(msg)
    return message

def change_LSB(RGB_elem, binary):
    """Change the least significant bit in red, blue, green value or RGB value
    of a pixel

    Args:
        RGB_elem: red, green, or blue value of a pixel
        binary: sequence of number 0 and 1 representing for textLength or secret
        text

    Returns:
        New RGB value after changing the least significant bit
    """

    temp = list('{0:08b}'.format(RGB_elem))
    binary = list(binary)
    temp[-1] = binary[0]
    temp  = ''.join(temp)
    RGB_elem = int(temp,2) 
    return RGB_elem

def encode(im, text):
    """Encode or hide the data (e.g. secret text) inside the least significant
    bit of each RGB value inside an image

    Args:
        im: image to be embedded with data
        text: data or secret message

    Returns:
        The new image with data embedded inside it
    """

    image_data = list(im.getdata())
    new_image_data = []
    text_in_binary = text_to_binary(text) 
    text_length = len(text_in_binary)

    """Hide textLength as binary inside 11 pixels of the image"""
    text_length_as_binary = format(text_length, '032b')

    pixels = im.load() #create a pixel map
    x,y = im.size
    w,l = im.size #used to reset x and y
    index = 0 
    y -=1
    
    """Extract RGB value from each pixel and start changing the least
    significant bit in each 8-bit red, green and blue value"""
    while text_length_as_binary:
        x -= 1
        r, b, g = im.getpixel((x, y))
        index -= 1 #keep track the pixel position 

        if text_length_as_binary:
            r = change_LSB(r, text_length_as_binary)
            text_length_as_binary = text_length_as_binary[1:]
            if not text_length_as_binary:
                new_image_data.append((r, b, g))
                break

            b = change_LSB(b, text_length_as_binary)
            text_length_as_binary = text_length_as_binary[1:]
            if not text_length_as_binary:
                new_image_data.append((r, b, g))
                break

            g = change_LSB(g, text_length_as_binary)
            text_length_as_binary = text_length_as_binary[1:]
            if not text_length_as_binary:
                new_image_data.append((r, b, g))
                break

        new_image_data.append((r, b, g)) 

    """Hide secret text as binary after the pixel 11 from bottom right to top
    left"""
    while text_in_binary:
        x -= 1

        r, b, g = im.getpixel((x, y))
        index -= 1 #keep track the pixel position

        if text_in_binary:
            r = change_LSB(r, text_in_binary)
            text_in_binary = text_in_binary[1:]

            if not text_in_binary:
                new_image_data.append((r, b, g))
                break

            b = change_LSB(b, text_in_binary)
            text_in_binary = text_in_binary[1:]
            if not text_in_binary:
                new_image_data.append((r, b, g))
                break

            g = change_LSB(g, text_in_binary)
            text_in_binary = text_in_binary[1:]
            if not text_length:
                new_image_data.append((r, b, g))
                break

        new_image_data.append((r, b, g))

        if x == 0:
            y = y - 1
            x = w

    """Because we try to hide data from bottom right to top left, reverse the list in order to decode in correct order"""
    new_image_data = new_image_data[::-1]

    """copy the rest pixels of the image into newImageData"""
    new_image_data = image_data[:index] + new_image_data

    return new_image_data


def main(image, output, read, is_encode):
    im = Image.open(image)
    if is_encode:
        with open(read) as content_file:
            content = content_file.read()
        new_image = encode(im, content)
        im.putdata(new_image)
        im.save(output, 'PNG')
    else:
        print(decode(im))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Stegenography Project CPSC353')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-d','--decode', help = 'decode on an image mode RGB', action = 'store_true', dest = 'decode', default = False)
    group.add_argument('-e', '--encode', help = 'encode on an image mode RGB', action = 'store_true', dest = 'encode', default = False)
    parser.add_argument('image', help = 'location of the image')
    parser.add_argument('-r', '--read', action='store',help = 'human-readable file')
    parser.add_argument('-o', '--output', help = 'Name of output file', dest = 'output',default = None)
    args = parser.parse_args()

    if args.encode and not args.read and not args.output:
        print('secret text is required')
        sys.exit(0)

    main(args.image, args.output, args.read, args.encode)
