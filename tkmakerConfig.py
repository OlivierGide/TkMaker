from enum import Enum
from tkinter import *


colorProperties = ["bg","fg","highlightbackground"]
hidenProperties = ["background","foreground","class","visual","borderwidth","highlightcolor"]
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



