import os
import sys
import wx
import wx.lib.ogl as ogl
import Constants
import CustomDialog
from SetupDialog import SetupDialog
from Element import Element

from wx.lib.wordwrap import wordwrap

import fpdf


class AppFrame(wx.Frame):
    "OGL Designer main window"
    title = "PyFPDF Template Designer (wx OGL)"

    def __init__(self):
        wx.Frame.__init__(
                        self,
                        None, -1, self.title,
                        size=(640, 480),
                        style=wx.DEFAULT_FRAME_STYLE
                    )
        sys.excepthook = self.except_hook
        self.filename = ""
        # Create a toolbar:
        tsize = (16, 16)
        self.toolbar = self.CreateToolBar(
            wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT
        )

        artBmp = wx.ArtProvider.GetBitmap
        self.toolbar.AddSimpleTool(
                wx.ID_NEW,
                artBmp(wx.ART_NEW, wx.ART_TOOLBAR, tsize),
                "New"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_OPEN,
                artBmp(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize),
                "Open"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_SAVE,
                artBmp(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize),
                "Save"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_SAVEAS,
                artBmp(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize),
                "Save As..."
            )
        self.toolbar.AddSimpleTool(
                wx.ID_SETUP,
                artBmp(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, tsize),
                "Template settings"
            )

        self.toolbar.AddSeparator()
        # ------- To Do:
        # ~ self.toolbar.AddSimpleTool(
        # ~ wx.ID_UNDO, artBmp(wx.ART_UNDO, wx.ART_TOOLBAR, tsize), "Undo")
        # ~ self.toolbar.AddSimpleTool(
        # ~ wx.ID_REDO, artBmp(wx.ART_REDO, wx.ART_TOOLBAR, tsize), "Redo")
        # ~ self.toolbar.AddSeparator()
        # -------
        self.toolbar.AddSimpleTool(
                wx.ID_CUT,
                artBmp(wx.ART_CUT, wx.ART_TOOLBAR, tsize),
                "Remove"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_COPY,
                artBmp(wx.ART_COPY, wx.ART_TOOLBAR, tsize),
                "Duplicate"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_PASTE,
                artBmp(wx.ART_PASTE, wx.ART_TOOLBAR, tsize),
                "Insert"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_REPLACE,
                artBmp(wx.ART_GO_FORWARD, wx.ART_TOOLBAR, tsize),
                "Move"
            )
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(
                wx.ID_FIND,
                artBmp(wx.ART_FIND, wx.ART_TOOLBAR, tsize),
                "Find"
            )
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(
                wx.ID_PRINT,
                artBmp(wx.ART_PRINT, wx.ART_TOOLBAR, tsize),
                "Print"
            )
        self.toolbar.AddSimpleTool(
                wx.ID_ABOUT,
                artBmp(wx.ART_HELP, wx.ART_TOOLBAR, tsize),
                "About"
            )

        self.toolbar.Realize()

        # self.toolbar.EnableTool(wx.ID_SAVEAS,       False)
        self.toolbar.EnableTool(wx.ID_UNDO,         False)
        self.toolbar.EnableTool(wx.ID_REDO,         False)
        self.toolbar.EnableTool(wx.ID_PRINT,        False)

        menu_handlers = [
            (wx.ID_NEW, self.do_new),
            (wx.ID_OPEN, self.do_open),
            (wx.ID_SAVE, self.do_save),
            (wx.ID_SAVEAS, self.do_save_as),
            (wx.ID_PRINT, self.do_print),
            (wx.ID_FIND, self.do_find),
            (wx.ID_REPLACE, self.do_modify),
            (wx.ID_CUT, self.do_cut),
            (wx.ID_COPY, self.do_copy),
            (wx.ID_PASTE, self.do_paste),
            (wx.ID_ABOUT, self.do_about),
            (wx.ID_SETUP, self.do_setup),
        ]
        for menu_id, handler in menu_handlers:
            self.Bind(wx.EVT_MENU, handler, id=menu_id)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # put stuff into sizer

        self.CreateStatusBar()

        canvas = self.canvas = ogl.ShapeCanvas(self)
        maxWidth = 2000
        maxHeight = 2000
        canvas.SetScrollbars(20, 20, maxWidth//20, maxHeight//20)
        sizer.Add(canvas, 1, wx.GROW)

        canvas.SetBackgroundColour("WHITE")

        diagram = self.diagram = ogl.Diagram()
        canvas.SetDiagram(diagram)
        diagram.SetCanvas(canvas)
        diagram.SetSnapToGrid(False)

        # apply sizer
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.Show(1)

        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_event)
        self.elements = []

        self.paper_size = Constants.DEFAULT_PAPER_SIZE
        self.paper_orientation = Constants.DEFAULT_PAPER_ORIENTATION

        self.draw_paper_size_guides()

        self.cur_dir = os.getcwd()

    def draw_paper_size_guides(self):
        idx = 0
        # Only one paper size guide
        for elem in self.elements:
            if elem.static:
                idx = self.elements.index(elem)
                elem.remove()
        orient = 'portrait' if self.paper_orientation == 'P' else 'landscape'
        current_paper_properties = "%s_%s" % (
                self.paper_size,
                orient
            )

        # ~ self.create_elements
        #   (
        #       current_paper_properties, 'R', 0, 0,
        #       Conststants.paper_size_options[current_paper_properties][0],
        #       Conststants.paper_size_options[current_paper_properties][1],
        #       size=70, foreground=0x808080, priority=-100,
        #       canvas=self.canvas, frame=self, static=True
        #   )

        guide = Element(
            name=current_paper_properties,
            type='R', x1=0, y1=0,
            x2=Constants.PAPER_SIZE_OPTIONS[current_paper_properties][0],
            y2=Constants.PAPER_SIZE_OPTIONS[current_paper_properties][1],
            font="Arial", size=70, bold=False, italic=False, underline=False,
            foreground=0x808080, background=0xFFFFFF,
            align="L", text='', priority=-100,
            canvas=self.canvas, frame=self, static=True
            )

        # Insert new element and shape respecting template previous z-order
        self.elements.insert(idx, guide)
        last_shape = self.canvas.GetDiagram().GetShapeList()[-1]
        del(self.canvas.GetDiagram().GetShapeList()[-1])
        self.canvas.GetDiagram().GetShapeList().insert(idx, last_shape)

        self.diagram.ShowAll(1)

        self.SetStatusText(current_paper_properties.replace("_", " "))

    def on_key_event(self, event):
        """ Respond to a keypress event.

            We make the arrow keys move the selected object(s) by one pixel in
            the given direction.
        """
        step = 1
        if event.ControlDown():
            step = 20

        if event.GetKeyCode() == wx.WXK_UP:
            self.move_elements(0, -step)
        elif event.GetKeyCode() == wx.WXK_DOWN:
            self.move_elements(0, step)
        elif event.GetKeyCode() == wx.WXK_LEFT:
            self.move_elements(-step, 0)
        elif event.GetKeyCode() == wx.WXK_RIGHT:
            self.move_elements(step, 0)
        elif event.GetKeyCode() == wx.WXK_DELETE:
            self.do_cut()
        else:
            event.Skip()

    def do_setup(self, evt=None):
        dlg = SetupDialog(self, -1, 'Select paper size')
        if dlg.ShowModal() == wx.ID_OK:
            self.paper_size = dlg.cmb_paper_size.GetValue()
            self.paper_orientation = dlg.cmb_paper_orientation.GetValue()[0]

            self.draw_paper_size_guides()

        dlg.Destroy()

    # Only use for empty Templates
    def do_new(self, evt=None):
        for element in self.elements:
            element.remove()
        self.elements = []

        if evt != "OPEN":
            self.filename = ''
            self.SetTitle("New template - " + self.title)

        # draw paper size guides
        self.draw_paper_size_guides()
        self.canvas.Refresh(False)
        self.diagram.ShowAll(1)

    def do_open(self, evt):
        dlg = wx.FileDialog(
                self, message="Choose a file",
                defaultDir=os.getcwd(),
                defaultFile="",
                wildcard="CSV Files (*.csv)|*.csv",
                style=wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            self.filename = dlg.GetPaths()[0]
            if self.filename:
                self.do_new("OPEN")
                self.toolbar.EnableTool(wx.ID_PRINT, True)
                os.chdir(os.path.dirname(self.filename))
                self.cur_dir = os.getcwd()
                dlg.Destroy()
                self.SetTitle(self.filename + " - " + self.title)

                tmp = self.__ReadCSV(self.filename)

                # sort by z-order (priority)
                for args in sorted(tmp, key=lambda t: t[-1]):
                    if __debug__:
                        print(args)
                    self.create_elements(*args)
                self.diagram.ShowAll(1)
                return True
        else:
            return False

    def __ReadCSV(self, filename):
        tmp = []
        with open(self.filename) as file:
            for lno, linea in enumerate(file.readlines()):
                if __debug__:
                    print("processing line", lno, linea)
                args = []
                for i, v in enumerate(linea.split(";")):
                    if not v.startswith("'"):
                        v = v.replace(",", ".")
                    if v.strip() == '':
                        v = None
                    else:
                        v = eval(v.strip())
                    args.append(v)
                tmp.append(args)
        return tmp

    def __WriteCSV(self):
        def csv_repr(v, decimal_sep="."):
            if isinstance(v, float):
                return ("%0.2f" % v).replace(".", decimal_sep)
            else:
                return repr(v)
        with open(self.filename, "w") as f:
            # Todo: I need to test this
            for element in sorted(self.elements, key=lambda e: e.name):
                if element.static:
                    continue
                d = element.as_dict()
                row = [
                        d['name'], d['type'],
                        d['x1'], d['y1'], d['x2'], d['y2'],
                        d['font'], d['size'],
                        d['bold'], d['italic'], d['underline'],
                        d['foreground'], d['background'],
                        d['align'], d['text'], d['priority'],
                    ]
                f.write(";".join([csv_repr(v) for v in row]))
                f.write("\n")

    def ask_forAName(self):
        dlg = wx.FileDialog(
                self, message="Give the file a name",
                defaultDir=os.getcwd(),
                defaultFile=self.filename,
                wildcard="CSV Files (*.csv)|*.csv",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            self.filename = dlg.GetPaths()[0]
            os.chdir(os.path.dirname(self.filename))
            self.cur_dir = os.getcwd()
            self.toolbar.EnableTool(wx.ID_PRINT, True)

        self.SetTitle(self.filename + " - " + self.title)
        dlg.Destroy()

    def do_save_as(self, evt, filename=None):
        self.ask_forAName()

        if self.filename:
            self.do_save(evt, filename=self.filename)

    def do_save(self, evt, filename=None):
        try:
            from time import gmtime, strftime
            ts = strftime("%Y-%m-%d_%H_%M", gmtime())
            os.rename(self.filename, self.filename + ts + ".bak")
        except Exception as e:
            if __debug__:
                print(e)
            pass
        if not self.filename:
            self.ask_forAName()

        # yes, I know.
        if not self.filename:
            return False
        self.__WriteCSV()

        return True

    def do_print(self, evt):
        # Generate the pdf with the in_memory template
        paper_size = self.paper_size or Constants.DEFAULT_PAPER_SIZE
        orient = self.paper_orientation or Constants.DEFAULT_PAPER_ORIENTATION

        t = fpdf.Template(
                format=paper_size,
                orientation=orient,
                elements=[e.as_dict() for e in self.elements if not e.static]
            )
        t.add_page()
        if not t['logo'] or not os.path.exists(t['logo']):
            # put a default logo so it doesn't throw an exception
            logo = os.path.join(
                   os.path.dirname(__file__),
                   'tutorial', 'logo.png'
                )
            t.set('logo', logo)
        try:
            t.render(self.filename + ".pdf")
        except Exception:
            if __debug__ and False:
                import pdb
                pdb.pm()
            else:
                raise
        if sys.platform.startswith("linux"):
            os.system('xdg-open "%s.pdf"' % self.filename)
        else:
            os.startfile(self.filename + ".pdf")

    def do_find(self, evt):
        # Search for an element by the name of a sertain field
        dlg = wx.TextEntryDialog(
                self,
                'Enter text to search for',
                'Find Text',
                ''
            )
        if dlg.ShowModal() == wx.ID_OK:
            txt = dlg.GetValue().encode("latin1").lower()
            for element in self.elements:
                if txt in element:
                    element.selected = True
                    if __debug__ and False:
                        print("Found:", element.name)
                    break
            self.canvas.Refresh(False)
        dlg.Destroy()

    def do_cut(self, evt=None):
        "Delete selected elements"
        new_elements = []
        for element in self.elements:
            if element.selected:
                if __debug__ and False:
                    print("Erasing:", element.name)
                element.selected = False
                self.canvas.Refresh(False)
                element.remove()
            else:
                new_elements.append(element)
        self.elements = new_elements
        self.canvas.Refresh(False)
        self.diagram.ShowAll(1)

    def do_copy(self, evt):
        "Duplicate selected elements"
        fields = ['qty', 'dx', 'dy']
        data = {'qty': 1, 'dx': 0.0, 'dy': 5.0}
        data = CustomDialog.do_input(self, 'Copy elements', fields, data)
        if not data:
            return False
        new_elements = []
        # TODO: this can be simplified with few nested nightmares
        for i in range(1, data['qty']+1):
            for element in self.elements:
                if element.selected:
                    if __debug__:
                        print("Copying: ", element.name)
                    pass
                    new_element = element.copy()
                    name = new_element.name
                    if len(name) > 2 and name[-2:].isdigit():
                        new_element.name = (
                                name[:-2] + "%02d" % (int(name[-2:])+i)
                            )
                    else:
                        new_element.name = new_element.name + "_copy"
                    new_element.selected = False
                    new_element.move(data['dx']*i, data['dy']*i)
                    new_elements.append(new_element)
        self.elements.extend(new_elements)
        self.canvas.Refresh(False)
        self.diagram.ShowAll(1)
        return True

    def do_paste(self, evt):
        "Insert new elements"
        element = Element.new(self)
        if element:
            self.canvas.Refresh(False)
            self.elements.append(element)
            self.diagram.ShowAll(1)

    def do_modify(self, evt):
        "Modify selected elements"
        fields = ['dx', 'dy']
        data = {'dx': 0.0, 'dy': 0.0}
        data = CustomDialog.do_input(
            self, 'Modify (move) elements',
            fields, data)
        if data:
            self.move_elements(data['dx'], data['dy'])
            self.canvas.Refresh(False)
            self.diagram.ShowAll(1)

    def create_elements(
                self, name, type, x1, y1, x2, y2,
                font="Arial", size=12,
                bold=False, italic=False, underline=False,
                foreground=0x000000, background=0xFFFFFF,
                align="L", text="", priority=0, canvas=None, frame=None,
                static=False, **kwargs):
        element = Element(
                    name=name, type=type, x1=x1, y1=y1, x2=x2, y2=y2,
                    font=font, size=size,
                    bold=bold, italic=italic, underline=underline,
                    foreground=foreground, background=background,
                    align=align, text=text, priority=priority,
                    canvas=canvas or self.canvas, frame=frame or self,
                    static=static
                )
        self.elements.append(element)

    def move_elements(self, x, y):
        for element in self.elements:
            if element.selected:
                if __debug__:
                    print("moving", element.name, x, y)
                element.x = element.x + x
                element.y = element.y + y

    def do_about(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = self.title
        info.Version = Constants.__version__
        info.Copyright = Constants.__copyright__
        info.Description = (
            "Visual Template designer for PyFPDF (using wxPython OGL library)\n"
            "Input files are CSV format describing the layout, separated by ;\n"
            "Use toolbar buttons to open, save, print (preview) your template, "
            "and there are buttons to find, add, remove or duplicate elements.\n"
            "Over an element, a double left click opens edit text dialog, "
            "and a right click opens edit properties dialog. \n"
            "Multiple element can be selected with shift left click. \n"
            "Use arrow keys or drag-and-drop to move elements.\n"
            "For further information see project webpage:"
            )
        info.WebSite = ("https://github.com/reingart/pyfpdf/blob/master/docs/Templates.md",
                        "pyfpdf GitHub Project")
        info.Developers = [Constants.__author__]

        info.License = wordwrap(Constants.__license__, 500, wx.ClientDC(self))

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)

    def except_hook(self, type, value, trace):
        import traceback
        exc = traceback.format_exception(type, value, trace)
        for e in exc:
            wx.LogError(e)
        wx.LogError('Unhandled Error: %s: %s' % (str(type), str(value)))
