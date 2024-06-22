import sqlite3

def store_api_key(db_path, api_key):
    """
    将 API 密钥写入数据库。
    
    参数:
    db_path (str): SQLite 数据库文件的路径。
    api_key (str): 要存储的 API 密钥。
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL
    )
    ''')
    
    # 检查 API 密钥格式是否正确
    if not is_valid_api_key(api_key):
        choice = input("API 密钥格式似乎不正确。是否仍要继续添加？(y/n): ")
        if choice.lower() != 'y':
            print("已取消添加。")
            return
    
    # 插入数据
    cursor.execute('INSERT INTO api_keys (key) VALUES (?)', (api_key,))
    
    conn.commit()
    conn.close()

def is_valid_api_key(api_key):
    """
    检查 API 密钥格式是否正确。
    
    参数:
    api_key (str): 要检查的 API 密钥。
    
    返回:
    bool: 如果格式正确返回 True，否则返回 False。
    """
    # 检查 API 密钥长度和是否以 "sk-" 开头
    return api_key.startswith("sk-") and len(api_key) == 38

def fetch_api_keys(db_path):
    """
    从数据库中查询所有 API 密钥。
    
    参数:
    db_path (str): SQLite 数据库文件的路径。
    
    返回:
    list: 包含所有 API 密钥的列表。
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询数据
    cursor.execute('SELECT * FROM api_keys')
    rows = cursor.fetchall()
    
    conn.close()
    
    return rows

# 主程序
if __name__ == "__main__":
    db_path = r'data\sfb_database.db'

    # 提供选择菜单
    choice = input("选择要插入的数据类型 (1: tong_yi_qian_wenkey): ")

    if choice == "1":
        # 用户选择插入 tong_yi_qian_wenkey
        api_key = input("请输入 API 密钥: ")
        store_api_key(db_path, api_key)
        print("tong_yi_qian_wenkey 数据插入完成。")
    else:
        print("无效的选择。")

    # 查询并打印 API 密钥
    api_keys = fetch_api_keys(db_path)
    print("当前数据库中的 API 密钥:")
    for row in api_keys:
        print(f'ID: {row[0]}, KEY: {row[1]}')
