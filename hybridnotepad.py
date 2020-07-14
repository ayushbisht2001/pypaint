from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
from tkinter.filedialog import *
from math import *
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import PIL.ImageGrab as ImageGrab
from PIL import ImageTk, Image
from sys import argv
import os
import sys
import speech_recognition as sr
import pyttsx3
from win32 import win32api
from pyautogui import *
import gtts
from playsound import playsound

# GOTO
GotoTextBox = 0  # here , we have A vala option for text
GotoFont = 0  # here, we have , font style ,
GotoMenuFile = 0  # here we have Menu bars, File handling , aboutus
GotoTextEditor = 0  # here we have font styles , Italic, bold etc and design vala font , infact it is 3rd row
GotoItems = 0  # it contain , all the general items , pencil , rubber etc
GotoBrushes = 0  # it contain brushes
GotoColorBox = 0  # color box
GotoOutline = 0  # outline and fill option
GotoShapes = 0  # shapes
GotoMoreColors = 0

"""  Created By Ayush Bisht  
    Date of completion :  10 june 2020 
    
    """

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
    


# Main window ............
win = Tk()
win.title("INDIpaint")
win.geometry("1000x600")
# ...............................


# Global variables ...............................................

outLinevar = 'black'
fillvar = ''
X, Y, z, sx, sy, cs, choosebox, zsize = 0, 0, 0, 0, 0, 1, 1, 0
dsp = [20, 30, 50, 60]
all_width = [1, 30, 30]
se = [0, 0, 0, 0]
dColor, Color1, Color2 = "#000000", "#000000", "#ffffff"
text = Text()
dataFromNotePad = ""
x0, y0, w, h = 0, 0, 0, 0
textIndex = -1
TextInPaint = ""
option = "paint"
CursorSet = "arrow"
# ......................................................................


# https://pythonexamples.org/python-tkinter-button-change-font/#:~:text=You%20can%20also%20change%20font,font%20size%20of%20tkinter%20button.

mfont = font.Font(size="15", family='Courier', weight='bold')

win['padx'] = 30
win["bg"] = "black"
win.columnconfigure(0, weight=200)
win.rowconfigure(0, weight=1)
win.rowconfigure(1, weight=0)
win.rowconfigure(2, weight=450)

optionLabel = LabelFrame(win, width='500', height='200', bg="white")
optionLabel.grid(row=0, sticky='nsew', padx=12, pady=2)

textLabel = LabelFrame(win, width='500', height=20, bg="white")
textLabel.grid(row=1, column=0, sticky='nsew', padx=10, pady=2)

contentLabel = Canvas(win, width="500", height="150", highlightthickness=1, highlightbackground="black",
                      background="white", cursor=CursorSet)
contentLabel.grid(row=2, column=0, sticky='news')

optionLabel.rowconfigure(0, weight=10)
optionLabel.columnconfigure(0, weight=30)
optionLabel.columnconfigure(1, weight=30)
optionLabel.columnconfigure(2, weight=30)
optionLabel.columnconfigure(3, weight=0)
optionLabel.columnconfigure(4, weight=0)
optionLabel.columnconfigure(5, weight=0)
optionLabel.columnconfigure(6, weight=20)
optionLabel.columnconfigure(7, weight=30)

items = LabelFrame(optionLabel, text='Tools', labelanchor='s', takefocus=True, fg="grey")
items.grid(row=0, column=0, sticky='nwes', pady=3, padx=1)
Brushes = LabelFrame(optionLabel, text='Brushes', labelanchor='s', takefocus=True, fg="grey")
Brushes.grid(row=0, column=1, sticky='nwes', padx=1, pady=3)
shapes = LabelFrame(optionLabel, text='Shapes', labelanchor='s', takefocus=True, fg="grey")
shapes.grid(row=0, column=2, sticky='nwes', padx=1, pady=3)
out_fill = LabelFrame(optionLabel, relief="flat")
out_fill.grid(row=0, column=3, sticky="nwes", padx=1, pady=3)
size = LabelFrame(optionLabel, text='Size', labelanchor='s', takefocus=True, fg="grey")
size.grid(row=0, column=4, sticky='nwes', padx=1, pady=3)
colorSelect = LabelFrame(optionLabel, takefocus=True, relief="flat", height=2)
colorSelect.grid(row=0, column=5, sticky='nwes', padx=1, pady=3)
colorbox = LabelFrame(optionLabel, text='colorbox', labelanchor='s', takefocus=True, fg="grey")
colorbox.grid(row=0, column=6, sticky='nwes', padx=1, pady=3)
editColor = LabelFrame(optionLabel, text="edit colors", labelanchor='s', takefocus=True, fg="grey")
editColor.grid(row=0, column=7, sticky='nwes', padx=1, pady=3)

GotoTextBox = 1




# Text Box ..................................................................................................................................

""" endCO is used to get  the last coordinate of the rectangle on which we are suppose to insert our text , it basically uses TEXT( )  widget to take the input which is passed off to create_text( ) 
so as to add text to canvas widget.

"""

def endCO(event):
    global se, x0, y0, w
    global t, text, dataFromNotePad, textInCanvas

    class Struct(object):
        pass

    data = Struct()
    data.win = win
    if se[0] < event.x:
        x0 = se[0]
    else:
        x0 = event.x
    if se[1] < event.y:
        y0 = se[1]
    else:
        y0 = event.y

    w, h = abs(event.x - se[0]), abs(event.y - se[1])
    text = Text(contentLabel, width=int(w / 11), height=int(h / 21))
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    text.configure(font=fontText, foreground=Color1)
    t = contentLabel.create_window(x0, y0, window=text, anchor='nw')
    contentLabel.delete(textInCanvasIndexer)


""" 
initialCO  is used to get the initial coordinate of that rectangle with whose reference we are suppose to add text in our canvas widget

"""
def initialCO(event):
    global se, t, textInCanvas, textInCanvasIndexer, textIndex
    if textIndex<1000:
        textIndex += 1
    textInCanvasIndexer = textInCanvas[textIndex]
    se[0], se[1] = event.x, event.y
    contentLabel.delete(t)

""" Here , that rectangle is created . 
"""
def textShape(event):
    global se, k
    contentLabel.delete(k)
    k = contentLabel.create_rectangle(se[0], se[1], event.x, event.y, fill="white", outline="white")

""" here, it clarify wheather you complete you text or not, when completes TextInPaint become "" , and  text is added to  canvas widget
  
  """
def selector(s):
    global t, text, dataFromNotePad, textInCanvas, se, x0, y0, k, w, h, Color1, fontType, textInCanvasIndexer
    global TextInPaint
    TextInPaint = s
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    if TextInPaint == "text":
        contentLabel.bind("<ButtonRelease-1>", endCO)
        contentLabel.bind("<Button-1>", initialCO)
        contentLabel.bind("<B1-Motion>", textShape)
    else:
        dataFromNotePad = text.get(1.0, END)
        textInCanvasIndexer = contentLabel.create_text(x0, y0, text=dataFromNotePad, font=fontText, width=w,
                                                       anchor='nw', fill=Color1)
        contentLabel.delete(t)
        contentLabel.delete(k)

""" here , event is bind to mouse , so that when you press mouse right button then text is added to you canvas widget

"""
def TextChange(event):
    global TextInPaint, polyy1, polyx1, choosebox
    if z==4:
        selector("")
        TextInPaint = ""
        polyx1, polyy1 = 0, 0
        choosebox = 1


k = contentLabel.create_rectangle(0, 0, 0, 0)
textInCanvas = [contentLabel.create_text(0, 0)] * 1000
textInCanvasIndexer = textInCanvas[0]
t = contentLabel.create_window(0, 0)

# .................................................................................................................................................................


GotoFont = 1

# Font Size  and Style  ........................................................................

SizeVar = IntVar()
SizeVar.set(15)
fontFamilyVar = StringVar()
fontFamilyVar.set("Arial")


""" It set the font size for our text editor feature
"""

def getSizeofFont():
    SizeVar.set(textButtonS.get())
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    text.configure(font=fontText, foreground=Color1)
    Notepad.configure(font=fontText, foreground=Color1)

