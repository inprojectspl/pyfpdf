import wx
import wx.lib.ogl as ogl


class MyEvtHandler(ogl.ShapeEvtHandler):
    "Custom Event Handler for Shapes"

    def __init__(self, callback):
        ogl.ShapeEvtHandler.__init__(self)
        self.callback = callback

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected() and keys & ogl.KEY_SHIFT:
            shape.Select(False, dc)
            # canvas.Redraw(dc)
            canvas.Refresh(False)
        else:
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected() and not keys & ogl.KEY_SHIFT:
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                canvas.Refresh(False)

        self.callback()

    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

        self.callback()

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):

        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)

        shape = self.GetShape()
        if isinstance(shape, ogl.BitmapShape):

            # Resize bitmap and reassing to shape
            w, h = pt._controlPointDragEndWidth, pt._controlPointDragEndHeight

            img = wx.Image(shape.GetFilename())
            img.Rescale(w, h, quality=wx.IMAGE_QUALITY_HIGH)
            bmp = wx.BitmapFromImage(img)
            shape.SetBitmap(bmp)
            shape.SetFilename(shape.GetFilename())
            shape.GetCanvas().Refresh(False)
        self.callback()

    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
        self.callback()
        if "wxMac" in wx.PlatformInfo:
            shape.GetCanvas().Refresh(False)

    def OnLeftDoubleClick(self, x, y, keys=0, attachment=0):
        self.callback("LeftDoubleClick")

    def OnRightClick(self, *dontcare):
        self.callback("RightClick")
