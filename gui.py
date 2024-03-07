"""  
@Time: 2023/12/22 14:37 
@Auth: Y5neKO
@File: asset.py
@IDE: PyCharm 
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# 创建GUI根
root = tk.Tk()

# 获取版本号
ver = tk.StringVar()
ver.set("1.0")
logo_image = tk.PhotoImage(file="asset/Closure_48x48.png")

# GUI主体
root.title(f"ClosureVulnScanner V{ver.get()} by Y5neKO")  # 标题
root.iconbitmap("asset/Closure.ico")  # 标题logo
root.geometry("800x500")  # 窗口默认大小
# label测试
label = tk.Label(root, image=logo_image, compound="left", text=f"ClosureVulnScanner V{ver.get()}", relief="flat",
              font=("", 20))
label.pack(anchor="n")


def callback():
    print("点击了按钮")
    e.insert(1, "123")


button = tk.Button(root, image=logo_image, text="按钮", compound="left", command=callback, relief="flat", font="calibri")
button.pack(expand=True, fill="none")

# 创建一个只读的文本框
e = ttk.Entry(state="readonly", validate="focus")
e.pack(padx=10, pady=10, expand=True)

tk.mainloop()
