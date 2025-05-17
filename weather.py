import requests
import random
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_weather(city):
    """
    使用高德天气API获取指定城市的当前天气信息，以猫咪友好的方式展示
    
    参数:
        city (str): 城市名称
    
    返回:
        str: 猫咪友好的天气信息
    """
    # 获取高德地图API密钥
    amap_key = os.getenv('AMAP_KEY')
    if not amap_key:
        return None, "喵呜！天气API密钥未配置，请检查.env文件喵~"

    # 高德天气API的基础URL
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    # 猫咪表情和描述
    cat_emojis = {
        '晴': '😺',    # 晴天
        '多云': '😸',  # 多云
        '阴': '😺',    # 阴天
        '雨': '😿',    # 雨天
        '雪': '😹',    # 雪天
        '雷': '🙀',    # 雷雨
        '雾': '😺',    # 雾天
    }
    
    # 温度相关的猫咪情绪和表情
    temperature_moods = {
        'freezing': {
            'emoji': '🥶',
            'mood': '瑟瑟发抖',
            'reactions': [
                '喵呜！好冷啊，我要钻被窝了！',
                '喵呜！冻死喵了，我要开暖气！',
                '喵呜！这么冷的天，我要穿毛衣了！',
                '喵呜！我要去壁炉边取暖了！'
            ]
        },
        'cold': {
            'emoji': '😿',
            'mood': '有点冷',
            'reactions': [
                '喵~ 有点冷，我要找个暖和的地方~',
                '喵~ 温度有点低，我要去晒太阳了~',
                '喵~ 好冷啊，我要去喝热牛奶了~',
                '喵~ 这种天气最适合窝在主人怀里了~'
            ]
        },
        'cool': {
            'emoji': '😺',
            'mood': '舒适',
            'reactions': [
                '喵~ 温度正好，适合打盹~',
                '喵~ 这种天气最舒服了~',
                '喵~ 温度真合适，我要去玩耍了~',
                '喵~ 天气真好，我要去探险了~'
            ]
        },
        'warm': {
            'emoji': '😸',
            'mood': '温暖',
            'reactions': [
                '喵~ 温度真舒服，我要去晒太阳了~',
                '喵~ 暖暖的，我要去花园里打盹了~',
                '喵~ 这种天气最适合在窗台上睡觉了~',
                '喵~ 温度正好，我要去追蝴蝶了~'
            ]
        },
        'hot': {
            'emoji': '😅',
            'mood': '有点热',
            'reactions': [
                '喵呜！好热啊，我要去阴凉处乘凉了！',
                '喵呜！太热了，我要去吹空调了！',
                '喵呜！这种天气最适合在风扇下睡觉了！',
                '喵呜！我要去喝冰水了！'
            ]
        },
        'scorching': {
            'emoji': '🥵',
            'mood': '热死了',
            'reactions': [
                '喵呜！热死喵了！我要去冰箱里避暑了！',
                '喵呜！太热了，我要去游泳池了！',
                '喵呜！这种天气最适合在空调房里睡觉了！',
                '喵呜！我要去北极避暑了！'
            ]
        }
    }
    
    # 猫咪天气描述和性格评论
    cat_descriptions = {
        '晴': [
            '喵~ 今天是个晒太阳的好日子！',
            '喵~ 阳光正好，适合在窗台上打盹~',
            '喵~ 太阳公公出来了，我要去晒肚皮了！',
            '喵~ 这么好的天气，不睡个午觉太可惜了~'
        ],
        '多云': [
            '喵~ 云朵遮住了太阳，但还是很舒服~',
            '喵~ 多云天气，适合在沙发上打盹~',
            '喵~ 云朵真漂亮，我要去追它们了~',
            '喵~ 这种天气最适合睡觉了~'
        ],
        '阴': [
            '喵~ 虽然没有太阳，但还是很舒服~',
            '喵~ 阴天最适合在窗台上打盹了~',
            '喵~ 这种天气最适合睡觉了~',
            '喵~ 阴天也是好天气呢~'
        ],
        '雨': [
            '喵~ 下雨了，还是待在屋里吧~',
            '喵~ 雨滴打在窗户上的声音真好听~',
            '喵~ 下雨天最适合窝在主人怀里了~',
            '喵~ 雨声真催眠，我要去睡觉了~'
        ],
        '雪': [
            '喵~ 下雪了！好想出去玩雪球~',
            '喵~ 雪花真漂亮，我要去追它们了~',
            '喵~ 雪地真软，我要去踩脚印了~',
            '喵~ 下雪天最适合在壁炉边打盹了~'
        ],
        '雷': [
            '喵呜！打雷了，好可怕！',
            '喵呜！我要躲到床底下了！',
            '喵呜！闪电好可怕，我要抱抱！',
            '喵呜！这种天气最适合躲在被窝里了！'
        ],
        '雾': [
            '喵~ 雾蒙蒙的，要小心走路哦~',
            '喵~ 雾好大，我要去探险了~',
            '喵~ 雾天最适合玩捉迷藏了~',
            '喵~ 雾里的世界好神秘啊~'
        ]
    }
    
    # 获取温度相关的猫咪情绪
    def get_temperature_mood(temp):
        if temp < 0:
            return temperature_moods['freezing']
        elif temp < 10:
            return temperature_moods['cold']
        elif temp < 20:
            return temperature_moods['cool']
        elif temp < 30:
            return temperature_moods['warm']
        elif temp < 35:
            return temperature_moods['hot']
        else:
            return temperature_moods['scorching']
    
    try:
        # 构建请求参数
        params = {
            'key': amap_key,
            'city': city,
            'extensions': 'base',  # 获取实时天气
            'output': 'JSON'
        }
        
        # 发送请求
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        result = response.json()
        
        # 检查响应状态
        if result['status'] != '1' or not result['lives']:
            return None, "喵呜！获取天气信息失败，请稍后再试喵~"
        
        # 获取天气信息
        weather_data = result['lives'][0]
        weather_type = weather_data['weather']
        temperature = float(weather_data['temperature'])
        humidity = weather_data['humidity']
        wind_direction = weather_data['winddirection']
        wind_power = weather_data['windpower']
        
        # 获取温度相关的猫咪情绪
        temp_mood = get_temperature_mood(temperature)
        temp_comment = random.choice(temp_mood['reactions'])
        
        # 获取天气描述
        weather_emoji = cat_emojis.get(weather_type, '😺')
        weather_comment = random.choice(cat_descriptions.get(weather_type, cat_descriptions['晴']))
        
        # 构建猫咪友好的天气信息
        cat_weather = f"""
喵喵喵~ 这里是{city}的天气播报喵~ {weather_emoji}

{weather_comment}
{temp_comment}

{city}天气: {weather_type} {weather_emoji}
温度: {temperature}°C {temp_mood['emoji']}
湿度: {humidity}%
风向: {wind_direction}
风力: {wind_power}级

喵~ 当前温度让我{temp_mood['mood']} {temp_mood['emoji']}
喵~ 记得多喝水，保持温暖哦！{weather_emoji}
"""
        return cat_weather, None
        
    except requests.exceptions.RequestException as e:
        return None, f"喵呜！网络出问题了: {e}"
    except Exception as e:
        return None, f"喵呜！发生了一些意外: {e}"

# 测试函数
if __name__ == "__main__":
    print("欢迎来到猫咪天气站！喵~")
    print("提示：请输入正确的城市名称，例如：北京、上海、广州、深圳等")
    
    while True:
        city = input("\n请输入你想知道天气的城市（输入 'q' 退出）喵~: ")
        if city.lower() == 'q':
            print("喵~ 下次再见！")
            break
            
        weather, error = get_weather(city)
        
        if weather:
            print(weather)
        else:
            print(error)
            print("\n喵~ 一些常见城市名称示例：")
            print("- 中国城市：北京、上海、广州、深圳")
            print("- 请确保输入正确的城市名称，不要包含省份或国家名称") 