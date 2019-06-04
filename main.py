import wx, os, random, webbrowser, json, copy, uuid

class EditUnitDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(EditUnitDialog, self).__init__(*args, **kw)

        self.bmp = wx.Bitmap()
        self.image = None
        self.nameBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.nameBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())
        self.pcBox = wx.CheckBox(self)
        self.dexBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.dexBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())
        self.initBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.initBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())
        self.acBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.acBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())
        self.hpBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.hpBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())
        self.notesBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.notesBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())

        idClose = wx.NewId()
        self.Bind(wx.EVT_MENU, lambda event: self.Close(), id=idClose)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_ESCAPE , idClose)
        ])
        self.SetAcceleratorTable(accel_tbl)

        self.rebuild()

    def rebuild(self):
        self.SetTitle("Edit Unit")

        outerBox = wx.BoxSizer(wx.VERTICAL)

        if self.image is not None:
            if not self.bmp.LoadFile(self.image): raise Exception()
            self.imageFrame = wx.StaticBitmap(self, 0, self.bmp)
            innerBox = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)
            panel.SetBackgroundColour(self.GetBackgroundColour())
            innerBox.Add(panel, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)
            innerBox.Add(self.imageFrame, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)
            panel = wx.Panel(self)
            panel.SetBackgroundColour(self.GetBackgroundColour())
            innerBox.Add(panel, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)
            outerBox.Add(innerBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
            removeBtn = wx.Button(self, 0, "Remove Image")
            removeBtn.Bind(wx.EVT_BUTTON, lambda event: self.removeImage())
            outerBox.Add(removeBtn,
                         0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        else:
            addBtn = wx.Button(self, 0, "Paste Image")
            addBtn.Bind(wx.EVT_BUTTON, lambda event: self.pasteImage())
            outerBox.Add(addBtn,
                         0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Name"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.nameBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "Is PC"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.pcBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Dex"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.dexBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "Init"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.initBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "AC"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.acBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "HP"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.hpBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Notes"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.notesBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        okBtn = wx.Button(self, 0, "OK")
        okBtn.Bind(wx.EVT_BUTTON, lambda event: self.OK())
        outerBox.Add(okBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        self.SetSizer(outerBox)
        self.Fit()

        self.Layout()

    def pasteImage(self):
        cb = wx.Clipboard().Get()
        if cb.Open():
            if cb.IsSupported(wx.DataFormat(format=wx.DF_BITMAP)):
                data = wx.BitmapDataObject()
                cb.GetData(data)
                bmp = data.GetBitmap()
                fn = '%s.png' % (uuid.uuid1().hex)
                if bmp.SaveFile(fn, wx.BITMAP_TYPE_PNG):
                    self.image = fn
                    self.bmp = bmp
                    self.rebuild()
            cb.Close()

    def removeImage(self):
        self.image = None
        self.bmp = None
        self.imageFrame.Hide()
        self.rebuild()

    def setUnit(self, unit):
        if 'image' in unit:
            self.image = unit['image']
            self.bmp.LoadFile(self.image)
        else:
            self.image = None
            self.bmp = None
        self.nameBox.SetValue(unit['name'])
        self.pcBox.SetValue(unit['pc'])
        self.dexBox.SetValue(str(unit['dex']))
        self.initBox.SetValue(str(unit['initiative'] or ''))
        self.acBox.SetValue(str(unit['ac']))
        self.hpBox.SetValue(str(unit['hp']))
        self.notesBox.SetValue(unit['notes'])
        self.rebuild()

    def isValid(self):
        try:
            int(self.dexBox.GetValue())
            if len(self.initBox.GetValue()) > 0: int(self.initBox.GetValue())
            int(self.acBox.GetValue())
            int(self.hpBox.GetValue())
        except ValueError as e:
            return False
        return True

    def OK(self):
        if self.isValid(): self.EndModal(wx.ID_OK)

    def getUnit(self):
        unit =  {
            'name': self.nameBox.GetValue(),
            'pc': self.pcBox.GetValue(),
            'dex': int(self.dexBox.GetValue()),
            'initiative': None,
            'ac': int(self.acBox.GetValue()),
            'hp': int(self.hpBox.GetValue()),
            'notes': self.notesBox.GetValue()
        }
        if len(self.initBox.GetValue()) > 0:
            unit['initiative'] = int(self.initBox.GetValue())
        if self.image is not None:
            unit['image'] = self.image
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

        addBtn = wx.Button(self, 0, "-")
        addBtn.Bind(wx.EVT_BUTTON, self.removeUnits)
        innerBox.Add(addBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        addBtn = wx.Button(self, 0, "+")
        addBtn.Bind(wx.EVT_BUTTON, lambda event: self.addUnit())
        innerBox.Add(addBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        cycleBtn = wx.Button(self, 0, "Cycle units")
        cycleBtn.Bind(wx.EVT_BUTTON, lambda event: self.cycleUnits())
        innerBox.Add(cycleBtn, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        upBtn = wx.Button(self, 0, u"\u2191")
        upBtn.Bind(wx.EVT_BUTTON, lambda event: self.moveUp())
        innerBox.Add(upBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        downBtn = wx.Button(self, 0, u"\u2193")
        downBtn.Bind(wx.EVT_BUTTON, lambda event: self.moveDown())
        innerBox.Add(downBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.AddSpacer(15)

        middleBox = wx.BoxSizer(wx.HORIZONTAL)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        rollBtn = wx.Button(self, 0, "Roll Initiative")
        rollBtn.Bind(wx.EVT_BUTTON, lambda event: self.rollInitiative())
        innerBox.Add(rollBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        reletterBtn = wx.Button(self, 0, "Reletter Units")
        reletterBtn.Bind(wx.EVT_BUTTON, lambda event: self.reletter())
        innerBox.Add(reletterBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        middleBox.Add(innerBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        middleBox.AddSpacer(40)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        self.dmgBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.dmgBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.doDamage(self.dmgBox.GetValue()))
        innerBox.Add(self.dmgBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBtn = wx.Button(self, 0, "Do damage")
        rollBtn.Bind(wx.EVT_BUTTON, lambda event: self.doDamage(self.dmgBox.GetValue()))
        innerBox.Add(rollBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        middleBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(middleBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.AddSpacer(15)

        middleBox = wx.BoxSizer(wx.HORIZONTAL)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        self.rollBox1 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.rollBox1.Bind(wx.EVT_TEXT_ENTER, lambda event: self.roll(self.rollBox1.GetValue(), self.rollBox2.GetValue()))
        innerBox.Add(self.rollBox1, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "d"), 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.rollBox2 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.rollBox2.Bind(wx.EVT_TEXT_ENTER, lambda event: self.roll(self.rollBox1.GetValue(), self.rollBox2.GetValue()))
        innerBox.Add(self.rollBox2, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBtn = wx.Button(self, 0, "Roll")
        rollBtn.Bind(wx.EVT_BUTTON, lambda event: self.roll(self.rollBox1.GetValue(), self.rollBox2.GetValue()))
        innerBox.Add(rollBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        middleBox.Add(innerBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        middleBox.AddSpacer(40)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Search"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        self.searchBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.searchBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.search(self.searchBox.GetValue()))
        innerBox.Add(self.searchBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        searchBtn = wx.Button(self, 0, "Go")
        searchBtn.Bind(wx.EVT_BUTTON, lambda event: self.search(self.searchBox.GetValue()))
        innerBox.Add(searchBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        middleBox.Add(innerBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(middleBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        self.SetSizer(outerBox)

        self.hasFocus = True
        self.Bind(wx.EVT_CLOSE, self.onClose)

        idClose = wx.NewId()
        idPreview = wx.NewId()
        idCycle = wx.NewId()
        self.Bind(wx.EVT_MENU, lambda event: self.Close(), id=idClose)
        self.Bind(wx.EVT_MENU, lambda event: self.openPreview(), id=idPreview)
        self.Bind(wx.EVT_MENU, lambda event: self.cycleUnits(), id=idCycle)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL,  ord('Q'), idClose),
            (wx.ACCEL_CTRL,  ord('W'), idClose),
            (wx.ACCEL_NORMAL, ord(' '), idPreview),
            (wx.ACCEL_NORMAL, wx.WXK_RETURN, idCycle)
        ])
        self.SetAcceleratorTable(accel_tbl)

        self.read()
        self.refreshMgmt()
        self.Layout()

    def onClose(self, event):
        self.write()
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

    def openPreview(self):
        if len(self.units) == 0: return

        dlg = EditUnitDialog(self)
        dlg.setUnit(self.units[0])
        if dlg.ShowModal() == wx.ID_OK:
            self.units[0] = dlg.getUnit()
        dlg.Destroy()
        self.refreshMgmt()

    def selectedUnits(self):
        selected = []
        for i in range(self.mgmt.GetItemCount()):
            if self.mgmt.IsSelected(i):
                selected.append(i)
                self.mgmt.Select(i, False)
        return selected

    def refreshMgmt(self):
        self.mgmt.ClearAll()

        self.mgmt.InsertColumn(0, "")
        self.mgmt.InsertColumn(1, "Name")
        self.mgmt.InsertColumn(2, "Init")
        self.mgmt.InsertColumn(3, "AC")
        self.mgmt.InsertColumn(4, "HP")
        self.mgmt.InsertColumn(5, "Notes")

        for i in range(len(self.units)):
            unit = self.units[i]

            if 'image' in unit: s = u'\u25A0'
            else: s = ' '

            self.mgmt.Append([s, unit['name'], unit['initiative'] or '', unit['ac'], unit['hp'], unit['notes']])
            if not unit['pc']:
                self.mgmt.SetItemTextColour(i, wx.Colour(255, 0, 0))

        self.mgmt.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(2, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)
        self.mgmt.SetColumnWidth(4, wx.LIST_AUTOSIZE_USEHEADER)

        self.mgmt.Bind(wx.EVT_LIST_COL_CLICK, self.colClicked)

    def colClicked(self, event):
        if event.GetColumn() == 1: self.units.sort(key = lambda entry: entry['name'])
        elif event.GetColumn() == 2: self.units.sort(key = lambda entry: entry['initiative'], reverse = True)
        elif event.GetColumn() == 3: self.units.sort(key = lambda entry: entry['ac'], reverse = True)
        elif event.GetColumn() == 4: self.units.sort(key = lambda entry: entry['hp'], reverse = True)
        elif event.GetColumn() == 5: self.units.sort(key = lambda entry: entry['notes'])
        self.refreshMgmt()

    def cycleUnits(self):
        if len(self.units) == 0: return

        unit = self.units[0]
        self.units.remove(self.units[0])
        self.units.append(unit)
        self.refreshMgmt()

    def moveUp(self):
        selected = self.selectedUnits()
        if len(selected) != 1: return
        idx = selected[0]
        if idx > 0:
            self.units[idx], self.units[idx - 1] = self.units[idx - 1], self.units[idx]
            self.refreshMgmt()
            self.mgmt.Select(idx - 1, True)

    def moveDown(self):
        selected = self.selectedUnits()
        if len(selected) != 1: return
        idx = selected[0]
        if idx < len(self.units) - 1:
            self.units[idx], self.units[idx + 1] = self.units[idx + 1], self.units[idx]
            self.refreshMgmt()
            self.mgmt.Select(idx + 1, True)

    def addUnit(self):
        selected = self.selectedUnits()
        for i in selected:
            self.units.append(copy.deepcopy(self.units[i]))

        if len(selected) == 0:
            dlg = EditUnitDialog(self)
            if dlg.ShowModal() == wx.ID_OK:
                unit = dlg.getUnit()
                self.units.append(unit)
            dlg.Destroy()

        self.refreshMgmt()

    def removeUnits(self, event):
        selected = self.selectedUnits()
        if len(selected) == 0: return

        toremove = []
        for i in selected: toremove.append(self.units[i])

        s = toremove[0]['name']
        for unit in toremove[1:]:
            s = s + '\n' + unit['name']

        dlg = wx.MessageDialog(self, s, caption="Remove these units?", style=wx.YES_NO|wx.CENTER)
        if dlg.ShowModal() == wx.ID_YES:
            for unit in toremove:
                self.units.remove(unit)
            self.refreshMgmt()

    def rollInitiative(self):
        selected = self.selectedUnits()
        for idx in selected:
            self.units[idx]['initiative'] = random.randint(1, 20) + self.units[idx]['dex']
        self.refreshMgmt()

    def _getLettering(self, name):
        s = name.strip().split(' ')
        if len(s) > 1 and len(s[-1]) == 1:
            c = ord(s[-1])
            if c >= ord('A') and c <= ord('Z'): return s[-1]

    def _stripLetter(self, name):
        if self._getLettering(name) is None: return name
        return name[:-2].strip()

    def reletter(self):
        selected = self.selectedUnits()
        for idx in selected:
            self.units[idx]['name'] = self._stripLetter(self.units[idx]['name'])

        firstLetter = ord('A') - 1
        for unit in self.units:
            letter = self._getLettering(unit['name'])
            if letter is not None: firstLetter = max(ord(letter), firstLetter)
        firstLetter = firstLetter + 1

        for idx in selected:
            if self._getLettering(self.units[idx]['name']) is None and firstLetter <= ord('Z'):
                self.units[idx]['name'] = self.units[idx]['name'].strip() + ' ' + chr(firstLetter)
                firstLetter = firstLetter + 1

        self.refreshMgmt()

    def doDamage(self, pts):
        try:
            pts = int(pts)
        except ValueError as e:
            return

        selected = self.selectedUnits()
        for idx in selected:
            self.units[idx]['hp'] = max(self.units[idx]['hp'] - pts, 0)
        self.refreshMgmt()

    def roll(self, n, dn):
        try:
            n = int(n)
            dn = int(dn)
        except:
            return

        rolls = []
        s = ''
        for i in range(n):
            rolls.append(random.randint(1, dn))
            if i > 0: s = s + ', '
            s = s + str(rolls[-1])
        wx.MessageDialog(self, "%s\nTotal: %d" % (s, sum(rolls)), caption="Rolls", style = wx.OK | wx.CENTRE).ShowModal()

    def search(self, queryStr):
        url = 'https://roll20.net/compendium/dnd5e/searchbook/?terms=%s' % (queryStr)
        webbrowser.open_new_tab(url)

    def read(self): self.units = json.load(open('dmhelper.json', 'r'))

    def write(self): json.dump(self.units, open('dmhelper.json', 'w'), indent=4)

app = wx.App()
frame = MainFrame(None)
frame.Center()
frame.Show()
app.MainLoop()
