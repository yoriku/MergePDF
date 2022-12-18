import os,sys
import PyPDF2
import glob
import tkinter
from tkinter import filedialog
def file_select():
    file_path = tkinter.filedialog.askdirectory()
    directory_input.delete(0, tkinter.END)
    directory_input.insert(tkinter.END, file_path)

def make_pdf(d,f):
    files = sorted(glob.glob(d + '/*.pdf'))


    merger = PyPDF2.PdfFileMerger()
    for i in range(len(files)):
        merger.append(files[i])


    merger.write(f + '.pdf')
    display_progress("Merged All File")
    merger.close()

def display_progress(input):
    results["text"] = input

def get_param():
    if os.path.exists(directory_input.get()):
        directory_path = directory_input.get()
        filename = filename_input.get()

        make_pdf(directory_path, filename)
    else:
        display_progress("Not Exist Directory")

root = tkinter.Tk()
root.title("PDF結合")
root.geometry("600x300")

directory_label = tkinter.Label(text="入力ディレクトリ")
directory_label.grid(row = 0, column = 0, pady=20)
directory_input = tkinter.Entry()
directory_input.grid(row = 0, column = 1, sticky=tkinter.EW, pady=20)
find_button = tkinter.Button(text="参照",command=file_select)
find_button.grid(row = 0, column = 2, pady=20)

filename_label = tkinter.Label(text="結合後ファイル名")
filename_label.grid(row = 1, column = 0, pady=20)
filename_input = tkinter.Entry()
filename_input.insert(0, "merge")
filename_input.grid(row = 1, column = 1, sticky=tkinter.EW, pady=20)

exe_button = tkinter.Button(text="実行",command=get_param)
exe_button.grid(row = 2, column = 0, sticky=tkinter.EW, columnspan = 3, pady=20)

results = tkinter.Label(text="")
results.grid(row = 4, column = 0, sticky=tkinter.EW, columnspan = 3, pady=20)

root.grid_columnconfigure(1, weight=1)

root.mainloop()
