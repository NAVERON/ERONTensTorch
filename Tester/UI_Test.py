
from tkinter import *
import matplotlib.pyplot as plt 

root = Tk()
w = Canvas(root,bg = 'white')
w.pack()

p_all = [0, 1, 2, 3, 4, 5, 6]
v_all = [12, 34, 56, 78, 90, 100, 300]
#测试plot清除和重绘
plt.figure("Value Loss")
plt.ion()
plt.scatter(p_all, v_all)
plt.pause(1)

plt.cla()
plt.pause(1)
p_all = [0, 1, 2, 3, 4, 5, 6]
v_all = [450, 123, 23, 2, 90, 100, 300]
#plt.figure("Policy Loss")
#plt.ion()
plt.scatter(p_all, v_all)

plt.pause(0.01)


def paint(event):
    x1,y1 = (event.x -1),(event.y -1)
    x2,y2 = (event.x +1),(event.y +1)
    w.create_oval(x1,y1,x2,y2,fill='red') #实时获取的坐标作为参数

w.bind('<B1-Motion>',paint)

Label(root,text = '按住鼠标左键并移动，绘图吧......').pack(side = BOTTOM)
mainloop()

