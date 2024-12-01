import json
import os
import tkinter
from tkinter import ttk, messagebox

# 初始化全局变量
sub = ""
Entry = ""
com = ""

def load():
    global data, setting, subjects
    with open('LessonRecord1.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open('setting.json', 'r', encoding='utf-8') as json_file:
        setting = json.load(json_file)

    subjects = []
    for record in data["records"]:
        subjects.append(record["subject"])

def main():
    global data, setting, subjects, sub, Entry, com

    top = tkinter.Tk()
    top.title("记录器v" + setting['version'])
    top.geometry("500x300")

    # 创建菜单栏
    menubar = tkinter.Menu(top)
    top.config(menu=menubar)

    # 添加文件菜单
    file_menu = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="保存", command=save)
    file_menu.add_separator()# 添加分割线
    file_menu.add_command(label="退出", command=top.quit)
    file_menu.add_separator()# 添加分割线
    file_menu.add_command(label="关于", command=about)
    file_menu.add_separator()# 添加分割线
    file_menu.add_command(label="统计信息", command=load_num)

    label = tkinter.Label(top, text="欢迎使用记录器v" + setting['version'] + "！")

    xVariable = tkinter.StringVar()  # 创建变量，便于取值
    com = ttk.Combobox(top, textvariable=xVariable)  # 创建下拉菜单
    com["values"] = subjects  # 给下拉菜单设定值
    com.current(0)  # 设定下拉菜单的默认值
    sub = com.get()

    Entry = tkinter.Entry(top, show=None)

    record_button = tkinter.Button(top, text="记录", command=record)
    save_button = tkinter.Button(top, text="保存", command=save)

    label.grid(row=0, columnspan=2)  # 显示欢迎信息
    com.grid(row=1, column=0, columnspan=2)  # 将下拉菜单绑定到窗体
    Entry.grid(row=2, column=0, columnspan=2)
    record_button.grid(row=3, column=0)
    save_button.grid(row=3, column=1)

    top.mainloop()

def record():
    global data, Entry, com  # 添加 com 到全局变量
    sub = com.get()  # 重新获取下拉菜单的当前值
    for record in data["records"]:
        if record["subject"] == sub:
            try:
                time = int(Entry.get())
            except ValueError:
                messagebox.showinfo(title='错误提示', message='您输入的数据不合法，请检查是否为阿拉伯数字、是否为空！')
                return  # 如果输入不合法，直接返回，不再继续执行

            record["lessons"].append(time)
            print("[info] 记录成功！")
            return

def about():
    global setting
    messagebox.showinfo(title='关于', message=setting['about'])

def load_num():
    global data
    stats = {}
    for record in data["records"]:
        subject = record["subject"]
        total_time = sum(record["lessons"])
        average_time = total_time / len(record["lessons"]) if record["lessons"] else 0
        stats[subject] = {
            "total": total_time,
            "average": average_time
        }

    message = "科目统计信息:\n"
    for subject, times in stats.items():
        message += f"{subject} - 总时长: {times['total']} 秒, 平均时长: {times['average']:.2f} 秒\n"

    messagebox.showinfo(title='统计信息', message=message)


def save():
    file_name = data['name'] + '.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("\n[info] json文件保存完毕！")


if __name__ == '__main__':
    load()
    main()