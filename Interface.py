from tkinter import *
from tkinter import messagebox, ttk
from translator import Translator
from PIL import Image, ImageTk
import os


class Interface(Translator):
    @staticmethod
    def start():
        inter.front_image()
        inter.quit_cont_btns()
        inter.root.mainloop()

    def dir_hist(self):
        path = os.path.join(self.owd, 'History')
        os.chdir(path)

    def displayList(self):
        self.dir_hist()
        mylist = Text(self.frame2, font=('Arial', 15), bg="#f8f8f8", borderwidth=0)
        mylist.config(height=self.frame2.winfo_screenheight(), width=self.frame2.winfo_screenwidth(), padx=10, pady=10)
        if os.access(self.path, os.R_OK):
            with open(self.path, 'r', encoding='utf-8') as file_out:
                for line in file_out:
                    mylist.insert(END, line)
            mylist.place(relx=0, rely=0)
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
            os.chdir(self.owd)
            return

    def button_src(self):
        src_label = Label(self.frame1, text='Select the source language :',
                          font=("Calibri", 20), fg="dodgerblue", bg="#fff")
        src_label.pack(fill=BOTH, padx=10, pady=10)
        src_lang = StringVar(self.frame1)
        src_drop = ttk.Combobox(self.frame1, textvariable=src_lang, font=self.style)
        src_drop['values'] = self.lang_list
        src_drop.pack(fill=X, padx=25, pady=15)
        return src_lang

    def button_trans(self):
        trans_label = Label(self.frame1, text='Select the language to translate to : ',
                            font=("Calibri", 20), fg="dodgerblue", bg="#fff")
        trans_label.pack(fill=BOTH, padx=10, pady=10)
        trans_lang = StringVar(self.frame1)
        trans_drop = ttk.Combobox(self.frame1, textvariable=trans_lang, font=self.style)
        trans_drop['values'] = self.lang_list
        trans_drop.pack(fill=X, padx=25, pady=15)
        return trans_lang

    def inp_word(self):
        word_label = Label(self.frame1, text='Enter the word : ', font=("Calibri", 20), fg="dodgerblue", bg="#fff")
        word_label.pack(fill=BOTH, padx=10, pady=10)

        word = StringVar(self.frame1)
        wordbox = Entry(self.frame1, textvariable=word, font=self.style, borderwidth=2)
        wordbox.pack(fill=X, padx=25, pady=15)
        return word

    def user_inp(self):
        src_lang = self.button_src()
        trans_lang = self.button_trans()
        word = self.inp_word()
        data = [src_lang, trans_lang, word]

        tran_btn_img = Image.open('image/button_translate.png')
        b3 = ImageTk.PhotoImage(tran_btn_img)
        t_btn = Button(self.frame1, image=b3, bg="#fafafa", borderwidth=0,command=lambda: self.recall(data), font=self.style)
        t_btn.pack(side=LEFT, expand=True)
        t_btn.image = b3

    def front_image(self):
        img_name = Image.open('image/logo.PNG')
        photo = ImageTk.PhotoImage(img_name)
        img_label = Label(self.root, image=photo, borderwidth=0, bg="#fafafa")
        img_label.image = photo
        img_label.pack(fill=BOTH)

    def quit_cont_btns(self):
        # Quit Button
        quit_btn_img = Image.open('image/button_quit.png')
        b1 = ImageTk.PhotoImage(quit_btn_img)
        q_btn = Button(self.root, image=b1, bg="#fafafa", borderwidth=0, command=lambda: self.root.destroy())
        q_btn.pack(side=LEFT, expand=True)
        q_btn.image = b1

        # Continue Button
        cont_btn_img = Image.open('image/button_continue.png')
        b2 = ImageTk.PhotoImage(cont_btn_img)
        c_btn = Button(self.root, image=b2, bg="#fafafa", borderwidth=0, command=lambda: self.next_window())
        c_btn.pack(side=RIGHT, expand=True)
        c_btn.image = b2

    def next_window(self):
        widget_list = self.root.winfo_children()
        for item in widget_list:
            item.pack_forget()

        self.create_layout()

    def create_layout(self):
        self.frame1 = self.create_frames(3, "white")
        self.frame2 = self.create_frames(2, "#f8f8f8")
        inter.user_inp()

    def create_frames(self, val, bg_col):
        wid = self.root.winfo_screenwidth()
        f = Frame(self.root, bg=bg_col, width=wid / val)
        f.pack(fill=BOTH, side=LEFT, expand=True)
        return f

    def __init__(self):
        super().__init__()
        self.owd = os.getcwd()
        self.root = Tk()
        self.root.config(bg="#fafafa")
        self.root.title('Multilingual Translator')
        self.style = ("Courier", 16, "bold")
        self.root.option_add('*TCombobox*Listbox.font', self.style)
        self.frame1 = self.frame2 = None
        self.root.geometry('1200x700')


if __name__ == '__main__':
    inter = Interface()
    inter.start()
