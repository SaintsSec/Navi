"""
Author: @marvhus 
"""
from ..cipher import Cipher
from googletrans import Translator, LANGUAGES


class Translate(Cipher):
    name = 'Google Translate'
    type = 'tool'

    @staticmethod
    def translate(text, src_lang, dest_lang):
        translator = Translator()
        translated = translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text

    @staticmethod
    def encode(args):
        from ....cryptex import get_argument_value
        text = get_argument_value(args, "text")
        src_lang = get_argument_value(args, "src_lang")
        dest_lang = get_argument_value(args, "dest_lang")

        if get_argument_value(args, "languages"):
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
        try:
            output = Translate.translate(text, src_lang, dest_lang)
        except Exception as e:
            return {'text': f"Error translating: {e}", 'success': False}

        return {'text': output, 'success': True}

    @staticmethod
    def decode(args):
        return Translate.encode(args)

    @staticmethod
    def print_options(self):
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
        total_tests = 2
        test_arg_list = ['translate', '-e', '-t', 'hello', '-src', 'en', '-dest', 'no']
        text_index = 3

        expect = 'Hallo'
        out = Translate.encode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to encode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        test_arg_list = ['translate', '-e', '-t', 'hallo', '-src', 'no', '-dest', 'en']
        expect = 'hello'
        out = Translate.decode(test_arg_list)
        if not out['success'] or out['text'] != expect:
            return {'status': False, 'msg': f'''Failed to decode "{test_arg_list[text_index]}"
            expected "{expect}" got "{out['text']}"'''}

        return {'status': True, 'msg': f'Ran {total_tests} tests'}
