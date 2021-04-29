# Import statements
from tkinter import Tk, Label, Button, StringVar, LEFT, X, BOTH, Spinbox, END, Frame
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter import scrolledtext
from tkinter.ttk import Combobox
import pyttsx3
import PyPDF2
from time import sleep

# initialization 
engine = pyttsx3.init('sapi5')
root = Tk()
root.title("Pdf Reader")
root.minsize(650, 650)

# file load function
def loadPdf():

    file = askopenfilename(defaultextension = ".pdf", filetypes = [("pdf files", "*.pdf")])
    
    try:
        book = open(file, 'rb')
        filename = file.split('/')
        title_lbl.config(text=filename[-1])

        global pdf

        pdf = PyPDF2.PdfFileReader(open(file, 'rb'))
        global pages

        pages = pdf.numPages

        # print(pages)

        pageNum.config(to=pages-1)

        pdf_read = pdf.getPage(0)
        global content

        content = pdf_read.extractText()

        textbox.delete(1.0, END)
        for line in content:
            textbox.insert(END, line)
    except Exception as e:
        print("")
        title_lbl.config(text="label")

# Previous page
def prevpage(event):
    global pdf
    try:
        if int(pageNum.get()) == 0:
            return
        else:
            currentPage = int(pageNum.get())-1

        if int(currentPage) < 0:

            currentPage = 0

            pageNum.delete(0,END)

            pageNum.insert(END, 0)

        # print(currentPage)

        pageNum.delete(0, END)

        pageNum.insert(END, currentPage)

        pdf_read = pdf.getPage(int(currentPage))
        textbox.delete(1.0, END)

        global txt
        txt = pdf_read.extractText()
        for line in txt:
            textbox.insert(END, line)
    except Exception as e:
        print("")
        showerror(title= "Error changing page", message= "Please load the PDF")

def nextpage(event):
    global pages, pdf
    try:
        currentPage = int(pageNum.get())+1
        if int(currentPage) > pages:
            currentPage = pages-1
            pageNum.delete(0,END)
            pageNum.insert(END, pages-1)

        pageNum.delete(0, END)
        pageNum.insert(END, currentPage)

        pdf_read = pdf.getPage(int(currentPage))
        textbox.delete(1.0, END)

        global txt
        txt = pdf_read.extractText()
        textbox.insert(END, txt)

    except Exception as e:
        print("")
        showerror(title= "Error changing page", message= "Please load the PDF")


def goto():
    global pages, pdf
    try:
        goto_page = pageNum.get()
        if int(goto_page) < 0 or int(goto_page) > pages-1:
            showerror(title="Page not found",
                    message="Enter the valid page number.")
        else:
            goto_txt = pdf.getPage(int(goto_page))
            textbox.delete(1.0, END)
            global goto_extractTxt
            goto_extractTxt = goto_txt.extractText()
            textbox.insert(END, goto_extractTxt)
    except Exception as e:
        print("")
        showerror(title= "Error changing page", message= "Please load the PDF")

def readPdf():
    try:
        readtxt = textbox.get(1.0,END)
        read = engine.say(readtxt)

        engine.runAndWait()
    except Exception as e:
        print("")
        showerror(title="Error reading the content", message="Unable to read the PDF, Please load the PDF")


title_lbl = Label(text="label", bg="black", fg="white")
title_lbl.pack(padx=30, pady=10, ipadx=30, ipady=10, fill=X)

textbox = scrolledtext.ScrolledText(root, bg="white", fg="black", cursor="arrow",
 font = ("times new roman", 10, "bold"))
textbox.pack(expand =1, fill = BOTH)


load_btn = Button(text="Load PDF", bg="black", pady=5, fg="white",command= loadPdf)
load_btn.pack(side=LEFT, expand=1, pady=20, ipadx=10)

prevPage_btn = Button(text="Previous", pady=5, bg = "green")
prevPage_btn.pack(side=LEFT, expand=1, pady=20, ipadx=10)
prevPage_btn.bind("<Button-1>", prevpage)

pageNum = Spinbox(root, from_=0, to=100, increment=1)
pageNum.pack(side=LEFT, expand=1)

nxtPage_btn = Button(text="Next", pady=5, bg = "green")
nxtPage_btn.pack(side=LEFT, expand=1, pady=20, ipadx=10)
nxtPage_btn.bind("<Button-1>", nextpage)

goto_btn = Button(text="Go To", bg="green", pady=5, command=goto)
goto_btn.pack(side=LEFT, pady=20, ipadx=10)


read_btn = Button(text="Read Page", bg="black",padx=10 ,pady=5, fg="white",command= readPdf)
read_btn.pack(expand=1, padx=20, pady=20, ipadx=10)

root.mainloop()

