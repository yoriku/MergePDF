import os,sys
import PyPDF2
import glob
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileReader, PdfFileWriter

def file_select():
    file_path = filedialog.askdirectory()
    directory_input.delete(0, tk.END)
    directory_input.insert(tk.END, file_path)

def resize(files):
    A4_WIDTH = 595.0
    A4_HEIGHT = 842.0
    path = []
    for i, file in enumerate(files):
        resize_path = file + "_resize.pdf"
        pdf = PdfFileReader(file, strict=False)
        out_pdf = PdfFileWriter()

        for page in range(pdf.getNumPages()):
            page_obj = pdf.getPage(page)
            page_obj.scale_to(A4_WIDTH,A4_HEIGHT)
            out_pdf.addPage(page_obj)

        with open(resize_path, "wb") as fp:
            out_pdf.write(fp)
        path.append(resize_path)
    display_progress("Process: Resized to A4")
    return path

def make_pdf(d,f,change_size = 0):
    files = sorted(glob.glob(d + '/*.pdf'))
    if change_size:
        files = resize(files)

    merger = PyPDF2.PdfFileMerger(strict=False)
    for i in range(len(files)):
        merger.append(files[i])
        display_progress("Process: Merging... " + files[i] + " (" + str(i+1) + "/" + str(len(files)) + ")")
        
    made_file = f + '.pdf'
    merger.write(made_file)
    display_progress("Successfully: Merged All Files and Made File " + made_file)
    merger.close()
    if change_size:
        for i, file in enumerate(files):
            os.remove(file)

def display_progress(input):
    tex.insert(tk.END, input + "\n") 

def get_param():
    tex.delete("1.0","end")
    if os.path.exists(directory_input.get()):
        directory_path = directory_input.get()
        filename = filename_input.get()
        size_flag = var_checkbutton.get()

        make_pdf(directory_path, filename,change_size=size_flag)
    else:
        display_progress("Error: Not Exist Directory")

root = tk.Tk()
root.title("PDF結合")
root.geometry("600x400")

directory_label = ttk.Label(text="入力ディレクトリ")
directory_label.grid(row = 0, column = 0, pady=10)
directory_input = ttk.Entry()
directory_input.grid(row = 0, column = 1, sticky=tk.EW, pady=10)
find_button = ttk.Button(text="参照",command=file_select)
find_button.grid(row = 0, column = 2, pady=10)

filename_label = ttk.Label(text="結合後ファイル名")
filename_label.grid(row = 1, column = 0, pady=10)
filename_input = ttk.Entry()
filename_input.insert(0, "merge")
filename_input.grid(row = 1, column = 1, sticky=tk.EW, pady=10)

var_checkbutton = tk.IntVar(value=1)
checkbutton = ttk.Checkbutton(
    root,
    text="A4サイズに変更するか否か．必要がないときはチェックを外すと高速．",
    variable=var_checkbutton,
    )
checkbutton.grid(row = 2, column = 0, sticky=tk.EW, columnspan = 3, pady=10)

exe_button = ttk.Button(text="実行",command=get_param)
exe_button.grid(row = 3, column = 0, sticky=tk.EW, columnspan = 3, pady=10)

# results = ttk.Label(text="")
# results.grid(row = 4, column = 0, sticky=tk.EW, columnspan = 3, pady=10)

scroll_Y = tk.Scrollbar( orient = 'vertical' )
tex = tk.Text( background = '#F2F2F2', yscrollcommand = scroll_Y.set, height=15)
tex.grid(row = 5, column = 0, columnspan = 3, sticky=tk.EW, pady=10)
scroll_Y[ 'command' ] = tex.yview
scroll_Y.grid(row = 5, column = 2, pady=10)

root.grid_columnconfigure(1, weight=1)
root.mainloop()