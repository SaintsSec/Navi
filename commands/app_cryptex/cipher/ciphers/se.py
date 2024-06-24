"""
Author: @marvhus
"""
from ..cipher import Cipher
from PIL import Image
import numpy as np


class SE(Cipher):
    name = 'Static Encryption'
    type = 'cipher'

    # Generate the image
    @staticmethod
    def gen_image(output, pixels):
        # Convert the pixels into an array using numpy
        array = np.array(pixels, dtype=np.uint8)

        # Use PIL to create an image from the new array of pixels
        new_image = Image.fromarray(array)
        new_image.save(output)

    # Read the image data
    @staticmethod
    def read_image(input_file):
        pixels = []
        img = Image.open(input_file)
        pix = img.load()
        width, height = img.size
        for i in range(height):  # Vertical
            row = []
            for j in range(width):  # Horizontal
                row.append(pix[j, i])
            pixels.append(row)
        return pixels

    default_check = lambda val, default: val if val else default

    @staticmethod
    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        image_width = int(SE.default_check(get_argument_value(args, "imageWidth"), 1))
        monocromatic = SE.default_check(get_argument_value(args, "monocromatic"), False)
        output = SE.default_check(get_argument_value(args, "output"), 'test.png')

        if not text:
            return {'text': "No input text", 'success': False}

        pixels = []
        for i in range(0, len(text), image_width * 3):
            row = text[i:i + (3 * image_width)]
            row_arr = []
            # Loop over the input text in groups of 3
            for i in range(0, len(row), 3):
                # The group of 3 chars
                chars = row[i:i + 3]
                # If there are not enough chars to make only groups of 3, then ths will say how many extra we will 
                # need (2, or 3)
                extra = 3 - len(chars)
                # Empty pixel array
                pixel = []

                # Get the ASCII values of the chars and add them to the pixel array
                for _, char in enumerate(chars):
                    pixel.append(ord(char))

                # Add the extra value
                for i in range(extra):
                    pixel.append(0)

                if monocromatic:
                    # use monocromatic
                    for _, val in enumerate(pixel):
                        row_arr.append(val)
                else:
                    # Convert the pixel array to an array with a tupel inside
                    pixel = (pixel[0], pixel[1], pixel[2])
                    row_arr.append(pixel)

            extra = image_width - len(row_arr)
            for i in range(extra):
                row_arr.append((0, 0, 0))  # add black pixel if there are to few
            print(row_arr)
            pixels.append(row_arr)

        SE.gen_image(output, pixels)

        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        from ....cryptex import get_argument_value
        monocromatic = SE.default_check(get_argument_value(args, "monocromatic"), False)
        input = SE.default_check(get_argument_value(args, "input"), 'test.py')

        try:
            # Get the pixel data
            pixels = SE.read_image(input)
        except FileNotFoundError as e:
            return {'text': f"Failed to read image, did you provide the correct image?\n{e}", 'success': False}

        # Make empty string for the decoded text to be in
        decrypted = ""
        for _, height in enumerate(pixels):  # Vertical
            if monocromatic:
                for _, val in enumerate(height):
                    decrypted += chr(val)
            else:
                try:
                    for _, width in enumerate(height):  # Horizontal
                        for _, val in enumerate(width):  # Pixel
                            # Convert the ASCII value to char and add it to the decrypted variable
                            decrypted += chr(val)
                except Exception as e:
                    return {
                        'text': f"Failed to decrypt image {input}, maybe you forgot to enable monocromatic mode.\n{e}",
                        'success': False}

        return {'text': decrypted, 'success': True}

    @staticmethod
    def print_options(self):
        print('''
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text --------- input text
        -o / --output ------- output file
        -i / --input -------- input file
        -iw / --imageWidth -- image width
        -m / --monocromatic - monocromatic mode

        ### Examples
        python main.py se -e -t 'hello'       -o 'hello.png'
        python main.py se -e -t 'hello' -iw 3 -o 'hello.png'
        python main.py se -e -t 'hello' -m    -o 'hello.png'
        python main.py se -d -i 'hello.png' 
        python main.py se -d -i 'hello.png' -iw 3
        python main.py se -d -i 'hello.png' -m
        ''')
