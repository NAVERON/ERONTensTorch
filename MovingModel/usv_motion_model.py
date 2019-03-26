

import pylab
import math
import numpy as np
from MovingModel.rk import RK4


class usv_model(object):

    def __init__(self):
        self.m11 = 200
        self.m22 = 250
        self.m33 = 80
        self.d11 = 70
        self.d22 = 100
        self.d33 = 50

    def usv_control(self, x, y, p, u, v, r, tau_u, tau_r):
        udot = lambda h, u, v, r, x, y, p: 1 / self.m11 * (self.m22 * v * r - self.d11 * u + tau_u)
        vdot = lambda h, u, v, r, x, y, p: 1 / self.m22 * (-self.m11 * u * r - self.d22 * v)
        rdot = lambda h, u, v, r, x, y, p: 1 / self.m33 * ((self.m11 - self.m22) * u * v - self.d33 * r + tau_r)
        xdot = lambda h, u, v, r, x, y, p: u * math.cos(p) - v * math.sin(p)
        ydot = lambda h, u, v, r, x, y, p: u * math.sin(p) + v * math.cos(p)
        pdot = lambda h, u, v, r, x, y, p: r

        rk4 = RK4(udot, vdot, rdot, xdot, ydot, pdot)
        t, s = rk4.solve([u, v, r, x, y, p], 1/60, 60/60)
        velocity = s[0:3]
        position = s[3:6]
        position[2] = np.mod(position[2], 2*math.pi)
        return t, velocity, position


if __name__ == "__main__":
    usv = usv_model()
    t, velocity, position = usv.usv_control(0,0,0,0.5,0,0,50,10)

    pylab.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
    pylab.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题

    fig1 = pylab.subplot(321)  # 3代表行，2代表列，所以一共有6个图，1代表此时绘制第二个图。
    fig1.plot(position[0], position[1])
    fig1.set_title("位置")
    fig1.set_xlabel("x")
    fig1.set_ylabel("y")


    fig2 = pylab.subplot(322)
    fig2.plot(t, position[2])
    fig2.set_title("航向角")
    fig2.set_xlabel("t")
    fig2.set_ylabel("φ")

    fig3 = pylab.subplot(323)
    fig3.plot(t, velocity[0])
    fig3.set_title("速度u")
    fig3.set_xlabel("t")
    fig3.set_ylabel("m/s")

    fig4 = pylab.subplot(324)
    fig4.plot(t, velocity[1])
    fig4.set_title("速度v")
    fig4.set_xlabel("t")
    fig4.set_ylabel("m/s")

    fig5 = pylab.subplot(325)
    fig5.plot(t, velocity[2])
    fig5.set_title("角速度r")
    fig5.set_xlabel("t")
    fig5.set_ylabel("r")

    fig5 = pylab.subplot(326)
    fig5.plot(t, np.sqrt(np.power(velocity[0],2)+np.power(velocity[1],2)))
    fig5.set_title("速度s")
    fig5.set_xlabel("t")
    fig5.set_ylabel("m/s")
    # pylab.plot(position[0], position[1])
    # pylab.plot(t, position[0])
    pylab.show()
    



















