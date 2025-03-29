# Description: A simple tkinter editor

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile
from tkinter import colorchooser
import importlib
from importlib import reload
import os

# Local imports
from tkmakerConfig import *
from tkmakerTooltip import CreateToolTip

widgetList = {} #List of widgets created
widgetnames = {} #List of widget names
currentProjectFile = "" #Current project file

class MainWindow:
    """
    MainWindow class provides a graphical user interface for creating and managing Tkinter widgets.
    This class allows users to design a GUI by adding, configuring, and arranging widgets interactively.
    It includes features for saving, exporting, and loading projects, as well as generating Python code
    for the designed GUI.
    Attributes:
        root (tk.Tk): The main application window.
        paramEntryList (dict): Dictionary to store entry widgets for widget parameters.
        layoutEntryList (dict): Dictionary to store entry widgets for layout parameters.
        selectionFrameList (list): List of frames used to highlight selected widgets.
        widget_type_list (list): List of widget types for the combo box.
        selectedWidget (tk.Widget): The currently selected widget.
        LayoutSelection (tk.IntVar): Variable to store the selected layout mode.
        appicons (dict): Dictionary containing all the icons used in the application.
        frm_structure (tk.Frame): Frame for the widget treeview and controls.
        frm_Dessin (tk.Frame): Frame for drawing widgets.
        frm_param (tk.Frame): Frame for displaying widget parameters.
        frm_ajout (tk.Frame): Frame containing controls to add or remove widgets.
        lbl_widget_type (tk.Label): Label for widget type selection.
        combo_widget_type (ttk.Combobox): Combobox for selecting widget types.
        lbl_widget_layout (tk.Label): Label for layout mode selection.
        R1, R2, R3 (tk.Radiobutton): Radiobuttons for selecting layout modes (place, grid, pack).
        frm_actions (tk.Frame): Frame containing action buttons (add, remove, save, export).
        tree (ttk.Treeview): Treeview for displaying the widget hierarchy.
        frm_layout_options (tk.Frame): Frame for displaying layout options.
        menu_bar (tk.Menu): Menu bar for file operations.
    Methods:
        __init__(root):
            Initializes the MainWindow class and sets up the GUI layout and components.
        open_file():
            Opens a file dialog to load a project and initializes the GUI with the loaded data.
        export_project():
            Exports the current project as Python code.
        save_project():
            Saves the current project as a backup.
        quit():
            Exits the application.
        addWidget(widget_type=None, widget_name=None, layout_mode=None, parent_widget=None):
            Adds a new widget to the GUI.
        getPackingMetod(widget):
            Determines the layout method (place, grid, pack) used by a widget.
        removeWidget():
            Removes the currently selected widget.
        highlight_widget(widget):
            Draws a frame around the selected widget to highlight it.
        selectionWidget(event):
            Handles widget selection via a left-click on the widget.
        chosecolor(event):
            Opens a color picker dialog to select a color for a widget property.
        displayOptions():
            Displays the parameters and layout options of the selected widget.
        changeParam(event):
            Updates a widget parameter when it is changed.
        changeName(event):
            Updates the name of the selected widget.
        changeLayoutParam(event):
            Updates a layout option of the selected widget.
        selectionTree(event):
            Handles widget selection via the treeview.
        generateCode(mode="EXPORT"):
            Generates Python code for the current GUI design.
        getDefaultParameters(widget):
            Retrieves the default parameters of a widget.
        loadWidgetList(widgetparent=None):
            Loads the list of widgets during project loading.
        loadWidgetNames():
            Loads the names of widgets during project loading.
        loadTreeView():
            Loads the treeview with the widget hierarchy during project loading.
    """
    # -----------------------------------------------------------------------------------------------
    # Class constructor
    # -----------------------------------------------------------------------------------------------
    def __init__(self, root):
        self.root = root
        self.root.title("TkMaker")
        self.root.geometry("800x600")
        self.paramEntryList = {} #List of entry widgets for the parameters
        self.layoutEntryList = {} #List of entry widgets for the layout parameters
        self.selectionFrameList= [] #Liste des cadres de selection qui entourent les widgets
        widget_type_list = [] #Liste des types de widgets pour la combo box
        self.selectedWidget:tk.Widget = None
        self.LayoutSelection = IntVar()
        self.LayoutSelection.set(1)

        # Configuration grid
        self.root.grid_columnconfigure(0, weight=0, minsize=250,pad=0)
        self.root.grid_columnconfigure(1, weight=1,pad=0)
        self.root.grid_rowconfigure(0, weight=1, pad=0)
        
        # This colletion contains all the icons used in the application
        self.appicons = {}
        for file in os.listdir("icons"):
            if file.endswith(".png"):
                self.appicons[file.split(".")[0]] = tk.PhotoImage(file=f"icons/{file}")
        
    
        # left frame for widget treeview and controls
        self.frm_structure = tk.Frame(self.root,padx=0,pady=0)
        self.frm_structure.grid(row=0, column=0, sticky=(tk.W,tk.E,tk.N, tk.S))
        self.frm_structure.grid_propagate(False)
        self.frm_structure.configure(relief="raised")
        self.frm_structure.configure(borderwidth=2)
        self.frm_structure.configure(padx=2)
        self.frm_structure.configure(pady=2)
        

        # Create right frame for drawing widgets
        self.frm_Dessin = tk.Frame(self.root,bg="#888")
        self.frm_Dessin.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))

        #Aframe that contains the widget parameters
        self.frm_param = tk.Frame(self.root,width=250)
        self.frm_param.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.frm_param.grid_propagate(False)
        self.frm_param.configure(relief="raised")
        self.frm_param.configure(borderwidth=2)
        self.frm_param.configure(padx=2)
        self.frm_param.configure(pady=2)

        # This frame contains the controls to add or remove widgets
        self.frm_ajout = tk.Frame(self.frm_structure,height=250,width=250)
        self.frm_ajout.pack(side=tk.TOP, fill=tk.X)
        
        self.frm_ajout.grid_columnconfigure(0,weight=1)
        self.frm_ajout.grid_columnconfigure(1,weight=1)
        self.frm_ajout.grid_columnconfigure(2,weight=1)
        self.frm_ajout.grid_columnconfigure(3,weight=1)
        self.frm_ajout.grid_columnconfigure(4,weight=1)
        self.frm_ajout.grid_columnconfigure(5,weight=1)
        

        #Label for the widget types
        self.lbl_widget_type = tk.Label(self.frm_ajout,text="Selec type :",justify='right',anchor='e')
        self.lbl_widget_type.grid(column=0,row=0,columnspan=3,sticky=(tk.W,tk.E))

        #Combobox containing the widget types
        for widget in WidgetType:
            widget_type_list.append(widget.name)
        self.combo_widget_type = ttk.Combobox(self.frm_ajout, values=widget_type_list)
        self.combo_widget_type.current(0)
        self.combo_widget_type.grid(column=3, row=0,columnspan=3,sticky=(tk.W,tk.E))

        

        #Label for the the layout mode
        self.lbl_widget_layout = tk.Label(self.frm_ajout,text="Selec layout mode :",justify='right',anchor='e')
        self.lbl_widget_layout.grid(column=0,row=1,columnspan=3,sticky=(tk.W,tk.E))
        self.lbl_widget_layout.configure(justify='left')

        #RadioBoutons for the layout
        self.R1 = Radiobutton(self.frm_ajout, text="place", variable=self.LayoutSelection, value=1)
        self.R1.grid(column=3,row=1,columnspan=1)

        self.R2 = Radiobutton(self.frm_ajout, text="grid", variable=self.LayoutSelection, value=2)
        self.R2.grid(column=4,row=1,columnspan=1)

        self.R3 = Radiobutton(self.frm_ajout, text="pack", variable=self.LayoutSelection, value=3)
        self.R3.grid(column=5,row=1,columnspan=1)

        self.frm_actions = tk.Frame(self.frm_ajout)
        self.frm_actions.grid(column=0,row=2,columnspan=6,sticky=(tk.W,tk.E))

        #Label for the widget name
        self.lbl_widget_name = tk.Label(self.frm_actions,text="Name:",justify='right',anchor='e')      
        self.lbl_widget_name.pack(side=tk.LEFT)


        #An entry widget to enter the widget name
        self.entry_widget_name = tk.Entry(self.frm_actions) 
        self.entry_widget_name.pack(side=tk.LEFT)
        self.entry_widget_name_tooltip = CreateToolTip(self.entry_widget_name, text="Enter the widget name")


        #Add widget button
        self.button_add = tk.Button(self.frm_actions, text="",image=self.appicons["add-box-line"], command=self.addWidget)
        self.button_add.pack(side=tk.LEFT)
        self.button_add.configure(relief="flat")
        self.button_add.configure(overrelief="raised")
        self.button_add_tooltip = CreateToolTip(self.button_add, text="Add a widget")

        #Remove widget button
        self.button_remove = tk.Button(self.frm_actions, text="",image=self.appicons["delete-bin-line"], command=self.removeWidget)
        self.button_remove.pack(side=tk.LEFT)
        self.button_remove.configure(relief="flat")
        self.button_remove.configure(overrelief="raised")
        self.button_remove_tooltip = CreateToolTip(self.button_remove, text="Remove a widget")

        #save widget button
        self.button_save = tk.Button(self.frm_actions, text="",image=self.appicons["save-3-fill"], command=self.save_project)
        self.button_save.pack(side=tk.LEFT)
        self.button_save.configure(relief="flat")
        self.button_save.configure(overrelief="raised") 
        self.button_save_tooltip = CreateToolTip(self.button_save, text="Save")

        #Export widget button
        self.button_export = tk.Button(self.frm_actions, text="",image=self.appicons["export-fill"], command=self.generateCode)
        self.button_export.pack(side=tk.LEFT)
        self.button_export.configure(relief="flat")
        self.button_export.configure(overrelief="raised")
        self.button_export_tooltip = CreateToolTip(self.button_export, text="Export")

        self.separator=ttk.Separator(self.frm_ajout)
        self.separator.place(x=0,y=45,width=300,height=2)


        #Treeview containing the widgets
        self.tree = ttk.Treeview(self.frm_structure, selectmode="extended")
        self.tree.bind("<Button-1>", self.selectionTree)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True) 
        self.tree.heading("#0", text="Widgets")

        self.frm_layout_options= tk.Frame(self.frm_structure,height=250,width=300)
        self.frm_layout_options.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frm_layout_options.grid_propagate(False)

        
        self.menu_bar = tk.Menu(self.root)
        self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_file.add_command(label="Open", command=self.open_file)
        self.menu_file.add_command(label="Save", command=self.save_project)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Export", command=self.export_project)
        self.menu_file.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.menu_file)
        self.root.config(menu=self.menu_bar)


        self.displayOptions()

    # -----------------------------------------------------------------------------------------------
    # Function to load a project
    # -----------------------------------------------------------------------------------------------
    def open_file(self):
        #whe ask the user to select a file
        pickedfiletypes = [("Python file","*.py")]
        f = askopenfile( initialdir= os.getcwd(),
                                    title= "Select a file:",
                                    filetypes = pickedfiletypes)
        if f:
            #Clearing the parameters and layout options
            #Parameters
            for widget in self.frm_param.winfo_children():
                widget.destroy()
            self.paramEntryList.clear()
            #Layout options
            for widget in self.frm_layout_options.winfo_children():
                widget.destroy()
            self.layoutEntryList.clear()
            #Clearin frm_Dessin
            for widget in self.frm_Dessin.winfo_children():
                widget.destroy()
            #we clear the list of widgets
            widgetList.clear()
            #we clear the treeview
            self.tree.delete(*self.tree.get_children())
           
            #we load the file
            module = importlib.import_module(f.name.split(".")[0].split("/")[-1])
            #we reload the module   
            reload(module)
            #we create an instance of the class
            my_class = getattr(module, 'Backup')
            my_instance = my_class(self.frm_Dessin)
            widgetnames.update(my_instance.widgetnames)
            
        
            self.loadWidgetList()
            self.loadWidgetNames()
            self.loadTreeView()
            self.displayOptions()

    # -----------------------------------------------------------------------------------------------
    # Function save the final code
    # -----------------------------------------------------------------------------------------------
    def export_project(self):
        self.generateCode(mode="EXPORT")

    # -----------------------------------------------------------------------------------------------
    # Function to save the project
    # -----------------------------------------------------------------------------------------------
    def save_project(self):
        self.generateCode(mode="BACKUP")
        
    # -----------------------------------------------------------------------------------------------
    # Function to quit the application
    # -----------------------------------------------------------------------------------------------
    def quit():
        pass
    
    # -----------------------------------------------------------------------------------------------
    # Function to create a widget this function is called by the add button
    # -----------------------------------------------------------------------------------------------
    def addWidget(self,widget_type=None,widget_name=None,layout_mode=None,parent_widget=None):
        
        if widget_name == None:
            widget_name = self.entry_widget_name.get()
        
        #we get the selected widget type from the combobox
        if widget_type == None:
            widget_type = list(WidgetType)[self.combo_widget_type.current()]  

        #we get the selected layout mode
        if layout_mode == None:
            layout_mode = self.LayoutSelection.get() 
        
        #getting the function to create the widget
        try:
            func = getattr(tk, widget_type.value) # type: ignore
        except:
            func = getattr(ttk, widget_type.value) # type: ignore

        if parent_widget == None:
            if self.selectedWidget != None:
                widgetparent = self.selectedWidget
            else:
                widgetparent = self.frm_Dessin
        else:
            widgetparent = parent_widget

        
        #If the parent is a frame we can add a widget to it
        # if not whe message the user
        if widgetparent.winfo_class() != "TFrame" and \
           widgetparent.winfo_class() != "Frame" and \
           widgetparent.winfo_class() != "TNotebook"   :
            tk.messagebox.showinfo("Error", "You can only add widgets to a Frame or a Notebook")
            return None
        
        #Whe check the other widgets of this container to see if the selected layout method is the same
        if len(widgetparent.children)>0:
            if self.getPackingMetod(list(widgetparent.children.values())[0])!=self.LayoutSelection.get():
                tk.messagebox.showinfo("Error", "You must select the same layout method \n than the other widgets of the container")
                return None
      
        #we create the widget
        Wid = func(widgetparent)
        #quick placing of the widget
        if widgetparent.winfo_class() == "TNotebook":
            Wid.pack(fill='both',expand=True)
        else:
            if self.LayoutSelection.get() == 1:
                Wid.place(x=0,y=0)
            elif self.LayoutSelection.get() == 2:
                Wid.grid(row=0, column=0)
            else:
                Wid.pack()
        Wid.bind("<Button-1>", self.selectionWidget)

        if widgetparent.winfo_class() == "TNotebook":
            widgetparent.add(Wid,text=str(Wid.winfo_id()))

        if Wid.keys().__contains__("text"):
            Wid.config(text=str(Wid.winfo_id()))

        #Adding the widget to the list of widgets
        widgetList[str(Wid.winfo_id())]=Wid

        #If the has no name we use type + id
        if widget_name == "":
            widget_name = widget_type.value + str(Wid.winfo_id())   


        #Adding the name of the widget the list of widget names
        widgetnames[str(Wid.winfo_id())]=widget_name
        

        #Adding the widget to the treeview
        if widgetparent.winfo_id() == self.frm_Dessin.winfo_id():
            self.tree.insert("", "end", text=widget_name,iid=Wid.winfo_id(), image=self.appicons["price-tag-3-fill"])
        else:
            self.tree.insert(widgetparent.winfo_id(), "end", text=widget_name,iid=Wid.winfo_id(), image=self.appicons["price-tag-3-fill"])
        #je met à jour le panneau de droite pour afficher le nouveau widget
        self.frm_Dessin.update()

        return Wid

    # -----------------------------------------------------------------------------------------------
    # Function that gets the layout method of a widget
    # -----------------------------------------------------------------------------------------------
    def getPackingMetod(self,widget:tk.Widget):
        try:
            if len(widget.place_info())>0:
                return 1
            if len(widget.grid_info())>0:
                return 2
            if len(widget.pack_info())>0:
                return 3
            else:
                return 0
        except:
            return 3

    # -----------------------------------------------------------------------------------------------
    # Function to remove a widget this function is called by the remove button
    # -----------------------------------------------------------------------------------------------
    def removeWidget(self):
        #we check if the widget has children
        if(len(self.selectedWidget.winfo_children())>0):
            tk.messagebox.showinfo("Error", "You can only remove a widget if it has no children")
            return


        #we get the selected widget
        selection = self.selectedWidget
        #if no widget is selected we return
        if selection == None:
            return
        
        #Deleting the widget from the treeview
        self.tree.delete(selection.winfo_id())
        id = str(selection.winfo_id())
        #Deleting the widget from the list of widgets
        widgetList[id].destroy()
        del widgetList[id]

       
        #Deleting the widget from the list of widget names
        del widgetnames[id] 

        #Clering the parameters and layout options
        self.selectedWidget = None 
        self.displayOptions()

        #Clearing the selection frame  
        for frame in self.selectionFrameList:
            frame.destroy()
        self.selectionFrameList = []
        
    # -----------------------------------------------------------------------------------------------
    # Function that draws a frame around the selected widget
    # -----------------------------------------------------------------------------------------------   
    def highlight_widget(self,widget):
        # We draw a frame around the selected widget
        # We retrieve the coordinates of the widget
        # To do this, we loop through each parent as long as master is not None, adding the coordinates
        x = 0
        y = 0
        w = widget.winfo_width()
        h = widget.winfo_height()
        
        while widget.master != None:
            x += widget.winfo_x()
            y += widget.winfo_y()
            widget = widget.master

        # We delete the old frames
        for frame in self.selectionFrameList:
            frame.destroy()
        self.selectionFrameList = []
        # We draw the new frames
    
        selectionT = tk.Canvas(self.root,width=w, height=2, bg="red",borderwidth=0,highlightthickness=0)
        selectionT.place(x=x,y=y) 
        selectionT.tag_raise("all")
        self.selectionFrameList.append(selectionT)

        selectionL = tk.Canvas(self.root,width=2, height=h-2, bg="red",borderwidth=0,highlightthickness=0)
        selectionL.place(x=x,y=y) 
        selectionL.tag_raise("all")
        self.selectionFrameList.append(selectionL)

        selectionR = tk.Canvas(self.root,width=2, height=h-2, bg="red",borderwidth=0,highlightthickness=0)
        selectionR.place(x=x+w,y=y)
        selectionR.tag_raise("all")
        self.selectionFrameList.append(selectionR)

        selectionB = tk.Canvas(self.root,width=w, height=2, bg="red",borderwidth=0,highlightthickness=0)
        selectionB.place(x=x,y=y+h-2) 
        selectionB.tag_raise("all")
        self.selectionFrameList.append(selectionB)
        self.root.update()

    # -----------------------------------------------------------------------------------------------
    # Fonction appelée lorsqu'un widget est selectionné via un clic gauche sur le widget
    # elle permet de selectionner le widget dans le treeview de gauche
    # -----------------------------------------------------------------------------------------------
    def selectionWidget(self,event):
        #si le widget est selectionné est le meme que le widget selectionné précédemment on le deselectionne
        if app.selectedWidget == event.widget:
            app.selectedWidget = None
            #On supprime les cadres de selection    
            for frame in app.selectionFrameList:
                frame.destroy()
            app.selectionFrameList = []
            #On deselectionne le widget dans le treeview
            app.tree.selection_remove(app.tree.selection())
            self.displayOptions()
            return
        
        app.selectedWidget = event.widget

        #On selectionne le widget dans le treeview  
        app.tree.selection_set(app.selectedWidget.winfo_id())
        #On affiche le cadre autour du widget
        self.highlight_widget(self.selectedWidget)

        #we display the parameters in the right panel
        self.displayOptions()
    
    # -----------------------------------------------------------------------------------------------
    # Color picker for the widget properties
    # -----------------------------------------------------------------------------------------------
    def chosecolor(self,event):
        color_code = colorchooser.askcolor(title="Chose color")
        print(color_code[1])
        event.widget.delete(0,tk.END)
        event.widget.insert(0,color_code[1])
        self.changeParam(event)

    # -----------------------------------------------------------------------------------------------
    # Display selected widgjet options
    # -----------------------------------------------------------------------------------------------
    def displayOptions(self):

        #Clearing the parameters and layout options
        #Parameters
        for widget in self.frm_param.winfo_children():
            widget.destroy()
        self.paramEntryList.clear()
        #Layout options
        for widget in self.frm_layout_options.winfo_children():
            widget.destroy()
        self.layoutEntryList.clear()

        #If no widget is selected we display only the top labels with the mention "No Widget selected"
        if self.selectedWidget == None:
            label = tk.Label(self.frm_layout_options, text="Layout mode : No Widget selected",bg="#999")
            label.place(x=0,y=0,relwidth=1)
            label2 = tk.Label(self.frm_param, text="Parameters : No Widget selected" ,bg="#999")
            label2.place(x=0,y=0,relwidth=1)
            return

        #Get the list of parameters
        param = self.selectedWidget.keys().copy()
        #we display the parameters in the right panel

        #Before displaying we diplays the widget name with an entry widget to change it
        #Grey big labl with the mention "Other option"
        labelOther = tk.Label(self.frm_param, text="Other options",bg="#999")
        labelOther.grid(row=0, column=0,columnspan=2,sticky=(tk.W,tk.E))
        #we display the widget name with an entry widget to change it
        labelName = tk.Label(self.frm_param, text="Name")
        labelName.grid(row=1, column=0, sticky=tk.W)    
        entryName = tk.Entry(self.frm_param)
        entryName.insert(0, widgetnames[str(self.selectedWidget.winfo_id())])
        entryName.grid(row=1, column=1, sticky=tk.W)
        entryName.bind("<FocusOut>", self.changeName)
        entryNameTooltip=CreateToolTip(entryName, text="Change the widget name \n this will be used to have better variables names in the code")

        #Grey big labl with the mention "Parameters"
        label2 = tk.Label(self.frm_param, text="Parameters : " + str(self.selectedWidget.winfo_id())  ,bg="#999")
        label2.grid(row=2, column=0,columnspan=2,sticky=(tk.W,tk.E))
        i = 3
        for key in param:
            #we dont display all the parameter 
            if key in hidenProperties:
                continue
            #we display the parameter name
            label = tk.Label(self.frm_param, text=key)
            label.grid(row=i, column=0, sticky=tk.W)
            #If the parameter is in the list of predefined values we display a combobox
            if key in listProperties:
                entry = ttk.Combobox(self.frm_param, values=listProperties[key],width=17)
                entry.insert(0, self.selectedWidget.cget(key))
                entry.grid(row=i, column=1, sticky=tk.W)
                #we save the entry widget in a list
                self.paramEntryList[entry.winfo_id()] = key
                #we bind the entry widget to the change event
                entry.bind("<<ComboboxSelected>>", self.changeParam)    
            else:
                #we display the parameter value
                entry = tk.Entry(self.frm_param)
                entry.insert(0, self.selectedWidget.cget(key))
                entry.grid(row=i, column=1, sticky=tk.W)
                #we save the entry widget in a list
                self.paramEntryList[entry.winfo_id()] = key
                #we bind the entry widget to the change event
                entry.bind("<FocusOut>", self.changeParam)
            if  key in colorProperties:
                entry.bind("<Double-Button-1>", self.chosecolor)
                tooltip=CreateToolTip(entry, text="Double click to chose a color")

            i += 1


        #get the list of layout options
        layoutmetod = self.getPackingMetod(self.selectedWidget)
        param={}
        #we display the layout options in the left panel
        if self.selectedWidget.master.winfo_class() == "TNotebook":
            param={}
            label = tk.Label(self.frm_layout_options, text="Layout mode : NA the widget is in a Notebook",bg="#999")
            label.grid(row=0, column=0,columnspan=2,sticky=(tk.W))
        else:
            if layoutmetod==1:
                param=self.selectedWidget.place_info().copy()
                label = tk.Label(self.frm_layout_options, text="Layout mode : PLACE",anchor="center",bg="#999")
                label.grid(row=0, column=0,columnspan=2,sticky=(tk.W,tk.E))
            if layoutmetod==2:
                param=self.selectedWidget.grid_info().copy()
                label = tk.Label(self.frm_layout_options, text="Layout mode : GRID",anchor="center",bg="#999")
                label.grid(row=0, column=0,columnspan=2,sticky=(tk.W,tk.E))
            if layoutmetod==3:
                param=self.selectedWidget.pack_info().copy()
                label = tk.Label(self.frm_layout_options, text="Layout mode : PACK",anchor="center",bg="#999")
                label.grid(row=0, column=0,columnspan=2,sticky=(tk.W,tk.E))

        
        i = 1
        for key in param:
            if key in hidenLayoutOptions:
                continue
            #we display the parameter name
            label = tk.Label(self.frm_layout_options, text=key,width=20,anchor="w")
            label.grid(row=i, column=0, sticky=tk.W)
            #we display the parameter value
            entry = tk.Entry(self.frm_layout_options,width=25)
            if layoutmetod==1:
                entry.insert(0, self.selectedWidget.place_info().get(key))
            if layoutmetod==2:
                entry.insert(0, self.selectedWidget.grid_info().get(key))
            if layoutmetod==3:
                entry.insert(0, self.selectedWidget.pack_info().get(key))
            entry.grid(row=i, column=1, sticky=tk.W)
            #we save the entry widget in a list
            self.layoutEntryList[entry.winfo_id()] = key
            #we bind the entry widget to the change event
            entry.bind("<FocusOut>", self.changeLayoutParam)
            i += 1

    # -----------------------------------------------------------------------------------------------
    # Function called when a parameter is changed
    # -----------------------------------------------------------------------------------------------
    def changeParam(self,event):
        #we get the parameter name
        param = self.paramEntryList[event.widget.winfo_id()]
    
        #we get the parameter value
        value = event.widget.get()
        #we set the parameter value
        self.selectedWidget.config({param: value})
        self.selectedWidget.update()
        self.highlight_widget(self.selectedWidget)

    # -----------------------------------------------------------------------------------------------
    # Function called when the widget name is changed
    # -----------------------------------------------------------------------------------------------
    def changeName(self,event):
        #we get the parameter value
        value = event.widget.get()
        #we set the parameter value
        widgetnames[str(self.selectedWidget.winfo_id())]=value
        self.tree.item(self.selectedWidget.winfo_id(), text=value)
        self.selectedWidget.update()
        self.highlight_widget(self.selectedWidget)


    # -----------------------------------------------------------------------------------------------
    # Function called when a layout option is changed
    # -----------------------------------------------------------------------------------------------
    def changeLayoutParam(self,event):
        #we get the parameter name
        parameter = self.layoutEntryList[event.widget.winfo_id()]
        #we get the parameter value
        value = event.widget.get()
        #we set the parameter value
        layoutmode=self.getPackingMetod(self.selectedWidget)
        if layoutmode == 1:
            self.selectedWidget.place_configure({parameter: value})
        if layoutmode == 2:
            self.selectedWidget.grid_configure({parameter: value})
        if layoutmode == 3:
            self.selectedWidget.pack_configure({parameter: value})
        
        #self.selectedWidget.config({param: value})
        self.selectedWidget.update()
        self.highlight_widget(self.selectedWidget)
    
    # ----------------------------------------------------------------------------------------------- 
    #Function called when selecting a widget in the treeview
    # -----------------------------------------------------------------------------------------------
    def selectionTree(self,event):
        #On recupere le widget selectionné
        widgetid = self.tree.identify('item', event.x, event.y)
        selection = None
        selection = widgetList[widgetid]
   
        #Si le widget selectionné est le meme que le widget selectionné précédemment on le deselectionne
        if self.selectedWidget == selection:
            self.selectedWidget = None
            #On supprime les cadres de selection    
            for frame in self.selectionFrameList:
                frame.destroy()
            self.selectionFrameList = []
            #On deselectionne le widget dans le treeview
            self.tree.selection_remove(self.tree.selection())
            self.displayOptions()
            return
            
        self.selectedWidget = selection

        #On affiche le cadre autour du widget
        if self.selectedWidget != None:
            if self.selectedWidget.keys().__contains__("width"):
                self.highlight_widget(self.selectedWidget)
        
        #for the selected widget we display the parameters in the right panel
        #we remove all the widgets from the right panel 
        for widget in self.frm_param.winfo_children():
            widget.destroy()
        #we display the parameters in the right panel
        self.displayOptions()


    # ----------------------------------------------------------------------------------------------- 
    # Generate code for EXPORT or BACKUP
    # -----------------------------------------------------------------------------------------------
    def generateCode(self, mode="EXPORT"):
        pickedfiletypes = [("Python file","*.py")]

        result = ""
        result += "import tkinter as tk\n"
        result += "from tkinter import ttk\n"
        result += "from tkinter import messagebox\n"
        result += "from tkinter import colorchooser\n"
        result += "\n"
        if mode == "BACKUP":
            result += "class Backup:\n"
        else:
            result += "class MainWindow:\n"
         
        
        result += "    def __init__(self, root):\n"
        result += "        self.root = root\n"
        if mode != "BACKUP":
            result += "        self.root.title(\"Tkinter Editor\")\n"
            result += "        self.root.geometry(\"800x600\")\n"
        else:
            result += "        self.widgetnames = {}\n"
        #wid=tk.Widget()
        #wid.master self.frm_Dessin
        for wid in widgetList.values():

            #Widget creation function
            if wid.master == self.frm_Dessin:
                parent ="self.root"
            else:
                parent = "self." + widgetnames[str(wid.master.winfo_id())]
            
            if wid.winfo_class() in ttkWidgets:
                result += "        self." + widgetnames[str(wid.winfo_id())] + " = ttk." + wid.winfo_class() + "(" + parent + ")\n"
                func = getattr(ttk, wid.winfo_class()) # type: ignore
            else:
                result += "        self." + widgetnames[str(wid.winfo_id())] + " = tk." + wid.winfo_class() + "(" + parent + ")\n"
                func = getattr(tk, wid.winfo_class()) # type: ignore

            #if we are in backup mode we add the widget name to the widgetnames list
            if mode == "BACKUP":
                result += "        self.widgetnames[str(self." + widgetnames[str(wid.winfo_id())]+".winfo_id())] = \"" + widgetnames[str(wid.winfo_id())] + "\"\n"
           

            #Parameters
            tmpfrm = tk.Frame(self.root)
            defwid = func(tmpfrm)
            defaultparams = defwid.keys().copy()
            for key in defaultparams:
                if defwid.cget(key) != wid.cget(key):
                         result += "        self." + widgetnames[str(wid.winfo_id())] + ".config({\""+key+"\":'" + str(wid.cget(key)) + "'})\n"
            

            #Layout parameters
            layoutTyp = self.getPackingMetod(wid)
            if layoutTyp == 1:
                defwid.place(x=0,y=0)
                defaultlayout = defwid.place_info().copy()
                result += "        self." + widgetnames[str(wid.winfo_id())] + ".place(x=0,y=0)\n" 
            elif layoutTyp == 2:
                defwid.grid(row=0, column=0)
                defaultlayout = defwid.grid_info().copy()
                result += "        self." + widgetnames[str(wid.winfo_id())]  + ".grid(row=0, column=0)\n" 
            else:
                defwid.pack()
                defaultlayout = defwid.pack_info().copy()
                result += "        self." + widgetnames[str(wid.winfo_id())] + ".pack()\n" 
            for key in defaultlayout:
                if key!="in":
                    if layoutTyp==1:
                        if defwid.place_info().get(key) != wid.place_info().get(key):
                            result += "        self." + widgetnames[str(wid.winfo_id())] + ".place_configure({\""+key+"\":'" + str(wid.place_info().get(key)) + "'})\n"
                    if layoutTyp==2:
                        if defwid.grid_info().get(key) != wid.grid_info().get(key):
                            result += "        self." + widgetnames[str(wid.winfo_id())] + ".grid_configure({\""+key+"\":'" + str(wid.grid_info().get(key)) + "'})\n"
                    if layoutTyp==3:
                        if defwid.pack_info().get(key) != wid.pack_info().get(key):
                            result += "        self." + widgetnames[str(wid.winfo_id())] + ".pack_configure({\""+key+"\":'" + str(wid.pack_info().get(key)) + "'})\n"
                    
            defwid.destroy()
            tmpfrm.destroy()

            

        result += "\n"
        if mode != "BACKUP":
            result += "if __name__ == \"__main__\":\n"
            result += "    root = tk.Tk()\n"
            result += "    app = MainWindow(root)\n"
            result += "    root.mainloop()\n"

        f = asksaveasfile( initialdir= os.getcwd(),
                                    title= "Enter à file:",
                                    filetypes = pickedfiletypes)
        if f:
            f.write(result)

    # ----------------------------------------------------------------------------------------------- 
    # Get Default parameter collection used to comapare with the widget parameters during the export
    # -----------------------------------------------------------------------------------------------
    def getDefaultParameters(self,widget:tk.Widget):
        result = ""
        #getting the function to create the widget
        try:
            func = getattr(tk, widget.winfo_class()) # type: ignore
        except:
            func = getattr(ttk, widget.winfo_class()) # type: ignore
        defwid = func(self.root)
        params = defwid.keys().copy()
        defwid.destroy()
        return params
    
    # -----------------------------------------------------------------------------------------------
    # Load the widget list (used during the loading of a project)
    # -----------------------------------------------------------------------------------------------
    def loadWidgetList(self,widgetparent:tk.Widget=None):
        if widgetparent == None:
            for widget in self.frm_Dessin.winfo_children():
                widgetList[str(widget.winfo_id())]=widget
                widget.bind("<Button-1>", self.selectionWidget)
                self.loadWidgetList(widget)
        else:
            for widget in widgetparent.winfo_children():
                widgetList[str(widget.winfo_id())]=widget
                widget.bind("<Button-1>", self.selectionWidget)
                self.loadWidgetList(widget)

    # -----------------------------------------------------------------------------------------------
    # Load the widget names (used during the loading of a project)
    # -----------------------------------------------------------------------------------------------
    def loadWidgetNames(self):
        i=0
        list2 = widgetnames.copy()
        names=[]
        for val in widgetnames.values():
            names.append(val)

       

        widgetnames.clear()
        for widget in widgetList.values():
            widgetnames[str(widget.winfo_id())]=names[i]
            i+=1
        
    # -----------------------------------------------------------------------------------------------
    # Load the treeview (used during the loading of a project)
    # -----------------------------------------------------------------------------------------------
    def loadTreeView(self):
        for widget in widgetList.values():
            if widget.master == self.frm_Dessin:
                self.tree.insert("", "end", text=widgetnames[str(widget.winfo_id())],iid=widget.winfo_id(), image=self.appicons["price-tag-3-fill"])
            else:
                self.tree.insert(widget.master.winfo_id(), "end", text=widgetnames[str(widget.winfo_id())],iid=widget.winfo_id(), image=self.appicons["price-tag-3-fill"])



if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()