import json,os

# 从文件中读取JSON字符串
with open('LessonRecord1.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
with open('setting.json', 'r', encoding='utf-8') as json_file:
    setting = json.load(json_file)

print("欢迎使用记录器v"+setting['version']+"！")
print("[info] json文件加载完毕！\n")
subject=input("请输入科目名称：")
if subject in str(data):
    time=int(input("请输入时间："))
    for record in data["records"]:
        if record["subject"] == subject:
            # 找到后，向lessons数组添加新项
            record["lessons"].append(time)
            break 
    print("记录成功！")
else:
    print("科目不存在！")

file_name=data['name']+'.json'
with open(file_name, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("\n[info] json文件保存完毕！")
print("按任意键退出。")

no_ans=input()