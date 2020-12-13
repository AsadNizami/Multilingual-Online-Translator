import requests
import sys
from bs4 import BeautifulSoup
import os


##global variables

global_final_lang = ""
global_words = ""
global_examples = ""
global_no_word = 0


class Translator:

    def start(self):
        self.accept()
        req_obj_list = self.connect()
        for req_obj in req_obj_list:
            self.formatting(req_obj=req_obj)
    
    def display(self):
        req_obj_list = self.connect()
        for req_obj in req_obj_list:
            self.formatting(req_obj=req_obj)
        return(global_final_lang, global_words, global_examples, global_no_word)

    @staticmethod
    def except_handler(lang=None):
        if lang:
            print("Sorry, the program doesn't support", lang, file=sys.stderr)
        else:
            print('Input the number from 1-13', file=sys.stderr)
            return
        # exit()

    @staticmethod
    def create_dir():
        dir_name = 'History'
        new_path = os.path.join(os.getcwd(), dir_name)
        if not os.access(new_path, os.F_OK):
            os.mkdir(new_path)
        os.chdir(new_path)
        return os.getcwd()

    def history(self):
        if os.access(self.path, os.R_OK):
            with open(self.path, 'r', encoding='utf-8') as file_out:
                print(file_out.read())
            return True
        else:
            return False

    def __init__(self, path='', src_lang='', trans_lang='', word=''):
        self.file_name = src_lang + '_to_' + trans_lang + '_' + word + '.txt'
        self.path = os.path.join(path, self.file_name)
        self.src_lang = src_lang
        self.trans_lang = trans_lang
        self.word = word

        self.lang_list = [
            'Arabic', 'German', 'English', 'Spanish',
            'French', 'Japanese', 'Portuguese', 'Russian',
        ]
        self.lang_ind = 0
        if trans_lang:
            self.lang_ind = 1 if not trans_lang == 'Arabic' else 0
        if self.history():
            return

    def accept(self):
        print("Hello, welcome to the translator. Translator supports: ")

        for no, lang in enumerate(self.lang_list):
            print(no + 1, '. ', lang, sep='')
        src_lang = int(input('Type the number of your language: '))  # to be translated
        trans_lang = int(input('Type the number of language you want to translate to: '))
        if not all([0 < src_lang < 13, 0 <= trans_lang < 13]):
            self.except_handler()
        word = input('Type the word you want to translate: ')
        path = ''
        path = self.create_dir()
        self.__init__(path=path, src_lang=self.lang_list[src_lang-1], trans_lang=self.lang_list[trans_lang-1], word=word)

    def url_gen(self):
        src_low = self.src_lang.lower()

        if self.trans_lang is not None:
            trans_lower = self.trans_lang.lower()
            return [f'https://context.reverso.net/translation/{src_low}-{trans_lower}/{self.word}', ]

        if self.trans_lang is None:
            url_list = []
            for trans_l in self.lang_list:
                if self.src_lang == trans_l:
                    continue
                else:
                    url = f'https://context.reverso.net/translation/{src_low}-{trans_l.lower()}/{self.word}'
                    url_list.append(url)
            return url_list

    def connect(self):
        user_agent = 'Mozilla/5.0'
        url_list = self.url_gen()
        req_obj_list = []

        try:
            for url in url_list:
                req_obj = requests.get(url, headers={'User-Agent': user_agent})
                req_obj_list.append(req_obj)

        except requests.exceptions.ConnectionError:
            print('Something wrong with your internet connection', file=sys.stderr)
            return
        return req_obj_list

    def parse(self, req_obj):
        parser = 'html.parser'
        data = req_obj.content
        soup = BeautifulSoup(data, parser)
        try:
            words = soup.find(id='translations-content').text.split()
            trans_mod = 'trg rtl arabic' if self.lang_ind == 0 else 'trg ltr'
            examples = [x.text.strip() for x in soup.find_all(class_=['src ltr', trans_mod])]
            return words, examples

        except AttributeError:
            print('Sorry, unable to find', self.word, file=sys.stderr)
            return
            # exit()

    def formatting(self, req_obj):
        try:
            words, examples = self.parse(req_obj=req_obj)
        except TypeError:
            return
        no_word = no_examples = 5  # Number of output
        final_lang = self.trans_lang

        if self.src_lang == self.lang_list[self.lang_ind]:
            self.lang_ind += 1

        # print(f'{final_lang} Examples:')
        # i = 0
        # for _ in range(no_examples):
        #     print(examples[i])
        #     print(examples[i+1], '\n')
        #     i += 2

        self.save_2_file(final_lang=final_lang, words=words, examples=examples, no_word=no_word)
        self.lang_ind += 1
        
        global global_final_lang, global_words, global_examples, global_no_word
        global_final_lang = final_lang
        global_words = words
        global_examples = examples
        global_no_word = no_word

    def save_2_file(self, final_lang, words, examples, no_word):
        with open(self.path, 'a', encoding='utf-8') as file_out:
            file_out.write(f'{final_lang} Translations:\n')
            print(*words[:no_word], file=file_out, sep='\n', end='\n\n')

            file_out.write(f'{final_lang} Examples:\n')
            i = 0
            for _ in range(no_word):
                file_out.write(examples[i])
                file_out.write('\n')
                file_out.write(examples[i + 1])
                file_out.write('\n\n')
                i += 2
                file_out.write('\n')


if __name__ == '__main__':
    obj = Translator()
    obj.start()
