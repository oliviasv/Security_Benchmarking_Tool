from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import Tk, IntVar, Checkbutton, Button, W
import tkinter as tk
import requests
import tarfile
import json
import os
import glob

global filename1
global file_title
global file_content
global logo_image

# downloadUrl = 'https://www.tenable.com/downloads/api/v1/public/pages/download-all-compliance-audit-files/downloads/7472/download?i_agree_to_tenable_license_agreement=true'
#
# req = requests.get(downloadUrl)
# filename = req.url[downloadUrl.rfind('/') + 1:]
#
#
# def download_file(url, file_name=''):
#     try:
#         if file_name:
#             pass
#         else:
#             file_name = req.url[downloadUrl.rfind('/') + 1:]
#
#         with requests.get(url) as req:
#             with open(file_name, 'wb') as f:
#                 for chunk in req.iter_content(chunk_size=8192):
#                     if chunk:
#                         f.write(chunk)
#             return file_name
#     except Exception as e:
#         print(e)
#         return None
#
#
# def exctract_file():
#     download_file(downloadUrl, 'audits.tar.gz')
#     tar = tarfile.open('audits.tar.gz')
#     tar.extractall()


root = tk.Tk()
root.title("Security Benchmarking Tool")
root.geometry("700x500")
root.resizable(False, False)


def file_parser(filename):
    file = open(filename, "r")
    file_read = file.read().replace('\n', ',')

    pattern = r'<custom_item>(.*?)</custom_item>'

    x = re.findall(pattern, file_read)
    x = [i.split(',') for i in x]

    audit_dict = {}

    for i in range(0, len(x)):
        store_policy = {}
        for j in x[i]:
            key_word = re.search(":", j)
            if key_word:
                j = j.replace('"', '')
                line = j.split(':')
                store_policy[line[0].strip()] = line[1].strip()
        audit_dict[i] = store_policy

    file_2 = open('AU_file.json', "w")
    file_2.write(json.dumps(audit_dict))
    file.close()
    file_2.close()
    re.purge()


def title_box(filename):
    adder = f'{filename}'
    file_title.insert('1.0', adder)


def content_box():
    AU_file = open('AU_file.json', "r").read()
    data = json.loads(AU_file)
    adder = f''
    for key in data:
        adder += data[key]['description']
        adder += '\n'
    file_content.insert('1.0', adder)


def open_file():
    title = "Select Audit File"
    filetypes = (('Audit files', '.audit'), ('all files', '.*'))
    this_file = filedialog.askopenfilename(initialdir='C:\\Users\Asus\Desktop\portal_audits\Windows', title=title, filetypes=filetypes)
    filename = this_file.split('/')[-1]
    file_parser(this_file)
    title_box(filename)
    content_box()


def save_file():
    filename = filedialog.asksaveasfilename(initialdir=".", title='Save Audit File', defaultextension='.audit')
    if filename is None:
        return
    os.system(filename1, filename)


def open_help():
    help_root = Toplevel(root)
    help_root.title("SBT | Help")
    help_root.geometry("520x430")
    logo = Label(help_root, text="", image=logo_image)
    logo.place(x=1, y=1)
    greetings = Label(help_root, text="As we are still developing this app, there is no need (yet) for this section to be completed.")
    greetings.place(x=20, y=215)
    help_root.config()


def open_about():
    about_root = Toplevel(root)
    about_root.title("SBT | About")
    about_root.geometry("520x430")
    logo = Label(about_root, text="", image=logo_image)
    logo.place(x=1, y=1)
    greetings = Label(about_root, text="This is a currently developing Security Benchmarking Tool (SBT)")
    greetings.place(x=95, y=215)

def find_text():
    file_content.tag_remove('found', '1.0', END)
    s = text_search.get()
    if s:
        idx = '1.0'
        while 1:
            idx = file_content.search(s, idx, nocase=1, stopindex=END)
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(s))
            file_content.tag_add('found', idx, lastidx)
            idx = lastidx
    file_content.tag_config('found', foreground='#e68a00')
    text_search.focus_set()


menu_bar = Menu(root, background='#d8dada', foreground='black', activebackground='#e68a00', activeforeground='black')
root.config(menu=menu_bar)

menu_logo = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="SBT", menu=menu_logo)

file_menu = Menu(menu_bar, tearoff=0, background='#d8dada', foreground='black', activebackground='#e68a00', activeforeground='black')

menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Download")
                      # command=lambda: [download_file(downloadUrl), exctract_file()])
file_menu.add_command(label="Import", command=lambda: open_file())
file_menu.add_command(label="Save as", command=lambda: save_file())
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

help_menu = Menu(menu_bar, tearoff=0, background='#d8dada', foreground='black', activebackground='#e68a00', activeforeground='black')
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Help", command=open_help)
help_menu.add_command(label="About", command=open_about)

display = Label(root, text='File:', background='#575b59', foreground='white', font=("Helvetica", 15))
display.place(x=5, y=8)

file_title = Text(bg='white', foreground='#575b59', cursor='arrow')
file_title.place(x=50, y=10, height=27, width=640)

button_search = Button(root, text='Find', background='#e68a00', activebackground='#e68a00', foreground='black')
button_search.place(x=640, y=45, height=25, width=50)
button_search.config(command=find_text)

text_search = Entry(root, foreground='#575b59', font=("Helvetica", 10))
text_search.place(x=50, y=45, height=25, width=585)
text_search.focus_set()

file_content = Text(root, background='white', foreground='#575b59',  cursor='arrow')
file_content.place(x=50, y=90, height=400, width=640)
scroll_bar = Scrollbar(root, command=file_content.yview)
file_content.configure(yscrollcommand=scroll_bar.set)
scroll_bar.pack(side="right")

photo = PhotoImage(file=r"logo.png")
logo_image = photo.subsample(1, 1)

root.config(background='#575b59', menu=menu_bar)
root.mainloop()
