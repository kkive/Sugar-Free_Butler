import json
import customtkinter as Ctk
from PIL import Image
import time
import speech_recognition as sr
from ctypes import windll
import logging
import os
import threading
from vosk import KaldiRecognizer, Model
from fuzzywuzzy import fuzz  # 新增：引入fuzzywuzzy库
from .sfb_find_the_location_of_the_python import CodeRunner

class FSBWindow:
    def __init__(self, callback=None):
        self.callback = callback
        self.FSB = None
        self.label = None
        self.assistant_photo = None
        self.assistant_dragging_photo = None
        self.assistant_blink_photo = None
        self.assistant_photo_width = None
        self.assistant_photo_height = None
        self.position_right = None
        self.position_bottom = None
        self.drag_time = None
        self.is_dragging = False
        self.prev_x = 0
        self.prev_y = 0
        self.recognizer = sr.Recognizer()
        self.lock = threading.Lock()
        self.code_run_flag = False  # 新增：用于指示是否运行了代码
        self.setup_logging()

        windll.shcore.SetProcessDpiAwareness(1)
        self.FSB = Ctk.CTk()
        self.configure_window()
        self.load_images()
        self.create_label()
        self.bind_events()

        self.FSB.mainloop()

    def setup_logging(self):
        """配置日志设置"""
        log_directory = 'logs'
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        logging.basicConfig(
            filename=os.path.join(log_directory, 'sfb_logs.log'),
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def configure_window(self):
        """配置窗口属性"""
        self.FSB.title("FSB-Free_Sugar_Butler[无糖管家]")
        self.FSB.iconbitmap(r'media\logo.ico')
        self.FSB.overrideredirect(True)
        self.FSB.attributes('-topmost', True)
        self.FSB.wm_attributes("-transparentcolor", 'gray')

    def recognize_speech(self):
        """识别语音"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
            self.recognizer.vosk_model = Model(model_path='model/vosk-model-small-cn-0.22', model_name='vosk-model-small-cn-0.22')
            text = self.recognizer.recognize_vosk(audio, language='zh-cn')
            result = json.loads(text)
            text = result["text"].replace(" ", "")
            logging.info(f"识别结果: {text}")

            # 新增：使用fuzzywuzzy库对比相似度
            if (fuzz.partial_ratio(text, "运行最近的代码") > 50 or 
                fuzz.partial_ratio(text, "运行上一次的代码") > 50):
                code_runner = CodeRunner()
                code_runner.run_script()
                logging.info("运行代码脚本")
                self.code_run_flag = True  # 设置标志
            else:
                return text

        except sr.WaitTimeoutError:
            logging.warning("在等待语音开始时超时")
            return None
        except sr.UnknownValueError:
            logging.warning("无法识别语音")
            return None
        except sr.RequestError as e:
            logging.error(f"语音识别服务请求失败: {e}")
            return None

    def load_image(self, file_path, scale=0.333):
        """加载并缩放图片"""
        image = Image.open(file_path)
        original_width, original_height = image.size
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        ctk_image = Ctk.CTkImage(light_image=image, size=(new_width, new_height))
        return ctk_image, new_width, new_height

    def on_drag_start(self, event):
        """处理拖动开始事件"""
        self.is_dragging = True
        self.prev_x = event.x_root
        self.prev_y = event.y_root

    def on_drag_motion(self, event):
        """处理拖动过程中事件"""
        if self.is_dragging:
            new_x = self.FSB.winfo_x() + (event.x_root - self.prev_x)
            new_y = self.FSB.winfo_y() + (event.y_root - self.prev_y)
            self.FSB.geometry(f'+{new_x}+{new_y}')
            self.prev_x = event.x_root
            self.prev_y = event.y_root

    def on_drag_release(self, event):
        """处理拖动结束事件"""
        self.is_dragging = False

    def on_label_click(self, event):
        """处理标签点击事件"""
        if event.num == 3:
            print('开始语音识别...')
            logging.debug("右键点击，启动语音识别线程")
            threading.Thread(target=self.start_speech_recognition).start()
        elif event.num == 1:
            self.on_drag_start(event)

    def start_speech_recognition(self):
        """启动语音识别"""
        print('聆听中...')
        logging.info("语音识别开始")
        result = self.recognize_speech()
        if result:
            print(f"识别结果: {result}")
            logging.info(f"语音识别结果: {result}")
            if self.callback:
                self.callback(result)
            time.sleep(3)
        elif self.code_run_flag == False:
            print('你好像还没说话！')
            logging.warning("未能识别任何结果")
        logging.debug("语音识别线程结束")

    def load_images(self):
        """加载图片资源"""
        self.assistant_photo, self.assistant_photo_width, self.assistant_photo_height = self.load_image(r"media\cat.png")
        self.assistant_dragging_photo = self.assistant_photo
        self.assistant_blink_photo = self.assistant_photo

    def create_label(self):
        """创建并配置标签"""
        self.label = Ctk.CTkLabel(self.FSB, image=self.assistant_photo, bg_color="gray", cursor="hand2", text="")
        self.label.pack()

        screen_width = self.FSB.winfo_screenwidth()
        screen_height = self.FSB.winfo_screenheight()
        self.position_right = int(screen_width - self.assistant_photo_width) + 35
        self.position_bottom = int(screen_height - self.assistant_photo_height) - 30
        self.drag_time = time.time()

        self.FSB.geometry(f'+{self.position_right}+{self.position_bottom}')

    def bind_events(self):
        """绑定事件"""
        self.label.bind("<ButtonPress-1>", self.on_drag_start)
        self.label.bind("<B1-Motion>", self.on_drag_motion)
        self.label.bind("<ButtonRelease-1>", self.on_drag_release)
        self.label.bind("<Button-3>", self.on_label_click)

    def set_callback(self, callback):
        """设置回调函数"""
        self.callback = callback

if __name__ == "__main__":
    FSBWindow()
