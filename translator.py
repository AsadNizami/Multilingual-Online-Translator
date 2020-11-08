import requests
from bs4 import BeautifulSoup


class Translator:

    def start(self):
        self.accept()
        self.display()

    def __init__(self, lang='', word=''):
        self.lang = lang
        self.word = word
        
    def accept(self):
        lang = input('Type "en" if you want to translate from French into English, or "fr" if you want to translate from English into French:')
        word = input('Type the word you want to translate:')
        self.__init__(lang, word)
        print(f'You chose "{lang}" as the language to translate "{word} to".')


    def url_gen(self):
        if self.lang == 'en':
            return f'https://context.reverso.net/translation/french-english/{self.word}'

        if self.lang == 'fr':
            return f'https://context.reverso.net/translation/english-french/{self.word}'

    def connect(self):
        user_agent = 'Mozilla/5.0'
        url = self.url_gen()
        req_obj = requests.get(url, headers={'User-Agent': user_agent})
        print(req_obj.status_code, 'OK')
        return req_obj

    def parse(self):
        data = self.connect().content
        parser = 'html.parser'
        soup = BeautifulSoup(data, parser)
        words = soup.find(id='translations-content').text.split()
        examples = [x.text.strip() for x in soup.find_all(class_=['src ltr', 'trg ltr'])]
        return words, examples

    def display(self):
        word, examples = self.parse()
        print('Translated word:', word, 'Examples:', examples, sep='\n')


if __name__ == '__main__':
    obj = Translator()
    obj.start()
