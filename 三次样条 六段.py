# 三次样条插值法
import matplotlib.pyplot as plt
import numpy as np
from sympy import *


# 第一类插值条件函数
def one(x, y, a, b, n):
    h = np.zeros(n)
    u = np.zeros(n - 1)
    r = np.zeros(n - 1)
    g = np.zeros(n + 1)
    A = np.zeros(shape=(n + 1, n + 1))
    q = np.zeros(n)
    w = np.zeros(n)
    e = np.zeros(n)
    t = np.zeros(n)
    # 计算和，u，r，g
    for i in range(0, n):
        h[i] = x[i + 1] - x[i]
    print("h=", h)
    for i in range(0, n - 1):
        u[i] = h[i] / (h[i] + h[i + 1])
    print("u=", u)
    for i in range(0, n - 1):
        r[i] = 1 - u[1]
    print("r=", r)
    for i in range(1, n):
        g[i] = (6 / (h[i - 1] + h[i])) * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])
    g[0] = 6 / h[0] * ((y[1] - y[0]) / h[0] - a)
    g[n] = (6 / h[n - 1]) * (b - (y[n] - y[n - 1]) / h[n - 1])
    # 对线性方程组系数矩阵进行赋值
    print("g=", g)
    for i in range(0, n + 1):
        A[i][i] = 2
    A[0][1] = 1
    A[n][n - 1] = 1
    for i in range(0, n - 1):
        A[i + 1][i] = u[i]
    for i in range(2, n + 1):
        A[i - 1][i] = r[i - 2]
    # 求解线性方程组
    M = np.linalg.solve(A, g)
    print("A=", A)
    print("M=", M)
    for i in range(0, n):
        q[i] = (M[i + 1] - M[i]) / 6 * h[i]
        w[i] = (M[i] * x[i + 1] - M[i + 1] * x[i]) / 2 * h[i]
        e[i] = (3 * M[i + 1] * pow(x[i], 2) - 3 * M[i] * pow(x[i + 1], 2) - 6 * y[i] + M[i]
                * pow(h[i], 2) + 6 * y[i + 1] - M[i + 1] * pow(h[i], 2)) / 6 * h[i]
        t[i] = (M[i] * pow(x[i + 1], 3) - M[i + 1] * pow(x[i], 3) + 6 * y[i] * x[i + 1] - M[i]
                * pow(h[i], 2) * x[i + 1] - 6 * y[i + 1] * x[i] + M[i + 1] * pow(h[i], 2) * x[i]) / 6 * h[i]
    print("q=", q)
    print("w=", w)
    print("e=", e)
    print("t=", t)


# 主函数部分
x = [0, 1, 2, 3, 4, 5, 6]
y = [1, 0, 0, 1, 2, 2, 1]
n = len(x) - 1
one(x, y, -0.6, -1.8, n)

# 对区间进行划分
x1 = np.linspace(0, 1, 100)
x2 = np.linspace(1, 2, 100)
x3 = np.linspace(2, 3, 100)
x4 = np.linspace(3, 4, 100)
x5 = np.linspace(4, 5, 100)
x6 = np.linspace(5, 6, 100)

# 分段函数定义
y1 = (0.64 * pow(x1, 3) + (-1.04) * pow(x1, 2) + (-0.6) * x1 + 1)
y2 = (-0.12 * pow(x2, 3) + 1.24 * pow(x2, 2) + (-2.88) * x2 + 1.76)
y3 = (-0.16 * pow(x3, 3) + 1.48 * pow(x3, 2) + (-3.36) * x3 + 2.08)
y4 = (-0.24 * pow(x4, 3) + 2.2 * pow(x4, 2) + (-5.52) * x4 + 4.24)
y5 = (0.12 * pow(x5, 3) + (-2.12) * pow(x5, 2) + 11.76 * x5 - 18.8)
y6 = (-0.24 * pow(x6, 3) + 3.28 * pow(x6, 2) + (-15.24) * x6 + 26.2)

# 画出图像
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.plot(x3, y3)
plt.plot(x4, y4)
plt.plot(x5, y5)
plt.plot(x6, y6)
plt.show()