""" It set the font family for our text editor feature

"""
def fontFamilyFun():
    global fontFamilyVar
    fontSt = vb.get()
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    fontFamilyVar.set(lis[fontSt])
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    text.configure(font=fontText, foreground=Color1)
    Notepad.configure(font=fontText, foreground=Color1)
    fontFamily["font"] = (fontFamilyVar.get, 10)


# ............................................................................................


GotoMenuFile = 1
#  Menu Bar  and File Handling .............................................................................

Notepad = Text()
notepadWin = contentLabel.create_window(0, 0)
notePadData = StringVar()
FileSave = None
ScreenShotSave = None
imgt = [None] * 100
imageIndex = 0

""" paintfile :  This one is the main component of this program,  as it did all the stuffs like opeing new file , saving , printing etc
"""
def paintfile(s):
    global ScreenShotSave, imgCanvas, imgt, imageIndex,ir, ic, it, iet, irt, ih1, ih2
    xind = win.winfo_rootx() + contentLabel.winfo_x()
    yind = win.winfo_rooty() + contentLabel.winfo_y()
    xx = xind + contentLabel.winfo_width()
    yy = yind + contentLabel.winfo_height()
    if s == "save":
        if ScreenShotSave == None:
            ScreenShotSave = asksaveasfilename(initialfile='Untitled.png',
                                               defaultextension=".png",
                                               filetypes=[("All Files", "*.*"),
                                                          ("png", "*.png"), ("jpg", "*.jpg"), ("gif", "*.gif")])
            if ScreenShotSave == "":
                ScreenShotSave = None

        ImageGrab.grab(bbox=(xind, yind, xx, yy)).save(ScreenShotSave)

    elif s == "save_as":
        ScreenShotSave = asksaveasfilename(initialfile='Untitled.png',
                                           defaultextension=".png",
                                           filetypes=[("All Files", "*.*"),
                                                      ("png", "*.png"), ("jpg", "*.jpg"), ("gif", "*.gif")])

        ImageGrab.grab(bbox=(xind, yind, xx, yy)).save(ScreenShotSave)
    elif s == "new":
        ir, ic, it, iet, irt, ih1, ih2 = -1, -1, -1, -1, -1, -1, -1
        contentLabel.delete(ALL)
    elif s == "open":
        openImageFile = askopenfilename(defaultextension=".png",
                                        filetypes=[("All Files", "*.*"),
                                                   ("png", "*.png"), ("jpg", "*.jpg"), ("gif", "*.gif")])

        # PIL(python imaging library) is used to work 30 more image formats
        #  http://effbot.org/tkinterbook/photoimage.htm
        resource_path(openImageFile)
        imgResize = Image.open(openImageFile)
        imgResize = imgResize.resize((xx - xind, yy - yind), Image.ANTIALIAS)
        imgt[imageIndex] = ImageTk.PhotoImage(imgResize)
        contentLabel.create_image(0, 0, image=imgt[imageIndex], anchor=NW)
        imageIndex += 1
    elif s == "print":
        if ScreenShotSave != None:
            os.startfile(ScreenShotSave, "print")
    elif s == "exit":
        # t = askokcancel("Quit", "Do you really wish to quit?")

        win.destroy()
        # win.destroy()


def Choice(s):
    global notePadData, notepadWin, Notepad, FileSave, option

    class Struct(object):
        pass

    option = "text"
    Data = Struct()
    Data.win = win
    if s == "text":

        Notepad = Text(contentLabel, width=500, height=500)
        fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                             slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
        Notepad.configure(font=fontText, foreground=Color1)
        notepadWin = contentLabel.create_window(0, 0, window=Notepad, anchor='nw')

    elif s == "save":
        print(Notepad.index("insert"))
        if FileSave == None:
            FileSave = asksaveasfilename(initialfile='Untitled.txt',
                                         defaultextension=".txt",
                                         filetypes=[("All Files", "*.*"),
                                                    ("Text Documents", "*.txt")])
            if FileSave == "":
                FileSave = None
            else:
                file = open(FileSave, 'w')
                file.write(Notepad.get(1.0, END))
                file.close()
        else:
            file = open(FileSave, 'w')
            file.write(Notepad.get(1.0, END))
            file.close()
    elif s == "save_as":
        FileSave = asksaveasfilename(initialfile='Untitled.txt',
                                     defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"),
                                                ("Text Documents", "*.txt")])
        if FileSave == "":
            FileSave = None
        else:
            file = open(FileSave, 'w')
            file.write(Notepad.get(1.0, END))
            file.close()
    elif s == "new":
        Notepad.delete(1.0, END)
    elif s == "print":
        if FileSave != None:
            os.startfile(FileSave, "print")
    elif s == "exit":
        option = "paint"
        contentLabel.delete(notepadWin)


def about_us():
    print("about us")
    about = Tk()
    about.title("ABOUT US")
    about.geometry("500x500")
    aboutText = Text(about, width=90, height=90, )

    aboutText.insert("end",
                     "\t\t\t About - Us \n\n\n Hello friends this is Ayush Bisht and I am a rising software engineer.Lets discuss few things about this application -- IndiPaint ,whch was"
                     " developed and designed under the guidance of expert seniors of BTKIT Dwarahat. This application  is an open source software , user can modified its code "
                     " according to their needs and desire. My main aim is  to implement our Knowledge and creates something new which could help ohters. Indipaint is an INDIAN software"
                     " and freely available to all. This project helps the students to learn Python Programming more precisely. This project gonna be a fun for the beginer who are neophyte in this"
                     " domain , they can easily learn all the major concept of GUI programmming and can create their own projects or their own self made software..."
                     "\n thank you all\n Project Manager \n Ayush Bisht \n............... Happy Coding ")

    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    aboutText.configure(font=fontText, foreground=Color1)
    aboutText.pack()
    about.mainloop()


menuBar = Menu(win)

file = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='File', menu=file)
file.add_command(label='New', command=lambda: paintfile("new"))
file.add_command(label='Open', command=lambda: paintfile("open"))
file.add_command(label='Save', command=lambda: paintfile("save"))
file.add_command(label='Save as', command=lambda: paintfile("save_as"))
file.add_command(label='Print', command=lambda: paintfile("print"))
file.add_command(label='About Us', command=lambda: about_us())
file.add_command(label='Exit', command=lambda: paintfile("exit"))

home = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Home', menu=home)
home.add_command(label="NOTEPAD", command=lambda: Choice('text'))
home.add_command(label='New', command=lambda: Choice('new'))
home.add_command(label='Save', command=lambda: Choice('save'))
home.add_command(label='Save as', command=lambda: Choice('save_as'))
home.add_command(label='Print', command=lambda: Choice('print'))
home.add_command(label='PAINT', command=lambda: Choice('exit'))

# ...........................................................................................


GotoTextEditor = 1
# Text Editor ..........................................................................................................

ItalicVar = StringVar()
BoldVar = StringVar()
UnderVar = BooleanVar()
OverVar = BooleanVar()
ItalicVar.set("roman")
BoldVar.set("normal")
UnderVar.set(False)
OverVar.set(False)


def getTextStyle():
    if var1.get():
        ItalicVar.set("italic")
    else:
        ItalicVar.set("roman")
    if var2.get():
        BoldVar.set("bold")
    else:
        BoldVar.set("normal")

    if var3.get():
        UnderVar.set(True)
    else:
        UnderVar.set(False)

    if var4.get():
        OverVar.set(True)
    else:
        OverVar.set(False)
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    text.configure(font=fontText, foreground=Color1)
    Notepad.configure(font=fontText, foreground=Color1)


textLabel.rowconfigure(0, weight=0)
textLabel.columnconfigure(0, weight=15)
textLabel.columnconfigure(1, weight=17)
textLabel.columnconfigure(2, weight=10)
textLabel.columnconfigure(3, weight=10)

fontFamilyFrame = LabelFrame(textLabel, height=1, foreground="white", background="black")
fontFamilyFrame.grid(row=0, column=0, sticky="news", padx=0)
fontFamily = Menubutton(fontFamilyFrame, textvariable=fontFamilyVar, anchor='n', font=(fontFamilyVar.get(), 10),
                        foreground="white", background="black")
