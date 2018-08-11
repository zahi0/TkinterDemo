import tkinter as tk
from PIL import Image, ImageTk
import time
import random
import threading
import tkinter.messagebox as messagebox


def init():
    for i in range(128):
        eventList.append(threading.Event())
    for i in range(1, 17):
        path1 = './image/3/part1/{}.jpg'.format(i)
        standard[i] = ImageTk.PhotoImage(Image.open(path1))
    for i in range(1, 17):
        dict2 = {}
        for j in range(1, 9):
            path2 = './image/3/part2/{}/{}.jpg'.format(i, j)
            dict2[j] = ImageTk.PhotoImage(Image.open(path2))
        compare.append(dict2)
        
    
def startThread(event):
    t = threading.Thread(target=mainLoop)
    t.start()
    
    
def mainLoop():
    global counter
    nums = [i for i in range(128)]
    random.shuffle(nums)
    for i in nums:
            group = int(i/8) + 1
            order = i % 8 + 1
            showImage(standard[group])
            time.sleep(0.5)    # 5s
            blank()
            time.sleep(0.3)  # 30s
            d[counter] = [order, 0, 0, 0, 0, group]     # 0图片的序号，1按键值，2开始时间，3结束时间,4正误,  5组数：1-8红紫 9-16蓝绿
            updateCLabel()
            showImage(compare[group][order])
            d[counter][2] = int(round(time.time() * 1000))
            eventList[counter].wait()
            counter += 1
    counter = 0
    try:
        doResult()
    except:
        messagebox.showinfo('result', '保存实验数据时出现错误')
    return


def showImage(arg):
    label.config(image=arg)


def updateCLabel():
    clabel.config(text=str(counter + 1) + '/128')


def blank():
    label.config(image='')


def pressF(event):
    d[counter][1] = 'f'
    d[counter][3] = int(round(time.time() * 1000))
    eventList[counter].set()


def pressJ(event):
    d[counter][1] = 'j'
    d[counter][3] = int(round(time.time() * 1000))
    eventList[counter].set()


def doResult():
    error = 0
    hzTime = []
    llTime = []
    hzErr = 0
    llErr = 0
    for i in range(128):
        if d[i][0] % 2 == 1 and d[i][1] != 'f':
            error += 1
            d[i][4] = '错误'
        elif d[i][0] % 2 == 0 and d[i][1] != 'j':
            error += 1
            d[i][4] = '错误'
        else:
            d[i][4] = '正确'
    correct = []
    total = []
    ratio = round(error / 128.0 * 100, 3)
    path = './result/3/' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + '.txt'
    f = open(path, 'w')
    f.write('次数\t图片序号\t按键\t反应时(ms)\t正误结果\n')
    for i in range(128):
        t = d[i][3] - d[i][2]
        if d[i][4] == '正确':
            correct.append(t)
            if 1 <= d[i][5] <= 8:    # 1-8红紫  9-16蓝绿
                hzTime.append(t)
            else:
                llTime.append(t)
        else:
            if 1 <= d[i][5] <= 8:    # 1-8红紫  9-16蓝绿
                hzErr += 1
            else:
                llErr += 1
        total.append(t)
        s = str(i) + '\t' + str(d[i][0]) + '\t\t' + str(d[i][1]) + '\t' + str(t) + '\t\t' + d[i][4] + '\n'
        f.write(s)
    f.write('总次数：128\t\t错误次数：' + str(error) + '\t\t错误率：' + str(ratio) + '%\n')
    ct = round(sum(correct) / len(correct)) if len(correct) else 0
    at = round(sum(total) / len(total))
    f.write('平均反应时：' + str(at) + 'ms\t\t平均正确反应时：' + str(ct) + 'ms')
    hzt = round(sum(hzTime) / len(hzTime)) if len(hzTime) else 0
    hzr = round(hzErr / 64.0 * 100, 3)
    llt = round(sum(llTime) / len(llTime)) if len(llTime) else 0
    llr = round(llErr / 64.0 * 100, 3)
    f.write('\n\n红紫：\t错误率：' + str(hzr) + '%\t\t平均正确反应时：' + str(hzt) + 'ms')
    f.write('\n蓝绿：\t错误率：' + str(llr) + '%\t\t平均正确反应时：' + str(llt) + 'ms')
    f.close()
    messagebox.showinfo('result', '实验结束')
    return


root = tk.Tk()
root.geometry('1024x720')
root.title("实验三")
counter = 0
d = {}          # 存放结果
standard = {}   # 存放标准色块1-16
compare = [0]    # 存放比较色块，每一项(1-16)是字典
eventList = []
init()
tips = tk.Label(root, text='\n你需要选出你认为与事先呈现的标准色块相匹配的比较色块，如果你认为左边色块与事先呈现的标准色块匹配，就按下F健；\n如果你认为右边色块与事先呈现的标准色块匹配，就按下J健。\n')
tips.pack()
start = tk.Button(root, text='开始', width=25)
start.bind("<Button-1>", startThread)
start.pack()
clabel = tk.Label(root, text='0/128')
clabel.pack()
label = tk.Label(root)
label.bind_all("<KeyPress-F>", pressF)
label.bind_all("<KeyPress-f>", pressF)
label.bind_all("<KeyPress-J>", pressJ)
label.bind_all("<KeyPress-j>", pressJ)
label.pack()
root.mainloop()
