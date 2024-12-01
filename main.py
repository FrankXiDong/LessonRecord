import json
import os
import tkinter
from tkinter import ttk, messagebox, font, simpledialog

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
    top.geometry("600x400")  # 调整窗口大小

    # 设置全局字体
    try:
        custom_font = font.Font(family="HarmonyOS Sans SC", size=12)
    except tkinter.TclError:
        custom_font = font.nametofont("TkDefaultFont")
    custom_font.configure(size=12)

    # 使用 ttk.Style 设置全局样式
    style = ttk.Style()
    style.configure('.', font=custom_font)

    # 创建菜单栏
    menubar = tkinter.Menu(top)
    top.config(menu=menubar)

    # 添加文件菜单
    file_menu = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="保存", command=save)
    file_menu.add_separator()  # 添加分割线
    file_menu.add_command(label="新增学科", command=add_subject)
    file_menu.add_separator()  # 添加分割线
    file_menu.add_command(label="清空数据", command=clear_data)
    file_menu.add_separator()  # 添加分割线
    file_menu.add_command(label="统计信息", command=load_num)
    file_menu.add_separator()  # 添加分割线
    file_menu.add_command(label="退出", command=top.quit)
    file_menu.add_separator()  # 添加分割线
    file_menu.add_command(label="关于", command=about)

    label = tkinter.Label(top, text="欢迎使用记录器v" + setting['version'] + "！", font=("HarmonyOS Sans SC", 14, "bold"))

    xVariable = tkinter.StringVar()  # 创建变量，便于取值
    com = ttk.Combobox(top, textvariable=xVariable, width=30)  # 创建下拉菜单
    com["values"] = subjects  # 给下拉菜单设定值
    com.current(0)  # 设定下拉菜单的默认值
    sub = com.get()

    Entry = tkinter.Entry(top, show=None, width=30)

    record_button = ttk.Button(top, text="记录", command=record, width=15)  # 使用 ttk.Button
    save_button = ttk.Button(top, text="保存", command=save, width=15)  # 使用 ttk.Button

    label.grid(row=0, columnspan=2, pady=20)  # 显示欢迎信息
    com.grid(row=1, column=0, columnspan=2, padx=20, pady=10)  # 将下拉菜单绑定到窗体
    Entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
    record_button.grid(row=3, column=0, padx=20, pady=10)
    save_button.grid(row=3, column=1, padx=20, pady=10)

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
        total_time_min = str(total_time // 60) + "分" + str(total_time % 60) + "秒"
        average_time_min = str(average_time // 60) + "分" + str(round(average_time % 60, 1)) + "秒"
        stats[subject] = {
            "total": total_time,
            "average": average_time,
            "total_min": total_time_min,
            "average_min": average_time_min
        }

    message = "科目统计信息:\n"
    for subject, times in stats.items():
        message += f"{subject} - 总时长: {times['total']} 秒（{times['total_min']}）, 平均时长: {times['average']:.2f} 秒（{times['average_min']}）\n"

    messagebox.showinfo(title='统计信息', message=message)

def save():
    file_name = data['name'] + '.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("\n[info] json文件保存完毕！")

def add_subject():
    global data, subjects, com

    new_subject = simpledialog.askstring("新增学科", "请输入新的学科名称:")
    if new_subject and new_subject not in subjects:
        subjects.append(new_subject)
        data["records"].append({"subject": new_subject, "lessons": []})
        com["values"] = subjects
        com.current(len(subjects) - 1)
        save()
        messagebox.showinfo(title='成功', message=f'学科 "{new_subject}" 已成功添加！')
    elif new_subject in subjects:
        messagebox.showinfo(title='错误提示', message=f'学科 "{new_subject}" 已存在！')
    else:
        messagebox.showinfo(title='错误提示', message='请输入有效的学科名称！')

def clear_data():
    global data, subjects, com

    confirm = messagebox.askyesno("确认清空数据", "您确定要清空所有时间记录吗？")
    if confirm:
        for record in data["records"]:
            record["lessons"] = []  # 清空每个学科的时间记录
        save()
        messagebox.showinfo(title='成功', message='所有时间记录已成功清空！')

if __name__ == '__main__':
    load()
    main()