#!/usr/bin/env python3
"""CPSC353 project STEGENOGRAPHY/TEXT IN IMAGE."""
import sys
import argparse
from PIL import Image

def text_to_binary(text):
    """Convert a string text into sequence of binary by using ASCII key number.
    First, convert each character in string into ASCII key number. Then, format
    the integer ASCII key number into 8-bit representing for each character.
    Finally, join them together to form a sequence of binary.

    Args:
        text: a string of character.

    Returns:
        A string of number 1 and 0 as sequence of binary.
    """

    return ''.join(format(ord(horizontal), '08b') for horizontal in text)


def binary_to_text(binary):
    """Convert a sequence of binary back to text. First, change binary to an
    integer. Then, use to_bytes() and decode() to change data again into bytes
    and ASCII key character respectively.

    Args:
        binary: a string of number 1 and 0 as sequence of binary.

    Returns:
        A string of character in human-readable mode.
    """

    binary_as_number = int(binary, 2)
    text = binary_as_number.to_bytes((binary_as_number.bit_length() + 7) // 8, 'big').decode()
    return text


def decode(img):
    """Decode the hidden secret text inside an image.

    Retrieves the textLength using the bottom right 11 pixels. Then, use the
    textLength to extract the text from image after those 11 pixels.

    Args:
        img: an image stores the textLength and secret message/text.

    Returns:
        A string contains the content of secret text.
    """

    horizontal, vertical = img.size #Get horizontal and vertical size of the image

    width = horizontal #Used to reset horizontal value

    """Use the first 11 pixels on the bottom right to read text length(number of bits)
    Store text length in binary.
    """
    num_of_bit = []
    vertical -= 1
    for _ in range(11):
        horizontal -= 1

        red, blue, green = img.getpixel((horizontal, vertical))

        """Each RGB has three sets of 8-bit, retrieve the least significant
        bit(LSB) in each set and add them in numOfBit to establish a sequence of binar
        """
        temp = '{0:08b}'.format(red)
        num_of_bit.append(temp[-1])

        temp = '{0:08b}'.format(blue)
        num_of_bit.append(temp[-1])

        temp = '{0:08b}'.format(green)
        num_of_bit.append(temp[-1])

    """11 pixels store 33 LSB, but only 32 LSB are used to read the text length.
    """
    num_of_bit = num_of_bit[:-1]

    """Convert binary to text length in number of LSB numOfBit is just a array
    containing elements that represent for a binary sequence, it is NOT a real
    binary.
    """
    text_length = int(''.join(num_of_bit), 2)
    print('The text length in bit:', text_length)
    print('The text length in binary:', bin(int(''.join(num_of_bit), 2))[2:].zfill(32))

    """Once knew the length of secret text, use it to find the sequence binary of the secret text.
    After that, use the function binary_to_text to decode it into message.
    """
    text = []
    while len(text) < text_length:
        horizontal -= 1
        red, blue, green = img.getpixel((horizontal, vertical))

        temp = '{0:08b}'.format(red)
        text.append(temp[-1])
        if len(text) == text_length:
            break

        temp = '{0:08b}'.format(blue)
        text.append(temp[-1])
        if len(text) == text_length:
            break

        temp = '{0:08b}'.format(green)
        text.append(temp[-1])
        if len(text) == text_length:
            break

        """If horizontal value becomes 0, program has reached the end of bottom
        left. Need to reset the values of horizontal and vertical to read the
        line above the current line and from right to left.
        """
        if horizontal == 0:
            vertical = vertical - 1
            horizontal = width

    msg = bin(int(''.join(text), 2)) #Convert sequence of LSB into a real binary
    message = binary_to_text(msg)
    return message


def change_least_significant_bit(color_value, binary):
    """Change the least significant bit in red, blue, green value or RGB value
    of a pixel

    Args:
        color_value: red, green, or blue value of a pixel
        binary: sequence of number 0 and 1 representing for textLength or secret
        text

    Returns:
        New RGB value after changing the least significant bit
    """

    temp = list('{0:08b}'.format(color_value))
    binary = list(binary)
    temp[-1] = binary[0]
    temp = ''.join(temp)
    color_value = int(temp, 2)
    return color_value


def encode(img, text):
    """Encode or hide the data (e.green. secret text) inside the least significant
    bit of each RGB value inside an image.

    Args:
        img: image to be embedded with data.
        text: data or secret message.

    Returns:
        The new image with data embedded inside it.
    """

    image_data = list(img.getdata())
    new_image_data = []
    text_in_binary = text_to_binary(text)
    text_length = len(text_in_binary)

    """Hide textLength as binary inside 11 pixels of the image.
    """
    text_length_as_binary = format(text_length, '032b')

    horizontal, vertical = img.size
    width = horizontal #used to reset horizontal value
    index = 0
    vertical -= 1

    """Extract RGB value from each pixel and start changing the least
    significant bit in each 8-bit red, green and blue value.
    """
    while text_length_as_binary:
        horizontal -= 1
        red, blue, green = img.getpixel((horizontal, vertical))
        index -= 1 #keep track the pixel position

        if text_length_as_binary:
            red = change_least_significant_bit(red, text_length_as_binary)
            text_length_as_binary = text_length_as_binary[1:]

            if not text_length_as_binary:
                new_image_data.append((red, blue, green))
                break

            blue = change_least_significant_bit(blue, text_length_as_binary)
            text_length_as_binary = text_length_as_binary[1:]
            if not text_length_as_binary:
                new_image_data.append((red, blue, green))
                break

            green = change_least_significant_bit(green, text_length_as_binary)
            text_length_as_binary = text_length_as_binary[1:]
            if not text_length_as_binary:
                new_image_data.append((red, blue, green))
                break

        new_image_data.append((red, blue, green))

    """Hide secret text as binary after the pixel 11 from bottom right to top
    left.
    """
    while text_in_binary:
        horizontal -= 1

        red, blue, green = img.getpixel((horizontal, vertical))
        index -= 1 #keep track the pixel position

        if text_in_binary:
            red = change_least_significant_bit(red, text_in_binary)
            text_in_binary = text_in_binary[1:]

            if not text_in_binary:
                new_image_data.append((red, blue, green))
                break

            blue = change_least_significant_bit(blue, text_in_binary)
            text_in_binary = text_in_binary[1:]
            if not text_in_binary:
                new_image_data.append((red, blue, green))
                break

            green = change_least_significant_bit(green, text_in_binary)
            text_in_binary = text_in_binary[1:]
            if not text_length:
                new_image_data.append((red, blue, green))
                break

        new_image_data.append((red, blue, green))

        if horizontal == 0:
            vertical = vertical - 1
            horizontal = width

    """Because we try to hide data from bottom right to top left,
    reverse the list in order to decode in correct order.
    """
    new_image_data = new_image_data[::-1]

    """Copy the rest pixels of the image into newImageData.
    """
    new_image_data = image_data[:index] + new_image_data

    return new_image_data


def main(image, output, read, is_encode):
    """Running the stegenography program by calling encode() or decode()
    function which is depended on user's command line.

    Args:
        image: location of the image.
        output: new image embedded with secret text.
        read: human-readable file.
        is_encode: flag for calling encode() or decode().

    Returns:
        None.
    """
    img = Image.open(image)
    if is_encode:
        with open(read) as content_file:
            content = content_file.read()
        new_image = encode(img, content)
        img.putdata(new_image)
        img.save(output, 'PNG')
    else:
        print(decode(img))
    sys.exit(0)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Stegenography Project CPSC353')

    GROUP = PARSER.add_mutually_exclusive_group(required=True)
    GROUP.add_argument('-d', '--decode', help='decode on an image mode RGB', \
            action='store_true', dest='decode', default=False)
    GROUP.add_argument('-e', '--encode', help='encode on an image mode RGB', \
            action='store_true', dest='encode', default=False)
    PARSER.add_argument('image', help='location of the image')
    PARSER.add_argument('-red', '--read', action='store', help='human-readable file')
    PARSER.add_argument('-o', '--output', help='Name of output file', dest='output', default=None)
    ARGS = PARSER.parse_args()

    if ARGS.encode and not ARGS.read and not ARGS.output:
        print('secret text is required')
        sys.exit(0)

    main(ARGS.image, ARGS.output, ARGS.read, ARGS.encode)
