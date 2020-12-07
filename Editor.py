# =============================================================================
# Created By  : Vikas Bhat
# Created Date: Sun August 25 18:54:00 PDT 2018
# =============================================================================


from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser


root = Tk()
root.title('My Text Editor')
root.geometry("1300x900")

# To open file
global check_status
check_status = False
global selected
selected = False


# New File
def new_file():
    # Delete previous
    new_text.delete("1.0", END)
    # Update status
    root.title('New File - TextPad!')
    status_bar.config(text="New File")

    global check_status
    check_status = False


# Open Files
def open_file():
    # Delete previous
    new_text.delete("1.0", END)

    # Grab Filename
    file_open = filedialog.askopenfilename(initialdir="C:/gui/", title="Open File", filetypes=(
    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if file_open:
        global check_status
        check_status = file_open

    name = file_open
    status_bar.config(text=f'{name} ')
    name = name.replace("C:/gui/", "")
    root.title(f'{name} - TextPad!')

    # Open the file
    text_file = open(file_open, 'r')
    stuff = text_file.read()

    new_text.insert(END, stuff)

    text_file.close()


# Save As File
def save_as_file():
    file_save = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File", filetypes=(
    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if file_save:
        # Update Status
        name = file_save
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace("C:/gui/", "")
        root.title(f'{name} - TextPad!')

        # Save  file
        text_file = open(file_save, 'w')
        text_file.write(new_text.get(1.0, END))

        text_file.close()


# Save File
def save_file():
    global check_status
    if check_status:
        # Save the file
        text_file = open(check_status, 'w')
        text_file.write(new_text.get(1.0, END))

        text_file.close()

        status_bar.config(text=f'Saved: {check_status}        ')
        name = check_status
        name = name.replace("C:/gui/", "")
        root.title(f'{name} - TextPad!')
    else:
        save_as_file()


# Cut Text
def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if new_text.selection_get():
            # Grab selected text
            selected = new_text.selection_get()
            # Cut Selected Text
            new_text.delete("sel.first", "sel.last")

            root.clipboard_clear()
            root.clipboard_append(selected)


# Copy Text
def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    if new_text.selection_get():
        # Grab selected text
        selected = new_text.selection_get()

        root.clipboard_clear()
        root.clipboard_append(selected)


# Paste Text
def paste_text(e):
    global selected
    # Check to see if keyboard shortcut used
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = new_text.index(INSERT)
            new_text.insert(position, selected)


# Bold Text
def bold_it():
    # Create our font
    tex_bold = font.Font(new_text, new_text.cget("font"))
    tex_bold.configure(weight="bold")

    new_text.tag_configure("bold", font=tex_bold)

    current_tags = new_text.tag_names("sel.first")

    if "bold" in current_tags:
        new_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        new_text.tag_add("bold", "sel.first", "sel.last")


# Change Color
def text_color():
    # Pick color
    my_color = colorchooser.askcolor()[1]
    if my_color:
        # Create  font
        change_color = font.Font(new_text, new_text.cget("font"))

        new_text.tag_configure("colored", font=change_color, foreground=my_color)

        # Define Current tags
        current_tags = new_text.tag_names("sel.first")

        # If statment to see if tag has been set
        if "colored" in current_tags:
            new_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            new_text.tag_add("colored", "sel.first", "sel.last")


# Change background color
def bg_color():
    new_color = colorchooser.askcolor()[1]
    if new_color:
        new_text.config(bg=new_color)


# Select all Text
def select_all(e):
    new_text.tag_add('sel', '1.0', 'end')


# Clear All Text
def clear_all():
    new_text.delete(1.0, END)


# Create a toolbar
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create  Frame
new_frame = Frame(root)
new_frame.pack(pady=5)

# Create  Scrollbar
text_scroll = Scrollbar(new_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Horizontal Scrollbar
scroll_hz = Scrollbar(new_frame, orient='horizontal')
scroll_hz.pack(side=BOTTOM, fill=X)

# Create Text Box
new_text = Text(new_frame, width=97, height=25, font=("Calibri", 12), selectbackground="red", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=scroll_hz.set)
new_text.pack()

text_scroll.config(command=new_text.yview)
scroll_hz.config(command=new_text.xview)

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste ", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_command(label="Undo", command=new_text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Redo", command=new_text.edit_redo, accelerator="(Ctrl+y)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=lambda: select_all(True), accelerator="(Ctrl+a)")
edit_menu.add_command(label="Clear", command=clear_all)

color_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Selected Text", command=text_color)
color_menu.add_command(label="Background", command=bg_color)

options_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Options", menu=options_menu)

status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

root.bind('<Control-A>', select_all)
root.bind('<Control-a>', select_all)

bold_button = Button(toolbar_frame, text="Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5, pady=5)


undo_button = Button(toolbar_frame, text="Undo", command=new_text.edit_undo)
undo_button.grid(row=0, column=2, padx=5, pady=5)
redo_button = Button(toolbar_frame, text="Redo", command=new_text.edit_redo)
redo_button.grid(row=0, column=3, padx=5, pady=5)


color_text_button = Button(toolbar_frame, text="Text Color", command=text_color)
color_text_button.grid(row=0, column=4, padx=5, pady=5)

root.mainloop()


