"""  
@Time: 2023/12/22 15:15 
@Auth: Y5neKO
@File: gui_test.py
@IDE: PyCharm 
"""
import subprocess
import tkinter as tk
from tkinter import scrolledtext

def run_command():
    command = entry.get()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output_text.insert(tk.END, f"Command: {command}\n")
    output_text.insert(tk.END, f"Output:\n{result.stdout}\n")
    output_text.insert(tk.END, f"Errors (if any):\n{result.stderr}\n")
    output_text.see(tk.END)  # 滚动到最新的输出

# 创建主窗口
root = tk.Tk()
root.title("Command Output Viewer")

# 创建输入框和运行按钮
entry = tk.Entry(root, width=50)
entry.pack(pady=10)
run_button = tk.Button(root, text="Run Command", command=run_command)
run_button.pack(pady=10)

# 创建 Text 组件用于显示输出
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_text.pack(pady=10)

# 运行主事件循环
root.mainloop()
