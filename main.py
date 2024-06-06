import threading
import pyautogui
from fsb_tools import fsb_window
from fsb_tools import fsb_tong_yi_qian_wen_code
from fsb_tools import fsb_qanything
from fsb_tools import fsb_find_the_location_of_the_python

# 初始化 qanything 和 tong_yi_qian_wen_code 对象
qAnything = fsb_qanything.YoudaoQAnything()
tong_yi_qian_wen = fsb_tong_yi_qian_wen_code.TongYiQianWen()

def process_code(text):

    # qanything 给出代码
    q = ''.join([
        text,
        '-只给出代码即可。',
        '-不要有过多的话语赘述。',
        '-给出的代码完成缩进等格式化。',
        '-必须根据知识库给出完整的代码。',
        '-不能连接互联网搜索。'
    ])
    chat_response = qAnything.chat(q)
    print(chat_response)
    
    # tong_yi_qian_wen_code 修正的代码
    user_message = ''.join([
        chat_response,
        '检查这个代码',
        '-不要修改代码功能和逻辑。',
        '-只要输出代码就行，不要有过多的话语赘述。',
        '-使用Makkdown格式输出',
        '-不要增加其他功能',
        "-(如果该代码是操作微信的，那就需要检查缩进是否正确，pyautogui.press('enter')这行代码是否在正确的位置，正确的位置是在'for'循环内的最后一行)",
        '-必须保证代码包含以下库的导入：',
        '（import time',
        'import pyautogui',
        'from fsb_tools import fsb_mouse_mover, fsb_window, fsb_browser_opener, fsb_first_process, fsb_ocr, fsb_write_text）',
        '检查代码，有没有未导入的库，如果有，根据上面的提示导入'
    ])
    tong_yi_qian_wen.call_with_messages(user_message)

    # 运行代码
    code_runner = fsb_find_the_location_of_the_python.CodeRunner()
    code_runner.run_script()

def speech_callback(text):
    threading.Thread(target=process_code, args=(text,)).start()

if __name__ == "__main__":
    window = fsb_window.FSBWindow(callback=speech_callback)
