# 🎯 AI 内容生产流水线 - 实现进度报告

## ✅ 已完成 (v0.1.0)

### 1. GitHub 仓库初始化
- ✅ 仓库：https://github.com/edisonwd/content-pipeline
- ✅ 基础架构搭建
- ✅ CI/CD 准备就绪

### 2. 项目结构
```
content-pipeline/
├── src/
│   ├── main.py           # 主入口 (CLI 工具)
│   ├── config/
│   │   └── __init__.py   # 配置管理
│   ├── scraper/
│   │   └── hot_search.py # 热搜抓取框架
│   ├── llm/
│   │   ├── topic_scoring.py      # AI 选题评分
│   │   └── article_generator.py  # 文章生成器
│   ├── notion/
│   │   └── __init__.py   # Notion 集成框架
│   └── publish/
│       └── __init__.py   # 小红书发布框架
├── .env.example          # 环境变量模板
├── requirements.txt      # Python 依赖
├── init.sh              # 自动初始化脚本
└── README.md            # 项目说明
```

### 3. CLI 功能
```bash
# 抓取热搜
python src/main.py scrape --platform weibo,zhihu,douyin

# 生成 AI 选题
python src/main.py generate --date 20260507 --output notion

# 发布到小红书
python src/main.py publish --draft-id xxx
```

---

## 🚧 待实现 (v0.2.0)

### 阶段 1: 热搜抓取增强
- [ ] 微博热搜 (Playwright 或 API)
- [ ] 知乎热榜 (API/Scrapy)
- [ ] 抖音热榜 (RPA)
- [ ] Twitter/X trending

### 阶段 2: LLM 集成
- [ ] OpenRouter API 集成 (多模型支持)
- [ ] llama-cpp 本地推理 (Qwen 1.5-7B)
- [ ] structured generation (outlines 库)
- [ ] Prompt 优化与版本管理

### 阶段 3: 配图生成
- [ ] Pexels API 免费图源
- [ ] DALL·E 3 生成式配图
- [ ] Image metadata extraction

### 阶段 4: Notion 数据库
- [ ] Create drafts database schema
- [ ] Auto-save with metadata
- [ ] Status tracking (Draft → Scheduled → Published)

### 阶段 5: 小红书发布
- [ ] CDP API 集成
- [ ] Playwright RPA fallback
- [ ] Scheduling system
- [ ] Analytics integration

---

## 🔑 需要的配置项

编辑 `.env` 文件填入你的 API Keys：

```bash
# 必需
GITHUB_TOKEN=ghp_xxx              # 已有
NOTION_API_KEY=xxx                # Notion Integration Token
PEXELS_API_KEY=xxx                # https://www.pexels.com/api/

# 可选 (选其一)
LLM_PROVIDER=openrouter           # 用云端 API
OPENROUTER_API_KEY=sk-or-v2-xxxx  # OpenRouter Key

# OR 本地部署
USE_LLAMA_CPP=true
LLAMA_MODEL_PATH=~/.cache/Qwen1.5-7B-Chat-GGUF/q4_k_m.gguf

# CDP Provider
XIAOHONGSHU_CDP_KEY=xxx
```

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境
cp .env.example .env
# Edit .env and fill your API keys

# 3. 测试爬虫
python src/main.py scrape --platform weibo

# 4. 测试 LLM 评分 (需要配置 API Key)
python src/main.py generate --date 20260507

# 5. 保存至 Notion
python src/main.py generate --date 20260507 --output notion

# 6. 自动发布
python src/main.py publish --draft-id <notion_page_id>
```

---

## 📊 预计开发时间

| 模块 | 工作量 | 优先级 |
|------|--------|--------|
| LLM 集成 | 3-5h | ⭐⭐⭐⭐⭐ |
| 热搜爬虫 | 4-6h | ⭐⭐⭐⭐ |
| 配图 API | 2-3h | ⭐⭐⭐ |
| Notion DB | 2-4h | ⭐⭐⭐⭐ |
| 小红书发布 | 3-5h | ⭐⭐⭐⭐⭐ |
| **总计** | **15-25h** | |

---

## 💡 下一步建议

1. **优先完成 LLM 集成** - 这是核心引擎
2. **先用 openrouter 测试** - 成本低，响应快
3. **Notion DB 先行设计** - 确定字段后再编码
4. **小红书发布可暂缓** - 先用手动 + Notion 过渡