fontFamily.menu5 = Menu(fontFamily, foreground="white", background="black")
fontFamily["menu"] = fontFamily.menu5
lis = list()
for fonter in font.families():
    lis.append(fonter)
vb = IntVar()
vb.set(990)
for i in range(0, len(lis)):
    fontFamily.menu5.add_radiobutton(label=lis[i], command=fontFamilyFun, variable=vb, value=i, background="black",
                                     foreground="white")

fontFamily.pack(expand=True, fill=BOTH)

var1, var2, var3, var4 = IntVar(), IntVar(), IntVar(), IntVar()
textStyle = LabelFrame(textLabel, width=10)
textStyle.grid(row=0, column=1, sticky="nws", padx=10)
textButtonI = Checkbutton(textStyle, text="I",
                          font=font.Font(family="stika heading", size=10, slant="italic", weight="bold"), relief="flat",
                          width=5, variable=var1, command=getTextStyle, indicatoron=0, foreground="white",
                          background="black", selectcolor=Color1)
textButtonI.pack(expand=True, fill=BOTH, side=LEFT, padx=10)

textButtonB = Checkbutton(textStyle, text="B", font=font.Font(family="stika heading", size=10, weight="bold"),
                          relief="flat", width=5, variable=var2, command=getTextStyle, indicatoron=0,
                          foreground="white", background="black", selectcolor=Color1)
textButtonB.pack(expand=True, side=LEFT, fill=BOTH, padx=10)

textButtonU = Checkbutton(textStyle, text="U",
                          font=font.Font(family="stika heading", size=10, weight="bold", underline=True), relief="flat",
                          width=5, variable=var3, command=getTextStyle, indicatoron=0, foreground="white",
                          background="black", selectcolor=Color1)
textButtonU.pack(expand=True, fill=BOTH, side=LEFT, padx=10)
textButtonO = Checkbutton(textStyle, text="abc",
                          font=font.Font(family="stika heading", size=10, weight="bold", overstrike=True),
                          relief="flat", width=5, variable=var4, command=getTextStyle, indicatoron=0,
                          foreground="white", background="black", selectcolor=Color1)
textButtonO.pack(expand=True, fill=BOTH, side=LEFT, padx=10)

textButtonS = Spinbox(textStyle, width=5, from_=1, to=100, command=getSizeofFont, foreground="white",
                      background="black", font=font.Font(family="stika heading", size=11, weight="bold"))
textButtonS.pack(expand=True, fill=BOTH, side=LEFT, padx=10)

designsImageList = ["Drectangle.png", "Dcircle.png", "Dtria.png", "Dtriangle.png", "Dheart.png", "Dstar.png"]

DesignList = [None] * 6
DesignImageList = [None] * 6
for i in range(0, 6):
    resource_path(".img\\"+designsImageList[i])
    DesignList[i] = Image.open(".img\\"+designsImageList[i])
    DesignList[i] = DesignList[i].resize((60, 60), Image.ANTIALIAS)
    DesignImageList[i] = ImageTk.PhotoImage(DesignList[i])

design = LabelFrame(textLabel, width=50, foreground="white", background="black")
design.grid(row=0, column=3, sticky='news')

design_menu = Menubutton(design, text="Designs", anchor='n', foreground="white", background="black")
design_menu.menu = Menu(design_menu, foreground="white", background="black")
design_menu["menu"] = design_menu.menu
design_menu.menu.add_radiobutton(command=lambda: shapesChoose('d1'), image=DesignImageList[0], background="black")
design_menu.menu.add_radiobutton(command=lambda: shapesChoose('d2'), image=DesignImageList[1], background="black")
design_menu.menu.add_radiobutton(command=lambda: shapesChoose('d3'), image=DesignImageList[2], background="black")
design_menu.menu.add_radiobutton(command=lambda: shapesChoose('d4'), image=DesignImageList[3], background="black")
design_menu.menu.add_radiobutton(command=lambda: shapesChoose('d5'), image=DesignImageList[4], background="black")
design_menu.menu.add_radiobutton(command=lambda: shapesChoose('d6'), image=DesignImageList[5], background="black")
design_menu.pack(expand=True, fill=BOTH)

# ....................................................................................................................


GotoItems = 1


# Items for Paint ...............................................


def paint(event):
    x2 = 0
    y2 = 0
    global X, Y, z, dColor, Color2, Color1, all_width, polyx1, polyy1, zindex, CursorSet
    polyx1, polyy1 = 0, 0
    if event.state == 1032:
        dColor = Color2
    else:
        dColor = Color1
    if X == 0 and Y == 0:
        x1, y1 = (event.x), (event.y)
        x2, y2 = (event.x + 1), (event.y + 1)
    else:
        x1, y1 = X, Y
        x2, y2 = (event.x), (event.y)
    X = x2
    Y = y2
    if z == 0:
        if all_width[z] <= 4:
            contentLabel.create_line(x1, y1, x2, y2, fill=dColor)
        else:
            contentLabel.create_rectangle(x1, y1, x2, y2, fill=dColor, width=all_width[zsize], outline=dColor)
    elif z == 1:
        contentLabel.create_oval(x1, y1, x2 - 0.5, y2 + 1, fill=dColor, outline=dColor, width=3)
    elif z == 2:
        contentLabel.create_rectangle(x1, y1, x2 - 1, y2 + 1, fill="white", outline="white", width=all_width[zsize])


def reset(event):
    global X, Y
    X = 0
    Y = 0


def items_f(p):
    global choosebox, polyx1, polyy1
    global z, TextInPaint
    if p == 4:
        TextInPaint = "text"
        selector("text")
        z=p
    else:
        TextInPaint = ""
        polyx1, polyy1 = 0, 0
        choosebox = 1
        z = p
        contentLabel.bind("<ButtonRelease-1>", reset)
        contentLabel.bind("<B1-Motion>", paint)
        contentLabel.bind("<ButtonRelease-3>", reset)
        contentLabel.bind("<B3-Motion>", paint)


items.rowconfigure(0, weight=1)
items.rowconfigure(1, weight=1)
items.columnconfigure(0, weight=1)
items.columnconfigure(1, weight=1)
items.columnconfigure(2, weight=1)

resource_path(".img\\pencil.png")
pencilIMG = Image.open(".img\\pencil.png")
pencilIMG = pencilIMG.resize((20, 20), Image.ANTIALIAS)
PencilImg = ImageTk.PhotoImage(pencilIMG)

resource_path(".img\\pen.png")
penIMG = Image.open(".img\\pen.png")
penIMG = penIMG.resize((20, 20), Image.ANTIALIAS)
PenImg = ImageTk.PhotoImage(penIMG)

resource_path(".img\\abc.png")
textIMG = Image.open(".img\\abc.png")
textIMG = textIMG.resize((20, 20), Image.ANTIALIAS)
TextImg = ImageTk.PhotoImage(textIMG)

resource_path(".img\\eraser.png")
eraserIMG = Image.open(".img\\eraser.png")
eraserIMG = eraserIMG.resize((20, 20), Image.ANTIALIAS)
EraserImg = ImageTk.PhotoImage(eraserIMG)

resource_path(".img\\fill.png")
fillIMG = Image.open(".img\\fill.png")
fillIMG = fillIMG.resize((20, 20), Image.ANTIALIAS)
FillImg = ImageTk.PhotoImage(fillIMG)

resource_path(".img\\search.png")
zoomIMG = Image.open(".img\\search.png")
zoomIMG = zoomIMG.resize((20, 20), Image.ANTIALIAS)
ZoomImg = ImageTk.PhotoImage(zoomIMG)

pencil = Button(items, command=lambda: items_f(0), width=35, image=PencilImg, compound=CENTER, relief="flat")
pencil.grid(row=0, column=0, )
pen = Button(items, command=lambda: items_f(1), width=35, image=PenImg, compound=CENTER, relief="flat")
pen.grid(row=0, column=1)
eraser = Button(items, command=lambda: items_f(2), width=35, image=EraserImg, compound=CENTER, relief="flat")
eraser.grid(row=1, column=0)
colorpicker = Button(items, command=lambda: items_f(3), width=35, image=FillImg, compound=CENTER, relief="flat")
colorpicker.grid(row=1, column=1)
TEXT = Button(items, command=lambda: items_f(4), width=35, image=TextImg, compound=CENTER, relief="flat")
TEXT.grid(row=0, column=2)
zoom = Button(items, command=lambda: items_f(5), width=35, image=ZoomImg, compound=CENTER, relief="flat")
zoom.grid(row=1, column=2)

