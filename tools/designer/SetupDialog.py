import wx
import Constants


class SetupDialog(wx.Dialog):

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 135))

        sizer = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box3 = wx.BoxSizer(wx.HORIZONTAL)

        self.cmb_paper_size = wx.ComboBox(
            self, -1, choices=Constants.PAPER_SIZES, style=wx.CB_READONLY)

        self.cmb_paper_size.SetValue(parent.paper_size)

        self.cmb_paper_orientation = wx.ComboBox(
                self, -1,
                choices=Constants.PAPER_ORIENTATIONS,
                style=wx.CB_READONLY
            )

        orient = 'Portrait' if parent.paper_orientation == 'P' else 'Landscape'
        self.cmb_paper_orientation.SetValue(orient)

        self.ok_btn = wx.Button(self, wx.ID_OK, 'Save')

        box1.Add(self.cmb_paper_size, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box1, wx.ALIGN_CENTRE | wx.ALL, 5)

        box2.Add(self.cmb_paper_orientation, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box2, wx.ALIGN_CENTRE | wx.ALL, 5)

        box3.Add(self.ok_btn, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box3, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.SetSizer(sizer)

        self.Centre()
