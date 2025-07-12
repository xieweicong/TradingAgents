# ✨ Enhanced 模块文档

这里是Enhanced TradingAgents的核心增强模块，所有自定义功能都组织在这个目录下。

## 📁 模块结构

```
enhanced/
├── __init__.py
├── multi_stock/          # 多股票并发分析
├── api/                  # FastAPI接口
├── utils/                # 通用工具
├── integrations/         # 第三方集成
└── cli/                  # 增强CLI
```

## 🎯 各模块说明

### 🧵 multi_stock - 多股票并发分析
**路径**: `enhanced/multi_stock/`

提供多股票并行分析能力，大幅提升分析效率。

**核心文件**:
- `analyzer.py` - 主分析器，管理并发任务
- `models.py` - 数据模型定义
- `utils.py` - 工具函数
- `config.py` - 配置管理

**使用示例**:
```python
from enhanced.multi_stock.analyzer import MultiStockAnalyzer

analyzer = MultiStockAnalyzer()
results = analyzer.analyze_batch(
    symbols=["AAPL", "NVDA", "TSLA"],
    analysis_date="2024-12-01"
)
```

### 🌐 api - FastAPI接口
**路径**: `enhanced/api/`

提供完整的REST API接口，支持前后端分离架构。

**核心文件**:
- `main.py` - FastAPI应用入口
- `routers/` - API路由分组
  - `analysis.py` - 分析相关接口
  - `stocks.py` - 股票信息接口
  - `health.py` - 健康检查接口
- `models/` - 请求/响应数据模型
- `middleware/` - 中间件（认证、限流、CORS）

**启动服务**:
```bash
python enhanced/api/main.py
# 或
uvicorn enhanced.api.main:app --reload
```

### 🛠️ utils - 通用工具
**路径**: `enhanced/utils/`

提供各种通用工具函数，支持整个enhanced模块。

**核心文件**:
- `memory.py` - 内存管理和优化
- `logging.py` - 统一日志配置
- `cache.py` - 缓存工具
- `validation.py` - 数据验证

### 🔗 integrations - 第三方集成
**路径**: `enhanced/integrations/`

集成各种第三方服务，扩展平台能力。

**子模块**:
- `databases/` - 数据库连接（PostgreSQL, MongoDB）
- `monitoring/` - 监控集成（Prometheus, Grafana）
- `notifications/` - 通知服务（邮件, Slack）

### 💻 cli - 增强CLI
**路径**: `enhanced/cli/`

提供更强大的命令行界面。

**核心文件**:
- `main.py` - CLI入口
- `commands/` - 命令分组
  - `analyze.py` - 分析命令
  - `server.py` - 服务器命令
  - `export.py` - 导出命令

## 🚀 快速开发指南

### 添加新的分析策略

1. **创建策略文件**:
```python
# enhanced/multi_stock/strategies/my_strategy.py
from typing import Dict, Any
from enhanced.multi_stock.models import AnalysisResult

class MyStrategy:
    def analyze(self, symbol: str, data: Dict[str, Any]) -> AnalysisResult:
        # 你的策略逻辑
        return AnalysisResult(
            symbol=symbol,
            recommendation="HOLD",
            confidence=0.75,
            reasoning="基于自定义策略"
        )
```

2. **注册策略**:
```python
# enhanced/multi_stock/analyzer.py
from enhanced.multi_stock.strategies.my_strategy import MyStrategy

# 在Analyzer类中添加
self.strategies["my_strategy"] = MyStrategy()
```

### 添加新的API端点

1. **创建路由文件**:
```python
# enhanced/api/routers/custom.py
from fastapi import APIRouter
from enhanced.api.models.responses import CustomResponse

router = APIRouter(prefix="/custom", tags=["custom"])

@router.get("/hello")
async def hello_world() -> CustomResponse:
    return CustomResponse(message="Hello from custom endpoint!")
```

2. **注册路由**:
```python
# enhanced/api/main.py
from enhanced.api.routers import custom

app.include_router(custom.router)
```

### 添加数据库集成

1. **创建数据库连接**:
```python
# enhanced/integrations/databases/postgresql.py
import asyncpg
from enhanced.utils.config import get_config

class PostgreSQLConnection:
    def __init__(self):
        self.config = get_config()
    
    async def connect(self):
        return await asyncpg.connect(self.config.database_url)
```

## 🧪 测试指南

### 运行模块测试

```bash
# 测试multi_stock模块
pytest tests/unit/test_multi_stock.py -v

# 测试API接口
pytest tests/integration/test_api.py -v

# 测试数据库集成
pytest tests/integration/test_database.py -v
```

### 添加新测试

```python
# tests/unit/test_my_feature.py
import pytest
from enhanced.multi_stock.strategies.my_strategy import MyStrategy

class TestMyStrategy:
    def test_analyze(self):
        strategy = MyStrategy()
        result = strategy.analyze("AAPL", {"price": 150.0})
        assert result.symbol == "AAPL"
        assert result.confidence > 0.5
```

## 📊 性能优化建议

### 并发分析优化
- 使用`asyncio`进行异步处理
- 合理设置线程池大小
- 实现连接池复用

### 内存优化
- 使用生成器处理大数据
- 实现LRU缓存
- 及时清理大对象

### API性能
- 添加响应缓存
- 使用连接池
- 实现请求限流

## 🔧 配置管理

### 环境变量
```bash
# 数据库配置
DATABASE_URL=postgresql://user:pass@localhost:5432/trading
REDIS_URL=redis://localhost:6379

# API配置
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# 分析配置
MAX_CONCURRENT_ANALYSIS=10
CACHE_TTL=3600
```

### 配置文件
```yaml
# configs/enhanced.yaml
multi_stock:
  max_workers: 10
  cache_enabled: true
  
api:
  rate_limit: "100/minute"
  cors_origins: ["http://localhost:3000"]
  
integrations:
  database:
    pool_size: 20
    max_overflow: 30
```

## 🆘 常见问题

### Q: 如何调试多股票分析？
A: 使用DEBUG模式并查看日志：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Q: API返回504错误？
A: 检查分析超时设置，增加超时时间：
```python
# 在请求中添加timeout参数
requests.post(url, json=data, timeout=300)
```

### Q: 内存使用过高？
A: 减少并发数量或启用内存清理：
```python
from enhanced.utils.memory import cleanup_memory
cleanup_memory()
```

## 📞 获取帮助

- **模块问题**: 创建GitHub Issue并标记`enhanced`标签
- **功能请求**: 使用GitHub Discussions
- **代码审查**: 提交Pull Request