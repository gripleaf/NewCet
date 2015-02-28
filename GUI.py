__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import wx
import sys

global sch, iddict, schdict
sch = [u'浙江师范大学', u'浙江工商大学', u'浙江大学', u'宁波大学', u'绍兴文理学院', u'湖州师范学院', u'浙江工业大学', u'其他']
iddict = ["330020", "330382,330381", '330011,330012,330013,330015', '330030', '330090,330091,330092', '330100', \
          '330361,330362', '330020'];
schdict = {}
for i in range(len(sch)):
    schdict.setdefault(sch[i], iddict[i])


class GUIFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title="CET4|6 ShowScore", size=(380, 300))
        self.panel = wx.Panel(self, id=-1);
        self.panel.SetBackgroundColour("white")
        self.__class__.kchlimit = 200
        self.__class__.zwhlimit = 30
        #create the radiobox
        self.cetrb = wx.RadioBox(self.panel, id=-1, label="CET Level", name="radiobox", choices=['CET4', 'CET6'],
                                 pos=(120, 30))

        #create the school list
        self.cetcs = wx.Choice(self.panel, id=-1, choices=sch, name="choice", pos=(50, 120))
        self.cetcs.SetStringSelection(sch[0])

        #create the textctrl
        self.cettc = wx.TextCtrl(self.panel, -1, u"准考证前六位,多个输入请用','隔开", pos=(170, 120), size=(150, 30))
        self.cettc.Show(False);

        self.cetname = wx.TextCtrl(self.panel, -1, u"请输入您的姓名", pos=(100, 170), size=(150, 30))

        #create the static text
        self.cetsc = wx.StaticText(self.panel, -1, u"you can't see this!", pos=(180, 123), size=(150, 30))
        self.cetsc.SetLabel(schdict[self.cetcs.GetStringSelection()])


        #create the submit button
        self.cetbut = wx.Button(self.panel, -1, label=u"确定", pos=(135, 210))
        self.cetkch = wx.Button(self.panel, -1, label=u"默认考场上限200，座位号上限30，如需更改，请点击此处", size=(380, 28))

        #create the bind
        self.Bind(wx.EVT_CHOICE, self.OnOtherChoice, self.cetcs)
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, self.cetbut)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_BUTTON, self.SetKZLimit, self.cetkch)

    def SetKZLimit(self, event):
        ted = wx.TextEntryDialog(self, u"输入两个整数分别表示考场号和座位号上限（用英文状态下输入的“逗号”隔开）", style=wx.OK | wx.CANCEL)
        if ted.ShowModal() == wx.ID_OK:
            try:
                self.__class__.kchlimit, self.__class__.zwhlimit = map(int, ted.GetValue().split(","))
            except Exception, e:
                self.__class__.kchlimit, self.__class__.zwhlimit = 200, 30

    def OnClose(self, event):
        sys.exit()

    def OnSubmit(self, event):
        self.__class__.cetname = self.cetname.GetValue()
        if self.cetrb.GetSelection() == 0:
            self.__class__.cetlev = '4'
        else:
            self.__class__.cetlev = '6'
        if self.cetcs.GetStringSelection() == u"其他":
            self.__class__.localid = self.cettc.GetValue()
        else:
            self.__class__.localid = self.cetsc.GetLabel()
        self.Destroy()

    def OnOtherChoice(self, event):
        if self.cetcs.GetStringSelection() == u"其他":
            self.cetsc.Show(False)
            self.cettc.Show(True)
            self.Refresh()
        elif self.cetcs.GetStringSelection() != "":
            self.cettc.Show(False)
            self.cetsc.Show(True)
            self.cetsc.SetLabel(schdict[self.cetcs.GetStringSelection()])
            self.Refresh()


if __name__ == '__main__':#main function
    app = wx.PySimpleApp();
    frame = GUIFrame()
    frame.Show(True)
    app.MainLoop();

