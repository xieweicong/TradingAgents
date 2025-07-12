# 🚀 快速开始指南

本指南将帮助你在5分钟内运行你的第一个增强版TradingAgents分析。

## 📋 前置检查

### ✅ 系统要求
```bash
# 检查Python版本
python --version  # 需要 3.8+

# 检查内存
free -h  # 推荐 8GB+

# 检查磁盘空间
df -h  # 推荐 10GB+ 可用空间
```

### 🔑 获取API密钥

1. **FinnHub API** (免费)
   - 访问 [finnhub.io](https://finnhub.io)
   - 注册账号获取免费API Key

2. **OpenAI API** (付费)
   - 访问 [OpenAI Platform](https://platform.openai.com)
   - 创建API Key

3. **设置环境变量**
```bash
# Linux/Mac
export FINNHUB_API_KEY="your_finnhub_key"
export OPENAI_API_KEY="your_openai_key"

# Windows
set FINNHUB_API_KEY=your_finnhub_key
set OPENAI_API_KEY=your_openai_key
```

## 🏃‍♂️ 5分钟上手

### 方式1：一键运行脚本

```bash
# 克隆项目
git clone https://github.com/your-username/EnhancedTradingAgents.git
cd EnhancedTradingAgents

# 一键安装和运行
python scripts/quick_start.py
```

### 方式2：手动步骤

#### 1️⃣ 安装依赖
```bash
# 创建虚拟环境
python -m venv trading_env
source trading_env/bin/activate  # Windows: trading_env\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 2️⃣ 验证安装
```bash
# 运行快速测试
python -c "from enhanced.multi_stock.analyzer import MultiStockAnalyzer; print('✅ 安装成功')"
```

#### 3️⃣ 运行第一次分析
```bash
# 分析单个股票
python scripts/run_analysis.py --symbol AAPL --date 2024-12-01

# 分析多个股票
python scripts/run_analysis.py --symbols AAPL,NVDA,TSLA --date 2024-12-01
```

#### 4️⃣ 启动API服务
```bash
# 启动开发服务器
python scripts/start_server.py

# 访问API文档
open http://localhost:8000/docs
```

## 📊 第一个分析结果

### 命令行输出示例
```
🚀 开始分析 AAPL...
📊 数据获取完成
🧠 智能体分析中...
📈 技术分析师: 看涨信号
📰 新闻分析师: 正面消息
💰 交易员决策: BUY
✅ 分析完成！

📋 结果摘要:
- 股票: AAPL
- 建议: BUY
- 信心度: 85%
- 目标价格: $195.50
- 止损价格: $175.20
```

### API响应示例
```json
{
  "symbol": "AAPL",
  "date": "2024-12-01",
  "recommendation": "BUY",
  "confidence": 0.85,
  "target_price": 195.5,
  "stop_loss": 175.2,
  "analysis": {
    "technical": "bullish",
    "fundamental": "strong",
    "sentiment": "positive",
    "risk": "moderate"
  }
}
```

## 🎯 下一步

### 📈 探索更多功能

1. **批量分析**
```bash
# 分析S&P 500前10只股票
python scripts/run_analysis.py --list sp500_top10 --date 2024-12-01

# 自定义股票列表
python scripts/run_analysis.py --symbols MSFT,GOOGL,AMZN,META --date 2024-12-01
```

2. **使用API**
```python
import requests

# 使用Python调用API
response = requests.post("http://localhost:8000/api/v1/analyze", json={
    "symbol": "NVDA",
    "date": "2024-12-01",
    "include_news": True
})
print(response.json())
```

3. **自定义配置**
```python
# 创建自定义配置
from enhanced.multi_stock.config import AnalysisConfig

config = AnalysisConfig(
    max_workers=5,
    cache_enabled=True,
    include_technical=True,
    include_fundamental=True
)
```

### 🐳 使用Docker

```bash
# 快速启动完整环境
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f api
```

## 🆘 常见问题

### ❌ "ImportError: No module named..."
```bash
# 重新安装依赖
pip install -r requirements.txt --upgrade

# 检查Python路径
python -c "import sys; print(sys.path)"
```

### ❌ "API Key错误"
```bash
# 检查环境变量
echo $FINNHUB_API_KEY
echo $OPENAI_API_KEY

# 重新设置
export FINNHUB_API_KEY="your_actual_key"
export OPENAI_API_KEY="your_actual_key"
```

### ❌ "内存不足"
```bash
# 减少并发数量
python scripts/run_analysis.py --symbols AAPL --workers 1

# 使用轻量级模型
export USE_LIGHTWEIGHT_MODEL=true
```

### ❌ "连接超时"
```bash
# 检查网络连接
ping api.finnhub.io

# 增加超时时间
python scripts/run_analysis.py --timeout 300
```

## 🎉 成功标志

当你看到以下输出时，说明环境配置成功：

```
✅ 环境检查通过
✅ API密钥验证成功
✅ 依赖安装完成
✅ 第一次分析成功
🎉 恭喜！你已经准备好使用Enhanced TradingAgents了
```

## 📞 获取帮助

如果遇到困难：

1. **查看日志**: `cat logs/error.log`
2. **GitHub Issues**: [创建Issue](https://github.com/your-username/EnhancedTradingAgents/issues)
3. **社区讨论**: [GitHub Discussions](https://github.com/your-username/EnhancedTradingAgents/discussions)

## 🎯 推荐学习路径

1. **第1天**: 完成本快速开始
2. **第2天**: 阅读[多股票分析指南](multi_stock.md)
3. **第3天**: 学习[配置管理](configuration.md)
4. **第4天**: 探索[API文档](../api/README.md)
5. **第5天**: 尝试[部署指南](deployment.md)