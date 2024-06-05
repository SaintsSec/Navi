import os
import fpdf
import readline
import click
import pyfiglet
from navi_shell import get_ai_name

# Import readline library for tab completion
# make ascii art for pdf converter using text "Pdf Converter" in figlet


command = "pdf"
use = "text to pdf conversion"


def complete(text, state):
    """Tab completion function."""
    options = [i for i in os.listdir('.') if i.startswith(text)]
    return options[state] if state < len(options) else None


def header_art():
    header = pyfiglet.figlet_format("PDF Converter", font="slant")
    click.echo(click.style(header, fg="cyan", bold=True))


def pdf_convert():
    header_art()
    readline.set_completer_delims(' \t\n')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)

    text_file = input(f"{get_ai_name}> Enter the full path and name of the text file:\n")
    pdf_file = input(f"{get_ai_name}> Enter the full path and name of the PDF file:\n")

    # Get the full path of the text file
    text_file_path = os.path.abspath(text_file)
    # Get the full path of the PDF file
    pdf_file_path = os.path.abspath(pdf_file)

    if not os.path.exists(text_file_path):
        print(f"{get_ai_name}> The text file does not exist.")
        return

    print(f"{get_ai_name}> Converting the text file to a PDF file.")
    with open(text_file_path, "r") as text_file:
        pdf_file = fpdf.FPDF(format='letter')
        pdf_file.add_page()
        pdf_file.set_font("Arial", size=12)
        for line in text_file:
            pdf_file.cell(200, 10, txt=line, ln=1, align="L")
        pdf_file.output(pdf_file_path)
        print(f"\n{get_ai_name()} The text file was converted to a PDF file.")
        input(f"\n{get_ai_name()} Press enter to return to main chat.")


def run():
    pdf_convert()
