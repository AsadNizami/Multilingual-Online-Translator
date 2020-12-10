from tkinter import *
from tkinter import ttk
from translator import *

root = Tk()
root.title("Translator")
root.geometry("400x500")

# scrollbar (For now, scrollbar code is copied. Comments will make it easy to understand how it works)

# Create A Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

# Create A Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

# Add A Scrollbar To The Canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Configure The Canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

# Create ANOTHER Frame INSIDE the Canvas
frame = Frame(my_canvas)

# Add that New frame To a Window In The Canvas
my_canvas.create_window((0,0), window=frame, anchor="nw")

## all the functions are below

def translate():
    final_output = Label(frame, padx = 100, pady = 200)
    output = Translator(set_src_lang.get(), set_trans_lang.get(), src_text.get())
    global_final_lang, global_words, global_examples, global_no_word = output.display()

    translations_label = Label(frame, text = f'{global_final_lang} Translations:\n')
    translations_label.pack()
    for _itr in range(global_no_word):
        words_label = Label(frame, text = f'{global_words[_itr]} \n')
        words_label.pack()

    examples_label = Label(frame, text = f'{global_final_lang} Examples:\n')
    examples_label.pack()
    
    for i in range(global_no_word):
        example1_lable = Label(frame, text = f'{global_examples[i]} \n')
        example1_lable.pack()
        example2_lable = Label(frame, text = f'{global_examples[i + 1]} \n\n')
        example2_lable.pack()
        i += 2
        print('\n')

## all the buttons are below. formatting can be done here

welcome_line = Label(frame, text = "Welcome to our translator. Enter you text: ")

src_text = Entry(frame, width = 50) #input field

set_src_lang = StringVar()      # dropdown menu variable data-type
set_src_lang.set('English')     #default value on drop-down

set_trans_lang = StringVar()
set_trans_lang.set('Arabic')

                               ###drop-downs

src_lang_drop = OptionMenu(frame, set_src_lang, 'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish')

trans_lang_drop = OptionMenu(frame, set_trans_lang, 'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish')

translate_button = Button(frame, text="translate", command = translate)

## position of all buttons can be changed here

welcome_line.pack()
src_text.pack()
src_lang_drop.pack()
trans_lang_drop.pack()
translate_button.pack()


frame.mainloop()