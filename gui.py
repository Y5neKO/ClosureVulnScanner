"""  
@Time: 2023/12/22 14:37 
@Auth: Y5neKO
@File: asset.py
@IDE: PyCharm 
"""
from tkinter import *

# 创建GUI根
root = Tk()

# 获取版本号
ver = StringVar()
ver.set("1.0")
logo_image = PhotoImage(file="asset/Closure_48x48.png")

# GUI主体
root.title(f"ClosureVulnScanner V{ver.get()} by Y5neKO")    # 标题
root.iconbitmap("asset/Closure.ico")     # 标题logo
root.geometry("800x500")                # 窗口默认大小

# label测试
label = Label(root, image=logo_image, compound="left", text=f"ClosureVulnScanner V{ver.get()}", relief="flat", font=("", 20))
label.pack(anchor="n")


def callback():
    print("点击了按钮")


button = Button(root, image=logo_image, text="按钮", compound="left", command=callback, relief="flat", font="calibri")
button.pack(expand=True, fill="none")


mainloop()
