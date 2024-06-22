
import sqlite3
from http import HTTPStatus
import dashscope
import logging
import os

class TongYiQianWen:
    def __init__(self, db_path=r'data\sfb_database.db', system_message="You are a helpful assistant."):
        self.setup_logging()
        self.db_path = db_path
        self.system_message = system_message
        self.api_key = self.get_or_prompt_api_key()
        dashscope.api_key = self.api_key

    def setup_logging(self):
        log_directory = 'logs'
        os.makedirs(log_directory, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_directory, 'sfb_logs.log'),
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def get_api_key_from_db(self):
        """
        从数据库中获取 API 密钥。
        
        返回:
        str: 存储在数据库中的 API 密钥，如果不存在则返回 None。
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查询 API 密钥
            cursor.execute('SELECT key FROM api_keys LIMIT 1')
            row = cursor.fetchone()
            conn.close()
            
            if row:
                logging.info("从数据库中获取了API密钥。")
                return row[0]
            else:
                logging.warning("数据库中没有找到API密钥。")
                return None
        except Exception as e:
            logging.error(f"从数据库获取API密钥时出错: {str(e)}")
            return None

    def get_or_prompt_api_key(self):
        """
        获取 API 密钥，如果数据库中没有则提示用户输入。
        
        返回:
        str: 存储在数据库中的 API 密钥。
        """
        api_key = self.get_api_key_from_db()
        if not api_key:
            logging.error("API 密钥未找到，请将 API 密钥添加到数据库并重新运行程序。")
            print("API 密钥未找到，请将 API 密钥添加到数据库并重新运行程序。")
            exit(1)
        return api_key

    def call_with_messages(self, user_message):
        messages = [
            {'role': 'system', 'content': self.system_message},
            {'role': 'user', 'content': user_message}
        ]

        try:
            response = dashscope.Generation.call(
                # dashscope.Generation.Models.qwen_turbo,
                'qwen-max',
                messages=messages,
                result_format='message'
            )

            if response.status_code == HTTPStatus.OK:
                logging.info("API 请求成功。")
                self.log_response(response)
                formatted_code = self.extract_code(response.output['choices'][0]['message']['content'])
                return formatted_code
            
            else:
                error_message = (
                    f"Request id: {response.request_id}, "
                    f"Status code: {response.status_code}, "
                    f"Error code: {response.code}, "
                    f"Error message: {response.message}"
                )
                logging.error(f"API 请求失败: {error_message}")
                raise Exception(error_message)
        except Exception as e:
            logging.error(f"API 请求失败: {str(e)}")
            return str(e)

    def extract_code(self, content):
        """
        提取 content 中 ```python ``` 之间的代码。
        
        参数:
        content: 包含代码块的文本内容。
        
        返回:
        str: 提取到的 Python 代码。
        """
        start = content.find("```python")
        end = content.find("```", start + len("```python"))
        if start != -1 and end != -1:
            python_code = content[start + len("```python"):end].strip()
            file_path = r'tmp.py'
            if not os.path.exists(file_path):
                open(file_path, 'w').close()
                logging.info(f"{file_path} 文件不存在，已创建新文件。")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
                logging.info(f"代码已写入 {file_path} 文件。")
                
            return python_code
        else:
            logging.error("无法找到代码块。")
            return "未能找到代码块"

    def log_response(self, response):
        """
        将 API 响应数据写入日志。
        
        参数:
        response: API 响应对象。
        """
        logging.info(f"Response: {response}")

# 确保在被导入时不会执行
if __name__ == "__main__":
    tong_yi_qian_wen = TongYiQianWen()
    
    user_message = """"""

    response = tong_yi_qian_wen.call_with_messages(user_message)
    print(response)
