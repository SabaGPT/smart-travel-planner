import requests
import json
from typing import Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

class Chatbot:
    def __init__(self):
        # API endpoints
        self.joke_api = "https://v2.jokeapi.dev/joke/Any"
        self.quote_api = "https://api.quotable.io/random"
        self.user_api = "https://randomuser.me/api/"
        
        # 设置重试策略
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get_joke(self) -> str:
        """
        获取一个随机笑话
        """
        try:
            response = self.session.get(self.joke_api, timeout=10)
            response.raise_for_status()  # 检查响应状态
            data = response.json()
            
            if data["type"] == "single":
                return data["joke"]
            else:
                return f"{data['setup']}\n{data['delivery']}"
        except requests.exceptions.RequestException as e:
            return f"抱歉，获取笑话时出现错误: {str(e)}"

    def get_quote(self) -> str:
        """
        获取一条励志名言
        """
        try:
            # 添加备用 API
            backup_quote_api = "https://api.quotable.io/quotes/random"
            try:
                response = self.session.get(self.quote_api, timeout=10)
                response.raise_for_status()
            except:
                # 如果主 API 失败，尝试备用 API
                response = self.session.get(backup_quote_api, timeout=10)
                response.raise_for_status()
            
            data = response.json()
            if isinstance(data, list):
                data = data[0]  # 如果返回的是列表，取第一个元素
            return f'"{data["content"]}"\n- {data["author"]}'
        except requests.exceptions.RequestException as e:
            return f"抱歉，获取名言时出现错误: {str(e)}"

    def get_random_profile(self) -> str:
        """
        生成一个随机用户资料
        """
        try:
            response = self.session.get(self.user_api, timeout=10)
            response.raise_for_status()
            data = response.json()
            user = data["results"][0]
            
            profile = f"""
随机用户资料:
姓名: {user['name']['first']} {user['name']['last']}
性别: {user['gender']}
邮箱: {user['email']}
国家: {user['location']['country']}
"""
            return profile
        except requests.exceptions.RequestException as e:
            return f"抱歉，生成用户资料时出现错误: {str(e)}"

def main():
    # 创建聊天机器人实例
    bot = Chatbot()
    
    print("欢迎使用多功能聊天机器人！")
    print("请选择以下功能：")
    print("1. 获取随机笑话")
    print("2. 获取励志名言")
    print("3. 生成随机用户资料")
    print("4. 退出")
    
    while True:
        try:
            choice = input("\n请输入选项 (1-4): ")
            
            if choice == "1":
                print("\n" + bot.get_joke())
            elif choice == "2":
                print("\n" + bot.get_quote())
            elif choice == "3":
                print(bot.get_random_profile())
            elif choice == "4":
                print("感谢使用，再见！")
                break
            else:
                print("无效的选项，请重新选择。")
        except Exception as e:
            print(f"发生错误: {str(e)}")
            print("请重试...")
            time.sleep(1)  # 添加短暂延迟

if __name__ == "__main__":
    main() 