import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API密钥配置
AMAP_KEY = os.getenv('AMAP_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

# 应用配置
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    DEBUG = True
    
    # 高德地图API配置
    AMAP_BASE_URL = "https://restapi.amap.com/v3"
    
    # DeepSeek配置
    DEEPSEEK_MODEL = "deepseek-chat"
    
    # OpenAI配置
    OPENAI_MODEL = "gpt-3.5-turbo"
    
    # 天气API配置
    WEATHER_BASE_URL = "https://api.weatherapi.com/v1" 