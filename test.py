from tkinter import *
from tkinter import messagebox
from translator import Translator
import os


class Interface(Translator):

    def dir_hist(self): # changes the current working directory to the history folder
        path = os.path.join(os.getcwd(), 'History')
        os.chdir(path)

    def display_interface(self): # will be used for error handling leave for now
        messagebox.showwarning('Error', message='Invalid Input')

    def displayList(self): # Reads the file ONLY IF THE FILE IS PRESENT
        self.dir_hist()
        file_name = 'English_to_Spanish_thank you.txt'  #'English_to_Spanish_hello.txt'
        mylist = Listbox(self.root,  width=60)
        with open(file_name, 'r', encoding='utf-8') as file_out:
            for line in file_out:
                mylist.insert(END, line)
        mylist.pack(side=RIGHT, fill=BOTH)

    def user_inp(self): # incomplete neeche la code bekar h
        varstr = StringVar(self.root)
        varstr.set(self.lang_list[2])
        popup = OptionMenu(self.root, varstr, *self.lang_list)
        Label(self.root, text='Choose a language').grid(row=1, column=1)
        popup.grid(row=2, column=1)

    def __init__(self): # you know what this is
        super().__init__()
        self.root = Tk()
        self.root.title('Test')
        self.root.geometry('800x600')


inter = Interface()

inter.displayList()
inter.root.mainloop()