GotoBrushes = 1
#  Brushes ..........................................................................................

brushType = 0


def paintBrush(event):
    global brushType, polyx1, polyy1, X, Y, fillvar,tcolor
    x, y = event.x, event.y
    polyx1, polyy1 = 0, 0
    tcolor = "black"
    if fillvar == '' and outLinevar == '':
        tcolor = "black"
    else:
        tcolor = fillvar

    if event.state == 1032:
        dColor = Color2
    else:
        dColor = Color1
    if X == 0 and Y == 0:
        x1, y1 = (event.x), (event.y)
        x2, y2 = (event.x + 1), (event.y + 1)
    else:
        x1, y1 = X, Y
        x2, y2 = (event.x), (event.y)
    X = x2
    Y = y2
    if brushType == 0:

        contentLabel.create_oval(x1, y1, x2 - 1, y2 + 1, fill=dColor, outline=dColor, width=all_width[zsize] + 10)
    elif brushType == 1:
        contentLabel.create_text(x, y, text=".", fill=dColor)
        contentLabel.create_text(x + 10, y + 10, text=".", fill=dColor)
        contentLabel.create_text(x + 10, y, text=".", fill=dColor)
        contentLabel.create_text(x, y + 10, text=".", fill=dColor)
        contentLabel.create_text(x - 10, y - 10, text=".", fill=dColor)
        contentLabel.create_text(x, y - 10, text=".", fill=dColor)
        contentLabel.create_text(x - 10, y, text=".", fill=dColor)
        contentLabel.create_text(x + 10, y - 10, text=".", fill=dColor)
        contentLabel.create_text(x - 10, y + 10, text=".", fill=dColor)
        contentLabel.create_text(x - 13, y, text=".", fill=dColor)
        contentLabel.create_text(x + 13, y - 14, text=".", fill=dColor)
        contentLabel.create_text(x - 16, y + 14, text=".", fill=dColor)
        contentLabel.create_text(x - 6, y, text=".", fill=dColor)
        contentLabel.create_text(x + 12, y - 10, text=".", fill=dColor)
        contentLabel.create_text(x - 4, y + 1, text=".", fill=dColor)
        contentLabel.create_text(x - 7, y + 5, text=".", fill=dColor)
        contentLabel.create_text(x + 1, y - 14, text=".", fill=dColor)
        contentLabel.create_text(x - 6, y + 14, text=".", fill=dColor)
        contentLabel.after(40)
    elif brushType == 2:
        contentLabel.create_rectangle(x1, y1, x2 - 1, y2 + 1, fill=dColor, outline=dColor, width=all_width[zsize] + 20)
    elif brushType == 3:
        contentLabel.create_rectangle(x1, y1, x2 - 1, y2 + 1, fill=Color1, outline=Color1, width=all_width[zsize])
        contentLabel.create_rectangle(x1, y1 + 2, x2 - 1, y2 + 3, fill=Color2, outline=Color2, width=all_width[zsize])
        contentLabel.create_rectangle(x1, y1 + 4, x2 - 1, y2 + 5, fill=Color1, outline=Color1, width=all_width[zsize])
        contentLabel.create_rectangle(x1, y1 + 6, x2 - 1, y2 + 7, fill=Color2, outline=Color2, width=all_width[zsize])
        contentLabel.create_rectangle(x1, y1 + 8, x2 - 1, y2 + 9, fill=Color1, outline=Color1, width=all_width[zsize])
        contentLabel.create_rectangle(x1, y1 + 10, x2 - 1, y2 + 11, fill=Color2, outline=Color2, width=all_width[zsize])


def brush_f(s):
    global brushType, TextInPaint
    TextInPaint = ""
    brushType = s
    contentLabel.bind("<ButtonRelease-1>", reset)
    contentLabel.bind("<B1-Motion>", paintBrush)
    contentLabel.bind("<ButtonRelease-3>", reset)
    contentLabel.bind("<B3-Motion>", paintBrush)


def size_f(c):
    global all_width, zsize
    all_width[zsize] = c


resource_path(".img\\brush.png")
MainIMG = Image.open(".img\\brush.png")
MainIMG = MainIMG.resize((50, 50), Image.ANTIALIAS)
MainImg = ImageTk.PhotoImage(MainIMG)

resource_path(".img\\brush1.png")
brush1IMG = Image.open(".img\\brush1.png")
brush1IMG = brush1IMG.resize((20, 20), Image.ANTIALIAS)
Brush1Img = ImageTk.PhotoImage(brush1IMG)

resource_path(".img\\brush2.png")
brush2IMG = Image.open(".img\\brush2.png")
brush2IMG = brush2IMG.resize((20, 20), Image.ANTIALIAS)
Brush2Img = ImageTk.PhotoImage(brush2IMG)

resource_path(".img\\brush3.png")
brush3IMG = Image.open(".img\\brush3.png")
brush3IMG = brush3IMG.resize((20, 20), Image.ANTIALIAS)
Brush3Img = ImageTk.PhotoImage(brush3IMG)

resource_path(".img\\brush4.png")
brush4IMG = Image.open(".img\\brush4.png")
brush4IMG = brush4IMG.resize((20, 20), Image.ANTIALIAS)
Brush4Img = ImageTk.PhotoImage(brush4IMG)

brush_menu = Menubutton(Brushes, anchor='n', image=MainImg, compound=CENTER)
brush_menu.menu = Menu(brush_menu)
brush_menu["menu"] = brush_menu.menu

brush_menu.menu.add_radiobutton(command=lambda: brush_f(0), background="white", image=Brush1Img, compound=LEFT,
                                label="Small")
brush_menu.menu.add_radiobutton(command=lambda: brush_f(2), background="white", image=Brush2Img, compound=LEFT,
                                label="Large")
brush_menu.menu.add_radiobutton(command=lambda: brush_f(1), background="white", image=Brush3Img, compound=LEFT,
                                label="Sprayer")
brush_menu.menu.add_radiobutton(command=lambda: brush_f(3), background="white", image=Brush4Img, compound=LEFT,
                                label="Roller")
brush_menu.pack()

resource_path(".img\\size.png")
sizeIMG = Image.open(".img\\size.png")
sizeIMG = sizeIMG.resize((45, 65), Image.ANTIALIAS)
SizeIMG = ImageTk.PhotoImage(sizeIMG)

size_menu = Menubutton(size, anchor='n', image=SizeIMG, compound=CENTER)
size_menu.menu = Menu(size_menu, foreground="white", background="black")
size_menu["menu"] = size_menu.menu
size_menu.menu.add_radiobutton(label="SIZE 1",
                               command=lambda: size_f(3), background="black", foreground="white",
                               font=font.Font(family="Sitka Heading", size=9))
size_menu.menu.add_radiobutton(label="SIZE 2",
                               command=lambda: size_f(15), background="black", foreground="white",
                               font=font.Font(family="Sitka Heading", size=9))
size_menu.menu.add_radiobutton(label="SIZE 3",
                               command=lambda: size_f(30), background="black", foreground="white",
                               font=font.Font(family="Sitka Heading", size=9))
size_menu.menu.add_radiobutton(label="SIZE 4",
                               command=lambda: size_f(40), font=font.Font(family="Sitka Heading", size=9),
                               background="black", foreground="white")
size_menu.pack()

# ..................................................................................................................................


GotoColorBox = 1


# Color BOX ..............................................................................


