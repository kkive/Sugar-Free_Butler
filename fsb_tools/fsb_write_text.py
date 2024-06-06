# import time
# import pyautogui
# import logging
# import os
# import pyperclip

# class TextTyper:
#     # 定义类属性 interval
#     interval = 0.1

#     def __init__(self, text):
#         self.text = text
#         self.setup_logging()

#     @staticmethod
#     def setup_logging():
#         # 配置日志设置
#         log_directory = 'logs'
#         if not os.path.exists(log_directory):
#             os.makedirs(log_directory)
#         logging.basicConfig(
#             filename=os.path.join(log_directory, 'fsb_logs.log'),
#             level=logging.INFO,
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S'
#         )

#     def type_text(self):
#         logging.info(f"写文字: {self.text}")
#         pyperclip.copy(self.text)  # 复制文本到剪贴板
#         pyautogui.hotkey('ctrl', 'v')  # 粘贴剪贴板内容
#         logging.info("文本输入已完成。")

# # 使用示例
# if __name__ == "__main__":
#     # 创建一个TextTyper对象，传入需要输入的内容
#     typer = TextTyper("杰")
#     # 调用type_text方法来输入内容
#     typer.type_text()
import time
import pyautogui
import logging
import os
import pyperclip

class TextTyper:
    interval = 0.1  # 定义类属性 interval

    def __init__(self, text):
        self.text = text
        self.setup_logging()

    @staticmethod
    def setup_logging():
        """配置日志设置"""
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)  # 使用 exist_ok=True 简化目录创建
        logging.basicConfig(
            filename=os.path.join(log_directory, 'fsb_logs.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def type_text(self):
        """将文本粘贴到当前焦点位置"""
        logging.info(f"写文字: {self.text}")
        pyperclip.copy(self.text)  # 复制文本到剪贴板
        pyautogui.hotkey('ctrl', 'v')  # 模拟按键操作粘贴内容
        logging.info("文本输入已完成。")

# 使用示例
if __name__ == "__main__":
    typer = TextTyper("杰")
    typer.type_text()
