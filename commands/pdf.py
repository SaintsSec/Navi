import os
import fpdf
import readline

# Import readline library for tab completion
# make ascii art for pdf converter using text "Pdf Converter" in figlet

art = """    ____  ____  ______   ______                           __           
   / __ \/ __ \/ ____/  / ____/___  ____ _   _____  _____/ /____  _____
  / /_/ / / / / /_     / /   / __ \/ __ \ | / / _ \/ ___/ __/ _ \/ ___/
 / ____/ /_/ / __/    / /___/ /_/ / / / / |/ /  __/ /  / /_/  __/ /    
/_/   /_____/_/       \____/\____/_/ /_/|___/\___/_/   \__/\___/_/     
"""
command = "/pdf"
use = "text to pdf conversion"


def complete(text, state):
    """Tab completion function."""
    options = [i for i in os.listdir('.') if i.startswith(text)]
    return options[state] if state < len(options) else None


def pdf_convert():
    print(art)
    readline.set_completer_delims(' \t\n')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    text_file = input("Navi> Enter the full path and name of the text file:\n")
    pdf_file = input("Navi> Enter the full path and name of the PDF file:\n")

    # Get the full path of the text file
    text_file_path = os.path.abspath(text_file)
    # Get the full path of the PDF file
    pdf_file_path = os.path.abspath(pdf_file)

    if not os.path.exists(text_file_path):
        print("Navi> The text file does not exist.")
        return

    print("Navi> Converting the text file to a PDF file.")
    with open(text_file_path, "r") as text_file:
        pdf_file = fpdf.FPDF(format='letter')
        pdf_file.add_page()
        pdf_file.set_font("Arial", size=12)
        for line in text_file:
            pdf_file.cell(200, 10, txt=line, ln=1, align="L")
        pdf_file.output(pdf_file_path)
        print("Navi> The text file was converted to a PDF file.")


def run():
    pdf_convert()