def setColor(colour):
    global Color1, Color2, cs, outLinevar, fillvar
    if cs == 1:
        Color1 = colour
        fillvar = Color1
    else:
        Color2 = colour
        outLinevar = Color2
    color1 = LabelFrame(colorSelect, text="Color 1", labelanchor='s', relief='flat')
    color1.grid(row=0, column=0, sticky='news', padx=2, pady=2)
    color1b = Button(color1, relief='flat', background=Color1, command=lambda: colorS(1))
    color1b.pack(fill=BOTH, expand=True)
    color2 = LabelFrame(colorSelect, text="Color 2", labelanchor='s', relief='flat')
    color2.grid(row=0, column=1, sticky='news', padx=2, pady=2)
    color2b = Button(color2, relief='flat', background=Color2, command=lambda: colorS(2))
    color2b.pack(fill=BOTH, expand=True)
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    text.configure(font=fontText, foreground=Color1)
    if Color1 != "#FFFFFF":
        textButtonI["selectcolor"] = Color1
        textButtonU["selectcolor"] = Color1
        textButtonB["selectcolor"] = Color1
        textButtonO["selectcolor"] = Color1


def colorS(t):
    global cs
    cs = t
    color1 = LabelFrame(colorSelect, text="Color 1", labelanchor='s', relief='flat')
    color1.grid(row=0, column=0, sticky='news', padx=2, pady=2)
    color1b = Button(color1, relief='flat', background=Color1, command=lambda: colorS(1))
    color1b.pack(fill=BOTH, expand=True)
    color2 = LabelFrame(colorSelect, text="Color 2", labelanchor='s', relief='flat')
    color2.grid(row=0, column=1, sticky='news', padx=2, pady=2)
    color2b = Button(color2, relief='flat', background=Color2, command=lambda: colorS(2))
    color2b.pack(fill=BOTH, expand=True)
    fontText = font.Font(family=fontFamilyVar.get(), size=SizeVar.get(), weight=BoldVar.get(),
                         slant=ItalicVar.get(), underline=UnderVar.get(), overstrike=OverVar.get())
    text.configure(font=fontText, foreground=Color1)


colorbox.rowconfigure(0)
colorbox.rowconfigure(1)
colorbox.columnconfigure(0)
colorbox.columnconfigure(1)
colorbox.columnconfigure(2)
colorbox.columnconfigure(3)
colorbox.columnconfigure(4)
colorbox.columnconfigure(5)
colorbox.columnconfigure(6)

c1 = Button(colorbox, width=2, command=lambda: setColor("#FF3333"), background="#FF3333", relief="flat")
c1.grid(row=0, column=0, padx=4, pady=5)
c2 = Button(colorbox, width=2, command=lambda: setColor("#FF6B33"), background="#FF6B33", relief="flat")
c2.grid(row=0, column=1, padx=4, pady=5)
c3 = Button(colorbox, width=2, command=lambda: setColor("#FFFFFF"), background="#FFFFFF", relief="flat")
c3.grid(row=0, column=2, padx=4, pady=5)
c4 = Button(colorbox, width=2, command=lambda: setColor("#FFB833"), background="#FFB833", relief="flat")
c4.grid(row=0, column=3, padx=4, pady=5)
c5 = Button(colorbox, width=2, command=lambda: setColor("#FFE933"), background="#FFE933", relief="flat")
c5.grid(row=0, column=4, padx=4, pady=5)
c6 = Button(colorbox, width=2, command=lambda: setColor("#A8FF33"), background="#A8FF33", relief="flat")
c6.grid(row=0, column=5, padx=4, pady=5)
c7 = Button(colorbox, width=2, command=lambda: setColor("#49FF33"), background="#49FF33", relief="flat")
c7.grid(row=0, column=6, padx=4, pady=5)
c8 = Button(colorbox, width=2, command=lambda: setColor("#33FF6B"), background="#33FF6B", relief="flat")
c8.grid(row=1, column=0, padx=4, pady=1)
c9 = Button(colorbox, width=2, command=lambda: setColor("#07531C"), background="#07531C", relief="flat")
c9.grid(row=1, column=1, padx=4, pady=1)
c10 = Button(colorbox, width=2, command=lambda: setColor("#13E2DF"), background="#13E2DF", relief="flat")
c10.grid(row=1, column=2, padx=4, pady=1)
c11 = Button(colorbox, width=2, command=lambda: setColor("#13B0E2"), background="#13B0E2", relief="flat")
c11.grid(row=1, column=3, padx=4, pady=1)
c12 = Button(colorbox, width=2, command=lambda: setColor("#1339E2"), background="#1339E2", relief="flat")
c12.grid(row=1, column=4, padx=4, pady=1)
c13 = Button(colorbox, width=2, command=lambda: setColor("#B613E2"), background="#B613E2", relief="flat")
c13.grid(row=1, column=5, padx=4, pady=1)
c14 = Button(colorbox, width=2, command=lambda: setColor("#E21374"), background="#E21374", relief="flat")
c14.grid(row=1, column=6, padx=4, pady=1)

colorSelect.rowconfigure(0, weight=0)
colorSelect.columnconfigure(0, weight=40)
colorSelect.columnconfigure(1, weight=40)
color1 = Labelframe(colorSelect, text="Color 1", labelanchor='s', height=2)
color1.grid(row=0, column=0, sticky='news', padx=2, pady=2)
color1b = Button(color1, relief='flat', background=Color1, command=lambda: colorS(1), width=2, height=2)
color1b.pack(fill=BOTH)
color2 = Labelframe(colorSelect, text="Color 2", labelanchor='s', height=2)
color2.grid(row=0, column=1, sticky='news', padx=2, pady=2)
color2b = Button(color2, relief='flat', background=Color2, command=lambda: colorS(2), width=2, height=2)
color2b.pack(fill=BOTH)
# ...............................................................................


GotoOutline = 1


# outline and fill color ..........................................

def out(s):
    global Color2, outLinevar
    if s == "OSC":
        outLinevar = Color2
    elif s == "NO":
        outLinevar = ''


def Fill(s):
    global fillvar, Color1
    if s == "FSC":
        fillvar = Color1
    elif s == "NF":
        fillvar = ''


resource_path(".img\\outline.png")
outlineIMG = Image.open(".img\\outline.png")
outlineIMG = outlineIMG.resize((15, 15), Image.ANTIALIAS)
Outline1Img = ImageTk.PhotoImage(outlineIMG)

resource_path(".img\\fill.png")
fillColorIMG = Image.open(".img\\fill.png")
fillColorIMG = fillColorIMG.resize((15, 15), Image.ANTIALIAS)
FillColor1IMG = ImageTk.PhotoImage(fillColorIMG)

outFrame = LabelFrame(out_fill, relief="flat")
outFrame.pack(pady=1, side=TOP)
fillFrame = LabelFrame(out_fill, relief="flat")
fillFrame.pack(pady=1, side=TOP)
outButton = Menubutton(outFrame, text="outline", anchor='n', image=Outline1Img, compound=LEFT, relief="flat")
outButton.menu2 = Menu(outButton, foreground="white", background="black")
outButton["menu"] = outButton.menu2
outButton.menu2.add_radiobutton(label="No Outline", command=lambda: out("NO"),
                                font=font.Font(family="Sitka Heading", size=9), background="black", foreground="white")
outButton.menu2.add_radiobutton(label="Solid Color", command=lambda: out("OSC"),
                                font=font.Font(family="Sitka Heading", size=9), background="black", foreground="white")
outButton.pack(side=TOP)

fillButton = Menubutton(fillFrame, text="fill color", image=FillColor1IMG, compound=LEFT, relief="flat")
fillButton.menu3 = Menu(fillButton, foreground="white", background="black")
fillButton["menu"] = fillButton.menu3
fillButton.menu3.add_radiobutton(label="No fill", command=lambda: Fill("NF"),
                                 font=font.Font(family="Sitka Heading", size=9), background="black", foreground="white")
fillButton.menu3.add_radiobutton(label="Solid Color", command=lambda: Fill("FSC"),
                                 font=font.Font(family="Sitka Heading", size=9), background="black", foreground="white")
fillButton.pack(side=TOP)

# .................................................................................


GotoShapes = 1

# shapes    RECTANGLE , TRAINGLE , CIRCLE , OVAL , STAR ETC ............................................................

ir, ic, it, iet, irt, ih1, ih2 = -1, -1, -1, -1, -1, -1, -1
px, py, polyi = 0, 0, -1
X, Y = 0, 0
sti = -1
polyx1, polyy1 = 0, 0
shapeType = "rectangle"


