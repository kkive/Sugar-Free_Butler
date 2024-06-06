import time
import pyautogui
from fsb_tools import fsb_mouse_mover, fsb_window, fsb_browser_opener, fsb_first_process, fsb_ocr, fsb_write_text

if __name__ == "__main__":
    fsb_first_process.WindowManager("微信").activate()
    time.sleep(5)
    x, y = fsb_ocr.OCR().Ocr("微信", "搜索")
    fsb_mouse_mover.MouseMover().move(x + 30, y)
    for text in ["老婆", "今天晚上吃了吗？"]:
        fsb_write_text.TextTyper(text).type_text()
        time.sleep(4 if text == "老婆" else 2)
        pyautogui.press('enter')  # 确保enter键按下动作在循环内每轮迭代的末尾