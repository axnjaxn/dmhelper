import wx, uuid

from unitdict import *

class EditUnitDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(EditUnitDialog, self).__init__(*args, **kw)

        self.bmp = wx.Bitmap()
        self.image = None
        self.save_image = False

        idClose = wx.NewId()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, lambda event: self.Close(), id=idClose)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_ESCAPE , idClose)
        ])
        self.SetAcceleratorTable(accel_tbl)

        self.rebuild()

    def rebuild(self):
        self.DestroyChildren()

        self.nameBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.nameBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.NavigateIn())
        self.pcBox = wx.CheckBox(self)
        self.dexBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        self.dexBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.NavigateIn())
        self.acBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        self.acBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.NavigateIn())
        self.hpBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        self.hpBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.NavigateIn())
        self.initBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(60, -1))
        self.initBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.NavigateIn())
        self.notesBox = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.notesBox.Bind(wx.EVT_TEXT_ENTER, lambda event: self.OK())

        self.SetTitle("Edit Unit")

        outerBox = wx.BoxSizer(wx.VERTICAL)

        if self.image is not None:
            if not self.bmp.LoadFile(self.image): raise Exception('Could not load image')

            screen_size = wx.DisplaySize()
            image_size = self.bmp.GetSize()
            scale = min(min((screen_size[0] - 20.0) / image_size[0], 0.5 * screen_size[1] / image_size[1]), 1.0)
            if scale < 1.0:
                image = self.bmp.ConvertToImage()
                image = image.Scale(int(scale * image_size[0]), int(scale * image_size[1]), wx.IMAGE_QUALITY_BICUBIC)
                self.bmp = wx.Bitmap(image)

            self.imageFrame = wx.StaticBitmap(self, 0, self.bmp)

            innerBox = wx.BoxSizer(wx.HORIZONTAL)
            panel = wx.Panel(self)
            innerBox.Add(panel, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)
            innerBox.Add(self.imageFrame, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)
            panel = wx.Panel(self)
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
        innerBox.Add(wx.StaticText(self, 0, "AC"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.acBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(wx.StaticText(self, 0, "HP"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.hpBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox.Add(wx.Panel(self), 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 0)

        innerBox.Add(wx.StaticText(self, 0, "Init"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.initBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        outerBox.Add(innerBox, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)

        innerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox.Add(wx.StaticText(self, 0, "Notes"),
                     0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        innerBox.Add(self.notesBox, 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
        saveBtn = wx.Button(self, 0, "Save to dictionary")
        saveBtn.Bind(wx.EVT_BUTTON, lambda event: self.saveUnit())
        innerBox.Add(saveBtn, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 1)
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
                else:
                    raise Exception('Could not save %s' % (fn))
            cb.Close()

    def removeImage(self):
        if self.image is not None:
            parent = self.GetParent()
            if not parent.hasImage(self.image):
                parent.removeImage(self.image)

        self.image = None
        self.bmp = None
        self.imageFrame.Hide()
        self.rebuild()

    def saveUnit(self):
        udict = UnitDict()
        unit = self.getUnit()
        if udict.has(unit['name']):
            dlg = wx.MessageDialog(self, 'Replace previous entry for "%s"?' % (unit['name'].strip()), caption='Overwrite unit', style=wx.YES_NO|wx.CENTER)
            if dlg.ShowModal() == wx.ID_YES:
                udict.add(unit)
                udict.write()
        else:
            udict.add(unit)
            udict.write()
            dlg = wx.MessageDialog(self, '', caption='Unit saved', style=wx.OK|wx.CENTER)
            dlg.ShowModal()


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
        if self.image is not None: self.save_image = True
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

    def OnClose(self, event):
        if self.image is not None and not self.save_image:
            self.GetParent().removeImage(self.image)
        event.Skip()
