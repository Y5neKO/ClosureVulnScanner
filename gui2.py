"""  
@Time: 2024/3/7 9:55 
@Auth: Y5neKO
@File: gui2.py 
@IDE: PyCharm 
"""

import sys
import time
import tkinter as tk
from tkinter import scrolledtext  # 导入滚动文本框的模块

# 生成主窗口，命名 window
root = tk.Tk()
# 定义主窗口标题
root.title('xxx程序')
# 定义主窗口的长宽，窗体距离屏幕上下的距离
root.geometry('800x500+100+60')


# 定义日志输出到tkiner类
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, str):
        self.text_widget.insert(tk.END, str)  # 在text末尾追加文字
        self.text_widget.see(tk.END)  # 光标一直追加到文件末尾
        self.text_widget.update()  # 一直更新输出

    def flush(self):
        pass


# 控制台输出函数，输出到t1
def ternimal_print(msg):
    DATE_TIME = time.strftime('[%Y-%m-%d %H:%M:%S]')
    t1.insert('end', f'{DATE_TIME}  {msg}\n')  # 向text文本框末尾追加文字
    t1.see(tk.END)  # 光标一直追加到文件末尾
    t1.update()  # 一直更新输出


# 定义按钮事件相关函数
def fun1():
    sys.stdout = StdoutRedirector(t1)  # 重定向标准输出
    t1.delete(1.0, tk.END)  # 清除text文本框原来文字
    ternimal_print('程序运行开始.....')
    print('这是 按钮1 的输出文字')
    for i in range(30):
        ternimal_print(f'程序运行中。。。{i}')
        time.sleep(0.1)


def fun2():
    sys.stdout = StdoutRedirector(t1)  # 重定向标准输出
    t1.delete(1.0, tk.END)  # 清除原来终端输出的内容
    ternimal_print('程序运行开始.....')
    print('这是 按钮2 的输出文字')
    ternimal_print('程序运行结束')


# 定义按钮相关组件
frm1 = tk.Frame(root)
frm1.pack()
button1 = tk.Button(frm1, text='功能1', font=('宋体', 12, 'bold'), command=fun1)
button1.pack(side='left', padx=20, pady=20, ipadx=20, ipady=10)
button2 = tk.Button(frm1, text='功能2', font=('宋体', 12, 'bold'), command=fun2)
button2.pack(side='left', padx=20, pady=20, ipadx=20, ipady=10)
button3 = tk.Button(frm1, text='退出', font=('宋体', 12, 'bold'), command=root.quit)
button3.pack(side='left', padx=20, pady=20, ipadx=20, ipady=10)

# 定义Laber组件
frm2 = tk.Frame(root)
frm2.pack(anchor='w')
l1 = tk.Label(frm2, text='程序运行日志：', font=('宋体', 12))
l1.pack(side='left', padx=1, pady=1, ipadx=1, ipady=1)

# 定义滚动文本组件
frm3 = tk.Frame(root)
frm3.pack(anchor='w')
t1 = scrolledtext.ScrolledText(frm3, width=200, height=300, bg='#cfdccf', font=('宋体', 13))
t1.pack(fill='both', side='left', expand=True)

# 启动默认打开帮助页面
sys.stdout = StdoutRedirector(t1)  # 重定向标准输出到t1
print('欢迎使用，这是测试文字')

# 启动窗口main
tk.mainloop()
