import wx

class ImagePreviewDialog(wx.Dialog):
    def __init__(self, unit, *args, **kw):
        super(ImagePreviewDialog, self).__init__(*args, **kw)

        self.bmp = wx.Bitmap()

        self.SetTitle("Preview")

        outerBox = wx.BoxSizer(wx.VERTICAL)

        if 'image' not in unit: raise Exception('Unit does not have an image')
        if not self.bmp.LoadFile(unit['image']): raise Exception('Could not load %s' % (unit['image']))

        self.imageFrame = wx.StaticBitmap(self, 0, self.bmp)
        outerBox.Add(self.imageFrame, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)

        idClose = wx.NewId()
        self.Bind(wx.EVT_MENU, lambda event: self.EndModal(wx.ID_OK), id=idClose)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_ESCAPE , idClose),
            (wx.ACCEL_NORMAL, ord(' ') , idClose)
        ])
        self.SetAcceleratorTable(accel_tbl)

        self.SetSizer(outerBox)
        self.Fit()
        self.Layout()

    def OnClose(self, e):
        self.Destroy()
