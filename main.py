import json
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QLineEdit, QPushButton, QAction, QMessageBox, QFileDialog, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# 初始化全局变量
sub = ""
Entry = ""
com = ""
current_file = "未加载任何文件"

def load():
    global data, setting, subjects, current_file
    try:
        with open('LessonRecord1.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        with open('setting.json', 'r', encoding='utf-8') as json_file:
            setting = json.load(json_file)

        subjects = []
        for record in data["records"]:
            subjects.append(record["subject"])
        
        current_file = 'LessonRecord1.json'
    except FileNotFoundError as e:
        QMessageBox.critical(None, "文件未找到", f"文件未找到: {e}")
    except json.JSONDecodeError as e:
        QMessageBox.critical(None, "JSON 解析错误", f"JSON 解析错误: {e}")
    except Exception as e:
        QMessageBox.critical(None, "错误", f"发生未知错误: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        load()  # 先加载数据和设置
        self.initUI()

    def initUI(self):
        self.setWindowTitle("记录器v" + setting['version'])
        self.setGeometry(100, 100, 600, 400)

        # 设置全局字体
        try:
            custom_font = QFont("HarmonyOS Sans SC", 12)
        except Exception:
            custom_font = QFont()
        custom_font.setPointSize(12)

        self.setFont(custom_font)

        # 创建菜单栏
        menubar = self.menuBar()

        # 添加文件菜单
        file_menu = menubar.addMenu('文件')
        file_menu.addAction('打开', self.select_json_file)
        file_menu.addAction('保存', self.save)
        file_menu.addAction('退出', self.close)

        # 添加数据处理菜单
        record_menu = menubar.addMenu('数据处理')
        record_menu.addAction('新增学科', self.add_subject)
        record_menu.addAction('清空数据', self.clear_data)
        record_menu.addAction('统计信息', self.load_num)

        # 添加关于菜单
        menubar.addAction('关于', self.about)

        # 创建布局
        layout = QVBoxLayout()

        label = QLabel(f"欢迎使用记录器v{setting['version']}！", self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("HarmonyOS Sans SC", 14, QFont.Bold))
        layout.addWidget(label)

        self.file_label = QLabel(f"当前文件: {current_file}", self)
        layout.addWidget(self.file_label)

        self.com = QComboBox(self)
        self.com.addItems(subjects)
        layout.addWidget(self.com)

        self.Entry = QLineEdit(self)
        layout.addWidget(self.Entry)

        record_button = QPushButton('记录', self)
        record_button.clicked.connect(self.record)
        layout.addWidget(record_button)

        save_button = QPushButton('保存', self)
        save_button.clicked.connect(self.save)
        layout.addWidget(save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def record(self):
        try:
            sub = self.com.currentText()
            for record in data["records"]:
                if record["subject"] == sub:
                    try:
                        time = int(self.Entry.text())
                    except ValueError:
                        QMessageBox.information(self, '错误提示', '您输入的数据不合法，请检查是否为阿拉伯数字、是否为空！')
                        return

                    record["lessons"].append(time)
                    print("[info] 记录成功！")
                    return
        except Exception as e:
            QMessageBox.critical(self, "错误", f"记录错误: {e}")

    def about(self):
        try:
            QMessageBox.information(self, '关于', setting['about'])
        except Exception as e:
            QMessageBox.critical(self, "错误", f"关于信息显示错误: {e}")

    def load_num(self):
        try:
            stats = {}
            for record in data["records"]:
                subject = record["subject"]
                total_time = sum(record["lessons"])
                average_time = total_time / len(record["lessons"]) if record["lessons"] else 0
                total_time_min = f"{total_time // 60}分{total_time % 60}秒"
                average_time_min = f"{average_time // 60}分{round(average_time % 60, 1)}秒"
                stats[subject] = {
                    "total": total_time,
                    "average": average_time,
                    "total_min": total_time_min,
                    "average_min": average_time_min
                }

            message = "科目统计信息:\n"
            for subject, times in stats.items():
                message += f"{subject} - 总时长: {times['total']} 秒（{times['total_min']}）, 平均时长: {times['average']:.2f} 秒（{times['average_min']}）\n"

            QMessageBox.information(self, '统计信息', message)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"统计信息加载错误: {e}")

    def save(self):
        try:
            file_name = data['name'] + '.json'
            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print("\n[info] json文件保存完毕！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"文件保存错误: {e}")

    def add_subject(self):
        try:
            new_subject = QInputDialog.getText(self, "新增学科", "请输入新的学科名称:")[0]
            if new_subject and new_subject not in subjects:
                subjects.append(new_subject)
                data["records"].append({"subject": new_subject, "lessons": []})
                self.com.addItem(new_subject)
                self.com.setCurrentText(new_subject)
                self.save()
                QMessageBox.information(self, '成功', f'学科 "{new_subject}" 已成功添加！')
            elif new_subject in subjects:
                QMessageBox.information(self, '错误提示', f'学科 "{new_subject}" 已存在！')
            else:
                QMessageBox.information(self, '错误提示', '请输入有效的学科名称！')
        except Exception as e:
            QMessageBox.critical(self, "错误", f"新增学科错误: {e}")

    def clear_data(self):
        try:
            confirm = QMessageBox.question(self, "确认清空数据", "您确定要清空所有时间记录吗？", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for record in data["records"]:
                    record["lessons"] = []
                self.save()
                QMessageBox.information(self, '成功', '所有时间记录已成功清空！')
        except Exception as e:
            QMessageBox.critical(self, "错误", f"清空数据错误: {e}")

    def select_json_file(self):
        global data, subjects, current_file
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择JSON记录文件", "", "JSON files (*.json);;All files (*)")
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                
                subjects = [record["subject"] for record in data["records"]]
                
                # 更新下拉菜单的选项
                self.com.clear()
                self.com.addItems(subjects)
                self.com.setCurrentIndex(0)
                
                current_file = file_path
                QMessageBox.information(self, '成功', f'已加载文件: {file_path}')
                
                # 更新文件名显示标签
                self.file_label.setText(f"当前文件: {current_file}")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "文件未找到", f"文件未找到: {e}")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "JSON 解析错误", f"JSON 解析错误: {e}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"选择文件错误: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())