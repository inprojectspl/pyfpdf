#!/usr/bin/python
# -*- coding: latin-1 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"Visual Template designer for PyFPDF (using wxPython OGL library)"

import wx
import wx.lib.ogl as ogl
from AppFrame import AppFrame

if __name__ == "__main__":
    app = wx.PySimpleApp()
    ogl.OGLInitialize()
    frame = AppFrame()
    app.MainLoop()
    app.Destroy()
