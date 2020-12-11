from tkinter import *
from translator import *


class Interface(Translator):
    def __init__(self):
        super().__init__()
        self.root = Tk()
        self.root.title('Multilingual Translator')
        self.root.geometry('800x600')
        self.click_src = StringVar()
        self.click_trans = StringVar()

    def show(self):
        myLabel = Label(self.root, text=self.click_src.get()).pack()

    def user_inp(self):
        src_lang = self.click_src.get()
        trans_lang = self.click_trans.get()
        print(src_lang, trans_lang)

    def design(self):

        self.click_src.set(self.lang_list[2])
        self.click_trans.set(self.lang_list[0])
        drop_src = OptionMenu(self.root, self.click_src, *self.lang_list)
        drop_src.grid(row=1, column=0)
        drop_trans = OptionMenu(self.root, self.click_trans, *self.lang_list)
        # drop_trans.grid(row=10, column=0)
        drop_src.pack()
        drop_trans.pack()

        button = Button(self.root, text='Translate', command=self.user_inp()).pack()
        self.root.mainloop()


if __name__ == '__main__':
    inter = Interface()
    inter.design()
