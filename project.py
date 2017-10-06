#!/usr/bin/python3

from __future__ import print_function
import sys, os, argparse
from PIL import Image

def text_to_bin(text):
    return ''.join(format(ord(x), 'b') for x in text)

def main():
    im = Image.open("testImage.png")
    width, height = im.size
    print(width, height)
    print(im.format, im.size, im.mode)
    foo = text_to_bin("foo")
    print(foo)


if __name__ == "__main__":
    main()
