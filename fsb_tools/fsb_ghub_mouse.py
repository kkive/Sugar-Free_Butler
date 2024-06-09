@ -0,0 +1,83 @@
#罗技驱动包：
from ctypes import CDLL, c_char_p
from os import path,system
import time

# 罗技函数：
# ↓↓↓↓↓↓↓↓↓ 调用ghub键鼠驱动 ↓↓↓↓↓↓↓↓↓
try:
    gm = CDLL(r'fsb_tools\ghub_device.dll')  # ghubdlldir
    gmok = gm.device_open()
    system('cls') 
    if not gmok:
        print('未安装ghub或者lgs驱动!!!')
    else:
        print('初始化成功!')
except FileNotFoundError:
    print('重要键鼠文件缺失')
    gmok = 0


gm.key_down.argtypes = [c_char_p]
gm.key_up.argtypes = [c_char_p]


def mouse_xy(x, y, abs_move = False):
    try:
        return gm.moveR(int(x), int(y), abs_move)
    except (NameError, OSError):
        print('键鼠调用严重错误!!!')


def mouse_down(key = 1):
    try:
        return gm.mouse_down(int(key))
    except (NameError, OSError):
        print('键鼠调用严重错误!!!')


def mouse_up(key = 1):
    try:
        return gm.mouse_up(int(key))
    except (NameError, OSError):
        print('键鼠调用严重错误!!!')


def scroll(num = 1):
    try:
        return gm.scroll(int(num))
    except (NameError, OSError):
        print('键鼠调用严重错误!!!')


def key_down(key=''):
    try:
        return gm.key_down(key.encode('utf-8'))
    except (NameError, OSError):
        print('键鼠调用严重错误!!!')


def key_up(key=''):
    try:
        return gm.key_up(key.encode('utf-8'))
    except (NameError, OSError):
        print('键鼠调用严重错误!!!')


def device_close():
    try:
        return gm.device_close()
    except (OSError, NameError):
        pass
# ↑↑↑↑↑↑↑↑↑ 调用ghub键鼠驱动 ↑↑↑↑↑↑↑↑↑
if __name__ == "__main__":
    mouse_down(key=1)
    mouse_up(key=1)







