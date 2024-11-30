import json,os,tkinter
from tkinter import ttk

sub=""
Entry=""

def load():
    global data,setting,subjects
    with open('LessonRecord1.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    with open('setting.json', 'r', encoding='utf-8') as json_file:
        setting = json.load(json_file)

    subjects = []
    for record in data["records"]:
        subjects.append(record["subject"])

def main():
    global data,setting,subjects,sub,Entry

    top = tkinter.Tk()
    top.title("记录器v"+setting['version'])
    top.geometry("300x150")
    top.resizable(0,0)

    label = tkinter.Label(top, text="欢迎使用记录器v"+setting['version']+"！")
    label.grid(row=0, columnspan=2)# 显示欢迎信息

    xVariable = tkinter.StringVar()     # #创建变量，便于取值
    
    com = ttk.Combobox(top, textvariable=xVariable)     # #创建下拉菜单
    com.grid(row=1, column=0, columnspan=2)  # #将下拉菜单绑定到窗体
    com["value"] = subjects    # #给下拉菜单设定值
    com.current(0)    #设定下拉菜单的默认值
    sub = com.get()

    Entry = tkinter.Entry(top, show=None)
    Entry.grid(row=2, column=0, columnspan=2)

    record_button = tkinter.Button(top, text="记录", command=record) 
    save_button = tkinter.Button(top, text="保存", command=save)
    record_button.grid(row=3, column=0)
    save_button.grid(row=3, column=1)
    top.mainloop()

def record():
    global sub,data,Entry
    for record in data["records"]:
        if record["subject"] == sub:
            try:
                time = int(Entry.get())
            except:
                tkinter.messagebox.showinfo(title='错误提示',
            		message='您输入的数据不合法，请检查是否为阿拉伯数字、是否为空！') 
                break
                
            record["lessons"].append(int(Entry.get()))
            print("[info] 记录成功！")
            break

def save():
    file_name=data['name']+'.json'
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("\n[info] json文件保存完毕！")


if __name__ == '__main__':
    load()
    main()
