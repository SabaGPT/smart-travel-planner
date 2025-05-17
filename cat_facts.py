# 导入requests库，用于发送HTTP请求
import requests
import time  # 导入time模块，用于添加延时
import json  # 导入json模块，用于保存数据
from datetime import datetime  # 导入datetime模块，用于记录时间

def get_cat_fact():
    """获取一条猫咪知识"""
    try:
        # 发送GET请求到猫咪知识API
        response = requests.get("https://catfact.ninja/fact")
        # 将响应转换为JSON格式
        data = response.json()
        return data["fact"]
    except Exception as e:
        return f"获取猫咪知识时出错: {str(e)}"

def save_fact(fact):
    """保存猫咪知识到文件"""
    try:
        # 准备要保存的数据
        save_data = {
            "fact": fact,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 读取现有数据（如果文件存在）
        try:
            with open("cat_facts.json", "r", encoding="utf-8") as f:
                facts = json.load(f)
        except FileNotFoundError:
            facts = []
        
        # 添加新数据
        facts.append(save_data)
        
        # 保存到文件
        with open("cat_facts.json", "w", encoding="utf-8") as f:
            json.dump(facts, f, ensure_ascii=False, indent=4)
            
        return True
    except Exception as e:
        print(f"保存数据时出错: {str(e)}")
        return False

def main():
    print("🐱 欢迎来到猫咪知识小站！")
    
    while True:
        # 获取用户输入
        user_input = input("\n你想了解猫咪知识吗？(输入 'y' 继续，输入 's' 查看保存的知识，输入其他键退出): ").lower()
        
        if user_input == 's':
            try:
                with open("cat_facts.json", "r", encoding="utf-8") as f:
                    facts = json.load(f)
                print("\n📚 已保存的猫咪知识：")
                for i, fact_data in enumerate(facts, 1):
                    print(f"\n{i}. 时间：{fact_data['timestamp']}")
                    print(f"   知识：{fact_data['fact']}")
            except FileNotFoundError:
                print("\n还没有保存任何猫咪知识哦！")
            continue
            
        if user_input != 'y':
            print("感谢使用，再见！👋")
            break
            
        # 获取并显示猫咪知识
        fact = get_cat_fact()
        print("\n🐱 Did you know?", fact)
        
        # 询问是否保存
        save_input = input("\n要保存这条知识吗？(y/n): ").lower()
        if save_input == 'y':
            if save_fact(fact):
                print("✅ 知识已保存！")
            else:
                print("❌ 保存失败！")
        
        # 添加1秒延时，避免请求过于频繁
        time.sleep(1)

if __name__ == "__main__":
    main() 