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
pip install -r rerequirements.txt
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
通义千问apikey申请入口：[如何开通DashScope并创建API-KEY_模型服务灵积(DashScope)-阿里云帮助中心](https://help.aliyun.com/zh/dashscope/developer-reference/activate-dashscope-and-create-an-api-key?spm=a2c4g.11186623.0.0.6d1b46c1tmtvCW)。  
## 安装必要的鼠标驱动
```python
cd 必要驱动
## 手动安装LGS_9.02.65_x64_Logitech.exe
```
## 运行
```python
python main.py
```

# 使用方法
右击小猫咪图片，说出需求，等待执行代码就好了🆗  

![image](https://github.com/kkive/Free-Suger_Butler/assets/51246778/1878e0c6-6bef-40fe-8964-04978f236c0c)

# 功能

|项目名称|是否支持|指令|版本|
| :----------- | :-:  |:------------|:---:|
|操作微信指定对象发消息|✅|"打开微信给老婆发消息，问她吃了吗"|v1.0|
|操作浏览器|❌|NULL|v1.1|
|操作命令行执行命令|❌|NULL|v1.1|
|英雄联盟匹配成功自动点击确认|✅|"英雄联盟帮我自动点击接受"|v1.1|
目前只能想到这些功能，大家有什么想法，请在[issues](https://github.com/kkive/Free-Suger_Butler/issues)选择Labels选择'需求'提交
# 代码目前只能实现基础功能，不是特别完善，希望大家多提一点意见，作者不会破防，代码之路任重道远加油💪
# 目前作者还有工作，所以不是SOHO，看到消息必回
# 最新消息可能更新在[飞书知识库](https://yetnfbtnyy.feishu.cn/wiki/EWS9wJ3JViSfP7kZ31pcgSPJnCe?fromScene=spaceOverview)
## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=kkive/Free-Suger_Butler&type=Date)](https://star-history.com/#kkive/Free-Suger_Butler&Date)
