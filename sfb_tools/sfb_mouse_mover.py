import pyautogui
import logging
import os
from datetime import datetime

# 定义 MouseMover 类
class MouseMover:
    def __init__(self):
        # 配置日志设置
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)
        
        # 优化日志记录配置
        logging.basicConfig(
            handlers=[logging.FileHandler(os.path.join(log_directory, 'sfb_logs.log'), 'a')],
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger('MouseMover')

    def move(self, x, y):
        start_time = datetime.now()
        pyautogui.moveTo(x, y, duration=0.5)  # 减少移动持续时间，加快移动速度
        pyautogui.click()
        end_time = datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()
        self.logger.info(f"鼠标移动到: ({x}, {y}), 耗时: {elapsed_time:.2f} 秒")

# 确保在被导入时不会执行
if __name__ == "__main__":
    mover = MouseMover()
    mover.move(100, 100)  # 示例用法
