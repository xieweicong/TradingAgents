# Multi-Stock Trading Agents Analyzer

## 概述

这是一个支持多线程、结构化数据保存的股票分析脚本，专为批量分析和数据库集成设计。

## 主要特性

### 🚀 核心功能
- **多线程分析**: 同时分析多个股票，充分利用API并发能力
- **分类保存**: 按agent类型分类保存分析结果（分析师、研究团队、交易员、风险管理、投资组合）
- **数据库准备**: 结构化JSON格式，易于导入数据库
- **股票列表管理**: 灵活的股票列表管理系统
- **进度监控**: 实时进度跟踪和日志记录

### 📊 数据结构
```
multi_analysis_results/
├── {ticker}/
│   └── {date}/
│       ├── analysis_result.json      # 完整结构化结果
│       ├── final_decision.txt        # 最终交易决策
│       ├── raw_state.json           # 原始状态数据
│       └── agents/                  # 按agent分类的报告
│           ├── analysts/            # 分析师团队
│           ├── research/            # 研究团队
│           ├── trader/              # 交易员
│           ├── risk_management/     # 风险管理
│           └── portfolio/           # 投资组合管理
```

## 快速开始

### 1. 基本使用
```python
python multi_stock_analyzer.py
```

### 2. 程序化使用
```python
from multi_stock_analyzer import MultiStockAnalyzer

# 初始化分析器
analyzer = MultiStockAnalyzer(max_workers=3)

# 分析股票
results = analyzer.analyze_stocks(
    stock_list=['AAPL', 'NVDA', 'MSFT'],
    analysis_date='2025-07-12',
    save_results=True
)
```

### 3. 查看示例
```python
python example_usage.py
```

## 配置选项

### 默认配置
```python
config = {
    "llm_provider": "deepseek",
    "backend_url": "https://api.deepseek.com/v1", 
    "deep_think_llm": "deepseek-reasoner",
    "quick_think_llm": "deepseek-chat",
    "max_debate_rounds": 1,
    "online_tools": True
}
```

### 自定义配置
```python
custom_config = analyzer.create_custom_config(
    max_debate_rounds=2,
    llm_provider="openai"
)

analyzer = MultiStockAnalyzer(config=custom_config, max_workers=5)
```

## 股票列表管理

### 预定义列表
- `us_stocks`: ['AAPL', 'NVDA', 'MSFT', 'GOOGL', 'AMZN']
- `jp_stocks`: ['7203.T', '6758.T', '9984.T', '6861.T', '8316.T'] 
- `test_stocks`: ['AAPL', 'NVDA'] (默认)

### 添加自定义列表
```python
analyzer.add_stock_list("my_portfolio", ['AAPL', 'TSLA', 'NVDA'])
```

### 查看可用列表
```python
lists = analyzer.get_available_stock_lists()
print(lists)
```

## 数据输出说明

### 1. 结构化JSON结果 (`analysis_result.json`)
包含完整的分析数据，按以下结构组织：
- `analyst_outputs`: 分析师团队输出（市场、情绪、新闻、基本面）
- `research_outputs`: 研究团队输出（看多、看空、研究经理）
- `trader_output`: 交易员分析
- `risk_outputs`: 风险管理团队输出（激进、保守、中性）
- `portfolio_output`: 投资组合管理决策

### 2. Agent报告文件 (`agents/` 目录)
每个agent的输出单独保存为Markdown文件，包含：
- 分析内容
- 时间戳
- 处理时间
- 状态信息

### 3. 日志系统
- `multi_analysis_logs/`: 主日志目录
- `analysis_session_{timestamp}.log`: 完整会话日志
- `session_summary_{timestamp}.json`: 会话摘要
- `stock_{ticker}_{timestamp}.log`: 单个股票分析日志

## 数据库集成指南

### JSON结构适合的数据库表设计

#### 1. 主分析表 (analysis_results)
```sql
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(20),
    analysis_date DATE,
    task_id VARCHAR(100),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    total_processing_time FLOAT,
    status VARCHAR(20),
    final_decision TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 2. Agent输出表 (agent_outputs)
```sql
CREATE TABLE agent_outputs (
    id SERIAL PRIMARY KEY,
    analysis_id INTEGER REFERENCES analysis_results(id),
    agent_type VARCHAR(50),
    agent_name VARCHAR(100), 
    content TEXT,
    timestamp TIMESTAMP,
    processing_time FLOAT,
    status VARCHAR(20),
    error_message TEXT
);
```

#### 3. 导入脚本示例
```python
def import_to_database(result: StockAnalysisResult):
    # 插入主记录
    analysis_id = insert_analysis_result(result)
    
    # 插入agent输出
    for agent_type, output in result.analyst_outputs.items():
        insert_agent_output(analysis_id, output)
    
    # ... 处理其他agent输出
```

## 性能调优

### 1. 并发设置
```python
# 根据API限制调整
analyzer = MultiStockAnalyzer(max_workers=3)  # 保守设置
analyzer = MultiStockAnalyzer(max_workers=5)  # 积极设置
```

### 2. 批处理建议
- 小批量: 2-5只股票
- 中批量: 5-10只股票  
- 大批量: 10+只股票（需要充足的API配额）

### 3. 监控API使用
脚本会记录每次分析的处理时间，帮助监控API性能。

## 故障排除

### 常见问题
1. **API限制**: 减少`max_workers`数量
2. **网络超时**: 检查网络连接和API状态
3. **存储空间**: 确保有足够的磁盘空间保存结果

### 错误处理
- 单个股票分析失败不会影响其他股票
- 详细错误信息记录在日志中
- 支持部分成功的批量分析

## 扩展功能

### 1. 添加新的Agent类型
继承`AgentOutput`类并在`_extract_agent_outputs`中添加处理逻辑。

### 2. 自定义数据保存格式
继承`ResultsManager`类并重写`save_analysis_result`方法。

### 3. 集成其他数据源
在配置中添加新的数据源设置。

---

**注意**: 此脚本为研究目的设计，交易决策可能因多种因素而异。请谨慎使用于实际交易。