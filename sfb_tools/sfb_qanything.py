import json
import sqlite3
import requests
import logging
import os
from .utils.AuthV3Util import addAuthParams

class YoudaoQAnything:
    def __init__(self, db_path=r'data\sfb_database.db'):
        self.db_path = db_path
        self.setup_logging()
        self.APP_KEY, self.APP_SECRET, self.kbId = self.fetch_api_info()

    def setup_logging(self):
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_directory, 'sfb_logs.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def fetch_api_info(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT app_key, app_secret, kb_id FROM qanything_api_key LIMIT 1')
            row = cursor.fetchone()

        if row:
            return row
        else:
            raise ValueError("在数据库中未找到 API 信息")

    def kbList(self):
        data = {'q': ''}
        addAuthParams(self.APP_KEY, self.APP_SECRET, data)
        header = {'Content-Type': 'application/json'}
        res = self.doCall('https://openapi.youdao.com/q_anything/paas/kb_list', header, json.dumps(data), 'post')
        logging.info(str(res.content, 'utf-8'))

    def fileList(self):
        data = {'q': self.kbId}
        addAuthParams(self.APP_KEY, self.APP_SECRET, data)
        header = {'Content-Type': 'application/json'}
        res = self.doCall('https://openapi.youdao.com/q_anything/paas/file_list', header, json.dumps(data), 'post')
        logging.info(str(res.content, 'utf-8'))

    def chat(self, q):
        data = {'q': q, 'kbIds': [self.kbId]}
        addAuthParams(self.APP_KEY, self.APP_SECRET, data)
        header = {'Content-Type': 'application/json'}
        res = self.doCall('https://openapi.youdao.com/q_anything/paas/chat', header, json.dumps(data), 'post')
        response_data = json.loads(res.content)

        if 'result' in response_data and 'response' in response_data['result']:
            code_module = response_data['result']['response']
            code_module_cleaned = self.clean_code_module(code_module)
            logging.info("Code Module Cleaned: %s", code_module_cleaned)
            return code_module_cleaned
        else:
            logging.error("在响应中未找到代码模块。")
            return None

    def clean_code_module(self, code_module):
        code_lines = code_module.strip('`').strip('.').split('\n')[1:-1]
        code_module_cleaned = '\n'.join(code_lines).replace('```', '')
        return code_module_cleaned

    def doCall(self, url, header, params, method):
        if method == 'get':
            return requests.get(url, params=params)
        elif method == 'post':
            return requests.post(url, data=params, headers=header)

# 示例用法:
if __name__ == '__main__':
    youdao_qanything = YoudaoQAnything()

    q = '打开浏览器访问抖音'
    chat_response = youdao_qanything.chat(q)
    print(chat_response)
