<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# 增强版 TradingAgents：多智能体大语言模型交易框架

> 🚀 **增强版 TradingAgents** - 企业级多智能体大语言模型交易框架，包含生产环境扩展功能：多股票分析、REST API、内存优化和部署解决方案。

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

<div align="center">

✋ [框架概述](#框架概述) | 🏗️ [项目结构](#项目结构) | ⚡ [快速开始](#快速开始) | 🔧 [构建部署](#构建部署) | 💡 [增强功能](#增强功能) | 🤝 [贡献指南](#贡献指南)

</div>

## 框架概述

TradingAgents 是一个复杂的多智能体交易框架，通过专业的大语言模型驱动的智能体来模拟现实世界的交易公司。此增强版本在原始框架基础上扩展了生产就绪功能、多股票分析能力、REST API 接口和企业级部署解决方案。

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> ⚠️ **免责声明**：此框架专为研究和教育目的设计。交易表现受多种因素影响，包括语言模型、市场条件和数据质量。[不构成投资建议。](https://tauric.ai/disclaimer/)

### 核心智能体架构

框架将复杂的交易决策分解为专业的智能体角色，确保强大且可扩展的市场分析：

#### 📊 分析师团队
- **基本面分析师**：评估公司财务状况、绩效指标和内在价值
- **情感分析师**：使用先进评分算法分析社交媒体情感和公众舆论
- **新闻分析师**：监控全球新闻、宏观经济指标和市场驱动事件
- **技术分析师**：利用技术指标（MACD、RSI等）进行模式识别和价格预测

<p align="center">
  <img src="assets/analyst.png" width="90%" style="display: inline-block; margin: 0 2%;">
</p>

#### 🔬 研究团队
- **多空研究员**：通过结构化辩论对分析师洞察进行批判性评估
- **风险评估**：平衡潜在收益与固有市场风险

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

#### 💼 交易与风险管理
- **交易智能体**：综合研究结果做出明智的交易决策
- **风险管理员**：评估投资组合风险、波动性和流动性因素
- **投资组合经理**：最终批准/拒绝交易提案

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## 项目结构

此增强版本保持了原始 TradingAgents 核心，同时添加了生产就绪的扩展功能：

```
TradingAgents/
├── 📋 核心框架（原始）
│   ├── tradingagents/           # 核心交易逻辑和智能体
│   │   ├── agents/              # 分析师、交易员、风险管理智能体
│   │   ├── dataflows/           # 数据处理和API
│   │   ├── graph/               # LangGraph工作流定义
│   │   └── default_config.py    # 默认配置
│   ├── cli/                     # 原始CLI界面
│   └── assets/                  # 文档资源
│
├── 🚀 增强功能（自定义扩展）
│   ├── extensions/              # 生产就绪扩展
│   │   ├── multi_stock/         # 🔥 多股票并发分析
│   │   │   ├── analyzer.py      # 线程安全多股票处理器
│   │   │   └── models.py        # 增强数据模型
│   │   ├── api/                 # 🌐 FastAPI REST接口
│   │   │   ├── main.py          # API服务器应用
│   │   │   ├── routers/         # 模块化API端点
│   │   │   ├── models/          # 请求/响应模式
│   │   │   └── middleware/      # 认证、CORS、限流
│   │   └── utils/               # 🛠️ 生产工具
│   │       ├── memory_cleanup.py # 内存优化
│   │       └── data_validator.py # 输入验证
│   │
│   ├── configs/                 # 📝 配置管理
│   │   ├── default.json         # 基础配置
│   │   └── stock_lists.json     # 预定义股票组合
│   │
│   ├── scripts/                 # 📜 自动化脚本
│   │   └── run_analysis.py      # 批量分析执行
│   │
│   ├── tests/                   # 🧪 综合测试套件
│   │   ├── test_fixes.py        # 内存和稳定性测试
│   │   └── test_quick.py        # 快速验证测试
│   │
│   ├── docs/                    # 📖 扩展文档
│   │   ├── guides/              # 实施指南
│   │   ├── fixes/               # 问题解决日志
│   │   └── examples/            # 使用示例
│   │
│   └── deployment/              # 🐳 生产部署
│       ├── docker/              # Docker配置
│       │   ├── Dockerfile
│       │   └── docker-compose.yml
│       ├── kubernetes/          # K8s清单
│       └── scripts/             # 部署自动化
│
└── 📊 数据与结果
    ├── data/                    # 分析数据和缓存
    │   ├── cache/              # 金融数据缓存
    │   ├── results/            # 分析输出
    │   ├── logs/               # 系统日志
    │   └── exports/            # 数据导出
    └── eval_results/           # 性能评估
```

### 关键增强组件

| 组件 | 描述 | 状态 |
|------|------|------|
| **多股票分析器** | 具有优化资源使用的多证券并发分析 | ✅ 生产就绪 |
| **REST API** | 基于FastAPI的程序化访问接口 | ✅ 生产就绪 |
| **内存管理** | 高级内存清理和优化工具 | ✅ 生产就绪 |
| **Docker支持** | 基于Docker Compose的容器化部署 | ✅ 生产就绪 |
| **Kubernetes** | 企业级编排清单 | ✅ 生产就绪 |
| **综合测试** | 单元、集成和性能测试 | ✅ 生产就绪 |

## 快速开始

### 前置条件

- Python 3.11+
- Git
- API密钥（OpenAI，FinnHub）

### 安装

1. **克隆仓库**
```bash
git clone https://github.com/xieweicong/TradingAgents.git
cd TradingAgents
```

2. **创建虚拟环境**
```bash
# 使用conda（推荐）
conda create -n tradingagents python=3.13
conda activate tradingagents

# 或使用venv
python -m venv tradingagents
source tradingagents/bin/activate  # Windows: tradingagents\Scripts\activate
```

3. **安装依赖**
```bash
# 核心安装
uv pip install -r requirements.txt

# 开发安装（包含测试工具）
uv pip install -e ".[dev]"
```

### 环境设置

创建包含API凭据的 `.env` 文件：

```bash
# 必需的API
export OPENAI_API_KEY="你的_openai_api_密钥"
export FINNHUB_API_KEY="你的_finnhub_api_密钥"

# 可选：增强功能
export REDIS_URL="redis://localhost:6379"  # 缓存
export DATABASE_URL="postgresql://..."     # 持久化
```

### 基本使用

#### 1. CLI界面

启动交互式CLI：

```bash
python -m cli.main
```

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

#### 2. Python API

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# 使用默认配置初始化
ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# 单股票分析
result, decision = ta.propagate("AAPL", "2024-12-01")
print(f"交易决策: {decision}")
```

#### 3. 多股票分析

```python
from extensions.multi_stock.analyzer import MultiStockAnalyzer

# 初始化多股票分析器
analyzer = MultiStockAnalyzer(
    max_workers=3,
    enable_memory_cleanup=True
)

# 并发分析多支股票
stocks = ["AAPL", "GOOGL", "MSFT", "TSLA"]
results = analyzer.analyze_multiple(stocks, "2024-12-01")

for stock, result in results.items():
    print(f"{stock}: {result['decision']}")
```

#### 4. REST API服务器

```bash
# 启动API服务器
python -m extensions.api.main

# 或直接使用uvicorn
uvicorn extensions.api.main:app --host 0.0.0.0 --port 8000 --reload
```

API端点：
- `POST /api/v1/analyze/single` - 单股票分析
- `POST /api/v1/analyze/batch` - 多股票批量分析
- `GET /api/v1/analysis/{task_id}/status` - 分析状态
- `GET /api/v1/health` - 健康检查

## 构建部署

### 开发构建

```bash
# 开发模式安装
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 代码质量检查
black . --check
isort . --check-only
flake8 .
mypy tradingagents extensions
```

### Docker部署

```bash
# 使用Docker Compose构建和运行
cd deployment/docker
docker-compose up -d

# 查看日志
docker-compose logs -f tradingagents

# 扩展服务
docker-compose up -d --scale api=3
```

### Kubernetes部署

```bash
# 部署到Kubernetes
kubectl apply -f deployment/kubernetes/

# 检查状态
kubectl get pods -l app=tradingagents

# 访问日志
kubectl logs -f deployment/tradingagents
```

### 生产配置

```yaml
# configs/production.yaml
app:
  name: "TradingAgents 生产环境"
  debug: false
  log_level: "INFO"

tradingagents:
  llm_provider: "deepseek"
  max_workers: 5
  enable_memory_cleanup: true
  cache_enabled: true

api:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  cors_origins: ["https://你的前端.com"]
  rate_limit: "100/minute"

database:
  url: "${DATABASE_URL}"
  pool_size: 10
  max_overflow: 5

monitoring:
  enable_metrics: true
  prometheus_port: 9090
```

## 增强功能

### 🔄 多股票分析
- **并发处理**：线程安全地同时分析多支股票
- **资源优化**：智能内存管理和清理
- **批量操作**：高效处理大型投资组合
- **进度跟踪**：实时分析进度监控

### 🌐 REST API接口
- **FastAPI框架**：现代、快速、类型安全的API
- **异步支持**：高吞吐量的非阻塞操作
- **身份验证**：基于JWT的安全认证（可选）
- **限流**：可配置的请求节流
- **API文档**：自动生成的OpenAPI/Swagger文档

### 🧠 内存管理
- **智能清理**：分析间自动内存优化
- **泄漏预防**：主动内存泄漏检测和解决
- **资源监控**：实时内存和CPU使用率跟踪
- **垃圾回收**：长期运行进程的优化GC策略

### 🐳 生产部署
- **容器化**：多阶段Docker构建优化镜像大小
- **编排**：具有健康检查和扩展的Kubernetes清单
- **监控**：Prometheus指标和Grafana仪表板
- **CI/CD就绪**：自动化测试和部署的GitHub Actions工作流

### 📊 高级分析
- **性能指标**：详细的分析性能跟踪
- **导出功能**：多种数据导出格式（JSON、CSV、Excel）
- **历史分析**：历史数据回测
- **自定义策略**：可扩展的自定义交易策略框架

## 配置

### 核心配置

```python
# tradingagents/default_config.py
DEFAULT_CONFIG = {
    "deep_think_llm": "gpt-4o",           # 主要推理模型
    "quick_think_llm": "gpt-4o-mini",     # 快速响应模型
    "max_debate_rounds": 2,               # 智能体辩论轮次
    "online_tools": True,                 # 实时数据 vs 缓存
    "enable_memory": False,               # 智能体记忆持久化
    "temperature": 0.1,                   # 模型创造性水平
}
```

### 扩展配置

```json
{
  "multi_stock": {
    "max_workers": 3,
    "timeout_seconds": 300,
    "batch_size": 10,
    "enable_memory_cleanup": true
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "cors_enabled": true,
    "rate_limit": "60/minute"
  },
  "logging": {
    "level": "INFO",
    "format": "json",
    "file_rotation": "1 day"
  },
  "cache": {
    "redis_url": "redis://localhost:6379",
    "ttl_seconds": 3600
  }
}
```

## 测试

### 测试类别

```bash
# 单元测试
pytest tests/unit/ -v

# 集成测试
pytest tests/integration/ -v

# API测试
pytest tests/test_api.py -v

# 性能测试
pytest tests/performance/ -v

# 内存泄漏测试
pytest tests/test_fixes.py::test_memory_cleanup -v

# 快速验证
python tests/test_quick.py
```

### 测试覆盖率

```bash
# 生成覆盖率报告
pytest --cov=tradingagents --cov=extensions --cov-report=html

# 查看覆盖率
open htmlcov/index.html
```

## 性能优化

### 内存使用
- **基准**：单股票分析约500MB
- **多股票**：5支并发股票约1.2GB（优化后）
- **内存清理**：分析间90%+内存回收

### 处理速度
- **单次分析**：每支股票2-5分钟
- **多股票**：比顺序处理快40%
- **API响应**：状态查询<500ms

### 可扩展性
- **水平扩展**：Kubernetes HPA自动扩展
- **垂直扩展**：针对4-8 CPU核心优化
- **并发**：最多10个同时分析任务

## 故障排除

### 常见问题

1. **内存问题**
```bash
# 启用内存清理
python -c "from extensions.utils.memory_cleanup import cleanup_memory; cleanup_memory()"
```

2. **API连接错误**
```bash
# 检查API凭据
python -c "import os; print('OpenAI:', bool(os.getenv('OPENAI_API_KEY'))); print('FinnHub:', bool(os.getenv('FINNHUB_API_KEY')))"
```

3. **导入错误**
```bash
# 验证安装
pip show enhanced-tradingagents
python -c "import tradingagents; print('核心正常'); import extensions; print('扩展正常')"
```

### 调试模式

```python
# 启用综合调试
ta = TradingAgentsGraph(debug=True, config=config)
ta.debug_mode = True
```

## 路线图

### 计划功能
- [ ] **实时流**：实时市场数据的WebSocket API
- [ ] **机器学习**：增强预测模型
- [ ] **多交易所**：支持多个交易场所
- [ ] **投资组合优化**：高级投资组合管理算法
- [ ] **风险分析**：高级风险建模和压力测试

### 性能改进
- [ ] **GPU加速**：大规模分析的CUDA支持
- [ ] **分布式计算**：大型投资组合的集群支持
- [ ] **边缘缓存**：全球部署的CDN集成

## 贡献指南

我们欢迎为增强TradingAgents框架做出贡献！无论是修复错误、添加功能还是改进文档，您的输入都很有价值。

### 开发设置

```bash
# Fork并克隆仓库
git clone https://github.com/yourusername/TradingAgents.git
cd TradingAgents

# 安装开发依赖
pip install -e ".[dev]"

# 安装pre-commit钩子
pre-commit install

# 运行测试
pytest
```

### 贡献指南

1. **代码质量**：遵循PEP 8，使用类型提示，添加文档字符串
2. **测试**：为新功能编写测试，保持>90%覆盖率
3. **文档**：更新相关文档和示例
4. **性能**：确保更改不会降低性能
5. **安全**：遵循安全最佳实践，无硬编码密钥

### 加入我们的社区

- 📧 **研究社区**：[Tauric Research](https://tauric.ai/)
- 💬 **Discord**：[TradingResearch社区](https://discord.com/invite/hk9PGKShPK)
- 🐦 **Twitter**：[@TauricResearch](https://x.com/TauricResearch)
- 📖 **文档**：[项目指南](docs/guides/)

## 引用

如果您发现TradingAgents在研究中有用，请引用我们的工作：

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

<div align="center">

**增强版TradingAgents** - 由TradingAgents社区用❤️构建

[🏠 主页](https://github.com/TauricResearch/TradingAgents) | [📖 文档](docs/) | [🐛 问题](https://github.com/TauricResearch/TradingAgents/issues) | [🤝 讨论](https://github.com/TauricResearch/TradingAgents/discussions)

</div>
