import tkinter as tk
from PIL import Image, ImageTk
import time
import random
import threading
import tkinter.messagebox as messagebox


def init():
    list1 = []  # 32张图片的序号
    for i in range(1, 33):
        list1.append(i)
        path = './image/1/{}.jpg'.format(i)
        dict1[i] = ImageTk.PhotoImage(Image.open(path))
    for i in range(5):  # 把32张图片的序号打乱，放入list2，重复5次，得到160张图片的显示顺序
        random.shuffle(list1)
        list2.extend(list1)
    for i in range(160):
        dict2[i] = [list2[i], 0, 0, 0, 0]    # value是一个列表：0图片的序号，1按键值，2开始时间，3结束时间,4正误。除0以外初始化为0
        eventList.append(threading.Event())
    

def startThread(event):
    thd = threading.Thread(target=mainLoop)
    thd.start()
    
    
def mainLoop():
    global counter
    for i in range(160):
        step1(dict1[list2[i]])
        dict2[counter][2] = int(round(time.time() * 1000))
        result = eventList[counter].wait(0.5)   # 原本为3s
        if result:
            pass
        else:
            dict2[counter][3] = int(round(time.time() * 1000))
            step2()
            time.sleep(0.1)   # 原本为1s
        counter += 1
    counter = 0
    # doResult()
    try:
        doResult()
    except:
        messagebox.showinfo('result', '保存实验数据时出现错误')
    return


def step1(arg):     # 显示图片，更新计数标签
    label.config(image=arg)
    clabel.config(text=str(counter + 1) + '/160')


def step2():        # 显示空白
    label.config(image='')


def doResult():
    error = 0   # 错误次数
    for i in range(160):
        if dict2[i][1] == 0:
            error += 1
            dict2[i][4] = '错误'
        elif dict2[i][0] % 2 == 1 and dict2[i][1] != 'f':
            error += 1
            dict2[i][4] = '错误'
        elif dict2[i][0] % 2 == 0 and dict2[i][1] != 'j':
            error += 1
            dict2[i][4] = '错误'
        else:
            dict2[i][4] = '正确'
    correct = []    # 正确的反应时间
    hzTime = []     # 红紫色图片的正确反应时间
    llTime = []     # 蓝绿色图片的正确反应时间
    hzErr = 0       # 红紫错误次数
    llErr = 0       # 蓝绿错误次数
    total = []      # 记录每次的反应时间
    ratio = round(error / 160.0 * 100, 3)       # 错误率
    path = './result/1/' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + '.txt'
    f = open(path, 'w')
    f.write('次数\t图片序号\t按键\t反应时(ms)\t正误结果\n')
    for i in range(160):
        t = dict2[i][3] - dict2[i][2]   # 每次的反应时间
        if dict2[i][4] == '正确':
            correct.append(t)
        total.append(t)
        if 1 <= dict2[i][0] <= 16:      # 序号1~16是红紫色图片
            if dict2[i][4] == '正确':
                hzTime.append(t)
            else:
                hzErr += 1
        else:                           # 序号17~32是蓝绿色图片
            if dict2[i][4] == '正确':
                llTime.append(t)
            else:
                llErr += 1
        record = str(i) + '\t' + str(dict2[i][0]) + '\t\t' + str(dict2[i][1]) + '\t' + str(t) + '\t\t' + dict2[i][4] + '\n'   # 一条记录
        f.write(record)
    f.write('总次数：160\t\t错误次数：' + str(error) + '\t\t错误率：' + str(ratio) + '%\n')
    correctTime = round(sum(correct) / len(correct)) if len(correct) else 0    # 平均正确反应时间
    averageTime = round(sum(total) / len(total))        # 平均每次反应时间
    f.write('平均反应时：' + str(averageTime) + 'ms\t\t平均正确反应时：' + str(correctTime) + 'ms')
    hzCorrectTime = round(sum(hzTime) / len(hzTime)) if len(hzTime) else 0     # 红紫色图片平均正确反应时间
    hzErrorRatio = round(hzErr / 80.0 * 100, 3)            # 红紫色图片错误率
    llCorrectTime = round(sum(llTime) / len(llTime)) if len(llTime) else 0        # 蓝绿色图片平均正确反应时间
    llErrorRatio = round(llErr / 80.0 * 100, 3)             # 蓝绿色图片错误率
    f.write('\n\n红紫：\t错误率：' + str(hzErrorRatio) + '%\t\t平均正确反应时：' + str(hzCorrectTime) + 'ms')
    f.write('\n蓝绿：\t错误率：' + str(llErrorRatio) + '%\t\t平均正确反应时：' + str(llCorrectTime) + 'ms')
    f.close()
    messagebox.showinfo('result', '实验结束')
    return


def pressF(event):
    dict2[counter][1] = 'f'
    dict2[counter][3] = int(round(time.time() * 1000))
    eventList[counter].set()


def pressJ(event):
    dict2[counter][1] = 'j'
    dict2[counter][3] = int(round(time.time() * 1000))
    eventList[counter].set()


root = tk.Tk()
root.geometry('1024x1024')
root.title("实验一")
counter = 0     # 计数器
list2 = []      # 图片的显示顺序
dict2 = {}      # 记录数据
dict1 = {}      # 存放32张图片
eventList = []  # 事件列表
init()
start = tk.Button(root, text='开始', width=25)
start.bind("<Button-1>", startThread)
start.pack()
clabel = tk.Label(root, text='0/160')   # 计数标签
clabel.pack()
label = tk.Label(root)
label.bind_all("<KeyPress-F>", pressF)
label.bind_all("<KeyPress-f>", pressF)
label.bind_all("<KeyPress-J>", pressJ)
label.bind_all("<KeyPress-j>", pressJ)
label.pack()
root.mainloop()
