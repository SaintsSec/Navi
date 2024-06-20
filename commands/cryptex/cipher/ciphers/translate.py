"""
Author: @marvhus 
"""
from cipher import Cipher
from googletrans import Translator, LANGUAGES

class Translate(Cipher): #make sure you change this from text to your cipher

    name = 'Google Translate' #change the name
    type = 'tool'

    @staticmethod
    def translate(text, src_lang, dest_lang):
        translator = Translator()
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text

    @staticmethod
    def encode(args):
        text = args.text
        src_lang = args.src_lang
        dest_lang = args.dest_lang

        if args.languages:
            print('--- Languages ---')
            for _, lang in enumerate(LANGUAGES):
                print(f" - {lang} \t- {LANGUAGES[lang]}")
            print('-----------------')
            return {'languages': True}

        if not text:
            return {'text': "No input text", 'success': False}
        if not src_lang:
            return {'text': "No source language", 'success': False}
        if not dest_lang:
            return {'text': "No destination language", 'success': False}
        
        output = Translate.translate(text, src_lang, dest_lang)

        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        return Translate.encode(args)

    @staticmethod
    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -lang ----------- shows languages
        -t / --text ------ input text
        -src ------------- source language
        -dest ------------ destination language

        ### Examples
        python main.py translate -e --lang
        python main.py translate -e -t 'hello' -src 'en' -dest 'no'
        python main.py translate -d -t 'hallo' -src 'no' -dest 'en'
        ''')

    def test(args):
        total = 2

        args.text = 'hello'
        args.src_lang = 'en'
        args.dest_lang = 'no'
        expect = 'Hallo'
        out = Translate.encode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        args.text = 'hallo'
        args.src_lang = 'no'
        args.dest_lang = 'en'
        expect = 'hello'
        out = Translate.decode(args)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{args.text}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total} tests'}
