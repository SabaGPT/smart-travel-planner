import requests
import json
from typing import Optional
from requests.exceptions import RequestException, Timeout
import time

def get_random_joke(max_retries: int = 3, timeout: int = 5) -> Optional[str]:
    """
    从 JokeAPI 获取一个随机笑话
    
    Args:
        max_retries (int): 最大重试次数
        timeout (int): 请求超时时间（秒）
    
    Returns:
        Optional[str]: 如果成功返回笑话，如果失败返回 None
    """
    # JokeAPI 的端点
    url = "https://v2.jokeapi.dev/joke/Any?safe-mode"
    
    for attempt in range(max_retries):
        try:
            # 发送 GET 请求获取笑话，添加超时设置
            response = requests.get(url, timeout=timeout)
            
            # 检查请求是否成功
            response.raise_for_status()
            
            # 解析 JSON 响应
            joke_data = response.json()
            
            # 验证响应数据
            if not isinstance(joke_data, dict):
                raise ValueError("API 返回的数据格式不正确")
                
            if "type" not in joke_data:
                raise ValueError("API 响应中缺少 'type' 字段")
            
            # 根据笑话类型返回不同的格式
            if joke_data["type"] == "single":
                if "joke" not in joke_data:
                    raise ValueError("单行笑话缺少 'joke' 字段")
                return joke_data["joke"]
            else:
                if "setup" not in joke_data or "delivery" not in joke_data:
                    raise ValueError("双行笑话缺少必要字段")
                return f"{joke_data['setup']}\n{joke_data['delivery']}"
                
        except Timeout:
            print(f"请求超时 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(1)  # 在重试之前等待1秒
                continue
            return None
            
        except RequestException as e:
            print(f"网络请求错误 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            return None
            
        except ValueError as e:
            print(f"数据验证错误: {e}")
            return None
            
        except Exception as e:
            print(f"发生未知错误: {e}")
            return None
    
    return None

def print_joke(joke: Optional[str]) -> None:
    """
    以美观的方式打印笑话，使用文本框格式
    
    Args:
        joke (Optional[str]): 要打印的笑话
    """
    if joke is None:
        print("\n" + "─" * 50)
        print("❌ 无法获取笑话")
        print("请检查网络连接或稍后再试")
        print("─" * 50 + "\n")
        return
    
    # 将笑话文本分割成行
    joke_lines = joke.split('\n')
    
    # 计算文本框的宽度（使用最长的行长度，最小宽度为40）
    width = max(max(len(line) for line in joke_lines), 40)
    
    # 创建装饰边框
    top_border = "┌" + "─" * (width + 2) + "┐"
    bottom_border = "└" + "─" * (width + 2) + "┘"
    
    # 打印标题
    print("\n" + "=" * (width + 4))
    print(" " * ((width - 8) // 2) + "🤣 随机笑话 🤣")
    print("=" * (width + 4))
    
    # 打印文本框
    print(top_border)
    for line in joke_lines:
        # 计算每行需要的填充空格
        padding = width - len(line)
        print(f"│ {line}{' ' * padding} │")
    print(bottom_border)
    print()  # 添加一个空行

def main():
    """
    主函数：获取并打印一个随机笑话
    """
    try:
        joke = get_random_joke()
        print_joke(joke)
    except Exception as e:
        print(f"程序运行出错: {e}")

if __name__ == "__main__":
    main() 