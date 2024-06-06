# fsb_tools/browser_opener.py
'''
打开浏览器的功能块
'''
import webbrowser
import logging
import os

class BrowserOpener:
    def __init__(self):
        # 配置日志设置
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_directory, 'fsb_logs.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def open_browser(self, url):
        webbrowser.open_new(url)
        result = f"打开网站 {url}"
        logging.info(result)
        return result

# 确保在被导入时不会执行
if __name__ == "__main__":
    browser_opener = BrowserOpener()
    browser_opener.open_browser("https://www.baidu.com")
