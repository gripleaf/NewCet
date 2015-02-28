__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import wx
import thread, threading;
import sys, timer, time

global runmt

class RunMulThreads(wx.Frame, threading.Thread):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title="CET4|6 ShowScore", size=(400, 400))
        threading.Thread.__init__(self)
        self.panel = wx.Panel(self, id=-1);
        self.panel.SetBackgroundColour("white")
        self.curnow = 0
        self.__class__.Flag = False
        #create the Gauge
        self.cetGua = wx.Gauge(self.panel, -1, 100, name="gauge", pos=(50, 90), size=(300, 20))
        self.__class__.cetProc = 0
        self.cetGua.Show(False)

        #create the staicText
        self.__class__.ShowLabel = u"  正在努力创建60个线程..."
        self.cetShowSt = wx.StaticText(self.panel, -1, self.__class__.ShowLabel, pos=(120, 25))


        #create the staticText
        self.cetRes = wx.StaticText(self.panel, -1, u"you can't see me!", pos=(140, 130))
        self.cetRes.Show(False)
        self.__class__.anslist = [];

        #create the button
        self.cetprebut = wx.Button(self.panel, -1, label=u"上一个", pos=(100, 300))
        self.cetnextbut = wx.Button(self.panel, -1, label=u"下一个", pos=(200, 300))
        self.cetprebut.Show(False)
        self.cetnextbut.Show(False)
        #create the bind
        self.Bind(wx.EVT_BUTTON, self.PreResult, self.cetprebut)
        self.Bind(wx.EVT_BUTTON, self.NextResult, self.cetnextbut)
        self.Bind(wx.EVT_CLOSE, self.ErrorLog)

        #open the file
        self.fe = open("error.log", "a")

    def ErrorLog(self, event):
        self.__class__.Flag = True
        try:
            print >> self.fe, self.__class__.anslist;
        except  Exception, e:
            print "write error"
        finally:
            self.fe.close()
        self.Destroy()


    def PreResult(self, event):
        self.curnow -= 1
        self.curnow %= len(self.__class__.anslist)
        self.cetRes.SetLabel(self.__class__.anslist[self.curnow])

    def NextResult(self, event):
        self.curnow += 1
        self.curnow %= len(self.__class__.anslist)
        self.cetRes.SetLabel(self.__class__.anslist[self.curnow])

    def run(self):
        while True:
            self.cetShowSt.SetLabel(self.__class__.ShowLabel)
            time.sleep(1);
            if len(self.cetShowSt.GetLabel()) > 30:
                break;
        time.sleep(1)
        self.cetGua.Show(True)
        while True:
            self.cetGua.SetValue(self.__class__.cetProc)
            time.sleep(6)
            if self.__class__.cetProc >= 100:
                self.cetGua.SetValue(self.__class__.cetProc)
                break;
        self.cetRes.SetLabel(u"努力处理数据中...")
        self.cetRes.Show(True)
        time.sleep(1)
        self.curnow = 0
        if len(self.__class__.anslist) > 0:
            self.cetRes.SetLabel(self.__class__.anslist[self.curnow])
            self.cetprebut.Show(True)
            self.cetnextbut.Show(True)
        else:
            self.cetRes.SetLabel(u"查找失败~~~~~~")


def RunMul():
    app = wx.PySimpleApp();
    runmt = RunMulThreads()
    runmt.Show(True)
    app.MainLoop();


if __name__ == '__main__':#main function
    thread.start_new_thread(RunMul, ())
    #print "yes"
    #thread.start_new_thread(RunMul, ())
    #time.sleep(2000)