def coordinate(event):
    global sx, sy, polyx1, polyy1
    sx, sy = event.x, event.y
    if polyx1 == 0 and polyy1 == 0:
        polyx1, polyy1 = event.x, event.y


def paintShapes(event):
    global X, sx, sy, r1s, c1s, shapeType, Y, outLinevar, fillvar, t1s, et1s, et1, rt1s, h1s, h2s, star1
    global px, py, poly1, polyx1, polyy1

    px, py = 0, 0
    if shapeType == "rectangle":
        polyx1, polyy1 = 0, 0
        contentLabel.delete(r1s)
        r1s = contentLabel.create_rectangle(sx, sy, event.x, event.y, outline=outLinevar, fill=fillvar)
    elif shapeType == "circle":
        polyx1, polyy1 = 0, 0
        contentLabel.delete(c1s)
        c1s = contentLabel.create_oval(sx, sy, event.x, event.y, outline=outLinevar, fill=fillvar)
    elif shapeType == 'triangle':
        polyx1, polyy1 = 0, 0
        contentLabel.delete(t1s)
        t1s = contentLabel.create_polygon(sx, sy, event.x + 100, event.y, event.x - 100, event.y, outline=outLinevar,
                                          fill=fillvar)
    elif shapeType == 'Etriangle':
        polyx1, polyy1 = 0, 0
        contentLabel.delete(et1s)
        et1s = contentLabel.create_polygon(sx, sy, event.x, event.y, 2 * sx - event.x, event.y, outline=outLinevar,
                                           fill=fillvar)
    elif shapeType == "Rtriangle":
        polyx1, polyy1 = 0, 0
        contentLabel.delete(rt1s)
        rt1s = contentLabel.create_polygon(sx, sy, event.x, event.y, sx, event.y, outline=outLinevar, fill=fillvar)
    elif shapeType == "heart":
        polyx1, polyy1 = 0, 0
        if fillvar != '':
            contentLabel.delete(h1s)
            contentLabel.delete(h2s)
            h1s = contentLabel.create_polygon(sx, sy, sx - (event.x - sx) / 3, sy - (event.y - sy) / 10,
                                              sx - (event.x - sx) / 2, sy + (event.y - sy) / 4, sx + (event.x - sx) / 9,
                                              event.y, smooth=True, fill=fillvar, outline=outLinevar)
            h2s = contentLabel.create_polygon(sx, sy, sx + (event.x - sx) / 3, sy - (event.y - sy) / 10,
                                              sx + (event.x - sx) / 2, sy + (event.y - sy) / 4, sx - (event.x - sx) / 9,
                                              event.y, smooth=True, fill=fillvar, outline=outLinevar)
        else:
            contentLabel.delete(h1s)
            contentLabel.delete(h2s)
            h1s = contentLabel.create_line(sx, sy, sx - (event.x - sx) / 4, sy - (event.y - sy) / 4,
                                           sx - (event.x - sx) / 2, sy + (event.y - sy) / 4, sx, event.y, smooth=True,
                                           fill=outLinevar)
            h2s = contentLabel.create_line(sx, sy, sx + (event.x - sx) / 4, sy - (event.y - sy) / 4,
                                           sx + (event.x - sx) / 2, sy + (event.y - sy) / 4, sx, event.y, smooth=True,
                                           fill=outLinevar)
    elif shapeType == "star":
        polyx1, polyy1 = 0, 0
        contentLabel.delete(star1)
        star1 = contentLabel.create_polygon(sx, sy, sx + (event.x - sx) / 3, sy + (event.y - sy) / 3, event.x,
                                            sy + (event.y - sy) / 2,
                                            sx + (event.x - sx) / 3, sy + 2 * (event.y - sy) / 3, sx, event.y,
                                            sx - (event.x - sx) / 3,
                                            sy + 2 * (event.y - sy) / 3, 2 * sx - event.x, sy + (event.y - sy) / 2,
                                            sx - (event.x - sx) / 3, sy + (event.y - sy) / 3, sx, sy, fill=fillvar,
                                            outline=outLinevar)
    elif shapeType == "poly":
        if fillvar == '':
            pfillvar = "black"
        else:
            pfillvar = fillvar
        contentLabel.delete(poly1)
        poly1 = contentLabel.create_line(polyx1, polyy1, event.x, event.y, fill=pfillvar)
    elif shapeType == "d1":
        contentLabel.create_rectangle(sx, sy, event.x, event.y, outline=outLinevar, fill=fillvar)
    elif shapeType == "d2":
        contentLabel.create_oval(sx, sy, event.x, event.y, outline=outLinevar, fill=fillvar)
    elif shapeType == "d3":
        contentLabel.create_polygon(sx, sy, event.x + 100, event.y, event.x - 100, event.y, outline=outLinevar,
                                    fill=fillvar)
    elif shapeType == "d4":
        contentLabel.create_polygon(sx, sy, event.x, event.y, 2 * sx - event.x, event.y, outline=outLinevar,
                                    fill=fillvar)
    elif shapeType == "d5":
        contentLabel.create_polygon(sx, sy, sx - (event.x - sx) / 3, sy - (event.y - sy) / 10,
                                    sx - (event.x - sx) / 2, sy + (event.y - sy) / 4, sx + (event.x - sx) / 9,
                                    event.y, smooth=True, fill=fillvar, outline=outLinevar)
        contentLabel.create_polygon(sx, sy, sx + (event.x - sx) / 3, sy - (event.y - sy) / 10,
                                    sx + (event.x - sx) / 2, sy + (event.y - sy) / 4, sx - (event.x - sx) / 9,
                                    event.y, smooth=True, fill=fillvar, outline=outLinevar)
    elif shapeType == "d6":
        contentLabel.create_polygon(sx, sy, sx + (event.x - sx) / 3, sy + (event.y - sy) / 3, event.x,
                                    sy + (event.y - sy) / 2,
                                    sx + (event.x - sx) / 3, sy + 2 * (event.y - sy) / 3, sx, event.y,
                                    sx - (event.x - sx) / 3,
                                    sy + 2 * (event.y - sy) / 3, 2 * sx - event.x, sy + (event.y - sy) / 2,
                                    sx - (event.x - sx) / 3, sy + (event.y - sy) / 3, sx, sy, fill=fillvar,
                                    outline=outLinevar)


def resetShapes(event):
    global r1, r1s, ir, ic, shapeType, c1s, c1, t1, t1s, it, iet, et1s, et1, rt1s, irt, rt1
    global h1, h2, h1s, h2s, ih1, ih2, Stars, star1, sti, poly, poly1, polyi, polyx1, polyy1

    if shapeType == "rectangle":
        if ir < 1000:
            ir = ir + 1
            r1s = r1[ir]
    elif shapeType == "circle":
        if ic < 1000:
            ic = ic + 1
            c1s = c1[ic]
    elif shapeType == "triangle":
        if it < 1000:
            it = it + 1
            t1s = t1[it]
    elif shapeType == "Etriangle":
        if iet < 1000:
            iet = iet + 1
            et1s = et1[iet]
    elif shapeType == "Rtriangle":
        if irt < 1000:
            irt = irt + 1
            rt1s = rt1[irt]
    elif shapeType == "heart":
        if ih1 < 1000:
            ih1 += 1
            ih2 += 1
            h1s = h1[ih1]
            h2s = h2[ih2]
    elif shapeType == "star":
        if sti < 1000:
            sti = sti + 1
            star1 = Stars[sti]
    elif shapeType == "poly":
        polyx1, polyy1 = event.x, event.y
        if polyi < 1000:
            polyi += 1
            poly1 = poly[polyi]


def shapesChoose(string):
    global choosebox, shapeType
    choosebox = 2
    shapeType = string
    contentLabel.bind("<ButtonRelease-1>", resetShapes)
    contentLabel.bind("<Button-1>", coordinate)
    contentLabel.bind("<B1-Motion>", paintShapes)


# Rectangle
r1 = [contentLabel.create_rectangle(0, 0, 0, 0)] * 1000
r1s = r1[0]
# circle
c1 = [contentLabel.create_oval(0, 0, 0, 0)] * 1000
c1s = c1[0]

