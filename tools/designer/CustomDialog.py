import wx
from CommonWX import showAlertE


class CustomDialog(wx.Dialog):
    "A dynamic dialog to ask user about arbitrary fields"

    def __init__(
            self, parent, ID, title, size=wx.DefaultSize,
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, fields=None, data=None,
            ):

        wx.Dialog.__init__(self, parent, ID, title, pos, size, style)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.textctrls = {}
        for field in fields:
            box = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(self, -1, field)
            label.SetHelpText("This is the help text for the label")
            box.Add(label, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

            text = wx.TextCtrl(self, -1, "", size=(80, -1))
            text.SetHelpText("Here's some help text for field #1")
            if field in data:
                text.SetValue(repr(data[field]))
            box.Add(text, 1, wx.ALIGN_CENTRE | wx.ALL, 1)
            sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 1)
            self.textctrls[field] = text

        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(
            line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    @classmethod
    def do_input(Class, parent, title, fields, data):
        dlg = Class(
            parent, -1, title, size=(350, 200),
            style=wx.DEFAULT_DIALOG_STYLE,     # & ~wx.CLOSE_BOX,
            fields=fields, data=data
            )

        dlg.CenterOnScreen()
        while 1:
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                values = {}
                for field in fields:
                    try:
                        values[field] = eval(dlg.textctrls[field].GetValue())
                    except Exception as e:
                        showAlertE(e, parent, field)
                        break
                else:
                    return dict([(field, values[field]) for field in fields])
            else:
                return None
