import os
import wx
import wx.lib.ogl as ogl

from CustomDialog import CustomDialog
from EventHandler import MyEvtHandler


class Element(object):
    "Visual class that represent a placeholder in the template"

    fields = [
                'name', 'type',
                'x1', 'y1', 'x2', 'y2',
                'font', 'size',
                'bold', 'italic', 'underline',
                'foreground', 'background',
                'align', 'text', 'priority'
            ]

    def __init__(
            self, canvas=None, frame=None, zoom=5.0, static=False, **kwargs
            ):
        self.kwargs = kwargs
        self.zoom = zoom
        self.frame = frame
        self.canvas = canvas
        self.static = static

        # name = kwargs['name']
        type = kwargs['type']

        x, y, w, h = self.set_coordinates(
            kwargs['x1'], kwargs['y1'],
            kwargs['x2'], kwargs['y2']
            )
        # text = kwargs['text'] if type is text, display text

        # If type is image, display it.
        if (type.lower() == 'i'):
            if os.path.exists(self.text):
                img = wx.Image(self.text)
                img.Rescale(w, h, quality=wx.IMAGE_QUALITY_HIGH)
                bmp = wx.BitmapFromImage(img)
                self.shape = ogl.BitmapShape()
                self.shape.SetBitmap(bmp)
                self.shape.SetFilename(self.text)
                shape = self.shape
            else:
                shape = self.shape = ogl.RectangleShape(w, h)

        else:
            shape = self.shape = ogl.RectangleShape(w, h)

        shape.SetMaintainAspectRatio(False)

        if static:
            shape.SetDraggable(False)

        shape.SetX(x)
        shape.SetY(y)
        # if pen:    shape.SetPen(pen)
        # if brush:  shape.SetBrush(brush)
        shape.SetBrush(wx.TRANSPARENT_BRUSH)

        if type not in ('L', 'B', 'BC'):
            if not static:
                pen = wx.LIGHT_GREY_PEN
            else:
                pen = wx.RED_PEN
            shape.SetPen(pen)

        self.text = kwargs['text']

        evthandler = MyEvtHandler(self.evt_callback)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)
        shape.SetCentreResize(False)

        canvas.AddShape(shape)

    @classmethod
    def new(Class, parent):
        data = dict(name='some_name', type='T',
                    x1=5.0, y1=5.0, x2=100.0, y2=10.0,
                    font="Arial", size=12,
                    bold=False, italic=False, underline=False,
                    foreground=0x000000,
                    background=0xFFFFFF,
                    align="L", text="", priority=0)
        data = CustomDialog.do_input(parent, 'New element', Class.fields, data)

        if data:
            return Class(canvas=parent.canvas, frame=parent, **data)

    def edit(self):
        "Edit current element (show a dialog box with all fields)"
        data = self.kwargs.copy()
        x1, y1, x2, y2 = self.get_coordinates()
        data.update(
                    dict(
                        name=self.name,
                        text=self.text,
                        x1=x1, y1=y1, x2=x2, y2=y2,
                       )
                   )
        data = CustomDialog.do_input(
                self.frame, 'Edit element', self.fields, data
            )
        if data:
            self.kwargs.update(data)
            self.name = data['name']
            self.text = data['text']
            x, y, w, h = self.set_coordinates(
                data['x1'], data['y1'],
                data['x2'], data['y2']
                )
            self.shape.SetX(x)
            self.shape.SetY(y)
            self.shape.SetWidth(w)
            self.shape.SetHeight(h)

            # Refresh bitmap
            if data['type'].lower() == 'i':
                img = wx.Image(self.text)
                img.Rescale(w, h, quality=wx.IMAGE_QUALITY_HIGH)
                bmp = wx.BitmapFromImage(img)
                self.shape.SetBitmap(bmp)
                self.shape.SetFilename(self.text)

            self.canvas.Refresh(False)
            self.canvas.GetDiagram().ShowAll(1)

    def edit_text(self):
        "Allow text edition (i.e. for doubleclick)"
        dlg = wx.TextEntryDialog(
            self.frame, 'Text for %s' % self.name,
            'Edit Text', '')
        if self.text:
            dlg.SetValue(self.text)
        if dlg.ShowModal() == wx.ID_OK:
            self.text = dlg.GetValue().encode("latin1")
        dlg.Destroy()

    def copy(self):
        "Return an identical duplicate"
        kwargs = self.as_dict()
        element = Element(
            canvas=self.canvas, frame=self.frame,
            zoom=self.zoom, static=self.static,
            **kwargs)
        return element

    def remove(self):
        """
        Erases visual shape from OGL canvas (element must be deleted manually)
        """
        self.canvas.RemoveShape(self.shape)

    def move(self, dx, dy):
        "Change pdf coordinates (converting to wx internal values)"
        x1, y1, x2, y2 = self.get_coordinates()
        x1 += dx
        x2 += dx
        y1 += dy
        y2 += dy
        x, y, w, h = self.set_coordinates(x1, y1, x2, y2)
        self.shape.SetX(x)
        self.shape.SetY(y)

    def evt_callback(self, evt_type=None):
        "Event dispatcher"
        x1, y1, x2, y2 = self.get_coordinates()
        if evt_type == "LeftDoubleClick":
            self.edit_text()
        if evt_type == 'RightClick':
            self.edit()
        # update the status bar
        self.frame.SetStatusText(
                "%s (%0.2f, %0.2f) - (%0.2f, %0.2f)" %
                    (self.name, x1, y1, x2, y2))

    def get_coordinates(self):
        "Convert from wx to pdf coordinates"
        x, y = self.shape.GetX(), self.shape.GetY()
        w, h = self.shape.GetBoundingBoxMax()
        w -= 1
        h -= 1
        x1 = x/self.zoom - w/self.zoom/2.0
        x2 = x/self.zoom + w/self.zoom/2.0
        y1 = y/self.zoom - h/self.zoom/2.0
        y2 = y/self.zoom + h/self.zoom/2.0
        return x1, y1, x2, y2

    def set_coordinates(self, x1, y1, x2, y2):
        "Convert from pdf to wx coordinates"
        x1 = x1 * self.zoom
        x2 = x2 * self.zoom
        y1 = y1 * self.zoom
        y2 = y2 * self.zoom

        # shapes seems to be centred, pdf coord not
        w = max(x1, x2) - min(x1, x2) + 1
        h = max(y1, y2) - min(y1, y2) + 1
        x = (min(x1, x2) + w/2.0)
        y = (min(y1, y2) + h/2.0)
        return x, y, w, h

    def text(self, txt=None):
        if txt is not None:
            if not isinstance(txt, str):
                txt = str(txt)
            self.kwargs['text'] = txt
            self.shape.ClearText()
            for line in txt.split('\n'):
                self.shape.AddText(line)
            self.canvas.Refresh(False)
        return self.kwargs['text']
    text = property(text, text)

    def set_x(self, x):
        self.shape.SetX(x)
        self.canvas.Refresh(False)
        self.evt_callback()

    def set_y(self, y):
        self.shape.SetY(y)
        self.canvas.Refresh(False)
        self.evt_callback()

    def get_x(self):
        return self.shape.GetX()

    def get_y(self):
        return self.shape.GetY()

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def selected(self, sel=None):
        if sel is not None:
            print("Setting Select(%s)" % sel)
            self.shape.Select(sel)
        return self.shape.Selected()
    selected = property(selected, selected)

    def name(self, name=None):
        if name is not None:
            self.kwargs['name'] = name
        return self.kwargs['name']
    name = property(name, name)

    def __contains__(self, k):
        "Implement in keyword for searchs"
        return k in self.name.lower() or self.text and k in self.text.lower()

    def as_dict(self):
        """
        Return a dictionary representation, used by pyfpdf.
        This will be upgrade for multiline implementation
        """
        d = self.kwargs
        x1, y1, x2, y2 = self.get_coordinates()
        d.update({
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                'text': self.text
            })
        return d
