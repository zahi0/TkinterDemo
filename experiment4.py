import tkinter as tk
import time
import random
import threading
import tkinter.messagebox as messagebox


def init():
    global counter, counter2, c
    counter = 0
    counter2 = 0
    c = 300
    for i in range(total*2+2):
        eventList.append(threading.Event())
        if i < total:
            record[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0]     # 0：匹配、控制,1:搜索开始时间，2：搜索结束时间，3：按键，4：搜索正误:，5：记忆开始，6：记忆结束，7：按键，8：记忆正误


def start(event):
    cvs.delete('s0')
    eventList.clear()
    record.clear()
    init()
    t = threading.Thread(target=run)
    t.start()


def run():
    num = [i for i in range(total)]
    random.shuffle(num)
    global counter, counter2
    pp = [int(total*0.2), int(total*0.5), int(total*0.8)]
    # 1 显示随机数
    step1()
    # time.sleep(2)
    eventList[-1].wait()
    cvs.delete('s1')
    for i in range(total):
        # if i == total/2:          # 中间的休息时间：5分钟
        #     stop()
        #     eventList[-2].wait()
            # time.sleep(301)
        random.shuffle(color)   # 0记忆/干扰，1左，2右
        if mode == 1:   # 1.匹配试次20%
            if num[i] < pp[0]:
                flag = record[i][0] = '匹配'
            else:
                flag = record[i][0] = '控制'
        elif mode == 2:  # 2.匹配试次50%
            if num[i] < pp[1]:
                flag = record[i][0] = '匹配'
            else:
                flag = record[i][0] = '控制'
        elif mode == 3:               # 3.匹配试次80%
            if num[i] < pp[2]:
                flag = record[i][0] = '匹配'
            else:
                flag = record[i][0] = '控制'
        else:
            messagebox.showinfo('error', '请先选择匹配试次')
            step0()
            return

        # 2 记忆项目
        step3(color[0])
        time.sleep(0.5)
        cvs.delete('s3')
        # 3 空白0.5s
        time.sleep(0.5)
        # 4 线索序列
        if flag == '匹配':
            step5(color[1], color[2])
        else:
            step5_1(color[1], color[0])
        plus()
        time.sleep(0.5)
        cvs.delete('s5')
        cvs.delete('s2')
        # 5 空白0.25s
        time.sleep(0.25)
        # 6 搜索序列
        n1 = random.randint(0, 1)
        n2 = random.randint(0, 1)
        if flag == '匹配':
            step6(n1, n2, color[1], color[2])
        else:
            step6(n1, n2, color[1], color[0])
        plus()
        record[counter][1] = int(round(time.time() * 1000))
        result = eventList[counter2].wait(1.5)
        counter2 += 1
        if result:
            if record[counter][3] == 'A' and n1 == 1:
                record[counter][4] = '正确'
            elif record[counter][3] == 'Z' and n1 == 0:
                record[counter][4] = '正确'
            else:
                record[counter][4] = '错误'
        else:
            record[counter][2] = int(round(time.time() * 1000))
            record[counter][4] = '错误'
        cvs.delete('s6')
        cvs.delete('s2')
        # 7 空白0.5s
        time.sleep(0.5)
        # 8 记忆探索序列
        col = random.randint(0, 3)
        step3(color[col])
        record[counter][5] = int(round(time.time() * 1000))
        result = eventList[counter2].wait(2)
        counter2 += 1
        if result:
            if record[counter][7] == 1 and col == 0:
                record[counter][8] = '正确'
            elif record[counter][7] == 2 and col != 0:
                record[counter][8] = '正确'
            else:
                record[counter][8] = '错误'
        else:
            record[counter][6] = int(round(time.time() * 1000))
            record[counter][8] = '错误'
        cvs.delete('s3')
        counter += 1
        time.sleep(1)
    doResult()
    step0()
    return


def step0():
    txt = '本实验开始时你将会看到一个四位数字，并要求在整个实验过程中以\n' \
          '每秒一到两次的速度不断重复该数字（不出声），记住后立刻按下J键，\n' \
          '之后屏幕会出现一个有颜色的圆，记住其颜色，并注意之后出现的圆圈\n' \
          '中央的黑色方框朝向，向上按A，向下按Z，最后又会出现一个圆，判断\n' \
          '与之前出现的圆颜色是否相同，是按1，否按2。准备好开始按下F键。'
    cvs.create_text((540, 260), tex=txt, font="time 20 bold", tags='s0')


