# Enhanced TradingAgents Framework

<div align="center">

![Enhanced TradingAgents](assets/TauricResearch.png)

**🚀 基于 TradingAgents 的增强版多股票分析平台**

[![Original TradingAgents](https://img.shields.io/badge/Based_on-TradingAgents-blue)](https://github.com/TauricResearch/TradingAgents)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [中文文档](#chinese)

</div>

---

# Chinese

## 🎯 项目概述

Enhanced TradingAgents 是基于 [TradingAgents](https://github.com/TauricResearch/TradingAgents) 的增强版框架，在保持原有核心功能的基础上，添加了以下增强功能：

### ✨ 主要增强功能

- 🧵 **多线程并发分析** - 同时分析多只股票，提高效率
- 🔧 **生产级修复** - 解决内存冲突、JSON序列化等关键问题  
- 🌐 **REST API 接口** - FastAPI驱动的现代化API服务
- 📊 **结构化数据输出** - 为数据库集成优化的数据格式
- 🐳 **容器化部署** - Docker/Kubernetes 生产部署支持
- 📈 **批量分析** - 支持股票列表批量处理
- 💾 **结果管理** - 完整的分析结果存储和检索系统

## 📁 项目结构

```
TradingAgents/
├── README.md                    # 项目说明文档
├── tradingagents/              # 🔒 原始TradingAgents核心库
├── cli/                        # 🔒 原始命令行界面
├── assets/                     # 🔒 原始项目资源
│
├── enhanced/                   # ✨ 增强功能模块
│   ├── multi_stock/           # 多股票分析器
│   ├── api/                   # REST API服务
│   ├── utils/                 # 工具函数
│   └── cli/                   # 增强CLI
│
├── configs/                    # 配置文件
│   ├── default.yaml           # 默认配置
│   ├── stock_lists/           # 股票列表配置
│   └── schemas/               # 配置模式
│
├── scripts/                    # 运行脚本
├── tests/                      # 测试套件
├── docs/                       # 文档
├── deployment/                 # 部署配置
├── data/                       # 数据目录 (gitignore)
└── tools/                      # 开发工具
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd TradingAgents

# 创建虚拟环境
conda create -n enhanced-trading python=3.11
conda activate enhanced-trading

# 安装依赖
pip install -r requirements.txt
```

### 2. API密钥配置

创建 `.env` 文件：

```bash
# 复制模板文件
cp .env.example .env

# 编辑配置 (必需)
export FINNHUB_API_KEY=your_finnhub_api_key
export OPENAI_API_KEY=your_openai_api_key

# 可选配置
export DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 3. 基本使用

#### 单股票分析 (原始功能)
```bash
# 使用原始CLI
python -m cli.main

# 或使用原始API
python main.py
```

#### 多股票分析 (增强功能)
```bash
# 分析指定股票列表
python scripts/run_analysis.py --stocks AAPL,NVDA,TSLA

# 使用预定义股票列表
python scripts/run_analysis.py --stock-list test_stocks

# 指定分析日期和并发数
python scripts/run_analysis.py --stocks AAPL,NVDA --date 2025-07-12 --workers 2
```

#### API服务启动
```bash
# 启动FastAPI服务
python enhanced/api/main.py

# 或使用脚本
python scripts/start_server.py

# 访问API文档
# http://localhost:8000/docs
```

## 💻 使用示例

### Python API 使用

#### 原始单股票分析
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 原始TradingAgents用法
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate("AAPL", "2025-07-12")
print(decision)
```

#### 增强多股票分析
```python
from enhanced.multi_stock.analyzer import MultiStockAnalyzer

# 多股票分析器
analyzer = MultiStockAnalyzer(max_workers=3)

# 分析股票列表
results = analyzer.analyze_stocks(
    stock_list=["AAPL", "NVDA", "TSLA"],
    analysis_date="2025-07-12",
    save_results=True
)

# 分析结果
for stock, result in results.items():
    print(f"{stock}: {result['decision']}")
```

#### REST API 调用
```python
import requests

# 分析单个股票
response = requests.post("http://localhost:8000/api/v1/analyze", json={
    "symbol": "AAPL",
    "date": "2025-07-12"
})

# 批量分析
response = requests.post("http://localhost:8000/api/v1/batch-analyze", json={
    "symbols": ["AAPL", "NVDA", "TSLA"],
    "date": "2025-07-12",
    "max_workers": 2
})
```

### 配置管理

```python
# 自定义配置
from enhanced.utils.config import load_config

config = load_config("configs/custom.yaml")
config.update({
    "tradingagents": {
        "deep_think_llm": "deepseek-reasoner",
        "quick_think_llm": "deepseek-chat",
        "max_debate_rounds": 2
    },
    "multi_stock": {
        "max_workers": 5,
        "timeout": 300
    }
})
```

## 🛠️ 高级功能

### 1. 批量分析
```bash
# 使用配置文件中的股票列表
python scripts/run_analysis.py --stock-list sp500_top50

# 自定义并发数和超时
python scripts/run_analysis.py --stocks AAPL,NVDA,TSLA --workers 3 --timeout 600
```

### 2. 结果导出
```bash
# 导出JSON格式
python scripts/export_data.py --format json --date 2025-07-12

# 导出CSV格式
python scripts/export_data.py --format csv --stock-list test_stocks
```

### 3. 监控和日志
```bash
# 查看实时日志
tail -f data/logs/analysis.log

# 启动监控面板
python scripts/monitor.py
```

## 🐳 容器化部署

### Docker 部署

```bash
# 构建镜像
cd deployment/docker
docker build -t enhanced-trading .

# 运行容器
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e FINNHUB_API_KEY=$FINNHUB_API_KEY \
  enhanced-trading

# 使用 Docker Compose
docker-compose up -d
```

### Kubernetes 部署

```bash
# 部署到Kubernetes
cd deployment/kubernetes
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## 🧪 测试

```bash
# 运行单元测试
python -m pytest tests/unit/

# 运行集成测试
python -m pytest tests/integration/

# 运行性能测试
python -m pytest tests/performance/

# 生成测试报告
python -m pytest --cov=enhanced tests/ --cov-report=html
```

## 📊 性能基准

| 功能 | 单线程 | 多线程 (3 workers) | 性能提升 |
|------|--------|-------------------|----------|
| 3股票分析 | ~15分钟 | ~6分钟 | 2.5x |
| 10股票分析 | ~50分钟 | ~18分钟 | 2.8x |
| API响应 | ~300ms | ~300ms | 一致 |

## 📚 文档

- [安装指南](docs/installation.md)
- [快速开始](docs/quickstart.md)
- [API文档](docs/api/)
- [配置指南](docs/guides/configuration.md)
- [部署指南](docs/guides/deployment.md)
- [开发指南](docs/development/)

## 🔧 故障排除

### 常见问题

1. **内存不足错误**
   ```bash
   # 减少并发worker数量
   python scripts/run_analysis.py --workers 1
   ```

2. **API限制错误**
   ```bash
   # 增加请求间隔
   export API_RATE_LIMIT=2  # 2秒间隔
   ```

3. **网络连接问题**
   ```bash
   # 使用离线模式
   python scripts/run_analysis.py --offline
   ```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目基于原始 TradingAgents 项目的许可证。增强功能部分采用 MIT 许可证。

## 🙏 致谢

特别感谢 [TauricResearch](https://github.com/TauricResearch/TradingAgents) 团队提供的优秀基础框架！

原始项目引用：
```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```

---

# English

## 🎯 Project Overview

Enhanced TradingAgents is an advanced framework built upon [TradingAgents](https://github.com/TauricResearch/TradingAgents), adding powerful enhancements while preserving the core functionality.

### ✨ Key Enhancements

- 🧵 **Multi-threaded Concurrent Analysis** - Analyze multiple stocks simultaneously
- 🔧 **Production-Grade Fixes** - Resolved memory conflicts, JSON serialization issues
- 🌐 **REST API Interface** - Modern FastAPI-driven web services
- 📊 **Structured Data Output** - Database-optimized data formats
- 🐳 **Containerized Deployment** - Docker/Kubernetes production support
- 📈 **Batch Processing** - Support for stock list batch analysis
- 💾 **Result Management** - Complete analysis result storage and retrieval

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd TradingAgents

# Create virtual environment
conda create -n enhanced-trading python=3.11
conda activate enhanced-trading

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Required API keys
export FINNHUB_API_KEY=your_finnhub_api_key
export OPENAI_API_KEY=your_openai_api_key

# Optional
export DEEPSEEK_API_KEY=your_deepseek_api_key
```

### 3. Basic Usage

#### Single Stock Analysis (Original)
```bash
python -m cli.main
```

#### Multi-Stock Analysis (Enhanced)
```bash
# Analyze specific stocks
python scripts/run_analysis.py --stocks AAPL,NVDA,TSLA

# Use predefined stock list
python scripts/run_analysis.py --stock-list test_stocks
```

#### API Server
```bash
# Start FastAPI server
python enhanced/api/main.py

# Access API docs at http://localhost:8000/docs
```

## 📖 Documentation

For detailed documentation, configuration options, and advanced usage, please refer to the [docs](docs/) directory.

---

⚠️ **Disclaimer**: This framework is designed for research purposes. Trading performance may vary based on various factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)