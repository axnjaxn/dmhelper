import wx, os, random, json, copy, operator
from editunit import *
from imagepreview import *
from unitdict import *
from initiative import *

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title = "DM Helper", style = wx.DEFAULT_FRAME_STYLE)
        self.units = []
        self.imagesToRemove = []

        self.SetMinSize((800, 600))
        self.SetSize((800, 600))

        outerBox = wx.BoxSizer(wx.VERTICAL)

        self.mgmt = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.mgmt.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onListItemActivated)
        outerBox.Add(self.mgmt, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)

        # Unit controls

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

        # Initiative and damage controls

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        clearBtn = wx.Button(self, 0, "Clear Initiative")
        clearBtn.Bind(wx.EVT_BUTTON, lambda event: self.clearInitiative())
        innerBox.Add(clearBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBtn = wx.Button(self, 0, "Roll Initiative")
        rollBtn.Bind(wx.EVT_BUTTON, lambda event: self.rollInitiative())
        innerBox.Add(rollBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        reletterBtn = wx.Button(self, 0, "Reletter Units")
        reletterBtn.Bind(wx.EVT_BUTTON, lambda event: self.reletter())
        innerBox.Add(reletterBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        dictionaryBtn = wx.Button(self, 0, "Unit Lookup")
        dictionaryBtn.Bind(wx.EVT_BUTTON, lambda event: self.dictionary())
        innerBox.Add(dictionaryBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.Panel(self), 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        dmgBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        dmgBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.doDamage(dmgBox.GetValue()))
        dmgBox.Bind(wx.EVT_SET_FOCUS, self.disableNumberShortcuts)
        dmgBox.Bind(wx.EVT_KILL_FOCUS, self.enableNumberShortcuts)
        innerBox.Add(dmgBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBtn = wx.Button(self, 0, "Do damage")
        rollBtn.Bind(wx.EVT_BUTTON, lambda event: self.doDamage(dmgBox.GetValue()))
        innerBox.Add(rollBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.AddSpacer(15)

        # Dice controls

        innerBox = wx.BoxSizer(wx.HORIZONTAL)

        self.totalBox = wx.TextCtrl(self, style=wx.TE_READONLY, size=(40, -1))

        addRoll = lambda value: str(value + int(self.totalBox.GetValue() or 0))

        innerBox.Add(wx.StaticText(self, 0, 'Roll'), 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '1', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(1))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '4', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(4))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '6', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(6))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '8', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(8))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '10', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(10))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '12', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(12))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '20', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(20))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, '100', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.addRoll(100))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox.Add(self.totalBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        btn = wx.Button(self, 0, 'C', style=wx.BU_EXACTFIT)
        btn.Bind(wx.EVT_BUTTON, lambda event: self.totalBox.SetValue(''))
        innerBox.Add(btn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox.Add(wx.Panel(self), 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBox1 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        rollBox1.Bind(wx.EVT_TEXT_ENTER, lambda event: self.roll(rollBox1.GetValue(), rollBox2.GetValue()))
        rollBox1.Bind(wx.EVT_SET_FOCUS, self.disableNumberShortcuts)
        rollBox1.Bind(wx.EVT_KILL_FOCUS, self.enableNumberShortcuts)
        innerBox.Add(rollBox1, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "d"), 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBox2 = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        rollBox2.Bind(wx.EVT_TEXT_ENTER, lambda event: self.roll(rollBox1.GetValue(), rollBox2.GetValue()))
        rollBox2.Bind(wx.EVT_SET_FOCUS, self.disableNumberShortcuts)
        rollBox2.Bind(wx.EVT_KILL_FOCUS, self.enableNumberShortcuts)
        innerBox.Add(rollBox2, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        rollBtn = wx.Button(self, 0, "Roll")
        rollBtn.Bind(wx.EVT_BUTTON, lambda event: self.roll(rollBox1.GetValue(), rollBox2.GetValue()))
        innerBox.Add(rollBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        self.SetSizer(outerBox)

        self.hasFocus = True
        self.Bind(wx.EVT_CLOSE, self.onClose)

        idClose = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.Close(), id=idClose)
        idPreview = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.openPreview(), id=idPreview)
        idCycle = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.cycleUnits(), id=idCycle)

        idRollClear = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.totalBox.SetValue(''), id=idRollClear)
        idRoll1 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(1, clear=True), id=idRoll1)
        idRoll4 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(4, clear=True), id=idRoll4)
        idRoll6 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(6, clear=True), id=idRoll6)
        idRoll8 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(8, clear=True), id=idRoll8)
        idRoll10 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(10, clear=True), id=idRoll10)
        idRoll12 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(12, clear=True), id=idRoll12)
        idRoll20 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(20, clear=True), id=idRoll20)
        idRollAdv = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(20, clear=True, advantage=1), id=idRollAdv)
        idRollDis = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(20, clear=True, advantage=-1), id=idRollDis)

        idRollAdd1 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(1), id=idRollAdd1)
        idRollAdd4 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(4), id=idRollAdd4)
        idRollAdd6 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(6), id=idRollAdd6)
        idRollAdd8 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(8), id=idRollAdd8)
        idRollAdd10 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(10), id=idRollAdd10)
        idRollAdd12 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(12), id=idRollAdd12)
        idRollAdd20 = wx.NewId(); self.Bind(wx.EVT_MENU, lambda event: self.addRoll(20), id=idRollAdd20)

        self.accel_numbers = wx.AcceleratorTable([
            (wx.ACCEL_CTRL,  ord('Q'), idClose),
            (wx.ACCEL_CTRL,  ord('W'), idClose),
            (wx.ACCEL_NORMAL, ord(' '), idPreview),
            (wx.ACCEL_NORMAL, wx.WXK_RETURN, idCycle),

            (wx.ACCEL_NORMAL, ord('c'), idRollClear), # C for Clear
            (wx.ACCEL_SHIFT, ord('1'), idRoll1),
            (wx.ACCEL_SHIFT, ord('4'), idRoll4),
            (wx.ACCEL_SHIFT, ord('6'), idRoll6),
            (wx.ACCEL_SHIFT, ord('8'), idRoll8),
            (wx.ACCEL_SHIFT, ord('0'), idRoll10),
            (wx.ACCEL_SHIFT, ord('2'), idRoll12),
            (wx.ACCEL_NORMAL, ord('s'), idRoll20), # S for Simple D20
            (wx.ACCEL_NORMAL, ord('a'), idRollAdv), # A for Advantage
            (wx.ACCEL_NORMAL, ord('d'), idRollDis), # D for Disadvantage

            (wx.ACCEL_NORMAL, ord('1'), idRollAdd1),
            (wx.ACCEL_NORMAL, ord('4'), idRollAdd4),
            (wx.ACCEL_NORMAL, ord('6'), idRollAdd6),
            (wx.ACCEL_NORMAL, ord('8'), idRollAdd8),
            (wx.ACCEL_NORMAL, ord('0'), idRollAdd10),
            (wx.ACCEL_NORMAL, ord('2'), idRollAdd12)
        ])

        self.accel_no_numbers = wx.AcceleratorTable([
            (wx.ACCEL_CTRL,  ord('Q'), idClose),
            (wx.ACCEL_CTRL,  ord('W'), idClose),
            (wx.ACCEL_NORMAL, ord(' '), idPreview)
        ])

        self.SetAcceleratorTable(self.accel_numbers)

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
        if len(self.units) == 0 or 'image' not in self.units[0]: return

        dlg = ImagePreviewDialog(self.units[0], self)
        dlg.ShowModal()
        dlg.Destroy()

    def selectedUnits(self):
        selected = []
        for i in range(self.mgmt.GetItemCount()):
            if self.mgmt.IsSelected(i):
                selected.append(i)
                self.mgmt.Select(i, False)
        return selected

    def playerUnits(self):
        pcs = []
        for unit in self.units:
            if unit['pc']: pcs.append(unit)
        return pcs

    def nonPlayerUnits(self):
        npcs = []
        for unit in self.units:
            if not unit['pc']: npcs.append(unit)
        return npcs

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
        self.mgmt.SetColumnWidth(5, wx.LIST_AUTOSIZE_USEHEADER)

        self.mgmt.Bind(wx.EVT_LIST_COL_CLICK, self.colClicked)

    def colClicked(self, event):
        if event.GetColumn() == 1: self.units.sort(key = lambda entry: entry['name'])
        elif event.GetColumn() == 2:
            self.units.sort(key = operator.itemgetter('initiative', 'dex'), reverse = True)
        elif event.GetColumn() == 3: self.units.sort(key = lambda entry: entry['ac'], reverse = True)
        elif event.GetColumn() == 4: self.units.sort(key = lambda entry: entry['hp'], reverse = True)
        elif event.GetColumn() == 5: self.units.sort(key = lambda entry: entry['notes'])
        self.refreshMgmt()

    def disableNumberShortcuts(self, event):
        self.SetAcceleratorTable(self.accel_no_numbers)
        event.Skip()

    def enableNumberShortcuts(self, event):
        self.SetAcceleratorTable(self.accel_numbers)
        event.Skip()

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

        for i in selected:
            self.mgmt.Select(i, True)

    def hasImage(self, image):
        for unit in self.units:
            if 'image' in unit and unit['image'] == image:
                return True
        return UnitDict().hasImage(image)

    # Note: these are actually removed when write() is called
    def removeImage(self, image):
        self.imagesToRemove.append(image)

    def removeUnit(self, unit):
        self.units.remove(unit)
        if 'image' in unit:
            if not self.hasImage(unit['image']):
                self.removeImage(unit['image'])

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
                self.removeUnit(unit)
            self.refreshMgmt()

    def clearInitiative(self):
        selected = self.selectedUnits()
        if len(selected) == 0:
            dlg = wx.MessageDialog(self, 'Clear initiative for all units?', caption='Clear initiative?', style=wx.YES_NO|wx.CENTER)
            if dlg.ShowModal() == wx.ID_YES:
                for unit in self.units:
                    unit['initiative'] = None
        else:
            for idx in selected:
                self.units[idx]['initiative'] = None
        self.refreshMgmt()

    def rollInitiative(self):
        selected = self.selectedUnits()

        roll = lambda unit: random.randint(1, 20) + unit['dex']

        if len(selected) > 0:
            for idx in selected:
                self.units[idx]['initiative'] = roll(self.units[idx])
        else:
            dlg = InitiativeDialog(self.playerUnits(), self)
            if dlg.ShowModal() == wx.ID_OK:
                for unit in self.nonPlayerUnits():
                    unit['initiative'] = roll(unit)
            dlg.Destroy()
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

    def dictionary(self):
        dlg = UnitDictDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            self.units.append(dlg.getUnit())
            self.refreshMgmt()
        dlg.Destroy()

    def doDamage(self, pts):
        try:
            pts = int(pts)
        except ValueError as e:
            return

        selected = self.selectedUnits()
        for idx in selected:
            self.units[idx]['hp'] = max(self.units[idx]['hp'] - pts, 0)
        self.refreshMgmt()

    def addRoll(self, dn, clear = False, advantage = 0):
        v = int(self.totalBox.GetValue() or 0)
        if clear: v = 0
        result = random.randint(1, dn)
        if advantage < 0:
            result = min(random.randint(1, dn), result)
        elif advantage > 0:
            result = max(random.randint(1, dn), result)
        v = v + result
        self.totalBox.SetValue(str(v))

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

    def read(self):
        if os.path.isfile('dmhelper.json'):
            self.units = json.load(open('dmhelper.json', 'r'))
        else:
            self.units = []
        self.imagesToRemove = []

    def write(self):
        json.dump(self.units, open('dmhelper.json', 'w'), indent=4)
        for image in self.imagesToRemove:
            os.remove(image)
        self.imagesToRemove = []

app = wx.App()
frame = MainFrame(None)
frame.Center()
frame.Show()
app.MainLoop()