def step1():
    num = random.randint(1000, 9999)
    cvs.create_text((540, 260), tex=num, font="time 80 bold", tags='s1')


def step3(col):
    x = 540
    y = 300
    r = 100
    cvs.create_oval(x-r, y-r, x+r, y+r, fill=col, tags='s3')


def step5(col1, col2):
    cvs.create_rectangle(30, 150, 330, 450, outline=col1, width=3, tags='s5')
    cvs.create_rectangle(700, 150, 1000, 450, outline=col2, width=3, tags='s5')


def step5_1(col1, col2):          # 控制试次
    x = 180
    y = 300
    r = 150
    nums1 = [x - r, x+ r, y - r, y + r]
    coords2 = [nums1[0], nums1[2], nums1[0], nums1[3], nums1[0], nums1[2], nums1[1], nums1[2], nums1[1], nums1[2],
               nums1[1], nums1[3]]  # down
    cvs.create_line(coords2, fill=col1, width=3, tags='s5')
    cvs.create_rectangle(700, 150, 1000, 450, outline=col2, width=3, tags='s5')


def step6(n1, n2, col1, col2):
    x1 = 200    # 圆心
    y1 = 300
    x2 = 850     # 圆心
    y2 = 300
    r = 150     # 半径
    r2 = 50
    nums1 = [x1 - r2, x1 + r2, y1 - r2, y1 + r2]
    nums2 = [x2 - r2, x2 + r2, y2 - r2, y2 + r2]
    coords1 = [nums1[0], nums1[2], nums1[0], nums1[3], nums1[0], nums1[3], nums1[1], nums1[3], nums1[1], nums1[2],
               nums1[1], nums1[3]]   # up
    coords2 = [nums1[0], nums1[2], nums1[0], nums1[3], nums1[0], nums1[2], nums1[1], nums1[2], nums1[1], nums1[2],
               nums1[1], nums1[3]]   # down
    coords3 = [nums2[0], nums2[2], nums2[1], nums2[2], nums2[1], nums2[2], nums2[1], nums2[3], nums2[0], nums2[3],
               nums2[1], nums2[3]]  # left
    coords4 = [nums2[0], nums2[2], nums2[1], nums2[2], nums2[0], nums2[2], nums2[0], nums2[3], nums2[0], nums2[3],
               nums2[1], nums2[3]]  # right
    if n1:
        left = coords1  # 1 up
    else:
        left = coords2  # 0 down
    if n2:
        right = coords3
    else:
        right = coords4
    cvs.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill=col1, tags='s6')
    cvs.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill=col2, tags='s6')
    cvs.create_line(left, width=5, tags='s6')
    cvs.create_line(right, width=5, tags='s6')


def stop():      # 休息时间
    global c, s
    cvs.delete('s')
    cvs.create_text((540, 200), tex='休息5分钟', font="time 50 bold", tags='s')
    cvs.create_text((540, 260), tex=str(c), font="time 50 bold", tags='s')
    if c == 0 or s:
        s = False
        cvs.delete('s')
        eventList[-2].set()
        return
    c -= 1
    cvs.after(1000, stop)


def plus():
    cvs.create_line(450, 300, 600, 300, width=10, tags='s2')
    cvs.create_line(525, 225, 525, 375, width=10, tags='s2')


def funA(event):
    record[counter][2] = int(round(time.time() * 1000))
    record[counter][3] = 'A'
    eventList[counter2].set()


def funZ(event):
    record[counter][2] = int(round(time.time() * 1000))
    record[counter][3] = 'Z'
    eventList[counter2].set()


def fun1(event):
    record[counter][6] = int(round(time.time() * 1000))
    record[counter][7] = 1
    eventList[counter2].set()


def fun2(event):
    record[counter][6] = int(round(time.time() * 1000))
    record[counter][7] = 2
    eventList[counter2].set()


def funJ(event):
    eventList[-1].set()


def click1():
    global mode
    mode = 1


def click2():
    global mode
    mode = 2


