import ctypes
import pygetwindow as gw
import logging
import os
from fuzzywuzzy import fuzz

# 从user32 DLL中定义必要的函数
user32 = ctypes.WinDLL('user32', use_last_error=True)
GetForegroundWindow = user32.GetForegroundWindow
IsIconic = user32.IsIconic
ShowWindow = user32.ShowWindow
SetForegroundWindow = user32.SetForegroundWindow
GetWindowRect = user32.GetWindowRect

# ShowWindow函数的常量
SW_RESTORE = 9
SW_SHOW = 5
SW_MAXIMIZE = 3  # 新增的常量，用于最大化窗口

class RECT(ctypes.Structure):
    _fields_ = [("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long)]

class WindowManager:
    def __init__(self, application_name):
        # 配置日志设置
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_directory, 'sfb_logs.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        self.application_name = application_name
        self.hwnd = self.find_window_by_title(application_name)

    def bring_to_foreground(self):
        if self.hwnd:
            ShowWindow(self.hwnd, SW_MAXIMIZE)  # 最大化窗口
            logging.info(f"窗口 {self.application_name} 被最大化。")
            SetForegroundWindow(self.hwnd)  # 将窗口置于前台
            logging.info(f"窗口 {self.application_name} 被置于前台。")
        else:
            error_message = f"未找到 {self.application_name} 的窗口。"
            print(error_message)
            logging.error(error_message)

    def find_window_by_title(self, partial_title):
        windows = gw.getAllWindows()
        best_match = None
        highest_ratio = 0
        for w in windows:
            ratio = fuzz.partial_ratio(partial_title.lower(), w.title.lower())
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = w
        if best_match:
            logging.info(f"找到窗口: {best_match.title} (匹配度: {highest_ratio})")
            return best_match._hWnd
        logging.warning(f"未找到包含标题 '{partial_title}' 的窗口。")
        return None

    def get_window_position(self):
        if self.hwnd:
            rect = RECT()
            if GetWindowRect(self.hwnd, ctypes.byref(rect)):
                position = (rect.left, rect.top)
                logging.info(f"{self.application_name} 的窗口位置: {position}")
                return position
            else:
                error = ctypes.get_last_error()
                logging.error(f"获取窗口位置失败: {ctypes.WinError(error)}")
                raise ctypes.WinError(error)
        else:
            error_message = f"未找到 {self.application_name} 的窗口。"
            print(error_message)
            logging.error(error_message)
            return None

    def activate(self):
        self.bring_to_foreground()
        position = self.get_window_position()
        if position:
            print(f"{self.application_name} 的窗口位置: {position}")

# 确保在被导入时不会执行
if __name__ == "__main__":
    wm = WindowManager("微信")
    wm.activate()
