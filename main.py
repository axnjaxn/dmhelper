import os, random, time
import wx

class Unit:
    counter = 1

    def __init__(self, name = "", pc = True, initiative = 0, ac = 0, hp = 0, notes = ""):
        self.ident = Unit.nextCounter()
        self.name = name
        self.pc = pc
        self.initiative = initiative
        self.ac = ac
        self.hp = hp
        self.notes = notes

    @staticmethod
    def nextCounter():
        ident = Unit.counter
        Unit.counter = Unit.counter + 1
        return ident

class EditUnitDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(EditUnitDialog, self).__init__(*args, **kw)

        self.SetTitle("Edit Unit")

        outerBox = wx.BoxSizer(wx.VERTICAL)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Name"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.nameBox = wx.TextCtrl(self)
        innerBox.Add(self.nameBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "Is PC"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.pcBox = wx.CheckBox(self)
        innerBox.Add(self.pcBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Init"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.initBox = wx.TextCtrl(self)
        innerBox.Add(self.initBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "AC"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.acBox = wx.TextCtrl(self)
        innerBox.Add(self.acBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "HP"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.hpBox = wx.TextCtrl(self)
        innerBox.Add(self.hpBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Notes"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.notesBox = wx.TextCtrl(self)
        innerBox.Add(self.notesBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        okBtn = wx.Button(self, 0, "OK")
        okBtn.Bind(wx.EVT_BUTTON, lambda event: self.OK())
        outerBox.Add(okBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        self.SetSizer(outerBox)
        self.Fit()

        self.Layout()

    def setUnit(self, unit):
        self.nameBox.SetValue(unit.name)
        self.pcBox.SetValue(unit.pc)
        self.initBox.SetValue(str(unit.initiative))
        self.acBox.SetValue(str(unit.ac))
        self.hpBox.SetValue(str(unit.hp))
        self.notesBox.SetValue(unit.notes)

    def isValid(self):
        try:
            int(self.initBox.GetValue())
            int(self.acBox.GetValue())
            int(self.hpBox.GetValue())
        except ValueError as e:
            return False
        return True

    def OK(self):
        if self.isValid(): self.EndModal(wx.ID_OK)

    def getUnit(self):
        unit = Unit(self.nameBox.GetValue(), self.pcBox.GetValue(),
                    int(self.initBox.GetValue()),
                    int(self.acBox.GetValue()),
                    int(self.hpBox.GetValue()),
                    self.notesBox.GetValue())
        return unit

    def OnClose(self, e):
        self.Destroy()

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "DM Helper", style = wx.DEFAULT_FRAME_STYLE)
        self.units = []

        self.SetMinSize((800, 600))
        self.SetSize((800, 600))

        outerBox = wx.BoxSizer(wx.VERTICAL)

        self.mgmt = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.mgmt.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onListItemActivated)
        outerBox.Add(self.mgmt, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)

        cycleBtn = wx.Button(self, 0, "Cycle units")
        cycleBtn.Bind(wx.EVT_BUTTON, lambda event: self.cycleUnits())
        innerBox.Add(cycleBtn, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        addBtn = wx.Button(self, 0, "+")
        addBtn.Bind(wx.EVT_BUTTON, lambda event: self.addUnit())
        innerBox.Add(addBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        self.SetSizer(outerBox)

        self.hasFocus = True
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.refreshMgmt()
        self.Layout()

    def onClose(self, event):
        event.Skip()

    def onListItemActivated(self, event):
        ind = event.GetIndex()
        unit = self.units[ind]

        dlg = EditUnitDialog(self)
        dlg.setUnit(unit)
        if dlg.ShowModal() == wx.ID_OK:
            self.units[ind] = dlg.getUnit()
        dlg.Destroy()
        self.refreshMgmt()

    def refreshMgmt(self):
        self.mgmt.ClearAll()

        self.mgmt.InsertColumn(0, "Name")
        self.mgmt.InsertColumn(1, "Init")
        self.mgmt.InsertColumn(2, "AC")
        self.mgmt.InsertColumn(3, "HP")
        self.mgmt.InsertColumn(4, "Notes")

        for i in range(len(self.units)):
            unit = self.units[i]
            self.mgmt.Append([unit.name, unit.initiative, unit.ac, unit.hp, unit.notes])
            if not unit.pc:
                self.mgmt.SetItemTextColour(i, wx.Colour(255, 0, 0))

        self.mgmt.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)

        self.mgmt.Bind(wx.EVT_LIST_COL_CLICK, self.colClicked)

    def colClicked(self, event):
        if event.GetColumn() == 0: self.units.sort(key = lambda entry: entry.name)
        elif event.GetColumn() == 1: self.units.sort(key = lambda entry: entry.initiative, reverse = True)
        elif event.GetColumn() == 2: self.units.sort(key = lambda entry: entry.ac, reverse = True)
        elif event.GetColumn() == 3: self.units.sort(key = lambda entry: entry.hp, reverse = True)
        elif event.GetColumn() == 4: self.units.sort(key = lambda entry: entry.notes)
        self.refreshMgmt()

    def cycleUnits(self):
        if len(units) == 0: return

        unit = self.units[0]
        self.units.remove(self.units[0])
        self.units.append(unit)
        self.refreshMgmt()

    def addUnit(self):
        dlg = EditUnitDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            unit = dlg.getUnit()
            self.units.append(unit)
        dlg.Destroy()
        self.refreshMgmt()

app = wx.App()
frame = MainFrame(None)
frame.Center()
frame.Show()
app.MainLoop()
