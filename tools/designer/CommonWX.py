import wx


def showAlertE(Exception, parent, field):
    message = (
          type(Exception) + "\n"
        + type(Exception.args) + "\n"
        + str(Exception) + "\n")

    msg = wx.MessageDialog(
            parent, message,
            "Error in field %s" % field,
            wx.OK | wx.ICON_INFORMATION
           )
    msg.ShowModal()
    msg.Destroy()
