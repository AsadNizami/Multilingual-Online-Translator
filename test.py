from tkinter import *
from tkinter import messagebox, ttk
from translator import Translator
import os


class Interface(Translator):

    def dir_hist(self): # changes the current working directory to the history folder
        path = os.path.join(self.owd, 'History')
        os.chdir(path)

    def display_interface(self):  # will be used for error handling leave for now
        messagebox.showwarning('Error', message='Invalid Input')

    def displayList(self):  # Reads the file ONLY IF THE FILE IS PRESENT
        self.dir_hist()
        # file_name = 'English_to_Spanish_thank you.txt'  # 'English_to_Spanish_hello.txt'
        mylist = Listbox(self.root, width=400, height=600)
        with open(self.path, 'r', encoding='utf-8') as file_out:
            for line in file_out:
                mylist.insert(END, line)
        mylist.place(relx=0.35)
        del mylist
        os.chdir(self.owd)

    def testdisplay(self, args):
        data = [x.get() for x in args]
        path = self.create_dir()
        print(path)
        src_lang = data[0]
        trans_lang = data[1]
        word = data[2]
        super().__init__(path=path, src_lang=src_lang, trans_lang=trans_lang, word=word)

        if os.access(self.path, os.R_OK):
            self.displayList()
        else:
            req_obj_list = self.connect()
            for req_obj in req_obj_list:
                self.formatting(req_obj=req_obj)
            self.displayList()

    def user_inp(self):
        style = ('Courier', 12)
        src_label = Label(self.root, text='Select the source language : ')  # grid(column=0, row=0, padx=10)
        src_label.config(font=style)
        src_label.place(relx=0.01, rely=0.02)
        src_lang = StringVar(self.root)
        src_drop = ttk.Combobox(self.root, width=35, textvariable=src_lang)
        src_drop['values'] = self.lang_list
        src_drop.place(relx=0.015, rely=0.06)

        trans_label = Label(self.root, text='Select the language to translate to : ')  # grid(column=0, row=0, padx=10)
        trans_label.place(relx=0.01, rely=0.16)
        trans_label.config(font=style)
        trans_lang = StringVar(self.root)
        trans_drop = ttk.Combobox(self.root, width=35, textvariable=trans_lang)
        trans_drop['values'] = self.lang_list
        trans_drop.place(relx=0.015, rely=0.2)

        word = StringVar(self.root)
        wordbox = Entry(self.root, width=45, textvariable=word)
        wordbox.place(relx=0.015, rely=0.35)
        data = [src_lang, trans_lang, word]
        button = Button(self.root, text='Translate', width=20, command=lambda: self.testdisplay(data))
        button.place(relx=0.017, rely=0.5)

    def __init__(self): # you know what this is
        self.owd = os.getcwd()
        super().__init__()
        self.root = Tk()
        self.root.title('Test')
        self.root.geometry('1200x700')


inter = Interface()
inter.user_inp()
# inter.displayList()
inter.root.mainloop()
