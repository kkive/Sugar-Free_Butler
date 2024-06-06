# 无糖管家手册
#  什么是 /Free-Suger_Butler（FSB管家）
Free-Suger_Butler（以下简称FSB）是第一个基于llm和OCR技术完成的一款大模型一样，可以帮助用户完成各种复杂以及繁琐的任务
# 应用开荒
## Python版本>=3.9.19
  使用命令查看版本
  ```python
python -V
  Python 3.9.19
```
## 下载代码并进入文件夹
```python
git clone https://github.com/kkive/Free-Suger_Butler.git
cd Free-Suger_Butler
pip install rerequirements.txt
```
## 将通义千问的api key加入数据库
```python
cd debugging
```
运行tong_yi_qian_wen-sk2db.py
```python
python tong_yi_qian_wen-sk2db.py
## 根据提示将apikey导入
```
通义千问apikey申请入口：如何开通DashScope并创建API-KEY_模型服务灵积(DashScope)-阿里云帮助中心
运行
```python
python main.py
```
