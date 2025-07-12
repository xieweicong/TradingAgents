# Enhanced Trading Agents

基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 的增强版股票分析平台

## 🚀 新增功能

- 🧵 **多线程支持**: 并发分析多个股票
- 🔧 **生产修复**: 内存冲突、JSON序列化等问题修复
- 🌐 **API接口**: FastAPI驱动的REST API
- 📊 **结构化数据**: 为数据库集成优化的数据结构
- 🐳 **容器化**: Docker部署支持

## 📁 项目结构

```
├── tradingagents/          # 原始核心库
├── extensions/             # 增强功能
│   ├── multi_stock/        # 多股票分析
│   ├── api/                # FastAPI接口
│   └── utils/              # 工具函数
├── scripts/                # 脚本文件
├── configs/                # 配置文件
├── data/                   # 数据和结果
└── docs/                   # 文档
```

## 🛠️ 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基础使用
```bash
python scripts/run_analysis.py --stocks AAPL,NVDA
```

### API服务
```bash
python extensions/api/main.py
```

### Docker部署
```bash
cd deployment/docker
docker-compose up
```

## 📚 文档

- [多股票分析指南](docs/guides/multi_stock_guide.md)
- [API使用指南](docs/guides/api_guide.md)
- [修复记录](docs/fixes/)

## 🤝 贡献

基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 开发
感谢 TauricResearch 团队的优秀工作！

## 📄 许可证

基于原项目许可证，请查看 LICENSE 文件
