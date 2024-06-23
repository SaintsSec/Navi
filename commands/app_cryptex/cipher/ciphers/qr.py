"""
Author: Alex Kollar | Project Manager: The Cryptex Project.
Links: https://github.com/CryptexProject | https://twitter.com/ssgcythes
Description: A QR Generator for Cryptex
"""

import qrcode
from ..cipher import Cipher


def validate_image_extension(file: str) -> str:
    """
    Validate the image extension and return the correct extension
    """

    extensions = [".png", ".jpg", ".jpeg", ".bmp", ".gif"]

    # check if the file has an extension
    if "." not in file:
        return file + ".png"

    # check if the extension is valid
    for extension in extensions:
        if file.endswith(extension):
            return file

    # if the extension is not valid then return the file with a png extension
    return file + ".png"


class qr(Cipher):  # I don't like that this doesn't follow the correct naming convention

    name = 'QR Code Generator'
    type = 'tool'

    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        filename = get_argument_value(args, "output")

        if not filename:
            return {'text': "No output file", 'success': False}

        if not text:
            return {'text': "No input text", 'success': False}

        qr = qrcode.QRCode(
            version=1,
            box_size=20,
            border=1,
        )

        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        filename = validate_image_extension(filename)
        try:
            img.save(filename)
        except Exception as e:
            return {'text': f"Error saving image: {e}", 'success': False}

        return {'text': filename, 'success': True}

    def print_options(self):
        print('''
        ### Modes
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -o / --output ---- output file

        ### Examples
        python main.py qr -e -t "hello" -o 'text.png'
        ''')
