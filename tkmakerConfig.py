from enum import Enum
from tkinter import *

# Properties filled with color
colorProperties = ["bg",
                   "fg",
                   "highlightbackground",
                   "highlightcolor",
                   "selectbackground",
                   "selectforeground",
                   "activebackground",
                   "activeforeground",
                   "disabledforeground",
                   "insertbackground",
                   "selectcolor",
                   "troughcolor",
                   "background",
                   "foreground"]

# Properties filled with a list of predefined values
listProperties = { "relief": ["","flat","groove","raised","ridge","solid","sunken"],
                   "anchor": ["","n","ne","e","se","s","sw","w","nw","center"],
                   "justify": ["","left","right","center"],
                   "side": ["","top","bottom","left","right"],
                   "orient": ["","horizontal","vertical"],
                   "wrap": ["","none","char","word"],
                   "fill": ["","none","x","y","both"],
                   "style": ["","default","alt","clam","classic"],
                   "mode": ["","normal","readonly","disabled"],    
                   "state": ["","normal","active","disabled"],
                   "selectmode": ["","browse","extended","multiple","single"]
                   }



# Properties hidden, as they can ot be changed or they already exist with anothe name
hidenProperties = ["background","foreground","class","visual","borderwidth","highlightcolor","colormap","container"]
hidenLayoutOptions = ["in"]



ttkWidgets= [
            "Combobox",
            "Notebook",
            "Progressbar",
            "Separator",
            "Sizegrip",
            "Treeview"]

class WidgetType(Enum):
    FRAME = 'Frame'
    LABEL = 'Label'
    TEXT = 'Text'
    BUTTON = 'Button'
    CANVAS = 'Canvas'
    CHECKBUTTON = 'Checkbutton'
    ENTRY = 'Entry'
    LISTBOX = 'Listbox'
    MENU = 'Menu'
    MENUBUTTON = 'Menubutton'
    MESSAGE = 'Message'
    RADIOBUTTON = 'Radiobutton'
    SCALE = 'Scale'
    SCROLLBAR = 'Scrollbar'
    SPINBOX = 'Spinbox'
    TOPLEVEL = 'Toplevel'
    TREEVIEW = 'Treeview'
    NOTEBOOK = 'Notebook'
    PROGRESSBAR = 'Progressbar'
    SEPARATOR = 'Separator'
    SIZEGRIP = 'Sizegrip'
    COMBOBOX = 'Combobox'
    PANEDWINDOW = 'Panedwindow'
    LABELED_FRAME = 'Labelframe'



