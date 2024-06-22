import sys
import subprocess

class CodeRunner:
    def __init__(self):
        self.interpreter_path = sys.executable

    def run_script(self, script_name="tmp.py"):
        # 直接调用解释器路径和脚本名运行脚本
        subprocess.call([self.interpreter_path, script_name])

if __name__ == "__main__":
    # 创建一个CodeRunner实例
    code_runner = CodeRunner()

    # 运行指定的 Python 脚本
    code_runner.run_script()
