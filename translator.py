import requests
from bs4 import BeautifulSoup


class Translator:

    def start(self):
        self.accept()
        self.formatting()

    def __init__(self, lang='', word=''):
        self.lang = lang
        self.word = word

    def accept(self):
        lang = input(
            'Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
        word = input('Type the word you want to translate:')
        self.__init__(lang, word)
        print(f'You chose "{lang}" as the language to translate "{word}" to.')

    def url_gen(self):
        if self.lang == 'en':
            return f'https://context.reverso.net/translation/french-english/{self.word}'

        if self.lang == 'fr':
            return f'https://context.reverso.net/translation/english-french/{self.word}'

    def connect(self):
        user_agent = 'Mozilla/5.0'
        url = self.url_gen()
        req_obj = requests.get(url, headers={'User-Agent': user_agent})
        print(req_obj.status_code, 'OK', end='\n')
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

        print('Translations:')
        print(*words[:no_word], sep='\n', end='\n\n')

        print('Examples:')
        for i in range(no_examples):
            print(examples[i])
            print(examples[i+1], '\n')


if __name__ == '__main__':
    obj = Translator()
    obj.start()
