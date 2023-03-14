from PyPDF2 import PdfReader, PdfWriter
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
import fitz


infile = r'.\1.pdf'
outfile = r'.\2.pdf'

pdf_input = PdfReader(open(infile, 'rb'))
page = pdf_input.pages[0]
width = float(page.mediabox.width)
height = float(page.mediabox.height)

global bian
bian = 'y1'
global w, h
w, h = width, height
global line1, line2,line3,line4
line1, line2,line3,line4 = None, None, None, None

win = Tk()
canvas = Canvas(win, width=int(width) + 1, height=int(height) + 1)
pdf_doc = fitz.open(infile)
page = pdf_doc.load_page(0)
pix = page.get_pixmap()
pdf_img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
tk_img = ImageTk.PhotoImage(pdf_img)
canvas.create_image((0, 0), anchor="nw", image=tk_img)
canvas.pack()


def key(event):
    global bian
    t = event.char
    if t == 'w':
        bian = 'y1'
    if t == 'a':
        bian = 'x1'
    if t == 's':
        bian = 'y2'
    if t == 'd':
        bian = 'x2'
    if t == 'e':
        global line1, line2, line3, line4
        pdf_output = PdfWriter()
        page = pdf_input.pages[0]
        y1 = canvas.coords(line1)[1]
        x1 = canvas.coords(line2)[0]
        y2 = canvas.coords(line3)[1]
        x2 = canvas.coords(line4)[0]
        page.mediabox.lower_left = (x1, h - y1)
        page.mediabox.lower_right = (x2, h - y1)
        page.mediabox.upper_left = (x1, h - y2)
        page.mediabox.upper_right = (x2, h - y2)
        pdf_output.add_page(page)

        # 7. 循环所有的页数后，将文件输出为 pdf 文件
        pdf_output.write(open(outfile, 'wb'))
        print('保存成功！')


canvas.bind('<Key>', key)
canvas.focus_set()


def callback(event):
    global bian
    global w, h
    global line1, line2, line3, line4
    if bian == 'y1':
        if line1:
            canvas.delete(line1)
        line1 = canvas.create_line(0, event.y, w, event.y)
    if bian == 'x1':
        canvas.delete(line2)
        line2 = canvas.create_line(event.x, 0, event.x, h)
    if bian == 'y2':
        canvas.delete(line3)
        line3 = canvas.create_line(0, event.y, w, event.y)
    if bian == 'x2':
        canvas.delete(line4)
        line4 = canvas.create_line(event.x, 0, event.x, h)


canvas.bind('<Button-1>', callback)

win.mainloop()
