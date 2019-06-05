import wx

class InitiativeDialog(wx.Dialog):
    def __init__(self, units, *args, **kw):
        super(InitiativeDialog, self).__init__(*args, **kw)

        self.SetTitle("Player Initiatives")

        outerBox = wx.BoxSizer(wx.VERTICAL)

        self.units = units
        self.boxes = []

        for unit in units:
            innerBox = wx.BoxSizer(wx.HORIZONTAL)
            innerBox.Add(wx.StaticText(self, 0, unit['name']),
                         1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
            self.boxes.append(wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER))
            innerBox.Add(self.boxes[-1], 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
            outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        for i in range(len(self.boxes) - 1):
            self.boxes[i].Bind(wx.EVT_TEXT_ENTER, lambda event: self.NavigateIn())
        self.boxes[-1].Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())

        okBtn = wx.Button(self, 0, "Done")
        okBtn.Bind(wx.EVT_BUTTON, lambda event: self.OK())
        outerBox.Add(okBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        idClose = wx.NewId()
        self.Bind(wx.EVT_MENU, lambda event: self.Close(), id=idClose)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_ESCAPE , idClose)
        ])
        self.SetAcceleratorTable(accel_tbl)

        self.SetSizer(outerBox)
        self.Fit()

        self.Layout()

    def OK(self):
        if self.isValid(): self.EndModal(wx.ID_OK)
        for i in range(len(self.boxes)):
            s = self.boxes[i].GetValue().strip()
            if len(s) > 0: self.units[i]['initiative'] = int(s)
            else: self.units[i]['initiative'] = None
        self.EndModal(wx.ID_OK)

    def isValid(self):
        try:
            for box in self.boxes:
                s = box.GetValue().strip()
                if len(s) > 0: int(s)
        except ValueError as e:
            return False
        return True

    def OnClose(self, e):
        self.Destroy()