# Triangle
t1 = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
t1s = t1[0]

# Equilateral Triangle
et1 = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
et1s = et1[0]

# Right Angled Triangle
rt1 = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
rt1s = rt1[0]

# Heart
h1 = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
h1s = h1[0]
h2 = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
h2s = h2[0]

# Star
Stars = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
star1 = Stars[0]

# Polygon
poly = [contentLabel.create_polygon(0, 0, 0, 0, 0, 0)] * 1000
poly1 = poly[0]

shapes.rowconfigure(0)
shapes.rowconfigure(1)
shapes.columnconfigure(0)
shapes.columnconfigure(1)
shapes.columnconfigure(2)
shapes.columnconfigure(3)

ShapesImageList = ["rectangle.png", "circle.png", "triangle.jpg", "Etriangle.png", "Rtriangle.png", "heart.png",
                   "star.png", "poly.png"]

shapeList = [None] * 8
shapeImageList = [None] * 8
for i in range(0, 8):
    resource_path(".img\\"+ShapesImageList[i])
    shapeList[i] = Image.open(".img\\"+ShapesImageList[i])
    shapeList[i] = shapeList[i].resize((20, 20), Image.ANTIALIAS)
    ShapesImageList[i] = ImageTk.PhotoImage(shapeList[i])

s1 = Button(shapes, command=lambda: shapesChoose("rectangle"), relief="flat", image=ShapesImageList[0], compound=CENTER,
            width=20)
s1.grid(row=0, column=0, padx=2, pady=5)
s2 = Button(shapes, command=lambda: shapesChoose("circle"), relief="flat", image=ShapesImageList[1], compound=CENTER,
            width=20)
s2.grid(row=0, column=1, padx=2, pady=5)
s3 = Button(shapes, command=lambda: shapesChoose("triangle"), relief="flat", image=ShapesImageList[2], compound=CENTER,
            width=20)
s3.grid(row=0, column=2, padx=2, pady=5)
s4 = Button(shapes, command=lambda: shapesChoose("Etriangle"), relief="flat", image=ShapesImageList[3], compound=CENTER,
            width=20)
s4.grid(row=0, column=3, padx=2, pady=5)
s5 = Button(shapes, command=lambda: shapesChoose("Rtriangle"), relief="flat", image=ShapesImageList[4], compound=CENTER,
            width=20)
s5.grid(row=1, column=0, padx=2, pady=5)
s6 = Button(shapes, command=lambda: shapesChoose("heart"), relief="flat", image=ShapesImageList[5], compound=CENTER,
            width=20)
s6.grid(row=1, column=1, padx=2, pady=5)
s7 = Button(shapes, command=lambda: shapesChoose("star"), relief="flat", image=ShapesImageList[6], compound=CENTER,
            width=20)
s7.grid(row=1, column=2, padx=2, pady=5)
s8 = Button(shapes, command=lambda: shapesChoose("poly"), relief="flat", image=ShapesImageList[7], compound=CENTER,
            width=20)
s8.grid(row=1, column=3, padx=2, pady=5)

# .........................................................................................................................................


GotoMoreColors = 1
# More Colors ............................ .           .                          ...............................................

colors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
          'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
          'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
          'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
          'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
          'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue', 'blue',
          'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
          'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
          'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
          'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
          'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
          'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
          'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
          'indian red', 'saddle brown', 'sandy brown',
          'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
          'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
          'pale violet red', 'maroon', 'medium violet red', 'violet red',
          'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
          'thistle', 'snow2', 'snow3',
          'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
          'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
          'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
          'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
          'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
          'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
          'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
          'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
          'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
          'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
          'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
          'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
          'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
          'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
          'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
          'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
          'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
          'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
          'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
          'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
          'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
          'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
          'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
          'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
          'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
          'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
          'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
          'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
          'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
          'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
          'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
          'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
          'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
          'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
          'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
          'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
          'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
          'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
          'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
          'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
          'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
          'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
          'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
          'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
          'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
          'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
          'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
          'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
          'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
          'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
          'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
          'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
          'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
          'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
          'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
          'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
          'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

resource_path(".img\\More.png")
colorMenuIMG = Image.open(".img\\More.png")
colorMenuIMG = colorMenuIMG.resize((60, 60), Image.AFFINE)
ColorMenuIMG = ImageTk.PhotoImage(colorMenuIMG)

color_menu = Menubutton(editColor, anchor='n', image=ColorMenuIMG, compound=CENTER, foreground="white",
                        background="black")
color_menu.menu = Menu(color_menu, background="black")
color_menu["menu"] = color_menu.menu
colorMore = StringVar()
colorMore.set("black")


def MoreColors():
    global Color1, Color2, cs, outLinevar, fillvar
    if cs == 1:
        Color1 = colorMore.get()
        fillvar = Color1
    else:
        Color2 = colorMore.get()
        outLinevar = Color2
    color1 = LabelFrame(colorSelect, text="Color 1", labelanchor='s', relief='flat')
    color1.grid(row=0, column=0, sticky='news', padx=2, pady=2)
    color1b = Button(color1, relief='flat', background=Color1, command=lambda: colorS(1))
    color1b.pack(fill=BOTH, expand=True)
    color2 = LabelFrame(colorSelect, text="Color 2", labelanchor='s', relief='flat')
    color2.grid(row=0, column=1, sticky='news', padx=2, pady=2)
    color2b = Button(color2, relief='flat', background=Color2, command=lambda: colorS(2))
    color2b.pack(fill=BOTH, expand=True)


for i in range(0, len(colors)):
    color_menu.menu.add_radiobutton(label=lis[i], command=MoreColors, variable=colorMore, value=colors[i],
                                    background=colors[i])

color_menu.pack()

# ....................................................................................................................................


# Speech Recognition  . . . . . . . . . . . . . . . . . . . . .. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
#   https://realpython.com/python-speech-recognition/
# https://pypi.org/project/SpeechRecognition/1.3.0/
# Initialize the recognizer

reco1 = sr.Recognizer()
reco1.energy_threshold = 3900
reco1.pause_threshold = 3
reco2 = sr.Recognizer()
reco2.energy_threshold = 3800
reco3 = sr.Recognizer()
reco3.energy_threshold = 3900
xrec, yrec = 0, 0
dicText = {"question mark": '?', "exclamation mark": '!', "full stop": '.', "comma": ',',
           "parentheses braces open": "(", "parentheses braces close": ")", "Apostrophe": "'", "Asterisk": "*",
           "colon": ':', "dash": "-", "semi colon": ';', "slash": '/', "curly braces open ": '{',
           "curly braces close": '}', "square braces open": "[", "square braces close": "]", "percent":
               '%', "equal": '=', "hyphen": '`', "new line": r'\n', "tab": r'\t'}
# Function to convert text to
# speech
MyText = "aww"
recoText = "aww"
checkPunText = "aww"
checkWinText = Text()
lanVar = IntVar()
languageSelect = "en-US"
languageSelectSay = 'en'
lanInd = 0
noiseVar = IntVar()
noiseVar.set(3900)


def extract():
    global instruct_ind, checkWinText
    checkWin = Tk()
    checkWin.title("Speech Recognition")
    checkWin.geometry("400x200")
    if speechVar == 0:
        checkWinText.destroy()
        return
    checkWinText = Text(checkWin, width=60, height=60)
    scrollerReco = Scrollbar(checkWin, orient="vertical", command=checkWinText.yview)
    checkWinText.configure(font=("Kokila", 13), background="black", foreground="#00F3E8",
                           yscrollcommand=scrollerReco.set)
    checkWinText.insert('end',
                        "Python is Everywhere ,thanks for your attention ...\n note : \n 1. Read the whole line till fullstop ,don't speak phrase of words speak the whole sentence \n 2 . At the end of each sentece try to speak the last word loudly "
                        "\n 3. Check your internet connection in case of Slow response.\n 4. Another solution in case of slow response is to increase the \nthreshold energy so as to ignore the unwanted noise during listening , "
                        "\nit can be acheived by increasing the value of value above 4000 in spinbox ,\n and you should have to speak loudly as compared background noise")
    checkWinText.see("end")
    scrollerReco.pack(side="right", fill="y")
    checkWinText.pack()
    checkWinText.mainloop()


