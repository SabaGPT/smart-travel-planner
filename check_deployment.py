import sys
import os
import pkg_resources
import requests
from dotenv import load_dotenv

def check_python_version():
    """检查Python版本"""
    print("检查Python版本...")
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"❌ Python版本过低！需要 {required_version[0]}.{required_version[1]} 或更高版本")
        return False
    print(f"✅ Python版本 {current_version[0]}.{current_version[1]} 符合要求")
    return True

def check_dependencies():
    """检查项目依赖"""
    print("\n检查项目依赖...")
    required_packages = {
        'flask': '2.0.1',
        'requests': '2.26.0',
        'python-dotenv': '0.19.0',
        'deepseek-ai': '0.1.0',
        'Werkzeug': '2.0.3'
    }
    
    all_installed = True
    for package, version in required_packages.items():
        try:
            pkg_resources.require(f"{package}=={version}")
            print(f"✅ {package} {version} 已安装")
        except pkg_resources.VersionConflict:
            print(f"⚠️ {package} 版本不匹配，需要 {version}")
            all_installed = False
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package} 未安装")
            all_installed = False
    
    return all_installed

def check_env_file():
    """检查环境变量文件"""
    print("\n检查环境变量配置...")
    required_vars = ['AMAP_KEY', 'DEEPSEEK_API_KEY', 'SECRET_KEY']
    
    if not os.path.exists('.env'):
        print("❌ .env 文件不存在")
        return False
    
    load_dotenv()
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少以下环境变量: {', '.join(missing_vars)}")
        return False
    
    print("✅ 环境变量配置完整")
    return True

def check_api_connections():
    """检查API连接"""
    print("\n检查API连接...")
    
    # 检查高德地图API
    amap_key = os.getenv('AMAP_KEY')
    try:
        response = requests.get(
            f"https://restapi.amap.com/v3/weather/weatherInfo?key={amap_key}&city=苏州",
            timeout=5
        )
        if response.status_code == 200:
            print("✅ 高德地图API连接正常")
        else:
            print("❌ 高德地图API连接失败")
            return False
    except Exception as e:
        print(f"❌ 高德地图API连接错误: {str(e)}")
        return False
    
    # 检查DeepSeek API
    deepseek_key = os.getenv('DEEPSEEK_API_KEY')
    try:
        response = requests.get(
            "https://api.deepseek.com/v1/health",
            headers={"Authorization": f"Bearer {deepseek_key}"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ DeepSeek API连接正常")
        else:
            print("❌ DeepSeek API连接失败")
            return False
    except Exception as e:
        print(f"❌ DeepSeek API连接错误: {str(e)}")
        return False
    
    return True

def main():
    """主函数"""
    print("=== 智能旅游规划助手部署检查 ===\n")
    
    checks = [
        ("Python版本检查", check_python_version),
        ("依赖包检查", check_dependencies),
        ("环境变量检查", check_env_file),
        ("API连接检查", check_api_connections)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n执行{check_name}...")
        if not check_func():
            all_passed = False
            print(f"\n❌ {check_name}失败")
        else:
            print(f"\n✅ {check_name}通过")
    
    if all_passed:
        print("\n🎉 所有检查通过！项目可以正常运行。")
        print("\n运行项目：")
        print("1. 确保在项目根目录")
        print("2. 执行命令：python app.py")
        print("3. 访问 http://localhost:5000")
    else:
        print("\n⚠️ 部分检查未通过，请解决上述问题后再运行项目。")

if __name__ == "__main__":
    main() 