def click3():
    global mode
    mode = 3


def skip(event):
    global s
    s = True


def doResult():
    s_time1 = []    # 搜索time  匹配
    j_time1 = []    # 记忆time
    s_time2 = []
    j_time2 = []
    s_correct1 = 0  # 搜索正确数  匹配
    j_correct1 = 0  # 记忆正确数
    s_correct2 = 0
    j_correct2 = 0
    path = './result/4/' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + '.txt'
    f = open(path, 'w')
    f.write('次数\t试次\t第6步反应时(ms)\t正误\t第8步反应时(ms)\t正误\n')
    for i in range(total):
        s_time = record[i][2] - record[i][1]
        j_time = record[i][6] - record[i][5]
        if record[i][0] == '匹配':
            if record[i][4] == '正确':
                s_correct1 += 1
            if record[i][8] == '正确':
                j_correct1 += 1
            s_time1.append(s_time)
            j_time1.append(j_time)
        else:
            if record[i][4] == '正确':
                s_correct2 += 1
            if record[i][8] == '正确':
                j_correct2 += 1
            s_time2.append(s_time)
            j_time2.append(j_time)
        s = str(i+1) + '\t' + record[i][0] + '\t' + str(s_time) + '\t\t' + record[i][4] + '\t' \
            + str(j_time)+'\t\t'+str(record[i][8])+'\n'
        f.write(s)
    s_ave1 = round(1.0*sum(s_time1)/len(s_time1), 2)
    j_ave1 = round(1.0*sum(j_time1)/len(j_time1), 2)
    s_ave2 = round(1.0*sum(s_time2)/len(s_time2), 2)
    j_ave2 = round(1.0*sum(j_time2)/len(j_time2), 2)
    if mode == 1:
        n = int(total*0.2)
        f.write('匹配试次出现概率20%')
    elif mode == 2:
        n = int(total*0.5)
        f.write('匹配试次出现概率50%')
    elif mode == 3:
        n = int(total*0.8)
        f.write('匹配试次出现概率80%')
    else:
        pass
    s_ratio1 = round(s_correct1 / n * 100.0, 2)
    j_ratio1 = round(j_correct1 / n * 100.0, 2)
    s_ratio2 = round(s_correct2 / (total-n) * 100.0, 2)
    j_ratio2 = round(j_correct2 / (total-n) * 100.0, 2)
    f.write('\n匹配试次\t'+'搜索RT(ms):'+str(s_ave1)+'\t搜索正确率(%):'+str(s_ratio1)+'\t记忆RT(ms):'+str(j_ave1)
            + '\t记忆正确率(%):' + str(j_ratio1))
    f.write('\n控制试次\t' + '搜索RT(ms):' + str(s_ave2) + '\t搜索正确率(%):' + str(s_ratio2) + '\t记忆RT(ms):' + str(
        j_ave2) + '\t记忆正确率(%):' + str(j_ratio2))
    f.close()
    messagebox.showinfo('result', '实验结束')
    return


root = tk.Tk()
root.title("窗口1")

btn1 = tk.Button(root, text='匹配试次出现概率20%', width=25, command=click1).pack()
btn2 = tk.Button(root, text='匹配试次出现概率50%', width=25, command=click2).pack()
btn3 = tk.Button(root, text='匹配试次出现概率80%', width=25, command=click3).pack()

top = tk.Toplevel(root)
top.title('窗口2')

cvs_width = 1080
cvs_height = 720
color = ['red', 'blue', 'yellow', 'green']
eventList = []
record = {}
counter = 0
counter2 = 0
total = 30
mode = 0
c = 300         # 300秒倒计时
s = False       # 是否跳过休息时间

cvs = tk.Canvas(top, bg='white', width=cvs_width, height=cvs_height)
cvs.pack()
step0()
cvs.bind_all("<KeyPress-Up>", funA)
cvs.bind_all("<KeyPress-Down>", funZ)
cvs.bind_all("<KeyPress-1>", fun1)
cvs.bind_all("<KeyPress-2>", fun2)
cvs.bind_all("<KeyPress-F>", start)
cvs.bind_all("<KeyPress-J>", funJ)
cvs.bind_all("<KeyPress-S>", skip)

root.mainloop()
