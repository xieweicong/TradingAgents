# GitHub Actions CI/CD 配置指南

## 🎯 概述

为 Enhanced TradingAgents 项目配置了完整的 CI/CD 流水线，包括：

- ✅ **代码质量检查** - 格式化、代码检查、复杂度分析
- ✅ **自动化测试** - 单元测试、集成测试、API测试
- ✅ **安全扫描** - 依赖检查、代码安全、秘钥扫描
- ✅ **多平台支持** - Ubuntu、macOS、Windows
- ✅ **性能测试** - 内存检查、基准测试

## 📁 工作流文件

```
.github/workflows/
├── ci.yml              # 主CI/CD流水线
├── test-suite.yml      # 详细测试套件
├── code-quality.yml    # 代码质量检查
└── security.yml        # 安全扫描
```

## 🚀 快速开始

### 1. 设置仓库秘钥

在 GitHub 仓库设置中添加以下 Secrets：

```bash
# 必需的API秘钥
OPENAI_API_KEY=your_openai_key
FINNHUB_API_KEY=your_finnhub_key

# 可选的API秘钥
DEEPSEEK_API_KEY=your_deepseek_key
```

### 2. 本地开发工具安装

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 安装pre-commit钩子
pre-commit install

# 手动运行代码格式化
black .
isort .
```

### 3. 本地测试

```bash
# 运行单元测试
pytest tests/unit/

# 运行所有测试
pytest

# 运行代码质量检查
flake8 .
mypy tradingagents/ extensions/
bandit -r tradingagents/ extensions/
```

## 🔄 工作流触发条件

### 主CI流水线 (ci.yml)
- **推送到**: `main`, `develop`, `pr/*` 分支
- **PR到**: `main`, `develop` 分支  
- **定时运行**: 每日 2:00 AM UTC

### 测试套件 (test-suite.yml)
- **文件变更**: `tradingagents/`, `extensions/`, `tests/`, `requirements.txt`
- **PR**: 任何对上述路径的修改

### 代码质量 (code-quality.yml)
- **推送/PR到**: `main`, `develop` 分支

### 安全扫描 (security.yml)
- **推送/PR到**: `main`, `develop` 分支
- **定时运行**: 每周日 3:00 AM UTC

## 📊 测试矩阵

| 操作系统 | Python版本 | 测试类型 |
|----------|-------------|----------|
| Ubuntu | 3.11, 3.12 | 单元+集成 |
| macOS | 3.11, 3.12 | 单元+集成 |
| Windows | 3.11 | 单元 |

## 🛡️ 安全检查

### 依赖安全
- **Safety**: Python包漏洞扫描
- **pip-audit**: 依赖审计
- **Bandit**: 代码安全扫描

### 秘钥检测
- **TruffleHog**: Git历史秘钥扫描
- **自定义规则**: API key模式检测

### 容器安全
- **Trivy**: Docker镜像漏洞扫描

## 📈 代码质量门禁

### 必须通过的检查
- ✅ 代码格式化 (Black)
- ✅ 导入排序 (isort)
- ✅ 基本语法检查 (flake8)
- ✅ 单元测试通过
- ✅ Docker构建成功

### 警告级别检查
- ⚠️ 类型检查 (mypy)
- ⚠️ 代码复杂度 (radon)
- ⚠️ 文档覆盖率 (interrogate)
- ⚠️ 安全扫描结果

## 🏗️ Docker 测试环境

### 测试服务配置
```yaml
services:
  - Redis (缓存)
  - PostgreSQL (数据库)
  - 主应用 (测试模式)
```

### 本地运行测试环境
```bash
cd deployment/docker
docker-compose -f docker-compose.test.yml up
```

## 🔧 故障排除

### 常见问题

#### 1. 测试失败：API密钥错误
```bash
# 解决方案：检查GitHub Secrets配置
# 或在本地设置环境变量
export OPENAI_API_KEY="your-key"
export FINNHUB_API_KEY="your-key"
```

#### 2. 代码格式化失败
```bash
# 解决方案：运行格式化工具
black .
isort .
git add .
git commit -m "Fix formatting"
```

#### 3. 依赖安全警告
```bash
# 解决方案：更新依赖
pip install --upgrade package-name
# 或添加例外到 .pipignore
```

#### 4. Docker构建失败
```bash
# 解决方案：检查Dockerfile和依赖
cd deployment/docker
docker build -t test-image .
```

## 📋 最佳实践

### 1. 提交前检查
```bash
# 运行pre-commit钩子
pre-commit run --all-files

# 快速测试
pytest tests/test_quick.py -v
```

### 2. PR创建
- 确保所有检查通过
- 添加适当的测试
- 更新文档（如需要）
- 使用描述性的commit消息

### 3. 性能考虑
- 使用 `[perf]` 标签触发性能测试
- 监控测试执行时间
- 避免在CI中运行长时间测试

### 4. 安全注意事项
- 不要在代码中硬编码API密钥
- 使用GitHub Secrets管理敏感信息
- 定期更新依赖
- 关注安全扫描结果

## 📚 参考资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [pytest 文档](https://docs.pytest.org/)
- [Black 代码格式化](https://black.readthedocs.io/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 确保所有CI检查通过
4. 创建PR并等待审核
5. 合并后自动部署

---

**注意**: 这些工作流配置针对生产环境优化，包含完整的测试、安全和质量检查。对于快速开发，可以创建简化版本的工作流。