import os, json, copy, wx

# This class is basically a lazily-implemented singleton
class UnitDict:
    def __init__(self):
        self.read()

    def add(self, unit):
        name = unit['name'].strip()
        self.units[name] = copy.deepcopy(unit)
        self.units[name]['initiative'] = None

    def names(self):
        return sorted(self.units.keys())

    def has(self, name):
        return name.strip() in self.units

    def get(self, name):
        return copy.deepcopy(self.units[name.strip()])

    def remove(self, name):
        name = name.strip()
        if name in self.units:
            del self.units[name]

    def read(self):
        if os.path.isfile('units.json'):
            self.units = json.load(open('units.json', 'r'))
        else:
            self.units = {}

    def write(self): json.dump(self.units, open('units.json', 'w'), indent=4)

    def hasImage(self, image):
        for name in self.units:
            unit = self.units[name]
            if 'image' in unit and unit['image'] == image:
                return True
        return False

class UnitDictDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(UnitDictDialog, self).__init__(*args, **kw)
        self.udict = UnitDict()

        self.SetTitle('Dictionary')

        outerBox = wx.BoxSizer(wx.VERTICAL)

        self.selector = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.selector.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.activate)
        outerBox.Add(self.selector, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        okBtn = wx.Button(self, 0, "Remove")
        okBtn.Bind(wx.EVT_BUTTON, self.remove)
        outerBox.Add(okBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        okBtn = wx.Button(self, 0, "Select")
        okBtn.Bind(wx.EVT_BUTTON, self.activate)
        outerBox.Add(okBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        self.SetMinSize((0, 600))

        self.SetSizer(outerBox)
        self.Fit()
        self.Layout()

        self.refresh()

    def OnClose(self, e):
        self.Destroy()

    def refresh(self):
        self.selector.ClearAll()
        self.selector.InsertColumn(0, "Name")
        self.names = self.udict.names()
        for name in self.names:
            self.selector.Append([name])
        self.selector.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

    def activate(self, event):
        for i in range(self.selector.GetItemCount()):
            if self.selector.IsSelected(i):
                self.select(i)

    def remove(self, event):
        for i in range(self.selector.GetItemCount()):
            if self.selector.IsSelected(i):
                dlg = wx.MessageDialog(self, 'Are you sure you want to remove "%s"?' % (self.names[i]), caption='Remove unit', style=wx.YES_NO|wx.CENTER)
                if dlg.ShowModal() == wx.ID_YES:
                    unit = self.udict.get(self.names[i])
                    self.udict.remove(self.names[i])
                    self.udict.write()
                    if 'image' in unit:
                        parent = self.GetParent()
                        if not parent.hasImage(unit['image']):
                            parent.removeImage(unit['image'])
                    self.refresh()
                break

    def select(self, idx):
        self.selected = self.udict.get(self.names[idx])
        self.EndModal(wx.ID_OK)

    def getUnit(self):
        return self.selected
