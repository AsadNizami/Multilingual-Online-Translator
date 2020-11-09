import requests
from bs4 import BeautifulSoup


class Translator:

    def start(self):
        self.accept()
        self.formatting()

    def __init__(self, src_lang='', trans_lang='', word=''):
        self.src_lang = src_lang
        self.trans_lang = trans_lang
        self.word = word

    def accept(self):
        print("Hello, you're welcome to the translator. Translator supports: ")
        lang_list = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
        for no, lang in enumerate(lang_list):
            print(no+1, '. ', lang, sep='')
        src_lang = int(input('Type the number of your language: '))  # to be translated
        trans_lang = int(input('Type the number of language you want to translate to: '))
        word = input('Type the word you want to translate:')
        self.__init__(src_lang=lang_list[src_lang-1], trans_lang=lang_list[trans_lang-1], word=word)

    def url_gen(self):
        src_low = self.src_lang.lower()
        trans_lower = self.trans_lang.lower()
        return f'https://context.reverso.net/translation/{src_low}-{trans_lower}/{self.word}'

    def connect(self):
        user_agent = 'Mozilla/5.0'
        url = self.url_gen()
        req_obj = requests.get(url, headers={'User-Agent': user_agent})
        return req_obj

    def parse(self):
        data = self.connect().content
        parser = 'html.parser'
        soup = BeautifulSoup(data, parser)
        words = soup.find(id='translations-content').text.split()
        examples = [x.text.strip() for x in soup.find_all(class_=['src ltr', 'trg ltr'])]
        return words, examples

    def formatting(self):
        no_word = no_examples = 5
        words, examples = self.parse()
        print('Context examples:\n')

        print(f'{self.trans_lang} Translations:')
        print(*words[:no_word], sep='\n', end='\n\n')

        print(f'{self.trans_lang} Examples:')
        for i in range(no_examples):
            print(examples[i])
            print(examples[i+1], '\n')


if __name__ == '__main__':
    obj = Translator()
    obj.start()
