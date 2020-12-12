from tkinter import *
from tkinter import messagebox, ttk
from translator import Translator
import os


class Interface(Translator):
    @staticmethod
    def start():
        inter.user_inp()
        inter.root.mainloop()

    def dir_hist(self):
        path = os.path.join(self.owd, 'History')
        os.chdir(path)

    def displayList(self):
        self.dir_hist()
        mylist = Listbox(self.root, width=400, height=600)
        if os.access(self.path, os.R_OK):
            with open(self.path, 'r', encoding='utf-8') as file_out:
                for line in file_out:
                    mylist.insert(END, line)
            mylist.place(relx=0.35)
            del mylist
        else:
            self.err_hand(unknown_word=self.word)
        os.chdir(self.owd)

    def check(self):
        if os.access(self.path, os.R_OK):
            self.displayList()
        else:
            req_obj_list = self.connect()
            for req_obj in req_obj_list:
                self.formatting(req_obj=req_obj)
            self.displayList()

    @staticmethod
    def err_hand(unknown_lang=None, unknown_word=None, inv_inp=False, same=False):
        if inv_inp:
            messagebox.showwarning('Warning', message=f'Invalid Input')
        if unknown_lang:
            messagebox.showwarning('Warning', message=f'Translator does not support {unknown_lang}')
        if unknown_word:
            messagebox.showwarning('Warning', message=f'No result found for {unknown_word}')
        if same:
            messagebox.showwarning('Warning', message=f'Cannot translate to same the language')

    def err_check(self, src_lang, trans_lang, word):
        if '' in [src_lang, trans_lang, word]:
            self.err_hand(inv_inp=True)
            return False
        if src_lang == trans_lang:
            self.err_hand(same=True)
            return False
        if src_lang or trans_lang:
            if src_lang not in self.lang_list:
                self.err_hand(unknown_lang=src_lang)
                return False
            if trans_lang not in self.lang_list:
                self.err_hand(unknown_lang=trans_lang)
                return False
            return True
        return True

    def recall(self, args):
        data = [x.get() for x in args]
        path = self.create_dir()
        src_lang = data[0].capitalize()
        trans_lang = data[1].capitalize()
        word = data[2]
        signal = self.err_check(src_lang, trans_lang, word)
        if signal:
            super().__init__(path=path, src_lang=src_lang, trans_lang=trans_lang, word=word)
            self.check()
        else:
            return

    def button_src(self):
        src_label = Label(self.root, text='Select the source language : ')
        src_label.config(font=self.style)
        src_label.place(relx=0.01, rely=0.02)
        src_lang = StringVar(self.root)
        src_drop = ttk.Combobox(self.root, width=35, textvariable=src_lang, font=('Arial', 10, 'bold'))
        src_drop['values'] = self.lang_list
        src_drop.place(relx=0.015, rely=0.06)
        return src_lang

    def button_trans(self):
        trans_label = Label(self.root, text='Select the language to translate to : ')
        trans_label.place(relx=0.01, rely=0.16)
        trans_label.config(font=self.style)
        trans_lang = StringVar(self.root)
        trans_drop = ttk.Combobox(self.root, width=35, textvariable=trans_lang, font=('Arial', 10, 'bold'))
        trans_drop['values'] = self.lang_list
        trans_drop.place(relx=0.015, rely=0.2)
        return trans_lang

    def inp_word(self):
        word_label = Label(self.root, text='Enter the word : ',
                           bd=3)
        word_label.config(font=self.style)
        word_label.place(relx=0.01, rely=0.30)

        word = StringVar(self.root)
        wordbox = Entry(self.root, width=45, textvariable=word, font=('Arial', 11, 'bold'))
        wordbox.place(relx=0.015, rely=0.35)
        return word

    def user_inp(self):
        src_lang = self.button_src()
        trans_lang = self.button_trans()
        word = self.inp_word()
        data = [src_lang, trans_lang, word]

        button = Button(self.root, text='Translate', width=20, command=lambda: self.recall(data), font=self.style)
        button.place(relx=0.017, rely=0.5)

    def __init__(self):
        super().__init__()
        self.owd = os.getcwd()
        self.root = Tk()
        self.root.config(bg='#D8D8D8')
        self.root.title('Multilingual Translator')
        self.root.geometry('1200x700')
        self.style = ('Courier', 12, 'bold')


if __name__ == '__main__':
    inter = Interface()
    inter.start()