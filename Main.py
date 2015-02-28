__author__ = 'glcsnz123'
#_*_encoding:utf-8_*_
import urllib2, urllib
import sys, time
import thread, threading
from GUI import GUIFrame
from RunMulThread import RunMulThreads, RunMul
import wx

cefy = []
wrongurl = []


def Check(stid="", name=u""):
    #print name,type(name)330020121101729
    #name = unicode(name, "utf-8")
    post_data = urllib.urlencode({"id": stid.decode("gbk"), "name": name.encode("gbk")});
    #print post_data
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", \
               "Accept-Charset": "GBK,utf-8;q=0.7,*;q=0.3", "Accept-Encoding": "gzip,deflate,sdch", \
               "Accept-Language": "zh-CN,zh;q=0.8", "Cache-Control": "max-age=0", "Connection": "keep-alive", \
               "Content-Length": "36", "Content-Type": "application/x-www-form-urlencoded", \
               "Cookie": "cnzz_a30023677=4; sin30023677=; rtime30023677=5; ltime30023677=1356177904700; cnzz_eid30023677=19927958-1318821986-http%3A//www.baidu.com/s%3Fwd%3D99%25CB%25DE%25C9%25E1%26rsv_bp%3D0%26rsv_spt%3D3%26oq%3D9; searchtime=1356177913"
        ,
               "Host": "cet.99sushe.com", "Origin": "http://cet.99sushe.com", "Referer": "http://cet.99sushe.com/", \
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.20 (KHTML, like Gecko) Chrome/25.0.1337.0 Safari/537.20"
    };

    pst = urllib2.Request("http://cet.99sushe.com/s", headers=headers);
    try:
        pst = urllib2.urlopen(pst, post_data)
    except Exception, e:
        try:
            mylock.acquire()
            hole.append(stid[-5::1])
            #print stid
        finally:
            mylock.release()
        return "w"
    html = pst.read()
    return html.decode("gbk")


def GetName():
    #name = raw_input(u"请输入你的姓名：");
    return GUIFrame.cetname


def GetLevel():
    #return raw_input("CET?");
    return GUIFrame.cetlev


anslist = [];
hole = []
mylock = thread.allocate_lock()


def LoopOne(stid, name):
    while True:
        try:
            mylock.acquire()
            if len(hole) <= 0:
                break
            i = hole[0]
            del hole[0]
        finally:
            mylock.release()
        result = Check(stid + i, name)
        if len(result) >= 10:
            print result
            anslist.append(result.split(','))
            cefy.append(stid + i)


def GetLocalNum():
    #return "330020"
    #return raw_input("请输入准考证号的前六位：")

    return GUIFrame.localid.split(",")


def GetYear(date):
    year = int(str(date[0])[2:])
    if date[1] < 8:
        year -= 1
    return str(year)


def Init():
    app = wx.PySimpleApp();
    frame = GUIFrame()
    frame.Show(True)
    app.MainLoop();


runmt = None


def RunMul():
    apps = wx.PySimpleApp();
    global runmt
    runmt = RunMulThreads()
    runmt.Show(True)
    runmt.start()
    apps.MainLoop();


if __name__ == "__main__":
    print "The console is a way to show if the program is running well.\nDon't kill this!!!"
    Init()
    name = GetName();
    try:
        names = name[0:6]
    except Exception, e:
        exit()
    date = time.localtime(time.time())
    stidls = GetLocalNum()
    RunMulThreads.cetProc = 0
    thread.start_new_thread(RunMul, ())
    time.sleep(1)
    ape = -1
    for stid in stidls:
        ape += 1
        if len(stid) != 6:
            RunMulThreads.ShowLabel = u"  正在努力创建60个线程...\n\n创建完成！^0^~ 开始查找..."
            RunMulThreads.cetProc = 100
            RunMulThreads.anslist.append(u"输入有误，程序终止~\n错误准考证号：" + str(stid))
            break
        stid += GetYear(date)
        if int(date[1]) >= 8 or int(date[1]) < 2:
            stid += '1'
        else:
            stid += '2'
        cetlv = GetLevel()
        if cetlv == '4':
            stid += '1'
        else:
            stid += '2'
        print stid
        #RunMulThreads.ShowLabel = ""
        time.sleep(1);
        print "KaoChangHao: ", GUIFrame.kchlimit, "| ZuoWeiHao: ", GUIFrame.zwhlimit
        global hole
        for i in range(1, GUIFrame.kchlimit):
            for j in range(1, GUIFrame.zwhlimit):
                hole.append("%03d%02d" % (i, j))
        now = len(hole) * 1.0;
        for i in range(0, 60):
            thread.start_new_thread(LoopOne, (stid, names))
            time.sleep(0.1);
            #pass
        RunMulThreads.ShowLabel = u"     正在努力创建60个线程...\n\n创建完成！^0^~ 开始查找..."
        while True:
            print "当前完成度：%.2f%%" % (100.0 - (len(hole) * 100.0 / (now)))
            RunMulThreads.cetProc = (100.0 - (len(hole) * 100.0 / (now))) / (len(stidls)) + ape * (
                100.0 / len(stidls))
            if len(hole) == 0:
                if RunMulThreads.cetProc > 90:
                    RunMulThreads.cetProc = 100
                break
            time.sleep(15);


        #result=Check()
        #print result
        #anslist.append(result.split(','))
        RunMulThreads.anslist = []

        for i in range(len(anslist)):
            tmp = anslist[i]
            scors = u"姓名： " + tmp[-1]
            scors += u"\n准考证号： " + cefy[i]
            scors += u"\n学校： " + tmp[-2]
            scors += u"\n总分： " + tmp[-3]
            scors += u"\n听力： " + tmp[1]
            scors += u"\n阅读： " + tmp[2]
            scors += u"\n综合： " + tmp[3]
            scors += u"\n写作： " + tmp[4]
            RunMulThreads.anslist.append(scors)
            print scors
            try:
                f = open("history_utf-8_open.txt", "a")
                f.write(scors.encode("utf-8"))
                f.write("\n--------------------------\n")
            finally:
                f.close()
                #runmt.join()
    time.sleep(10)
    while RunMulThreads.Flag == False:
        time.sleep(2);


