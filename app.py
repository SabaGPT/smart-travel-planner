from flask import Flask, render_template, request, jsonify
import requests
import json
from config import Config, AMAP_KEY, DEEPSEEK_API_KEY
from openai import OpenAI
from datetime import datetime
import weather
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
app.config.from_object(Config)

# 初始化DeepSeek客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

class TripPlanner:
    """旅游规划器类，负责处理天气、行程生成和路线规划等功能"""
    
    def __init__(self):
        """初始化旅游规划器"""
        self.amap_key = AMAP_KEY
        # 创建带有重试机制的session
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,  # 最大重试次数
            backoff_factor=1,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        # 禁用SSL验证，解决SSL连接问题
        self.session.verify = False

    def get_weather_forecast(self, location):
        """
        获取指定城市的天气信息
        
        参数:
            location (str): 城市名称
            
        返回:
            str: 天气信息，如果获取失败则返回None
        """
        try:
            weather_data = weather.get_weather(location)
            return weather_data
        except Exception as e:
            print(f"获取天气信息失败: {str(e)}")
            return None

    def generate_itinerary(self, location, interests, dietary_preferences):
        """
        使用DeepSeek生成个性化行程
        
        参数:
            location (str): 城市名称
            interests (str): 用户兴趣
            dietary_preferences (str): 饮食偏好
            
        返回:
            str: 生成的行程，如果生成失败则返回None
        """
        try:
            # 构建提示词
            prompt = f"""
            基于以下信息，生成一个完美的一日游行程：
            地点：{location}
            兴趣：{interests}
            饮食偏好：{dietary_preferences}
            
            请按照以下格式生成行程：

            ### 完美一日游行程规划

            # 上午行程
            [景点1]
            - 游览时间：[具体时间]
            - 简介：[景点介绍]
            - 交通建议：[如何到达]

            [景点2]
            - 游览时间：[具体时间]
            - 简介：[景点介绍]
            - 交通建议：[如何到达]

            # 午餐
            [餐厅1]
            - 用餐时间：[具体时间]
            - 推荐菜品：[特色菜品]
            - 交通建议：[如何到达]

            # 下午行程
            [景点3]
            - 游览时间：[具体时间]
            - 简介：[景点介绍]
            - 交通建议：[如何到达]

            [景点4]
            - 游览时间：[具体时间]
            - 简介：[景点介绍]
            - 交通建议：[如何到达]

            # 晚餐
            [餐厅2]
            - 用餐时间：[具体时间]
            - 推荐菜品：[特色菜品]
            - 交通建议：[如何到达]

            # 晚间行程（可选）
            [景点5]
            - 游览时间：[具体时间]
            - 简介：[景点介绍]
            - 交通建议：[如何到达]

            # 交通总建议
            - 提供该城市的整体交通建议
            - 包括公共交通、打车、步行等建议
            - 可以推荐交通APP或实用工具

            注意事项：
            1. 请确保每个景点和餐厅都用【】标注，这样我可以提取它们进行路线规划
            2. 时间安排要合理，考虑交通时间
            3. 景点之间要相对集中，减少不必要的奔波
            4. 交通建议要具体且实用
            5. 推荐当地特色美食和必去景点
            """
            
            # 调用DeepSeek API生成行程
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个专业的旅游规划师，擅长规划合理且有趣的行程。"},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"生成行程失败: {str(e)}")
            return None

    def extract_locations(self, itinerary):
        """
        从行程文本中提取地点名称
        
        参数:
            itinerary (str): 行程文本
            
        返回:
            list: 提取的地点名称列表
        """
        if not itinerary:
            return []
        
        # 使用正则表达式提取【】中的地点，排除重复
        locations = list(set(re.findall(r'【(.*?)】', itinerary)))
        
        # 过滤掉空字符串和太短的地点名称
        locations = [loc for loc in locations if loc and len(loc) > 1]
        
        print(f"提取的地点: {locations}")  # 调试信息
        return locations

    def get_route_planning(self, locations):
        """
        使用高德地图API规划路线
        
        参数:
            locations (list): 地点名称列表
            
        返回:
            dict: 路线规划结果，包含错误信息或路线详情
        """
        try:
            # 检查地点数量
            if not locations or len(locations) < 2:
                return {"error": "需要至少两个地点才能规划路线"}
            
            coordinates = []  # 存储地点坐标
            failed_locations = []  # 存储获取失败的地点
            
            # 高德地图地理编码API地址
            geocode_url = "https://restapi.amap.com/v3/geocode/geo"
            
            # 遍历地点列表，获取每个地点的坐标
            for location in locations:
                # 构建搜索参数
                params = {
                    'key': self.amap_key,
                    'address': f"苏州市{location}",
                    'city': '苏州',
                    'extensions': 'all'  # 获取更详细的信息
                }
                
                print(f"正在搜索地点: {location}")  # 调试信息
                
                try:
                    # 发送地理编码请求
                    response = self.session.get(geocode_url, params=params, timeout=10)
                    result = response.json()
                    
                    if result['status'] == '1' and result['geocodes']:
                        # 获取最匹配的结果
                        best_match = result['geocodes'][0]
                        location_coord = best_match['location']
                        coordinates.append(location_coord)
                        print(f"成功获取坐标: {location} -> {location_coord}")
                        print(f"地点详情: {best_match['formatted_address']}")  # 打印详细地址
                    else:
                        # 尝试不带"苏州市"前缀重新搜索
                        params['address'] = location
                        response = self.session.get(geocode_url, params=params, timeout=10)
                        result = response.json()
                        
                        if result['status'] == '1' and result['geocodes']:
                            best_match = result['geocodes'][0]
                            location_coord = best_match['location']
                            coordinates.append(location_coord)
                            print(f"成功获取坐标(第二次尝试): {location} -> {location_coord}")
                            print(f"地点详情: {best_match['formatted_address']}")
                        else:
                            failed_locations.append(location)
                            print(f"无法获取地点坐标: {location}, API响应: {result}")
                except Exception as e:
                    print(f"获取地点坐标时发生错误: {str(e)}")
                    failed_locations.append(location)
            
            # 检查是否有获取失败的地点
            if failed_locations:
                return {
                    "error": f"无法获取以下地点的坐标: {', '.join(failed_locations)}",
                    "locations": locations
                }
            
            # 检查是否获取到足够的坐标
            if len(coordinates) < 2:
                return {
                    "error": "无法获取足够的地点坐标来规划路线",
                    "locations": locations
                }
            
            # 调用高德地图API规划路线
            route_url = "https://restapi.amap.com/v3/direction/driving"
            params = {
                'key': self.amap_key,
                'origin': coordinates[0],  # 起点坐标
                'destination': coordinates[-1],  # 终点坐标
                'waypoints': '|'.join(coordinates[1:-1]) if len(coordinates) > 2 else '',  # 途经点坐标
                'extensions': 'all'  # 获取详细信息
            }
            
            print(f"路线规划参数: {params}")
            
            try:
                # 发送路线规划请求
                response = self.session.get(route_url, params=params, timeout=10)
                route_data = response.json()
                
                # 添加地点名称到路线数据中
                if route_data['status'] == '1':
                    route_data['locations'] = locations
                    # 添加起点和终点名称到路线步骤中
                    if 'route' in route_data and 'paths' in route_data['route']:
                        for path in route_data['route']['paths']:
                            if 'steps' in path:
                                for i, step in enumerate(path['steps']):
                                    # 为每个步骤添加起点和终点名称
                                    if i < len(locations) - 1:
                                        step['start_location'] = locations[i]
                                        step['end_location'] = locations[i + 1]
                                    else:
                                        step['start_location'] = locations[-2]
                                        step['end_location'] = locations[-1]
                
                return route_data
            except Exception as e:
                print(f"路线规划请求失败: {str(e)}")
                return {
                    "error": f"路线规划请求失败: {str(e)}",
                    "locations": locations
                }
                
        except Exception as e:
            print(f"路线规划失败: {str(e)}")
            return {
                "error": f"路线规划失败: {str(e)}",
                "locations": locations
            }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    # 获取请求数据
    data = request.json
    location = data.get('location')
    interests = data.get('interests')
    dietary_preferences = data.get('dietary_preferences')
    
    # 创建旅游规划器实例
    planner = TripPlanner()
    
    # 获取天气信息
    weather_info = planner.get_weather_forecast(location)
    
    # 生成行程
    itinerary = planner.generate_itinerary(location, interests, dietary_preferences)
    
    # 从行程中提取地点
    locations = planner.extract_locations(itinerary)
    
    # 规划路线
    route = planner.get_route_planning(locations) if locations else {"error": "无法提取地点信息"}
    
    # 返回结果
    return jsonify({
        'weather': weather_info,
        'itinerary': itinerary,
        'route': route
    })

if __name__ == '__main__':
    app.run(debug=True) 