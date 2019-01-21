
from tkinter import *

root = Tk()
w = Canvas(root,bg = 'white')
w.pack()

def paint(event):
    x1,y1 = (event.x -1),(event.y -1)
    x2,y2 = (event.x +1),(event.y +1)
    w.create_oval(x1,y1,x2,y2,fill='red') #实时获取的坐标作为参数

w.bind('<B1-Motion>',paint)

Label(root,text = '按住鼠标左键并移动，绘图吧......').pack(side = BOTTOM)
mainloop()

