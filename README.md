# 🎯 智能旅游规划助手

[![版本](https://img.shields.io/badge/版本-1.0.0-blue.svg)](https://github.com/SabaGPT/smart-travel-planner)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![许可证](https://img.shields.io/badge/许可证-MIT-green.svg)](https://github.com/SabaGPT/smart-travel-planner/blob/main/LICENSE)
[![构建状态](https://img.shields.io/badge/构建-通过-brightgreen.svg)](https://github.com/SabaGPT/smart-travel-planner/actions)
[![代码覆盖率](https://img.shields.io/badge/覆盖率-85%25-green.svg)](https://github.com/SabaGPT/smart-travel-planner/actions)
[![依赖状态](https://img.shields.io/badge/依赖-最新-brightgreen.svg)](https://github.com/SabaGPT/smart-travel-planner/blob/main/requirements.txt)

这是一个基于 AI 的智能旅游规划助手，它能帮你规划完美的旅行路线！无论是美食、文化还是自然风光，它都能为你量身定制最佳行程。

## 🌟 特色功能

- 🤖 AI 智能规划：使用 DeepSeek AI 生成个性化行程
- 🌤️ 实时天气：提供目的地天气预报
- 🗺️ 智能路线：使用高德地图 API 规划最优路线
- 📱 响应式界面：支持手机和电脑访问
- 💾 行程导出：一键导出完整行程安排

## 🚀 快速开始

### 1. 系统要求

- Python 3.8 或更高版本
- pip（Python 包管理器）
- 网络连接
- 高德地图 API 密钥
- DeepSeek API 密钥

### 2. 克隆项目

```bash
git clone https://github.com/SabaGPT/smart-travel-planner.git
cd smart-travel-planner
```

### 3. 创建虚拟环境（推荐）

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

1. 复制示例环境文件：

```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 API 密钥：

```
AMAP_KEY=你的高德地图API密钥
DEEPSEEK_API_KEY=你的DeepSeek API密钥
SECRET_KEY=你的Flask密钥
```

### 6. 运行部署检查

```bash
python check_deployment.py
```

### 7. 启动应用

```bash
python app.py
```

访问 http://localhost:5000 开始使用！

## 🔍 部署检查

项目包含一个部署检查脚本，可以验证所有必要的组件是否正确配置：

```bash
python check_deployment.py
```

检查项目将验证：

- Python 版本
- 依赖包安装
- 环境变量配置
- API 连接状态

## 🛠️ 故障排除

### 常见问题

1. **依赖安装失败**

   ```bash
   # 尝试更新pip
   python -m pip install --upgrade pip

   # 重新安装依赖
   pip install -r requirements.txt
   ```

2. **API 连接错误**

   - 检查 API 密钥是否正确
   - 确认网络连接
   - 验证 API 服务是否可用

3. **环境变量问题**

   - 确保.env 文件存在
   - 检查变量名是否正确
   - 确认没有多余的空格

4. **端口被占用**
   ```bash
   # 修改端口
   python app.py --port 5001
   ```

### 日志查看

应用日志位于 `logs/app.log`，可以查看详细错误信息。

## 📝 开发指南

### 项目结构

```
smart-travel-planner/
├── app.py              # 主应用文件
├── config.py           # 配置文件
├── weather.py          # 天气模块
├── check_deployment.py # 部署检查脚本
├── requirements.txt    # 项目依赖
├── .env               # 环境变量（不包含在git中）
└── templates/         # 模板目录
    └── index.html     # 主页模板
```

### 添加新功能

1. 创建新分支

```bash
git checkout -b feature/新功能名称
```

2. 开发完成后提交

```bash
git add .
git commit -m "添加: 新功能描述"
git push origin feature/新功能名称
```

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📜 开源协议

MIT License

## 🎨 趣味小贴士

- 🌟 这个项目最初是为了解决"今天去哪玩"的世纪难题
- 🎯 每次生成的行程都是独特的，就像雪花一样
- 🎮 试试输入不同的兴趣组合，可能会有惊喜哦！
- 📱 在手机上使用效果更佳，方便随时查看行程

## 🆘 常见问题

Q: 为什么我的行程生成失败了？
A: 请检查你的网络连接和 API 密钥是否正确配置。

Q: 如何获取高德地图 API 密钥？
A: 访问高德开放平台 (https://lbs.amap.com/) 注册并创建应用。

Q: 支持哪些城市？
A: 目前主要支持中国城市，特别是苏州地区。

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系我们：

- 提交 Issue
- 发送邮件到：[你的邮箱]

## 🎉 特别鸣谢

感谢所有为这个项目做出贡献的开发者！

---

Made with ❤️ by [你的名字]
