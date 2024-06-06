
from paddleocr import PaddleOCR
from PIL import ImageGrab
import pygetwindow as gw
import numpy as np
import logging
import os
from fuzzywuzzy import process
import logreset

logreset.reset_logging()  # 在日志设置之前

class OCR:
    def __init__(self):
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_directory, 'fsb_logs.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")

    def fuzzy_match(self, target, choices, threshold=80):
        matches = process.extract(target, choices, limit=3)
        for match in matches:
            if match[1] >= threshold:
                return match[0]
        return None

    def Ocr(self, app_name, click_name):
        all_windows = gw.getAllTitles()
        matched_app_name = self.fuzzy_match(app_name, all_windows)
        if not matched_app_name:
            app_name_parts = app_name.split()
            for part in app_name_parts:
                matched_app_name = self.fuzzy_match(part, all_windows)
                if matched_app_name:
                    break

        if not matched_app_name:
            error_message = f"Error: 找不到进程：'{app_name}'."
            print(error_message)
            logging.error(error_message)
            return

        try:
            app_window = gw.getWindowsWithTitle(matched_app_name)[0]
            logging.info(f"找到进程：'{matched_app_name}'，窗口位置和大小：{app_window}")
        except IndexError:
            error_message = f"Error: 找不到进程：'{matched_app_name}'."
            print(error_message)
            logging.error(error_message)
            return

        window_rect = (app_window.left, app_window.top, app_window.right, app_window.bottom)
        screenshot = ImageGrab.grab(window_rect)
        screenshot_np = np.array(screenshot)
        
        # 将截图一分为二
        height, width = screenshot_np.shape[:2]
        left_half = screenshot_np[:, :width // 2]
        right_half = screenshot_np[:, width // 2:]
        
        # OCR识别
        result_left = self.ocr.ocr(left_half, cls=True)
        result_right = self.ocr.ocr(right_half, cls=True)
        
        # 合并结果并调整右半部分的坐标
        for res in result_right:
            for line in res:
                for point in line[0]:
                    point[0] += width // 2
        result = result_left + result_right

        recognized_texts = [line[1][0] for res in result for line in res]

        matched_click_name = self.fuzzy_match(click_name, recognized_texts)
        if not matched_click_name:
            click_name_parts = click_name.split()
            for part in click_name_parts:
                matched_click_name = self.fuzzy_match(part, recognized_texts)
                if matched_click_name:
                    break

        if matched_click_name:
            for res in result:
                for line in res:
                    text = line[1][0]
                    if matched_click_name in text:
                        send_coordinates = line[0]
                        x, y = send_coordinates[0]
                        success_message = f"找到按钮：'{matched_click_name}'，坐标：({x}, {y})"
                        print(success_message)
                        logging.info(success_message)
                        return x, y

        error_message = f"Error: 找不到按钮：'{click_name}'."
        print(error_message)
        logging.error(error_message)
        return

if __name__ == "__main__":
    ocr = OCR()
    app_name = "微信"
    click_name = "搜索"
    ocr.Ocr(app_name, click_name)
