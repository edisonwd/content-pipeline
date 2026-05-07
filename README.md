# AI 内容生产流水线

自动化内容创作与发布系统：抓热搜 → AI 选题 → 写稿配图 → Notion 存储 → 自动发布小红书

## 🎯 功能模块

```
1. 热搜抓取层 (scrapers/)
   ├── 微博热搜
   ├── 知乎热榜  
   └── 抖音/Twitter

2. AI 选题筛选 (llm/score.py)
   - 评分维度：AI 相关性 + 热度 + 稀缺性

3. 内容生成 (llm/generate.py)
   - LLM 写作初稿
   - DALL·E/Pexels 配图

4. Notion 草稿库 (notion/)
   - 结构化存储

5. 自动发布 (publish/)
   - CDP + 小红书 API
```

## 📋 安装步骤

### 1. 环境准备

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. 配置环境变量 (.env)

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Keys
```

### 3. GitHub Token 获取

**方式 A - 快速授权（推荐）**
```bash
export GITHUB_TOKEN=your_token_here
gh auth login --with-token <<< "$GITHUB_TOKEN"
```

**方式 B - 手动获取 Token**
1. GitHub → Settings → Developer settings → Personal access tokens
2. Tokens (classic) → Generate new token
3. Scope: `repo` (创建仓库), `workflow` (Actions)
4. 复制 Token 并设置：`export GITHUB_TOKEN=xxx`

## 🚀 使用示例

### 初始化项目
```bash
./init.sh  # 自动创建远程仓库并推送
```

### 抓取热搜
```bash
python src/main.py --mode scrape --platform weibo,zhihu,douyin
```

### 生成内容
```bash
python src/main.py --generate --topic "AI 新进展" --output notion
```

### 自动发布
```bash
python src/main.py --publish platform=xiaohongshu draft_id=xxx
```

## 🔧 核心依赖

- **LLM**: llama-cpp / vLLM / OpenRouter API
- **Notion**: `notion-client`
- **Scrapers**: playwright, beautifulsoup4
- **Images**: PIL, requests (Pexels/DALL-E)
- **Xiaohongshu**: CDP SDK / Playwright RPA

## 📖 架构文档

详细技术架构请阅读：
- [src/architecture.md](src/architecture.md) - 系统架构图
- [docs/scraping.md](docs/scraping.md) - 爬虫实现细节
- [docs/notion-sync.md](docs/notion-sync.md) - Notion 集成

## 🤝 贡献指南

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