def languageFun():
    global languageSelect, languageSelectSay
    if lanVar.get():
        LanguageB["image"] = LanguageHin
        languageSelect = "hi-IN"
        languageSelectSay = 'hi'
    elif lanVar.get() == 0:
        LanguageB["image"] = LanguageEng
        languageSelect = "en-US"
        languageSelectSay = 'en'


def Noiselevel():
    global reco1, reco2, reco3
    reco1.energy_threshold = int(NoiseLevel.get())
    reco2.energy_threshold = int(NoiseLevel.get())
    reco3.energy_threshold = int(NoiseLevel.get())


def SpeakText(command, languageSend):
    # Initialize the engine
    global lanInd
    if languageSend == 'hi':
        lanInd += 1
        getAud = gtts.gTTS(command, lang=languageSelectSay)
        getAud.save("voice{}.mp3".format(lanInd))
        playsound("voice{}.mp3".format(lanInd))
        os.remove("voice{}.mp3".format(lanInd))
    elif languageSend == 'en':
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()


def checkVoiceCom():
    global MyText, checkWinText, checkPunText, l
    indexReco = 3
    with sr.Microphone() as source2:
        while (indexReco):
            SpeakText(recoText, 'hi')
            checkWinText.insert('end', "\n*. STATEMENT :  {} ".format(recoText))
            checkWinText.see("end")
            checkWinText["foreground"] = "white"
            checkWinText.insert('end',
                                "\nx. INSTRUCTION :  Say \'best\' if statement correct otherwise say \'net\' and in case of punctuation say get")
            checkWinText.see("end")
            SpeakText("Say best if statement is correct and say net if not and in case of punctuation say get", 'en')

            # speechRecoActivate["text"] = "Say Set"
            audio3 = reco2.record(source2, duration=3)
            try:
                checkText = reco2.recognize_google(audio3)
                checkText = checkText.lower()
                print(checkText)

                if checkText == "best" or checkText == 'bast':
                    print(checkText)
                    return 1
                elif checkText == "net" or checkText == 'nat':
                    return 0
                elif checkText == "get" or checkText == 'gat':
                    print("p")
                    punT = 3

                    for keysT in dicText:
                        checkWinText.insert('end', " \n {0}   =  {1} ".format(keysT, dicText[keysT]))
                    checkWinText.insert('end', "select any punctuation within 4 sec ..")
                    checkWinText.see("end")
                    while (punT):
                        with sr.Microphone() as source4:
                            print("say pun")
                            audio4 = reco3.record(source4, duration=4)
                            try:
                                checkPunText = reco3.recognize_google(audio4)
                                checkPunText = checkPunText.lower()
                                pun = dicText.get(checkPunText, None)
                                print(checkPunText)
                                if option == "text" and pun != None:
                                    Notepad.insert("end", pun + " ")
                                    return 0
                            except sr.RequestError as e:
                                checkWinText.insert("end", "\n {} ".format(e))
                                checkWinText.see("end")
                                print("errer {0}".format(e))

                            except sr.UnknownValueError:
                                print("Speak Again ...............")
                                checkWinText.insert("end", "\nSpeak Again ...............")
                                checkWinText.see("end")
                        punT -= 1
                    return 0

            except sr.RequestError as e:
                checkWinText.insert("end", "\n{} ".format(e))
                checkWinText.see("end")
                print("errer {0}".format(e))

            except sr.UnknownValueError:
                print("Speak Again ...............")
                checkWinText.insert("end", "\nSpeak Again ...............")
                checkWinText.see("end")
            indexReco = indexReco - 1

    checkWinText.insert('end', "\nspeak new statement..")
    checkWinText.see('end')
    speechRecoActivate["image"] = SpeechRecoIMG[0]


def getRecoCor(event):
    global xrec, yrec
    xrec = event.x
    yrec = event.y


def callback(reco1, audio2):
    print("callback")
    global recoText, x0, y0

    try:

        MyText = reco1.recognize_google(audio2, language=languageSelect)
        recoText = str(MyText)
        if checkVoiceCom() == 1:
            if option == "text":
                Notepad.insert("end", MyText + " ")
            else:
                if x0 == 0 and y0 == 0:
                    x0, y0 = 20, 20
                contentLabel.create_text(x0, y0 + 5, text=MyText, anchor='nw')
        else:
            SpeakText("Please speak it again", 'en')

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        checkWinText.insert("end", "\n{} ".format(e))
        checkWinText.see("end")

    except sr.UnknownValueError:
        print("Speak Again ...............")
        SpeakText("Speak Again", 'en')
        checkWinText.insert("end", "\n Speak Again ...............")
        checkWinText.see("end")


def SpeechRecognition():
    global instruct_ind, MyText, recoText
    global notePadData, notepadWin, Notepad, FileSave, option
    speechRecoActivate["image"] = SpeechRecoIMG[0]
    if speechVar.get():
        source2 = sr.Microphone()
        print("YES")
        reco1.listen_in_background(source2, callback)
    elif speechVar.get() == 0:
        print(speechVar.get())
        speechRecoActivate["image"] = SpeechRecoIMG[1]


ImgReco = ["listen.png", "record.png", "wait.png"]
speechRecoIMG = [None] * 3
SpeechRecoIMG = [None] * 3
for i in range(0, 3):
    speechRecoIMG[i] = Image.open(".img\\"+ImgReco[i])
    speechRecoIMG[i] = speechRecoIMG[i].resize((20, 20), Image.AFFINE)
    SpeechRecoIMG[i] = ImageTk.PhotoImage(speechRecoIMG[i])

resource_path(".img\\Eng2.jpg")
resource_path(".img\\Hin1.png")

languageEng = Image.open(".img\\Eng2.jpg")
languageEng = languageEng.resize((20, 20), Image.AFFINE)
LanguageEng = ImageTk.PhotoImage(languageEng)
languageHin = Image.open(".img\\Hin1.png")
languageHin = languageHin.resize((20, 20), Image.ADAPTIVE)
LanguageHin = ImageTk.PhotoImage(languageHin)

speechVar = IntVar()
speechReco = LabelFrame(textLabel, width=10)
speechReco.grid(row=0, column=2, sticky="news", padx=20)
speechRecoActivate = Checkbutton(speechReco, text="SPEAK", variable=speechVar, command=SpeechRecognition,
                                 image=SpeechRecoIMG[1], indicatoron=0, foreground="white", background="white",
                                 selectcolor="red", relief='flat')
speechRecoActivate.pack(expand=True, fill=BOTH, side="left", padx=5)
traceB = Button(speechReco, text="Trace", command=extract, foreground="white", background="black", width=5,
                relief='flat')
traceB.pack(fill=BOTH, expand=True, side="left", padx=5)
LanguageB = Checkbutton(speechReco, command=languageFun, foreground="white", background="black", width=10,
                        image=LanguageEng, variable=lanVar, indicatoron=0, relief='flat')
LanguageB.pack(fill=BOTH, expand=True, side="left", padx=5)
NoiseLevel = Spinbox(speechReco, command=Noiselevel, from_=120, to=8000, width=5, foreground="white",
                     background="black", textvariable=noiseVar, relief='flat')
NoiseLevel.pack(fill=BOTH, expand=True, side="left", padx=5)


# .........................................................................................................................................

# https://www.tcl.tk/man/tcl8.6/TkCmd/keysyms.htm

def Savefilehandler(event):
    if option == "paint":
        paintfile("save")
    elif option == "text":
        Choice("save")


def Printfilehandler(event):
    if option == "paint":
        paintfile("print")
    elif option == "text":
        Choice("print")


win.bind("<Control-S>", Savefilehandler)
win.bind("<Control-s>", Savefilehandler)

win.bind("<Control-p>", Printfilehandler)
win.bind("<Control-P>", Printfilehandler)

win.bind("<Button-3>", TextChange)
win.bind("<Escape>", TextChange)

imgCanvas = contentLabel.create_image(0, 0)
win.config(menu=menuBar)

win.mainloop()
