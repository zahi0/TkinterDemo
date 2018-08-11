import tkinter as tk
from PIL import Image, ImageTk
import time
import random
import threading
import tkinter.messagebox as messagebox


def init():
    global list4
    list1 = [i for i in range(1, 17)]
    for i in range(5):      # 把16张图片的序号打乱，放入list2，重复5次，得到80张图片的显示顺序
        random.shuffle(list1)
        list2.extend(list1)
    k = 0
    for i in range(2):
        for j in list2:
            dict[k] = [j, 0, 0, 0, 0, 0]    # value是一个列表：0图片的序号，1按键值，2开始时间，3结束时间,4正误,5分组。除0以外初始化为0
            k += 1
    dict1 = {}      # 0号是标准色块，1-16目标色块
    dict2 = {}      # 0号是标准色块，1-16目标色块
    for i in range(17):
        path1 = './image/2/part1/{}.jpg'.format(i)
        path2 = './image/2/part2/{}.jpg'.format(i)
        dict1[i] = ImageTk.PhotoImage(Image.open(path1))
        dict2[i] = ImageTk.PhotoImage(Image.open(path2))
    list4 = [dict1, dict2]  # 0：dict1红紫  1：dict2蓝绿
    for i in range(160):
        eventList.append(threading.Event())


def startThread(event):
    thd = threading.Thread(target=mainLoop)
    thd.start()


def mainLoop():
    global counter
    error = 0   # 错误次数
    ts = '正确'
    fs = '错误'
    list3 = [0, 1] if random.random() > 0.5 else [1, 0]
    for i in list3:
        for j in range(81):
            if j == 0:
                showImage(list4[i][j])
                time.sleep(2)
                blank()
                time.sleep(1)
            else:
                updateCLabel()
                showImage(list4[i][list2[j-1]])
                dict[counter][5] = i
                dict[counter][2] = int(round(time.time() * 1000))
                result = eventList[counter].wait(0.5)  # 2s
                if result:
                    if dict[counter][0]%2 == 1 and dict[counter][1] == 'f':
                        dict[counter][4] = ts
                        showMessage('\n\n\n' + ts)
                    elif dict[counter][0] % 2 == 0 and dict[counter][1] == 'j':
                        showMessage('\n\n\n' + ts)
                        dict[counter][4] = ts
                    else:
                        dict[counter][4] = fs
                        showMessage('\n\n\n'+fs)
                        error += 1
                else:
                    dict[counter][3] = int(round(time.time() * 1000))
                    dict[counter][4] = fs
                    showMessage('\n\n\n'+fs)
                    error += 1
                time.sleep(0.1)  # 1s
                counter += 1
        blank()
        time.sleep(1)
    # doResult(error)
    counter = 0
    try:
        doResult(error)
    except:
        messagebox.showinfo('result', '保存实验数据时出现错误')
    return


def showImage(arg):  # 显示图片
    label.config(image=arg)


def updateCLabel():     # 更新计数标签
    clabel.config(text=str(counter + 1) + '/160')


def blank():        # 什么也不显示
    label.config(image='', text='')


def showMessage(string):
    label.config(image='', text=string)


def pressF(event):      # 按下F键
    dict[counter][3] = int(round(time.time() * 1000))
    dict[counter][1] = 'f'
    eventList[counter].set()


def pressJ(event):      # 按下J键
    dict[counter][3] = int(round(time.time() * 1000))
    dict[counter][1] = 'j'
    eventList[counter].set()


def doResult(error):
    correct = []    # 正确反应时间
    total = []      # 每次的反应时间
    hzTime = []     # 红紫色正确反应时间
    llTime = []     # 蓝绿色正确反应时间
    hzErr = 0       # 红紫色错误次数
    llErr = 0       # 蓝绿色错误次数
    ratio = round(error/160.0*100, 3)       # 错误率
    path = './result/2/' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + '.txt'
    f = open(path, 'w')
    f.write('次数\t图片序号\t按键\t反应时(ms)\t正误结果\n')
    for i in range(160):
        t = dict[i][3]-dict[i][2]   # 反应时间
        if dict[i][4] == '正确':
            correct.append(t)
            if dict[i][5] == 0:    # 0：dict1红紫  1：dict2蓝绿
                hzTime.append(t)
            else:
                llTime.append(t)
        else:
            if dict[i][5] == 0:    # 0：dict1红紫  1：dict2蓝绿
                hzErr += 1
            else:
                llErr += 1
        total.append(t)
        record = str(i) + '\t' + str(dict[i][0]) + '\t\t' + str(dict[i][1]) + '\t' + str(t)+'\t\t'+dict[i][4]+'\n'      # 一条记录
        f.write(record)
    f.write('总次数：160\t\t错误次数：'+str(error)+'\t\t错误率：'+str(ratio)+'%\n')
    correctTime = round(sum(correct)/len(correct)) if len(correct) else 0       # 平均正确反应时间
    averageTime = round(sum(total)/len(total))      # 平均每次反应时间
    f.write('平均反应时：' + str(averageTime) + '\t\t平均正确反应时：' + str(correctTime))
    hzCorrectTime = round(sum(hzTime) / len(hzTime)) if len(hzTime) else 0      # 红紫色图片平均正确反应时间
    hzErrorRatio = round(hzErr / 80.0 * 100, 3)     # 红紫色图片错误率
    llCorrectTime = round(sum(llTime) / len(llTime)) if len(llTime) else 0      # 蓝绿色图片平均正确反应时间
    llErrorRatio = round(llErr / 80.0 * 100, 3)      # 蓝绿色图片错误率
    f.write('\n\n红紫：\t错误率：' + str(hzErrorRatio) + '%\t\t平均正确反应时：' + str(hzCorrectTime) + 'ms')
    f.write('\n蓝绿：\t错误率：' + str(llErrorRatio) + '%\t\t平均正确反应时：' + str(llCorrectTime) + 'ms')
    f.close()
    messagebox.showinfo('result', '实验结束')


root = tk.Tk()
root.geometry('720x500')
root.title("实验二")
counter = 0  # 计数器
list4 = []  # 存放字典
list2 = []  # 5*16个打乱的数字，图片的显示顺序
dict = {}      # 记录数据
eventList = []   # 事件列表
init()
tips = tk.Label(root, text='\n你现在要学习把一系列刺激分为两组，左边一组，右边一组，实验首先会先呈现两个左右样本色块，本实验一共有两个试次。\n')
tips.pack()
start = tk.Button(root, text='开始', width=25)
start.bind("<Button-1>", startThread)
start.pack()
clabel = tk.Label(root, text='0/160')       # 计数标签
clabel.pack()
label = tk.Label(root)
label.bind_all("<KeyPress-F>", pressF)
label.bind_all("<KeyPress-f>", pressF)
label.bind_all("<KeyPress-J>", pressJ)
label.bind_all("<KeyPress-j>", pressJ)
label.pack()
root.mainloop()
